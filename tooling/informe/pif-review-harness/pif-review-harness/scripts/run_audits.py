#!/usr/bin/env python3
"""Ejecuta la Capa 1 completa y escribe artifacts/manifest.json (lo exige AGENTS.md antes de empezar)."""
import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import artifacts, load_json, now_iso, project_dir, save_json  # noqa: E402

HERE = Path(__file__).resolve().parent


def run(name, args, manifest, required_input=None):
    if required_input is not None and not required_input:
        manifest["auditorias"][name] = {"estado": "omitido", "motivo": "falta el insumo"}
        print(f"[run_audits] {name}: omitido")
        return
    t0 = time.time()
    r = subprocess.run([sys.executable, "-I", "-X", "utf8", str(HERE / args[0]), *args[1:]], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=HERE.parent)
    manifest["auditorias"][name] = {"estado": "ok" if r.returncode == 0 else "error", "segundos": round(time.time() - t0, 1),
                                     "salida": (r.stdout.strip().splitlines() or [""])[-1][:300], "error": r.stderr.strip()[-1500:] if r.returncode else ""}
    print(r.stdout.strip() if r.returncode == 0 else f"[run_audits] {name}: ERROR\n{r.stderr[-1500:]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--pdf-anterior")
    ap.add_argument("--offline", action="store_true", help="No consultar Crossref/OpenAlex (usa solo caché)")
    a = ap.parse_args()
    pdir = project_dir(a.id)
    art = artifacts(a.id)
    st = load_json(pdir / "review_state.json", {}) or {}
    m = {"generado_el": now_iso(), "proyecto_id": a.id, "instancia": ((st.get("entregas") or [{}])[-1]).get("instancia"),
         "python": platform.python_version(), "auditorias": {}}
    # Los scripts corren con -I (modo aislado); cada uno agrega su propio directorio a sys.path para importar lib/.
    run("extract_pdf", ["extract_pdf.py", "--id", a.id, "--pdf", a.pdf], m)
    if a.pdf_anterior:
        run("extract_pdf_prev", ["extract_pdf.py", "--id", a.id, "--pdf", a.pdf_anterior, "--out-name", "pdf_pages_prev.json", "--text-dir", "pdf_text_prev"], m)
    run("audit_pdf_format", ["audit_pdf_format.py", "--id", a.id], m)
    run("audit_coherence", ["audit_coherence.py", "--id", a.id], m)
    run("audit_apa_citations", ["audit_apa_citations.py", "--id", a.id], m)
    run("audit_references", ["audit_references.py", "--id", a.id] + (["--offline"] if a.offline else []), m)
    run("audit_repos", ["audit_repos.py", "--id", a.id], m, required_input=(pdir / "input" / "repo_codigo").exists())
    run("audit_repos_docs", ["audit_repos.py", "--id", a.id, "--which", "docs"], m, required_input=(pdir / "input" / "repo_docs").exists())
    run("audit_sdd_harness", ["audit_sdd_harness.py", "--id", a.id], m)
    run("audit_proceso", ["audit_proceso.py", "--id", a.id], m)
    run("audit_spelling", ["audit_spelling.py", "--id", a.id], m)
    run("diff_versions", ["diff_versions.py", "--id", a.id], m, required_input=bool(a.pdf_anterior))
    # resumen de estados por artifact
    m["artifacts"] = {}
    for f in sorted(art.glob("*.json")):
        d = load_json(f, {}) or {}
        if isinstance(d, dict) and "resumen" in d:
            m["artifacts"][f.name] = d["resumen"]
    save_json(art / "manifest.json", m)
    errs = [k for k, v in m["auditorias"].items() if v["estado"] == "error"]
    print(f"[run_audits] manifest.json escrito. Errores: {', '.join(errs) or 'ninguno'}")
    sys.exit(1 if "extract_pdf" in errs else 0)


if __name__ == "__main__":
    main()
