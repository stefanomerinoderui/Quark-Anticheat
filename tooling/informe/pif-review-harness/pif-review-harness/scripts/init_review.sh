#!/usr/bin/env bash
# init_review.sh — Ciclo de vida: prepara el workspace de una entrega, ingesta PDF y repos, y corre la Capa 1.
#
# Uso:
#   scripts/init_review.sh --id <proyecto_id> --instancia <AE1|AE2|AE4|REENTREGA-1> --pdf <archivo.pdf>
#        [--pdf-anterior <archivo.pdf>]
#        [--code-url <url> | --code-dir <carpeta>] [--tag <tag> | --commit <hash>]
#        [--docs-url <url> | --docs-dir <carpeta>] [--docs-ref <ref>]
#        [--portafolio-dir <carpeta>] [--bitacoras-dir <carpeta>]   (entregas parciales de AE)
#        [--offline]
#
# Seguridad: los repos se clonan "bare" en input/_git/ (sin árbol de trabajo) y se exporta la referencia
# evaluada a input/repo_codigo/ con los archivos de instrucciones para agentes renombrados a *.STUDENT_DATA,
# para que el agente revisor no los cargue como instrucciones.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$HERE")"
PY="${PYTHON:-python3}"   # en Windows (Git Bash): PYTHON=python scripts/init_review.sh ...
export PYTHONUTF8=1

ID="" ; INST="" ; PDF="" ; PDF_PREV="" ; CODE_URL="" ; CODE_DIR="" ; TAG="" ; COMMIT="" ; DOCS_URL="" ; DOCS_DIR="" ; DOCS_REF="" ; OFFLINE="" ; PORT_DIR="" ; BITA_DIR=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --id) ID="$2"; shift 2;;
    --instancia) INST="$2"; shift 2;;
    --pdf) PDF="$2"; shift 2;;
    --pdf-anterior) PDF_PREV="$2"; shift 2;;
    --code-url) CODE_URL="$2"; shift 2;;
    --code-dir) CODE_DIR="$2"; shift 2;;
    --tag) TAG="$2"; shift 2;;
    --commit) COMMIT="$2"; shift 2;;
    --docs-url) DOCS_URL="$2"; shift 2;;
    --docs-dir) DOCS_DIR="$2"; shift 2;;
    --docs-ref) DOCS_REF="$2"; shift 2;;
    --portafolio-dir) PORT_DIR="$2"; shift 2;;
    --bitacoras-dir) BITA_DIR="$2"; shift 2;;
    --offline) OFFLINE="--offline"; shift;;
    -h|--help) sed -n '2,16p' "$0"; exit 0;;
    *) echo "Opción desconocida: $1" >&2; exit 2;;
  esac
done
[[ -z "$ID" || -z "$INST" || -z "$PDF" ]] && { echo "Faltan --id, --instancia o --pdf" >&2; exit 2; }
[[ "$ID" =~ ^[a-z0-9_-]+$ ]] || { echo "--id solo admite minúsculas, números, - y _" >&2; exit 2; }
[[ -f "$PDF" ]] || { echo "No existe el PDF: $PDF" >&2; exit 2; }

P="$ROOT/entregas/$ID"
mkdir -p "$P/input/_git" "$P/artifacts/findings" "$P/informes"

if [[ ! -f "$P/plan_entregas.json" ]]; then
  "$PY" - "$ROOT/templates/plan_entregas.ejemplo.json" "$P/plan_entregas.json" "$ID" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8")); d["proyecto_id"] = sys.argv[3]
json.dump(d, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=2)
EOF
  echo "[init] Se creó plan_entregas.json desde la plantilla: COMPLETAR equipo, modalidad e instancias antes de evaluar."
fi

PDF_DST="$P/input/${INST}_$(basename "$PDF")"
cp -f "$PDF" "$PDF_DST"
PDF_PREV_DST=""
if [[ -n "$PDF_PREV" ]]; then
  PDF_PREV_DST="$P/input/${INST}_anterior_$(basename "$PDF_PREV")"
  cp -f "$PDF_PREV" "$PDF_PREV_DST"
fi

for pair in "portafolio|$PORT_DIR" "bitacoras|$BITA_DIR"; do
  name="${pair%%|*}"; src="${pair#*|}"
  if [[ -n "$src" ]]; then
    [[ -d "$src" ]] || { echo "No existe la carpeta: $src" >&2; exit 2; }
    rm -rf "$P/input/$name"; mkdir -p "$P/input/$name"; cp -a "$src/." "$P/input/$name/"
    echo "[init] $name: $(find "$P/input/$name" -type f | wc -l) archivos"
  fi
done

RENAMED="$P/artifacts/renombrados.txt"
: > "$RENAMED"

