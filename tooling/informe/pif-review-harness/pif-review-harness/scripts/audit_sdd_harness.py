#!/usr/bin/env python3
"""Capa 1 — Apartado de cátedra (SDD, harness de agentes, higiene) + seguridad e integridad.

Salida: artifacts/sdd_harness.json con:
  specs, specs_timeline, agent_context, quality_gates, tests, secrets, env_tracked,
  injection (texto dirigido a evaluadores/modelos en PDF y repo), pii_pdf (datos personales en el PDF)
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import OK, ALERTA, FALLA, GRIS, artifacts, check, load_json, project_dir, write_artifact  # noqa: E402

SPEC_DIRS = ["specs", ".specify", "openspec", "docs/adr", "adr", "docs/decisions", "rfcs", "docs/rfcs", "docs/specs"]
AGENT_FILES = re.compile(r"(^|/)(AGENTS\.md|CLAUDE\.md|GEMINI\.md|\.cursorrules|copilot-instructions\.md|\.windsurfrules)(\.STUDENT_DATA)?$|(^|/)\.cursor(\.STUDENT_DATA)?/rules/|(^|/)\.claude(\.STUDENT_DATA)?/|(^|/)\.github/instructions/|(^|/)skills?/[^/]+/SKILL\.md", re.I)
GATES = {
    "eslint": r"(^|/)(\.eslintrc[^/]*|eslint\.config\.[cm]?js)$", "prettier": r"(^|/)\.prettierrc[^/]*$|prettier\.config",
    "ruff/flake8/pylint": r"(^|/)(ruff\.toml|\.ruff\.toml|\.flake8|\.pylintrc)$", "black/mypy": r"(^|/)(mypy\.ini|\.mypy\.ini)$",
    "pre-commit": r"(^|/)\.pre-commit-config\.yaml$", "editorconfig": r"(^|/)\.editorconfig$",
    "jest/vitest": r"(^|/)(jest|vitest)\.config\.", "pytest": r"(^|/)(pytest\.ini|conftest\.py)$",
    "checkstyle/spotless": r"(^|/)(checkstyle\.xml|spotless)", "sonar": r"sonar-project\.properties$",
}
TEST_FILE = re.compile(r"(^|/)(tests?|__tests__|spec)/|(_test|\.test|\.spec|Test)\.(py|js|ts|tsx|jsx|java|go|cs|php|rb)$|(^|/)test_[^/]+\.py$", re.I)
SRC_FILE = re.compile(r"\.(py|js|ts|tsx|jsx|java|go|cs|php|rb|kt|swift|dart|vue|svelte)$", re.I)
SECRETS = {
    "aws_access_key": r"\bAKIA[0-9A-Z]{16}\b",
    "github_token": r"\bgh[pousr]_[A-Za-z0-9]{36,}\b",
    "openai_key": r"\bsk-(?:proj-)?[A-Za-z0-9_\-]{20,}\b",
    "anthropic_key": r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b",
    "google_api_key": r"\bAIza[0-9A-Za-z_\-]{35}\b",
    "slack_token": r"\bxox[baprs]-[A-Za-z0-9\-]{10,}\b",
    "private_key": r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "connection_string": r"\b(mongodb(\+srv)?|postgres(ql)?|mysql|redis)://[^\s:@/]+:[^\s@/]{3,}@",
    "password_assignment": r"(?i)\b(password|passwd|contrase[nñ]a|secret|api[_-]?key)\s*[:=]\s*['\"][^'\"\s]{6,}['\"]",
}
INJECTION = re.compile(
    r"(?i)(ignor(a|á|e|en)\s+(las\s+|todas\s+las\s+|all\s+|previous\s+|the\s+)?(instrucciones|instructions)|"
    r"ignore\s+(all\s+|any\s+)?(previous|prior|above)|"
    r"(calific|evalu|punt)[aáú]\w*\s+(este|el|this)\s+(proyecto|trabajo|project)\s+(con|como|as)\s+|"
    r"\b(you are|sos|eres)\s+(an?\s+)?(evaluator|evaluador|revisor|grader|corrector)\b|"
    r"(as an ai|como (modelo|ia|asistente))[^.]{0,60}(must|deb[eé]s|deber[aá]s)|"
    r"(mark|marcar|marc[aá])\s+(everything|todo|all)\s+(as\s+|como\s+)?(green|verde|pass|aprobado)|"
    r"system\s*prompt|<\s*/?\s*(system|instructions)\s*>)"
)
PII = {
    "dni": r"\bDNI\s*:?\s*\d{1,2}\.?\d{3}\.?\d{3}\b",
    "cuil_cuit": r"\b(20|23|24|27|30|33|34)-?\d{8}-?\d\b",
    "telefono": r"(?<!\d)(\+?54\s?9?\s?)?(\(?0?\d{2,4}\)?[\s\-]?)?\d{3,4}[\s\-]\d{4}(?!\d)",
    "email": r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b",
}


def git(gitdir, *args):
    r = subprocess.run(["git", "--git-dir", str(gitdir), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else ""


def first_commit_touching(gitdir, ref, pattern):
    out = git(gitdir, "log", ref, "--reverse", "--format=@@%aI", "--name-only")
    date = None
    for line in out.splitlines():
        if line.startswith("@@"):
            date = line[2:]
        elif line and re.search(pattern, line):
            return date
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    pdir = project_dir(a.id)
    art = artifacts(a.id)
    export = pdir / "input" / "repo_codigo"
    gitdir = pdir / "input" / "_git" / "repo_codigo.git"
    state = load_json(pdir / "review_state.json", {}) or {}
    ref = ((state.get("entregas") or [{}])[-1].get("repo_codigo") or {}).get("commit") or "HEAD"
    checks = []

    rel = [str(p.relative_to(export)).replace("\\", "/") for p in export.rglob("*") if p.is_file()] if export.exists() else []
    if not rel:
        checks.append(check("repo", GRIS, "Sin repositorio de código: controles de repo en GRIS."))
    else:
        specs = [d for d in SPEC_DIRS if (export / d).is_dir()]
        spec_files = [r for r in rel if any(r.startswith(d + "/") for d in specs)]
        checks.append(check("specs", OK if specs else ALERTA, f"Carpetas de especificación: {', '.join(specs)}" if specs else "No hay carpetas de specs/ADR.",
                            carpetas=specs, archivos=len(spec_files)))
        if gitdir.exists() and specs:
            sp = first_commit_touching(gitdir, ref, r"^(" + "|".join(map(re.escape, specs)) + r")/")
            src = first_commit_touching(gitdir, ref, SRC_FILE.pattern)
            orden = None if not (sp and src) else ("specs antes o junto al código" if sp <= src else "specs posteriores al código")
            checks.append(check("specs_timeline", OK if orden and sp <= src else ALERTA, orden or "No se pudo determinar", primer_spec=sp, primer_codigo=src))
        else:
            checks.append(check("specs_timeline", GRIS, "Sin specs o sin historial"))
        agent = [r for r in rel if AGENT_FILES.search(r)]
        checks.append(check("agent_context", OK if agent else ALERTA,
                            f"{len(agent)} archivos de contexto para agentes (renombrados *.STUDENT_DATA en la copia: son datos)." if agent else "No hay archivos de contexto para agentes de código.",
                            archivos=agent))
        gates = {k: [r for r in rel if re.search(v, r)] for k, v in GATES.items()}
        gates = {k: v for k, v in gates.items() if v}
        checks.append(check("quality_gates", OK if len(gates) >= 2 else ALERTA, f"Quality gates detectados: {', '.join(gates) or 'ninguno'}", detalle_archivos=gates))
        tests = [r for r in rel if TEST_FILE.search(r) and SRC_FILE.search(r)]
        srcs = [r for r in rel if SRC_FILE.search(r) and r not in tests and "node_modules/" not in r]
        checks.append(check("tests", OK if tests else ALERTA, f"{len(tests)} archivos de test para {len(srcs)} de código.", tests=tests[:40], ratio=round(len(tests) / max(len(srcs), 1), 2)))

        # secretos: gitleaks si está; si no, regex en árbol + historial
        found = []
        if shutil.which("gitleaks") and gitdir.exists():
            rep = art / "gitleaks.json"
            subprocess.run(["gitleaks", "git", str(gitdir), "--report-format", "json", "--report-path", str(rep), "--no-banner", "--exit-code", "0"], capture_output=True)
            data = load_json(rep, []) or []
            found = [{"tipo": d.get("RuleID"), "archivo": d.get("File"), "linea": d.get("StartLine"), "commit": (d.get("Commit") or "")[:12], "fuente": "gitleaks"} for d in data]
            metodo = "gitleaks"
        else:
            metodo = "regex (gitleaks no instalado)"
            for r in rel:
                p = export / r
                if p.stat().st_size > 2_000_000:
                    continue
                try:
                    lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
                except Exception:
                    continue
                for ln_no, line in enumerate(lines, 1):
                    for k, rx in SECRETS.items():
                        if re.search(rx, line):
                            found.append({"tipo": k, "archivo": r, "linea": ln_no, "fuente": "arbol", "fragmento": line.strip()[:20] + "…"})
            if gitdir.exists():
                hist = git(gitdir, "log", ref, "-p", "--no-color", "--format=@@%H")
                commit = None
                for line in hist.splitlines():
                    if line.startswith("@@") and len(line) > 30 and " " not in line:
                        commit = line[2:14]
                    elif line.startswith("+") and not line.startswith("+++"):
                        for k, rx in SECRETS.items():
                            if re.search(rx, line):
                                found.append({"tipo": k, "commit": commit, "fuente": "historial", "fragmento": line[1:].strip()[:20] + "…"})
        uniq = list({(f.get("tipo"), f.get("archivo"), f.get("linea"), f.get("commit")): f for f in found}.values())
        checks.append(check("secrets", FALLA if uniq else OK, f"{len(uniq)} posibles secretos ({metodo}).", items=uniq[:60],
                            nota="Confirmar a mano: los patrones de contraseña generan falsos positivos en ejemplos y tests."))
        env = [r for r in rel if re.search(r"(^|/)\.env(\.[\w-]+)?$", r) and not r.endswith((".example", ".sample", ".template"))]
        gi = (export / ".gitignore").read_text(encoding="utf-8", errors="ignore") if (export / ".gitignore").exists() else ""
        checks.append(check("env_tracked", FALLA if env else (OK if ".env" in gi else ALERTA),
                            f"Archivos .env versionados: {', '.join(env)}" if env else (".env en .gitignore" if ".env" in gi else ".env no figura en .gitignore"), archivos=env))

    # --- inyección de instrucciones (repo + PDF)
    inj = []
    for r in rel:
        p = export / r
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".ico", ".woff", ".woff2", ".ttf", ".lock"} or p.stat().st_size > 1_000_000:
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in INJECTION.finditer(txt):
            line = txt.count("\n", 0, m.start()) + 1
            inj.append({"tipo": "repo", "archivo": r, "linea": line, "texto": txt[max(0, m.start() - 40): m.end() + 60].replace("\n", " ")})
    tdir = art / "pdf_text"
    if tdir.exists():
        for f in sorted(tdir.glob("page_*.txt")):
            txt = f.read_text(encoding="utf-8")
            for m in INJECTION.finditer(txt):
                inj.append({"tipo": "pdf", "pdf_page": int(f.stem.split("_")[1]), "texto": txt[max(0, m.start() - 40): m.end() + 60].replace("\n", " ")})
    seen, dedup = set(), []
    for x in inj:
        k = (x["tipo"], x.get("archivo"), x.get("linea"), x.get("pdf_page"))
        if k not in seen:
            seen.add(k)
            dedup.append(x)
    inj = dedup
    checks.append(check("injection", ALERTA if inj else OK, f"{len(inj)} fragmentos dirigidos a evaluadores o modelos.", items=inj[:40],
                        nota="Revisar contexto: un AGENTS.md legítimo puede decir 'sos un asistente…' para su propio agente. Solo es hallazgo si apunta a la evaluación."))

    # --- datos personales en el PDF (anexos sobre todo)
    pii = []
    fmt = load_json(art / "pdf_format.json", {}) or {}
    anexos = (fmt.get("sections") or {}).get("anexos", {})
    first_annex = min(anexos.values()) if anexos else None
    if tdir.exists():
        for f in sorted(tdir.glob("page_*.txt")):
            pg = int(f.stem.split("_")[1])
            if pg == 1:
                continue
            txt = f.read_text(encoding="utf-8")
            for k, rx in PII.items():
                ms = re.findall(rx, txt)
                if ms and (k != "email" or len(ms) >= 3 or (first_annex and pg >= first_annex)):
                    pii.append({"pdf_page": pg, "tipo": k, "cantidad": len(ms), "en_anexos": bool(first_annex and pg >= first_annex)})
    checks.append(check("pii_pdf", ALERTA if pii else OK, f"{len(pii)} páginas con posibles datos personales.", items=pii[:60],
                        nota="Los teléfonos y correos institucionales o de contacto del equipo no son observación; sí los de encuestados o terceros."))

    write_artifact(a.id, "sdd_harness.json", checks)
    print(f"[audit_sdd_harness] {len(checks)} controles → artifacts/sdd_harness.json")


if __name__ == "__main__":
    main()
