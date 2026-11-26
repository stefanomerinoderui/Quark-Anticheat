#!/usr/bin/env python3
"""Capa 1 — Portafolio Digital y Bitácoras Individuales (entregas parciales de AE, Guía de Evaluación Multimodal).

Entradas (las copia init_review.sh con --portafolio-dir y --bitacoras-dir):
  input/portafolio/   archivos del Portafolio Digital del equipo (cualquier estructura)
  input/bitacoras/    una o más bitácoras por integrante (.pdf, .docx, .md, .txt); el nombre del archivo
                      o de su carpeta debe contener el nombre o apellido del integrante (plan_entregas.equipo)

Salida: artifacts/proceso.json
  portafolio        elementos esperados según la consigna de la instancia: encontrado / no encontrado
  bitacoras         por integrante: archivo, entradas fechadas, seis elementos de cada entrada, señales
  bitacoras_similitud  pares de bitácoras casi idénticas
Es heurístico (nombres de archivo y palabras clave): propone COMPLETO / INCOMPLETO y el docente confirma (GD2 7).
"""
import argparse
import difflib
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import OK, ALERTA, FALLA, GRIS, check, load_json, norm, project_dir, write_artifact  # noqa: E402

# Contenido mínimo del Portafolio por instancia (consignas AE1, AE2 y AE4 2026)
PORTAFOLIO = {
    "AE1": {
        "instrumentos 1 a 22": r"instrumento",
        "acta de constitución del equipo": r"acta.{0,20}constituci|constituci.{0,20}equipo",
        "análisis del entorno (PESTEL, cinco fuerzas, cadena de valor, FODA)": r"pestel|cinco.?fuerzas|5.?fuerzas|cadena.?de.?valor|foda",
        "registro de fuentes": r"registro.{0,10}fuentes|fuentes",
        "evidencia de contacto con la organización": r"contacto|entrevista|correo|mail|reuni[oó]n|minuta",
        "versiones sucesivas del documento": r"v\d|versi[oó]n|borrador",
        "devolución docente / versión mejorada": r"devoluci|mejorad",
    },
    "AE2": {
        "instrumentos de la Unidad Dos (delimitación, lienzo, rivalidad, recursos)": r"lienzo|canvas|rivalidad|recursos|delimitaci|dominio",
        "matriz de trazabilidad": r"trazabilidad",
        "acta de validación de requisitos con el referente": r"validaci",
        "versiones del documento y del catálogo": r"v\d|versi[oó]n|cat[aá]logo",
        "evidencia de integración continua": r"\bci\b|integraci[oó]n.?continua|pipeline|build|workflow|actions",
        "devolución de AE1 y constancia de correcciones": r"devoluci|correcci",
    },
    "AE4": {
        "instrumentos de la Unidad Cuatro (hoja de ruta, factibilidad, búsqueda marcaria, escalabilidad)": r"hoja.?de.?ruta|roadmap|factibilidad|marca|inpi|escalab",
        "actas de revisión y retrospectiva de los sprints": r"retro|revisi[oó]n.{0,10}sprint|sprint.{0,10}review",
        "plan de implantación y acta de cierre": r"implantaci|cierre",
        "evidencia de CI y verificación del manual en máquina limpia": r"\bci\b|integraci[oó]n.?continua|pipeline|build|m[aá]quina.?limpia|despliegue",
        "versiones sucesivas del informe": r"v\d|versi[oó]n|borrador",
        "devoluciones y constancia de correcciones": r"devoluci|correcci",
        "guion de la demostración y protocolo de contingencia": r"gui[oó]n|demo|contingencia",
    },
}
# Seis elementos de cada entrada de la Bitácora (consignas AE1, AE2 y AE4; GD2 8.2)
BITACORA = {
    "qué se decidió": r"decid|decisi[oó]n",
    "alternativas y criterio de descarte": r"alternativ|descart|opci[oó]n",
    "evidencia que sostiene la decisión": r"evidencia|fuente|dato|prueba|validaci|resultado",
    "aporte personal (commit, tarjeta, apartado)": r"aport|commit|tarjeta|issue|pull request|\bpr\b|apartado|realic[eé]|hice|implement[eé]|redact[eé]",
    "desacuerdos y su resolución": r"desacuerdo|conflicto|discrepan|sin desacuerdo|no hubo desacuerdo",
    "herramienta auxiliar utilizada": r"herramienta|inteligencia artificial|\bia\b|chatgpt|copilot|claude|gemini|asistente|no se utiliz",
}
DATE = re.compile(r"\b(\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4}|\d{4}-\d{2}-\d{2}|\d{1,2}\s+de\s+(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre)(\s+de\s+\d{4})?)\b", re.I)
TEXT_EXT = {".md", ".txt", ".csv", ".json", ".yml", ".yaml"}


