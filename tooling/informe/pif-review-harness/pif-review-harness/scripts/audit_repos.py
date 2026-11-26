#!/usr/bin/env python3
"""Capa 1 — Repositorios: referencia congelada, LICENSE, README, despliegue, CI, dependencias, licencias y commits.

Trabaja sobre:
  input/_git/repo_codigo.git   clon bare (historial, sin árbol de trabajo)
  input/repo_codigo/           export de la referencia evaluada (sin .git, archivos de agente renombrados)
Salida: artifacts/repos.json
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import OK, ALERTA, FALLA, GRIS, check, load_json, project_dir, write_artifact  # noqa: E402

LOCKFILES = ["package-lock.json", "yarn.lock", "pnpm-lock.yaml", "poetry.lock", "Pipfile.lock", "uv.lock", "composer.lock", "Gemfile.lock", "go.sum", "Cargo.lock", "packages.lock.json", "gradle.lockfile"]
CI = [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile", "azure-pipelines.yml", ".circleci", "bitbucket-pipelines.yml", ".drone.yml"]
COPYLEFT = re.compile(r"\b(A?GPL|GNU (Affero )?General Public)", re.I)
WEAK = re.compile(r"\b(LGPL|MPL|EPL)", re.I)
IGNORE_LINES = re.compile(r"(lock\.json|\.lock|lock\.yaml|\.min\.js|\.map|dist/|build/|node_modules/|vendor/|\.svg|\.png|\.jpg)$|/(dist|build|node_modules|vendor)/")


def git(gitdir, *args):
    r = subprocess.run(["git", "--git-dir", str(gitdir), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else None


def license_kind(text):
    t = text[:4000]
    for name, rx in [("AGPL-3.0", r"GNU AFFERO GENERAL PUBLIC LICENSE"), ("LGPL", r"GNU LESSER GENERAL PUBLIC"), ("GPL", r"GNU GENERAL PUBLIC LICENSE"),
                     ("Apache-2.0", r"Apache License,?\s+Version 2\.0"), ("MIT", r"\bMIT License\b|Permission is hereby granted, free of charge"),
                     ("BSD", r"Redistribution and use in source and binary forms"), ("MPL-2.0", r"Mozilla Public License"),
                     ("Propietaria", r"(?i)all rights reserved|todos los derechos reservados|EULA|propietari")]:
        if re.search(rx, t):
            return name
    return "Desconocida"


def project_class(kind):
    if kind in (None, "Propietaria", "Desconocida"):
        return "propietaria"
    if kind in ("GPL", "AGPL-3.0"):
        return "copyleft"
    return "permisiva"


def deps_inventory(root: Path):
    deps, files = [], []
    for pj in root.rglob("package.json"):
        if "node_modules" in pj.parts:
            continue
        files.append(str(pj.relative_to(root)))
        try:
            d = json.loads(pj.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for sec in ("dependencies", "devDependencies"):
            for k, v in (d.get(sec) or {}).items():
                deps.append({"ecosistema": "npm", "nombre": k, "version": v, "dev": sec == "devDependencies", "archivo": str(pj.relative_to(root)), "licencia": None})
    lic_npm = {}
    for lf in root.rglob("package-lock.json"):
        if "node_modules" in lf.parts:
            continue
        try:
            d = json.loads(lf.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for path, info in (d.get("packages") or {}).items():
            if path.startswith("node_modules/") and isinstance(info, dict) and info.get("license"):
                lic_npm[path.split("node_modules/")[-1]] = info["license"]
    for dep in deps:
        if dep["ecosistema"] == "npm":
            dep["licencia"] = lic_npm.get(dep["nombre"])
    for rq in list(root.rglob("requirements*.txt")):
        files.append(str(rq.relative_to(root)))
        for line in rq.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.split("#")[0].strip()
            if line and not line.startswith("-"):
                m = re.match(r"([A-Za-z0-9_.\-\[\]]+)\s*(.*)", line)
                if m:
                    deps.append({"ecosistema": "pypi", "nombre": m.group(1), "version": m.group(2) or None, "dev": False, "archivo": str(rq.relative_to(root)), "licencia": None})
    for pp in root.rglob("pyproject.toml"):
        files.append(str(pp.relative_to(root)))
        txt = pp.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"dependencies\s*=\s*\[(.*?)\]", txt, re.S)
        for d_ in re.findall(r"\"([A-Za-z0-9_.\-]+)[^\"]*\"", m.group(1) if m else ""):
            deps.append({"ecosistema": "pypi", "nombre": d_, "version": None, "dev": False, "archivo": str(pp.relative_to(root)), "licencia": None})
    for pom in root.rglob("pom.xml"):
        files.append(str(pom.relative_to(root)))
        for g, a_ in re.findall(r"<groupId>([^<]+)</groupId>\s*<artifactId>([^<]+)</artifactId>", pom.read_text(encoding="utf-8", errors="replace")):
            deps.append({"ecosistema": "maven", "nombre": f"{g}:{a_}", "version": None, "dev": False, "archivo": str(pom.relative_to(root)), "licencia": None})
    for gm in root.rglob("go.mod"):
        files.append(str(gm.relative_to(root)))
        for mod in re.findall(r"^\s*([\w./\-]+\.[\w./\-]+)\s+v[\d.]+", gm.read_text(encoding="utf-8", errors="replace"), re.M):
            deps.append({"ecosistema": "go", "nombre": mod, "version": None, "dev": False, "archivo": str(gm.relative_to(root)), "licencia": None})
    for cj in root.rglob("composer.json"):
        files.append(str(cj.relative_to(root)))
        try:
            d = json.loads(cj.read_text(encoding="utf-8", errors="replace"))
            for k, v in (d.get("require") or {}).items():
                deps.append({"ecosistema": "composer", "nombre": k, "version": v, "dev": False, "archivo": str(cj.relative_to(root)), "licencia": None})
        except Exception:
            pass
    for cs in root.rglob("*.csproj"):
        files.append(str(cs.relative_to(root)))
        for k, v in re.findall(r"<PackageReference\s+Include=\"([^\"]+)\"\s+Version=\"([^\"]+)\"", cs.read_text(encoding="utf-8", errors="replace")):
            deps.append({"ecosistema": "nuget", "nombre": k, "version": v, "dev": False, "archivo": str(cs.relative_to(root)), "licencia": None})
    return deps, sorted(set(files))


def build_plan(root: Path):
    plan = []
    if list(root.glob("docker-compose*.y*ml")) or list(root.glob("compose*.y*ml")):
        plan.append("docker compose up --build -d && docker compose ps")
    elif (root / "Dockerfile").exists():
        plan.append("docker build -t pif-eval . && docker run --rm pif-eval")
    if (root / "package.json").exists():
        try:
            s = json.loads((root / "package.json").read_text(encoding="utf-8")).get("scripts", {})
        except Exception:
            s = {}
        plan.append("npm ci" if (root / "package-lock.json").exists() else "npm install")
        for k in ("build", "test", "start"):
            if k in s:
                plan.append(f"npm run {k}")
    if (root / "requirements.txt").exists() or (root / "pyproject.toml").exists():
        plan.append("pip install -r requirements.txt" if (root / "requirements.txt").exists() else "pip install .")
        plan.append("pytest -q")
    if (root / "pom.xml").exists():
        plan.append("mvn -B package")
    if list(root.glob("build.gradle*")):
        plan.append("./gradlew build")
    if (root / "go.mod").exists():
        plan.append("go build ./... && go test ./...")
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--which", default="codigo", choices=["codigo", "docs"])
    ap.add_argument("--late-days", type=int, default=7)
    a = ap.parse_args()
    pdir = project_dir(a.id)
    gitdir = pdir / "input" / "_git" / f"repo_{a.which}.git"
    export = pdir / "input" / f"repo_{a.which}"
    state = load_json(pdir / "review_state.json", {}) or {}
    plan = load_json(pdir / "plan_entregas.json", {}) or {}
    last = (state.get("entregas") or [{}])[-1]
    rinfo = (last.get("repo_codigo") if a.which == "codigo" else last.get("repo_docs")) or {}
    checks = []
    out_name = "repos.json" if a.which == "codigo" else "repos_docs.json"

    if not export.exists():
        write_artifact(a.id, out_name, [check("repo", GRIS, f"No se ingresó el repositorio de {a.which}")])
        print(f"[audit_repos] sin repo {a.which}")
        return
    has_git = gitdir.exists()
    files = [p for p in export.rglob("*") if p.is_file()]
    rel = [str(p.relative_to(export)) for p in files]

    # --- referencia y congelamiento
    if has_git:
        tags = (git(gitdir, "for-each-ref", "--format=%(refname:short)|%(objecttype)|%(taggerdate:iso-strict)|%(*committerdate:iso-strict)|%(committerdate:iso-strict)", "refs/tags") or "").strip().splitlines()
        tag_list = []
        for t in tags:
            name, otype, tdate, peeled, cdate = (t.split("|") + [""] * 5)[:5]
            tag_list.append({"tag": name, "anotado": otype == "tag", "fecha": tdate or peeled or cdate})
        want = rinfo.get("ref")
        detail = f"Referencia evaluada: {want or 'HEAD'} → {rinfo.get('commit', '?')[:12]}; clonado el {rinfo.get('clonado_el', '?')}."
        estado = OK
        if rinfo.get("tag_esperado") and rinfo["tag_esperado"] not in [t["tag"] for t in tag_list]:
            estado = FALLA
            detail += f" No existe la etiqueta esperada '{rinfo['tag_esperado']}'."
        if rinfo.get("antes_del_vencimiento") is False:
            estado = ALERTA
            detail += " La fecha declarada del tag es posterior al vencimiento."
        checks.append(check("frozen_ref", estado, detail, tags=tag_list,
                            nota="Las fechas de tag/commit las fija el cliente: la marca confiable es 'clonado_el' + hash."))
    else:
        checks.append(check("frozen_ref", GRIS, "El repositorio se ingresó sin historial git (carpeta suelta)."))

    # --- LICENSE
    lic_files = [p for p in files if re.match(r"^(LICEN[SC]E|COPYING)(\.|$)", p.name, re.I) and p.parent == export]
    kind = license_kind(lic_files[0].read_text(encoding="utf-8", errors="replace")) if lic_files else None
    checks.append(check("license", OK if lic_files and kind != "Desconocida" else (ALERTA if lic_files else FALLA),
                        f"LICENSE: {kind}" if lic_files else "No hay archivo LICENSE en la raíz.", tipo=kind, archivo=str(lic_files[0].name) if lic_files else None))

    # --- README y despliegue
    readmes = [p for p in files if re.match(r"^readme(\.|$)", p.name, re.I)]
    root_readme = next((p for p in readmes if p.parent == export), None)
    rtxt = root_readme.read_text(encoding="utf-8", errors="replace") if root_readme else ""
    run_kw = re.findall(r"(?im)^#+\s*(instalaci[oó]n|install|ejecuci[oó]n|ejecutar|run|despliegue|deploy|requisitos|requirements|getting started|uso|usage)\b", rtxt)
    checks.append(check("readme", OK if root_readme and run_kw else (ALERTA if root_readme else FALLA),
                        (f"README con secciones: {', '.join(sorted(set(k.lower() for k in run_kw)))}" if run_kw else "README sin secciones de instalación/ejecución") if root_readme else "No hay README en la raíz.",
                        archivo=root_readme.name if root_readme else None, palabras=len(rtxt.split())))
    deploy_docs = [r for r in rel if re.search(r"(?i)(deploy|despliegue|install|instalaci|manual)", r) and r.lower().endswith((".md", ".pdf", ".txt", ".adoc", ".docx"))]
    infra = [r for r in rel if re.search(r"(?i)(^|/)(dockerfile|docker-compose[^/]*\.ya?ml|compose[^/]*\.ya?ml|procfile|render\.yaml|vercel\.json|netlify\.toml|fly\.toml|app\.yaml|serverless\.ya?ml|.*\.tf)$", r)]
    has_manual = bool(deploy_docs) or bool(re.search(r"(?im)^#+\s*(despliegue|deploy)", rtxt))
    checks.append(check("deploy_manual", OK if has_manual else FALLA,
                        "Hay manual o sección de despliegue" if has_manual else "No se encontró manual de despliegue (archivo o sección del README).",
                        documentos=deploy_docs[:20], infraestructura=infra[:20]))
    bp = build_plan(export)
    checks.append(check("build_plan", OK if bp else ALERTA, "Pasos de construcción inferidos (para sandbox_build.sh)" if bp else "No se pudo inferir cómo construir el sistema.", pasos=bp))

    # --- CI y lockfiles
    ci = [c for c in CI if (export / c).exists()]
    checks.append(check("ci", OK if ci else ALERTA, f"CI: {', '.join(ci)}" if ci else "No hay configuración de integración continua.", archivos=ci))
    locks = [r for r in rel if Path(r).name in LOCKFILES]
    deps, manifests = deps_inventory(export)
    checks.append(check("lockfiles", OK if locks or not manifests else ALERTA, f"{len(locks)} lockfiles para {len(manifests)} manifiestos.", lockfiles=locks, manifiestos=manifests))

    # --- dependencias y compatibilidad de licencias
    pclass = project_class(kind)
    conflicts, unknown = [], []
    for d in deps:
        lic = d.get("licencia")
        if not lic:
            unknown.append(d["nombre"])
        elif COPYLEFT.search(lic) and not WEAK.search(lic) and pclass != "copyleft" and not d["dev"]:
            conflicts.append({**d, "motivo": f"dependencia {lic} en proyecto {pclass}"})
    estado = FALLA if conflicts else (GRIS if deps and len(unknown) == len(deps) else (ALERTA if unknown else OK))
    checks.append(check("dependencies", estado,
                        f"{len(deps)} dependencias; {len(conflicts)} conflictos candidatos; {len(unknown)} sin licencia conocida offline.",
                        clase_proyecto=pclass, conflictos=conflicts, sin_licencia=unknown[:80], inventario=deps[:300],
                        nota="Las licencias de PyPI/Maven/Go no se resuelven offline: correr pip-licenses o license-checker en el sandbox si hace falta."))

    # --- commits
    if has_git:
        ref = rinfo.get("commit") or "HEAD"
        log = git(gitdir, "log", ref, "--use-mailmap", "--no-merges", "--numstat", "--format=@@%H|%aN|%aE|%aI") or ""
        commits, cur = [], None
        for line in log.splitlines():
            if line.startswith("@@"):
                h, name, email, date = line[2:].split("|", 3)
                cur = {"hash": h[:12], "autor": name, "email": email.lower(), "fecha": date, "add": 0, "del": 0, "archivos": 0}
                commits.append(cur)
            elif line.strip() and cur is not None:
                p = line.split("\t")
                if len(p) == 3 and not IGNORE_LINES.search(p[2]):
                    cur["add"] += int(p[0]) if p[0].isdigit() else 0
                    cur["del"] += int(p[1]) if p[1].isdigit() else 0
                    cur["archivos"] += 1
        email_to = {}
        for m in plan.get("equipo", []):
            for e in m.get("emails_git", []):
                email_to[e.lower()] = m["nombre"]
        per = defaultdict(lambda: {"commits": 0, "lineas": 0, "primero": None, "ultimo": None, "semanas": set(), "emails": set()})
        for c in commits:
            who = email_to.get(c["email"], c["autor"])
            d = per[who]
            d["commits"] += 1
            d["lineas"] += c["add"] + c["del"]
            d["emails"].add(c["email"])
            d["primero"] = min(filter(None, [d["primero"], c["fecha"]]))
            d["ultimo"] = max(filter(None, [d["ultimo"], c["fecha"]]))
            d["semanas"].add(dt.datetime.fromisoformat(c["fecha"]).strftime("%G-W%V"))
        total_lines = sum(c["add"] + c["del"] for c in commits) or 1
        por_autor = [{"autor": k, "commits": v["commits"], "lineas": v["lineas"], "proporcion_lineas": round(v["lineas"] / total_lines, 3),
                      "semanas_activas": len(v["semanas"]), "primero": v["primero"], "ultimo": v["ultimo"], "emails": sorted(v["emails"]),
                      "en_equipo": k in {m["nombre"] for m in plan.get("equipo", [])}} for k, v in sorted(per.items(), key=lambda kv: -kv[1]["lineas"])]
        sin_commits = [m["nombre"] for m in plan.get("equipo", []) if m["nombre"] not in per]
        # concentración tardía
        deadline = None
        for inst in plan.get("instancias", []):
            if inst.get("id") == last.get("instancia") and inst.get("fecha_limite"):
                deadline = dt.datetime.fromisoformat(inst["fecha_limite"])
        if not deadline and commits:
            deadline = dt.datetime.fromisoformat(commits[0]["fecha"])
        late_share = None
        if deadline and commits:
            cut = deadline - dt.timedelta(days=a.late_days)
            late = sum(c["add"] + c["del"] for c in commits if dt.datetime.fromisoformat(c["fecha"]) >= cut)
            late_share = round(late / total_lines, 2)
        mega = [c for c in commits if c["add"] + c["del"] > 2000]
        flags = []
        externos = [x["autor"] for x in por_autor if not x["en_equipo"]] if plan.get("equipo") else []
        if externos:
            flags.append(f"autores que no figuran en el equipo: {', '.join(externos)}")
        if sin_commits:
            flags.append(f"integrantes sin commits: {', '.join(sin_commits)}")
        if late_share is not None and late_share > 0.4:
            flags.append(f"{late_share:.0%} de las líneas en los últimos {a.late_days} días")
        if mega:
            flags.append(f"{len(mega)} commits de más de 2000 líneas")
        if len(commits) < 10:
            flags.append(f"historial corto ({len(commits)} commits)")
        checks.append(check("commits", ALERTA if flags else OK,
                            f"{len(commits)} commits; " + ("; ".join(flags) if flags else "distribución sin alertas"),
                            por_autor=por_autor, sin_commits=sin_commits, proporcion_tardia=late_share, mega_commits=mega[:20],
                            nota="Usar como preguntas de coloquio, no como prueba de autoría. Mapear correos con .mailmap o plan_entregas.equipo[].emails_git."))
        checks.append(check("late_bulk", ALERTA if late_share and late_share > 0.4 else OK, f"Proporción de líneas en los últimos {a.late_days} días: {late_share}", valor=late_share))
    else:
        checks.append(check("commits", GRIS, "Sin historial git."))

    write_artifact(a.id, out_name, checks, meta={"repo": a.which, "archivos": len(rel), "ref": rinfo})
    print(f"[audit_repos] {a.which}: {len(rel)} archivos, {len(checks)} controles → artifacts/{out_name}")


if __name__ == "__main__":
    main()