sanitize() {  # $1 = carpeta exportada
  local dir="$1"
  while IFS= read -r -d '' f; do
    mv "$f" "$f.STUDENT_DATA"; echo "${f#$dir/}" >> "$RENAMED"
  done < <(find "$dir" -type f \( -name 'AGENTS.md' -o -name 'CLAUDE.md' -o -name 'CLAUDE.local.md' -o -name 'GEMINI.md' \
            -o -name '.cursorrules' -o -name '.windsurfrules' -o -name 'copilot-instructions.md' \) -print0)
  while IFS= read -r -d '' d; do
    mv "$d" "$d.STUDENT_DATA"; echo "${d#$dir/}/" >> "$RENAMED"
  done < <(find "$dir" -depth -type d \( -name '.claude' -o -name '.cursor' \) -print0)
}

# ingest <codigo|docs> <url> <dir> <ref>  → imprime "commit|ref|origen|tagfecha"
ingest() {
  local which="$1" url="$2" dir="$3" ref="$4"
  local bare="$P/input/_git/repo_${which}.git" export="$P/input/repo_${which}"
  local origen=""
  if [[ -n "$url" ]]; then
    origen="$url"
    if [[ -d "$bare" ]]; then git --git-dir "$bare" fetch --quiet --tags --force origin '+refs/heads/*:refs/heads/*' >&2
    else git clone --quiet --bare "$url" "$bare" >&2; fi
  elif [[ -n "$dir" ]]; then
    origen="$(cd "$dir" && pwd)"
    if git -C "$dir" rev-parse --git-dir >/dev/null 2>&1; then
      rm -rf "$bare"; git clone --quiet --bare "$dir" "$bare" >&2
    else
      echo "[init] $dir no es un repositorio git: se copia sin historial (controles de git en GRIS)." >&2
      rm -rf "$export"; mkdir -p "$export"; cp -a "$dir/." "$export/"; sanitize "$export"
      echo "|carpeta|$origen|"; return 0
    fi
  else
    return 0
  fi
  [[ -z "$ref" ]] && ref="HEAD"
  local commit
  commit="$(git --git-dir "$bare" rev-parse --verify --quiet "${ref}^{commit}")" || { echo "[init] No existe la referencia '$ref' en $which" >&2; exit 3; }
  local tagdate=""
  if git --git-dir "$bare" show-ref --verify --quiet "refs/tags/$ref"; then
    tagdate="$(git --git-dir "$bare" for-each-ref "refs/tags/$ref" --format='%(taggerdate:iso-strict)')"
    [[ -z "$tagdate" ]] && tagdate="$(git --git-dir "$bare" log -1 --format=%cI "$commit")"
  fi
  rm -rf "$export"; mkdir -p "$export"
  git --git-dir "$bare" archive "$commit" | tar -x -C "$export"
  # .mailmap del estudiante: se conserva en el bare (git lo aplica con --use-mailmap)
  sanitize "$export"
  echo "$commit|$ref|$origen|$tagdate"
}

REF="${TAG:-$COMMIT}"
CODE_INFO="$(ingest codigo "$CODE_URL" "$CODE_DIR" "$REF")"
DOCS_INFO="$(ingest docs "$DOCS_URL" "$DOCS_DIR" "$DOCS_REF")"
IFS='|' read -r C_COMMIT C_REF C_ORIG C_TAGDATE <<< "${CODE_INFO:-|||}"
IFS='|' read -r D_COMMIT D_REF D_ORIG _ <<< "${DOCS_INFO:-|||}"

ARGS=(register --id "$ID" --instancia "$INST" --pdf "$PDF_DST")
[[ -n "$C_COMMIT" ]] && ARGS+=(--commit "$C_COMMIT" --ref "$C_REF" --origen "$C_ORIG")
[[ -n "$C_TAGDATE" ]] && ARGS+=(--tag-fecha "$C_TAGDATE")
[[ -n "$D_COMMIT" ]] && ARGS+=(--docs-commit "$D_COMMIT" --docs-ref "$D_REF" --docs-origen "$D_ORIG")
"$PY" "$HERE/state.py" "${ARGS[@]}"

[[ -s "$RENAMED" ]] && echo "[init] Archivos de agente del estudiante renombrados a *.STUDENT_DATA: $(wc -l < "$RENAMED")"

RUN=(--id "$ID" --pdf "$PDF_DST")
[[ -n "$PDF_PREV_DST" ]] && RUN+=(--pdf-anterior "$PDF_PREV_DST")
[[ -n "$OFFLINE" ]] && RUN+=(--offline)
"$PY" "$HERE/run_audits.py" "${RUN[@]}"

cat <<EOF

[init] Listo. Capa 1 en entregas/$ID/artifacts/ (ver manifest.json).
Siguiente paso, en Claude Code desde la raíz del harness:
  "Revisá la entrega $INST del proyecto $ID siguiendo AGENTS.md."
EOF
