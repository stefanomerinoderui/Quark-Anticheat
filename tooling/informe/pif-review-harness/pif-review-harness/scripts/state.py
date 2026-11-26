#!/usr/bin/env python3
"""Estado longitudinal del proyecto (review_state.json).

Subcomandos:
  register  registra una entrega (hash del PDF, commit, fecha de clon, tag y vencimiento)
  merge     consolida los hallazgos auditados en observaciones OBS-xx estables y detecta reincidencia
  matriz    imprime la matriz de respuesta (Markdown) para la devolución
  show      resumen del estado
"""
import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import artifacts, load_json, now_iso, project_dir, save_json, sha256  # noqa: E402

OPEN = {"abierta", "reincidente", "parcial"}


def load_state(pid):
    p = project_dir(pid) / "review_state.json"
    return p, load_json(p, {"proyecto_id": pid, "entregas": [], "observaciones": []})


def cmd_register(a):
    p, st = load_state(a.id)
    plan = load_json(project_dir(a.id) / "plan_entregas.json", {}) or {}
    inst = next((i for i in plan.get("instancias", []) if i.get("id") == a.instancia), {})
    entry = {"instancia": a.instancia, "recibido_el": now_iso(), "perfil": inst.get("perfil"), "informes": []}
    if a.pdf:
        entry["pdf"] = {"archivo": Path(a.pdf).name, "sha256": sha256(Path(a.pdf))}
    for which, commit, ref, tagdate in (("codigo", a.commit, a.ref, a.tag_fecha), ("docs", a.docs_commit, a.docs_ref, None)):
        if not commit:
            continue
        info = {"origen": a.origen if which == "codigo" else a.docs_origen, "ref": ref, "commit": commit, "clonado_el": now_iso(),
                "tag_esperado": inst.get("tag_esperado") if which == "codigo" else None, "tag_fecha": tagdate or None, "antes_del_vencimiento": None}
        if tagdate and inst.get("fecha_limite"):
            try:
                info["antes_del_vencimiento"] = dt.datetime.fromisoformat(tagdate) <= dt.datetime.fromisoformat(inst["fecha_limite"])
            except ValueError:
                pass
        entry["repo_" + which] = info
    prev = [e for e in st["entregas"] if e.get("pdf", {}).get("sha256") and e.get("pdf", {}).get("sha256") == entry.get("pdf", {}).get("sha256")]
    if prev:
        print(f"[state] Aviso: el PDF es idéntico al de la entrega {prev[-1]['instancia']}.")
    st["entregas"].append(entry)
    save_json(p, st)
    print(f"[state] entrega {a.instancia} registrada")


