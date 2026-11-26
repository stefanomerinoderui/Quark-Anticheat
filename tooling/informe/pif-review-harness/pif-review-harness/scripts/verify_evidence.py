#!/usr/bin/env python3
"""Checker mecánico: comprueba que cada cita literal exista donde el hallazgo dice.

Lee   artifacts/findings/<ITEM>.maker.json  (lista de hallazgos, o {"hallazgos": [...]})
Escribe artifacts/findings/<ITEM>.verified.json  y  artifacts/verify_evidence.json (resumen)

Resultado por hallazgo (campo verificacion_mecanica.estado):
  valida            todas las ubicaciones se verificaron
  pagina_corregida  la cita existe, pero en otra página del PDF (se corrige la página)
  descartada        alguna cita no aparece, el archivo no existe, o faltan campos obligatorios
Advertencias (no descartan, las resuelve el Checker): contradice_script, pide_bitacora_no_exigida,
  falta_que_se_espera, cita_aproximada.
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import artifacts, load_json, norm, project_dir, save_json  # noqa: E402

REQ = ["item_id", "clave", "semaforo", "norma", "ubicaciones", "observacion", "destino", "origen"]
CLAVE = re.compile(r"^[A-Z]+-[0-9]{2}:[a-z0-9_\-]+$")


def contains(haystack: str, needle: str):
    h, n = norm(haystack), norm(needle)
    if not n:
        return False, 0.0
    if n in h:
        return True, 1.0
    sm = difflib.SequenceMatcher(None, h, n, autojunk=False)
    m = sm.find_longest_match(0, len(h), 0, len(n))
    ratio = m.size / len(n)
    return ratio >= 0.9, round(ratio, 2)


def current_instance(plan, state):
    inst = ((state.get("entregas") or [{}])[-1]).get("instancia")
    return next((i for i in plan.get("instancias", []) if i.get("id") == inst), {})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    pdir = project_dir(a.id)
    art = artifacts(a.id)
    fdir = art / "findings"
    texts = {int(f.stem.split("_")[1]): f.read_text(encoding="utf-8") for f in sorted((art / "pdf_text").glob("page_*.txt"))}
    plan = load_json(pdir / "plan_entregas.json", {}) or {}
    state = load_json(pdir / "review_state.json", {}) or {}
    inst = current_instance(plan, state)
    no_bitacora = inst.get("exige_portafolio_bitacora") is not True  # por defecto no se exigen (alcance: RR 97/23)
    summary = []

    for mf in sorted(fdir.glob("*.maker.json")):
        raw = load_json(mf)
        items = raw.get("hallazgos", raw) if isinstance(raw, dict) else raw
        out = []
        for f in items:
            vm = {"estado": "valida", "ubicaciones": [], "advertencias": [], "errores": []}
            for k in REQ:
                if k not in f or f[k] in (None, "", []):
                    vm["errores"].append(f"falta el campo '{k}'")
            if f.get("clave") and not CLAVE.match(f["clave"]):
                vm["errores"].append("clave con formato inválido (ITEM-NN:texto_en_minusculas)")
            if f.get("semaforo") == "GRIS" and not f.get("motivo_gris"):
                vm["errores"].append("GRIS sin motivo_gris")
            if f.get("semaforo") in ("ROJO", "AMARILLO") and f.get("destino") in ("devolucion", "ambos"):
                if not f.get("que_se_espera") or not f.get("evidencia_a_presentar"):
                    vm["advertencias"].append("falta_que_se_espera_o_evidencia")
            if no_bitacora and re.search(r"(?i)bit[aá]cora|portafolio", f.get("evidencia_a_presentar", "") or ""):
                vm["advertencias"].append("pide_bitacora_no_exigida")

            for u in f.get("ubicaciones", []) or []:
                r = {"tipo": u.get("tipo")}
                t = u.get("tipo")
                cita = u.get("cita_literal", "")
                if t == "pdf":
                    pg = u.get("pdf_page")
                    if not cita:
                        r["resultado"] = "sin_cita"
                        vm["errores"].append("ubicación PDF sin cita_literal")
                    elif pg not in texts:
                        r["resultado"] = "pagina_inexistente"
                        vm["errores"].append(f"página {pg} no existe")
                    else:
                        ok, ratio = contains(texts[pg], cita)
                        if ok:
                            r["resultado"] = "ok" if ratio == 1.0 else "aproximada"
                            if ratio < 1.0:
                                vm["advertencias"].append("cita_aproximada")
                        else:
                            hit = next((p for p, tx in texts.items() if contains(tx, cita)[0]), None)
                            if hit:
                                r["resultado"] = f"pagina_corregida:{pg}->{hit}"
                                u["pdf_page"] = hit
                                vm["estado"] = "pagina_corregida"
                            else:
                                r["resultado"] = f"no_encontrada (mejor coincidencia {ratio:.0%})"
                                vm["errores"].append(f"cita no encontrada en el PDF: '{cita[:60]}'")
                elif t == "repo":
                    base = pdir / "input" / ("repo_docs" if u.get("repo") == "docs" else "repo_codigo")
                    p = base / (u.get("path") or "")
                    if not u.get("path") or not p.is_file():
                        r["resultado"] = "archivo_inexistente"
                        vm["errores"].append(f"archivo inexistente: {u.get('path')}")
                    elif cita:
                        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
                        ln = u.get("line")
                        window = "\n".join(lines[max(0, ln - 4): ln + 3]) if ln else "\n".join(lines)
                        ok, ratio = contains(window, cita)
                        r["resultado"] = "ok" if ok else f"no_encontrada (mejor {ratio:.0%})"
                        if not ok:
                            vm["errores"].append(f"cita no encontrada en {u['path']}:{ln}")
                    else:
                        r["resultado"] = "archivo_ok_sin_cita"
                elif t == "artifact":
                    ref = u.get("artifact", "")
                    name, _, cid = ref.partition("#")
                    data = load_json(art / name)
                    if data is None:
                        r["resultado"] = "artifact_inexistente"
                        vm["errores"].append(f"artifact inexistente: {name}")
                    elif cid:
                        chk = next((c for c in data.get("checks", []) if c.get("id") == cid), None)
                        if not chk:
                            r["resultado"] = "check_inexistente"
                            vm["errores"].append(f"check inexistente: {ref}")
                        else:
                            r["resultado"] = f"ok ({chk['estado']})" if chk["estado"] == "OK" else f"check ({chk['estado']})"
                            if f.get("semaforo") == "VERDE" and chk["estado"] in ("FALLA", "ALERTA"):
                                vm["advertencias"].append(f"contradice_script:{ref}={chk['estado']}")
                            if f.get("semaforo") in ("ROJO", "AMARILLO") and chk["estado"] == "OK" and f.get("origen") == "script":
                                vm["advertencias"].append(f"contradice_script:{ref}=OK")
                    else:
                        r["resultado"] = "artifact_ok_sin_check"
                elif t == "web":
                    r["resultado"] = "registrada" if u.get("url") and u.get("fecha") else "incompleta"
                    if r["resultado"] == "incompleta":
                        vm["errores"].append("ubicación web sin url o fecha")
                else:
                    r["resultado"] = "tipo_desconocido"
                    vm["errores"].append(f"tipo de ubicación desconocido: {t}")
                vm["ubicaciones"].append(r)
            if f.get("semaforo") == "VERDE" and not any(x.get("resultado", "").startswith(("ok", "aproximada", "pagina_corregida")) and x.get("resultado") != "artifact_ok_sin_check" for x in vm["ubicaciones"]):
                vm["errores"].append("VERDE sin evidencia positiva verificable")
            if vm["errores"]:
                vm["estado"] = "descartada"
            f["verificacion_mecanica"] = vm
            out.append(f)
            summary.append({"archivo": mf.name, "clave": f.get("clave"), "estado": vm["estado"], "errores": vm["errores"], "advertencias": vm["advertencias"]})
        save_json(mf.with_name(mf.name.replace(".maker.json", ".verified.json")), out)

    tally = {}
    for s in summary:
        tally[s["estado"]] = tally.get(s["estado"], 0) + 1
    save_json(art / "verify_evidence.json", {"resumen": tally, "hallazgos": summary})
    print(f"[verify_evidence] {len(summary)} hallazgos: {tally}")
    for s in summary:
        if s["estado"] == "descartada":
            print(f"  DESCARTADA {s['clave']}: {'; '.join(s['errores'])}")


if __name__ == "__main__":
    main()