def read_text(p: Path) -> str:
    try:
        if p.suffix.lower() in TEXT_EXT:
            return p.read_text(encoding="utf-8", errors="replace")
        if p.suffix.lower() == ".pdf":
            try:
                import pymupdf
            except ImportError:
                import fitz as pymupdf  # type: ignore
            return "\n".join(pg.get_text() for pg in pymupdf.open(p))
        if p.suffix.lower() == ".docx":
            with zipfile.ZipFile(p) as z:
                xml = z.read("word/document.xml").decode("utf-8", "replace")
            xml = re.sub(r"</w:p>", "\n", xml)
            return re.sub(r"<[^>]+>", "", xml)
    except Exception:
        return ""
    return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    pdir = project_dir(a.id)
    plan = load_json(pdir / "plan_entregas.json", {}) or {}
    state = load_json(pdir / "review_state.json", {}) or {}
    inst_id = ((state.get("entregas") or [{}])[-1]).get("instancia", "")
    inst = next((i for i in plan.get("instancias", []) if i.get("id") == inst_id), {})
    exige = inst.get("exige_portafolio_bitacora") is True
    key = next((k for k in PORTAFOLIO if inst_id.upper().startswith(k)), None)
    checks = []

    if not exige:
        write_artifact(a.id, "proceso.json", [check("alcance", GRIS, f"La instancia {inst_id or '?'} no exige portafolio ni bitácora (versión final: RR 97/23).")])
        print("[audit_proceso] no aplica en esta instancia")
        return

    # --- Portafolio
    port = pdir / "input" / "portafolio"
    if not port.exists() or not any(port.rglob("*")):
        checks.append(check("portafolio", GRIS, "No se ingresó el portafolio (usar --portafolio-dir en init_review.sh)."))
    else:
        files = [p for p in port.rglob("*") if p.is_file()]
        corpus = [(str(p.relative_to(port)), norm(str(p.relative_to(port))) + " " + norm(read_text(p)[:20000])) for p in files]
        items = {}
        for name, rx in (PORTAFOLIO.get(key) or {}).items():
            hits = [f for f, txt in corpus if re.search(rx, txt, re.I)]
            items[name] = hits[:8]
        falt = [k for k, v in items.items() if not v]
        estado = GRIS if not key else (OK if not falt else ALERTA)
        checks.append(check("portafolio", estado,
                            (f"{len(files)} archivos; elementos esperados para {key}: {len(items) - len(falt)} de {len(items)} encontrados." if key else
                             f"{len(files)} archivos; no hay lista de elementos esperados para la instancia {inst_id}.")
                            + (f" No encontrados: {'; '.join(falt)}." if falt else ""),
                            elementos=items, archivos=len(files), propuesta="COMPLETO" if key and not falt else "INCOMPLETO (a confirmar)",
                            nota="Heurístico por nombre y contenido de archivo. COMPLETO = presentado y con los mínimos (GD2 7); lo confirma el docente."))

    # --- Bitácoras
    bdir = pdir / "input" / "bitacoras"
    team = [m["nombre"] for m in plan.get("equipo", [])]
    if not bdir.exists() or not any(bdir.rglob("*")):
        checks.append(check("bitacoras", GRIS, "No se ingresaron bitácoras (usar --bitacoras-dir en init_review.sh)."))
    elif not team:
        checks.append(check("bitacoras", GRIS, "plan_entregas.json no tiene integrantes: no se puede asignar cada bitácora."))
    else:
        files = [p for p in bdir.rglob("*") if p.is_file()]
        per, texts = {}, {}
        for m in team:
            toks = [norm(t) for t in m.split() if len(t) > 2]
            mine = [p for p in files if any(t in norm(str(p.relative_to(bdir))) for t in toks)]
            txt = "\n".join(read_text(p) for p in mine)
            texts[m] = txt
            dates = DATE.findall(txt)
            elems = {k: bool(re.search(rx, txt, re.I)) for k, rx in BITACORA.items()}
            words = len(txt.split())
            senales = []
            if mine and words < 150:
                senales.append("muy breve")
            if mine and not elems["qué se decidió"]:
                senales.append("no registra decisiones (¿crónica de reuniones?, GD2 8.2)")
            if mine and len(dates) < 2:
                senales.append("menos de dos entradas fechadas")
            falt = [k for k, v in elems.items() if not v]
            per[m] = {"archivos": [str(p.relative_to(bdir)) for p in mine], "palabras": words, "entradas_fechadas": len(dates),
                      "elementos_presentes": [k for k, v in elems.items() if v], "elementos_ausentes": falt if mine else list(BITACORA),
                      "senales": senales, "propuesta": "COMPLETO" if mine and not falt and not senales else "INCOMPLETO (a confirmar)"}
        sin = [m for m, v in per.items() if not v["archivos"]]
        pairs = []
        names = [m for m in team if texts.get(m)]
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                r = difflib.SequenceMatcher(None, norm(texts[names[i]])[:20000], norm(texts[names[j]])[:20000]).ratio()
                pairs.append({"a": names[i], "b": names[j], "similitud": round(r, 2)})
        high = [p for p in pairs if p["similitud"] > 0.6]
        estado = FALLA if sin else (ALERTA if any(v["propuesta"] != "COMPLETO" for v in per.values()) or high else OK)
        checks.append(check("bitacoras", estado,
                            f"Bitácoras: {len(team) - len(sin)} de {len(team)} integrantes"
                            + (f"; sin bitácora: {', '.join(sin)}" if sin else "")
                            + (f"; {len(high)} pares casi idénticos" if high else "") + ".",
                            por_integrante=per, similitud=pairs,
                            nota="La Bitácora es individual y componente de cierre en las AE grupales (GD2 8.2). Elementos por palabras clave: confirmar leyendo."))

    write_artifact(a.id, "proceso.json", checks, meta={"instancia": inst_id, "lista_portafolio": key})
    print(f"[audit_proceso] {len(checks)} controles → artifacts/proceso.json")


if __name__ == "__main__":
    main()