def cmd_merge(a):
    p, st = load_state(a.id)
    fdir = artifacts(a.id) / "findings"
    checked = sorted(fdir.glob("*.checked.json"))
    if not checked:
        sys.exit("No hay artifacts/findings/*.checked.json: correr verify_evidence.py y el subagente checker primero.")
    final, evaluated_items = [], set()
    for f in checked:
        evaluated_items.add(f.name.split(".")[0])  # el ítem se evaluó aunque no haya dejado hallazgos
        for h in load_json(f) or []:
            evaluated_items.add(h.get("item_id"))
            dec = (h.get("checker") or {}).get("decision", "aprobado")
            if dec == "descartado" or (h.get("verificacion_mecanica") or {}).get("estado") == "descartada":
                continue
            final.append(h)
    by_key = {o["clave"]: o for o in st["observaciones"]}
    nxt = max([int(o["id"].split("-")[1]) for o in st["observaciones"]] + [0]) + 1
    seen = set()
    # seguimiento explícito desde SEG-01
    for h in final:
        seg = h.get("seguimiento")
        if seg and seg.get("obs_id"):
            o = next((x for x in st["observaciones"] if x["id"] == seg["obs_id"]), None)
            if o:
                o["estado"] = seg.get("estado", o["estado"])
                o["historial"].append({"instancia": a.instancia, "estado": o["estado"], "nota": seg.get("nota", "")})
                seen.add(o["clave"])
    for h in final:
        if h.get("seguimiento") or h.get("semaforo") not in ("ROJO", "AMARILLO") or h.get("destino") == "informe_docente":
            continue
        k = h["clave"]
        if k in by_key:
            o = by_key[k]
            if o["estado"] in OPEN or o["estado"] == "subsanada_a_confirmar":
                o["estado"] = "reincidente" if o["instancia_origen"] != a.instancia else o["estado"]
            else:
                o["estado"] = "reincidente"
            o["semaforo"] = h["semaforo"]
            o["historial"].append({"instancia": a.instancia, "estado": o["estado"]})
        else:
            o = {"id": f"OBS-{nxt:02d}", "clave": k, "item_id": h["item_id"], "semaforo": h["semaforo"], "resumen": h["observacion"][:200],
                 "instancia_origen": a.instancia, "estado": "abierta", "historial": [{"instancia": a.instancia, "estado": "abierta"}]}
            nxt += 1
            st["observaciones"].append(o)
            by_key[k] = o
        h["obs_id"] = o["id"]
        h["obs_estado"] = o["estado"]
        seen.add(k)
    for o in st["observaciones"]:
        if o["estado"] in OPEN and o["clave"] not in seen and o["item_id"] in evaluated_items and o["instancia_origen"] != a.instancia:
            o["estado"] = "subsanada_a_confirmar"
            o["historial"].append({"instancia": a.instancia, "estado": o["estado"], "nota": "no reapareció; confirmar en SEG-01 o en el coloquio"})
    save_json(p, st)
    order = {"ROJO": 0, "AMARILLO": 1, "VERDE": 2, "GRIS": 3}
    final.sort(key=lambda h: (order.get(h["semaforo"], 9), h.get("obs_id") or "ZZ", h["item_id"]))
    save_json(artifacts(a.id) / f"findings_final_{a.instancia}.json", final)
    tally = {}
    for h in final:
        tally[h["semaforo"]] = tally.get(h["semaforo"], 0) + 1
    print(f"[state] {len(final)} hallazgos consolidados {tally}; observaciones: {len(st['observaciones'])} "
          f"({sum(1 for o in st['observaciones'] if o['estado'] == 'reincidente')} reincidentes)")


def cmd_matriz(a):
    _, st = load_state(a.id)
    rows = ["| N.º | Observación | Cambio realizado | Ubicación (pág./archivo) | Evidencia presentada | Responsable | Uso de IA |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for o in st["observaciones"]:
        if o["estado"] in OPEN:
            rows.append(f"| {o['id']} | {o['resumen'].replace('|', '/')} |  |  |  |  |  |")
    print("\n".join(rows))


def cmd_show(a):
    _, st = load_state(a.id)
    print(f"Proyecto {st['proyecto_id']}: {len(st['entregas'])} entregas")
    for e in st["entregas"]:
        rc = e.get("repo_codigo") or {}
        print(f"  {e['instancia']}  {e['recibido_el']}  pdf={e.get('pdf', {}).get('sha256', '')[:10]}  commit={rc.get('commit', '')[:10]}")
    for o in st["observaciones"]:
        print(f"  {o['id']} [{o['semaforo']}] {o['estado']:<22} {o['clave']}")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    r = sp.add_parser("register")
    for k in ("--id", "--instancia"):
        r.add_argument(k, required=True)
    for k in ("--pdf", "--commit", "--ref", "--origen", "--tag-fecha", "--docs-commit", "--docs-ref", "--docs-origen"):
        r.add_argument(k)
    m = sp.add_parser("merge")
    m.add_argument("--id", required=True)
    m.add_argument("--instancia", required=True)
    mt = sp.add_parser("matriz")
    mt.add_argument("--id", required=True)
    s = sp.add_parser("show")
    s.add_argument("--id", required=True)
    a = ap.parse_args()
    {"register": cmd_register, "merge": cmd_merge, "matriz": cmd_matriz, "show": cmd_show}[a.cmd](a)


if __name__ == "__main__":
    main()
