#!/usr/bin/env bash
# sandbox_build.sh — Intenta construir y probar el sistema del estudiante en un contenedor aislado.
#
# Uso: scripts/sandbox_build.sh --id <proyecto_id> [--image node:20|python:3.12|maven:3-eclipse-temurin-21|golang:1.22] [--no-network] [--timeout 900]
#
# Aislamiento: el código se monta SOLO LECTURA y se copia dentro del contenedor; no se montan el home,
# credenciales, ni el socket de Docker; no se pasan variables de entorno del host; CPU, memoria y procesos limitados.
# La red está habilitada por defecto porque instalar dependencias la necesita; con --no-network se prueba
# que el sistema construya sin descargar nada. docker compose NO se ejecuta acá (requiere Docker-in-Docker):
# si el proyecto se despliega con compose, el docente lo levanta a mano en una VM descartable.
#
# Salida: entregas/<id>/artifacts/build.json  (pasos, código de salida, últimas líneas del log)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; ROOT="$(dirname "$HERE")"
ID=""; IMAGE=""; NET="bridge"; TIMEOUT=900
while [[ $# -gt 0 ]]; do case "$1" in
  --id) ID="$2"; shift 2;; --image) IMAGE="$2"; shift 2;; --no-network) NET="none"; shift;; --timeout) TIMEOUT="$2"; shift 2;;
  *) echo "Opción desconocida: $1" >&2; exit 2;; esac; done
P="$ROOT/entregas/$ID"; SRC="$P/input/repo_codigo"; OUT="$P/artifacts/build.json"
[[ -d "$SRC" ]] || { echo "No hay input/repo_codigo" >&2; exit 2; }
if ! command -v docker >/dev/null || ! docker info >/dev/null 2>&1; then
  echo '{"estado":"GRIS","detalle":"Docker no disponible (no instalado o daemon detenido)","checks":[{"id":"build","estado":"GRIS","detalle":"Docker no disponible"}]}' > "$OUT"
  echo "[sandbox_build] Docker no disponible: build.json en GRIS"; exit 0
fi

PY="${PYTHON:-python3}"
mapfile -t STEPS < <("$PY" -c "import json,sys; d=json.load(open('$P/artifacts/repos.json')); print('\n'.join(next(c for c in d['checks'] if c['id']=='build_plan').get('pasos',[])))" | grep -v '^docker')
if [[ -z "$IMAGE" ]]; then
  if [[ -f "$SRC/package.json" ]]; then IMAGE="node:20"; elif [[ -f "$SRC/requirements.txt" || -f "$SRC/pyproject.toml" ]]; then IMAGE="python:3.12"
  elif [[ -f "$SRC/pom.xml" ]]; then IMAGE="maven:3-eclipse-temurin-21"; elif [[ -f "$SRC/go.mod" ]]; then IMAGE="golang:1.22"; else IMAGE="debian:stable-slim"; fi
fi
SCRIPT="set -o pipefail; cp -a /src/. /work/ && cd /work"
for s in "${STEPS[@]}"; do [[ "$s" == "npm run start" ]] && s="timeout 60 npm run start || [ \$? -eq 124 ]"; SCRIPT+="; echo '>>> $s'; $s"; done
LOG="$P/artifacts/build.log"
set +e
timeout "$TIMEOUT" docker run --rm --network "$NET" --cpus 2 --memory 4g --pids-limit 512 --security-opt no-new-privileges \
  -v "$SRC:/src:ro" --tmpfs /work:exec,size=4g -w /work "$IMAGE" bash -lc "$SCRIPT" > "$LOG" 2>&1
RC=$?
set -e
"$PY" - "$OUT" "$RC" "$IMAGE" "$NET" "$LOG" "${STEPS[@]}" <<'EOF'
import json, sys, datetime
out, rc, image, net, log, *steps = sys.argv[1:]
tail = open(log, encoding="utf-8", errors="replace").read().splitlines()[-60:]
json.dump({"generado_el": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "imagen": image, "red": net,
           "pasos": steps, "codigo_salida": int(rc), "estado": "OK" if int(rc) == 0 else "FALLA",
           "checks": [{"id": "build", "estado": "OK" if int(rc) == 0 else "FALLA", "detalle": f"exit {rc} con {image}"}],
           "log_final": tail, "nota": "Un FALLA es evidencia para GATE-01; el ROJO de ejecutabilidad lo confirma el docente."},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"[sandbox_build] exit {rc} → {out}")
EOF
