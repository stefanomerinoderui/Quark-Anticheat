#!/usr/bin/env python3
"""Capa 1 — Formato físico y estructura del PDF (RR97 Art. 20, 21, 22).

Lee artifacts/pdf_pages.json y escribe artifacts/pdf_format.json con:
  page_size, margins, line_spacing, fonts, page_numbers, annex_numbering,
  abstract_words, chapter_title_pages, first_person  (checks)
  sections  (mapa de secciones → páginas, lo usan otros scripts)
"""
import argparse
import re
import statistics as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import OK, FALLA, ALERTA, GRIS, ROMAN, check, load_pages, norm, write_artifact  # noqa: E402

A4 = (595.3, 841.9)
CM = 72 / 2.54
LR_MIN, TOP_MIN, TOL = 3 * CM, 2.5 * CM, 6.0
HEADER_ZONE = 60.0       # pt desde el borde superior: encabezado (se excluye de la medición del margen superior)
FOOTER_FRAC = 0.90       # todo lo que empieza por debajo del 90 % de la altura es pie

ROMAN_RE = re.compile(r"^\s*(?:CAP[IÍ]TULO\s+)?(XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\s*[.\-–:]?\s*$", re.I)
ROMAN_TITLE_RE = re.compile(r"^\s*(?:CAP[IÍ]TULO\s+)?(XIII|XII|XI|X|IX|VIII|VII|VI|V|IV|III|II|I)\s*[.\-–:]\s*([A-ZÁÉÍÓÚÑ ,]{4,})$")
HEAD = {
    "resumen": re.compile(r"^\s*RESUMEN\s*$", re.I),
    "indice": re.compile(r"^\s*[IÍ]NDICE(\s+(GENERAL|DE\s+CAP[IÍ]TULOS))?\s*$", re.I),
    "conclusiones": re.compile(r"^\s*CONCLUSIONES(\s+DEL\s+PROYECTO)?\s*$", re.I),
    "bibliografia": re.compile(r"^\s*(BIBLIOGRAF[IÍ]A|REFERENCIAS(\s+BIBLIOGR[AÁ]FICAS)?)\s*$", re.I),
    "anexo": re.compile(r"^\s*ANEXO\s+(III|II|I|[0-9]+)\b.*$", re.I),
}
FIRST_PERSON = re.compile(
    r"\b(nosotros|nuestr[oa]s?|hicimos|realizamos|decidimos|consideramos|creemos|desarrollamos|implementamos|"
    r"elegimos|utilizamos|usamos|logramos|tuvimos|pudimos|optamos|buscamos|propusimos|vamos a|queremos|necesitamos)\b",
    re.I,
)


def is_body_size(s):
    return 11.4 <= s <= 12.6


def heading_lines(p):
    """Líneas candidatas a título: cortas y fuera de encabezado/pie."""
    out = []
    for ln in p["lines"]:
        if ln["y0"] < HEADER_ZONE or ln["y0"] > p["height"] * FOOTER_FRAC:
            continue
        t = ln["text"].strip()
        if 1 <= len(t) <= 80:
            out.append(ln)
    return out


def find_sections(pages):
    sec = {"chapters": {}, "resumen": None, "indice": None, "conclusiones": None, "bibliografia": None, "anexos": {}}
    for p in pages:
        hl = heading_lines(p)
        texts = [ln["text"].strip() for ln in hl]
        # carátula de capítulo: pocas palabras, numeral romano centrado y título en mayúsculas
        if p["words"] <= 45:
            numeral, title = None, None
            for ln in hl:
                t = ln["text"].strip()
                cx = (ln["x0"] + ln["x1"]) / 2
                centered = abs(cx - p["width"] / 2) < 45
                m = ROMAN_RE.match(t) or ROMAN_TITLE_RE.match(t)
                if m and centered and numeral is None:
                    numeral = m.group(1).upper()
                    if m.re is ROMAN_TITLE_RE:
                        title = m.group(2).strip()
                    continue
                if numeral and title is None and t.upper() == t and len(t) > 3 and centered:
                    title = t
            if numeral and numeral not in sec["chapters"]:
                sec["chapters"][numeral] = {"title_page": p["index"], "title": title}
                continue
        for t in texts[:6]:
            for key in ("resumen", "indice", "conclusiones", "bibliografia"):
                if sec[key] is None and HEAD[key].match(t):
                    sec[key] = p["index"]
            m = HEAD["anexo"].match(t)
            if m and m.group(1).upper() not in sec["anexos"] and p["index"] > 3:
                sec["anexos"][m.group(1).upper()] = p["index"]
    # rangos de capítulos
    order = sorted(sec["chapters"].items(), key=lambda kv: kv[1]["title_page"])
    stops = sorted([v["title_page"] for v in sec["chapters"].values()]
                   + [x for x in (sec["conclusiones"], sec["bibliografia"]) if x]
                   + list(sec["anexos"].values()) + [len(pages) + 1])
    for num, info in order:
        nxt = min(s for s in stops if s > info["title_page"])
        info["start"] = info["title_page"] + 1
        info["end"] = nxt - 1
    return sec


def body_pages(pages, sec):
    excluded = {1} | {v["title_page"] for v in sec["chapters"].values()}
    first_annex = min(sec["anexos"].values()) if sec["anexos"] else None
    out = []
    for p in pages:
        if p["index"] in excluded or p["words"] < 80:
            continue
        if first_annex and p["index"] >= first_annex:
            continue
        if sec["indice"] and sec["chapters"]:
            first_ch = min(v["title_page"] for v in sec["chapters"].values())
            if sec["indice"] <= p["index"] < first_ch:
                continue  # el índice tiene líneas de puntos que distorsionan márgenes
        out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    pages = load_pages(a.id)
    checks = []
    if not pages:
        write_artifact(a.id, "pdf_format.json", [check("pdf", GRIS, "PDF sin páginas")])
        return
    if sum(1 for p in pages if p["words"] < 5) > len(pages) * 0.5:
        write_artifact(a.id, "pdf_format.json", [check("pdf", GRIS, "PDF mayormente sin texto (¿escaneado?). Verificación visual con pdftoppm -r 50.")])
        print("[audit_pdf_format] PDF sin texto: todo GRIS")
        return

    sec = find_sections(pages)
    body = body_pages(pages, sec)

    # --- tamaño de hoja
    bad = [p["index"] for p in pages if abs(p["width"] - A4[0]) > 3 or abs(p["height"] - A4[1]) > 3]
    checks.append(check("page_size", FALLA if bad else OK,
                        f"{len(bad)} páginas no A4" if bad else "Todas las páginas A4",
                        paginas=bad[:50], valor=f"{pages[0]['width']}×{pages[0]['height']} pt", umbral="595×842 pt ±3"))

    # --- márgenes
    per_page, viol = [], {"izquierdo": [], "derecho": [], "superior": []}
    for p in body:
        ls = [ln for ln in p["lines"] if ln["chars"] > 3 and ln["y0"] > HEADER_ZONE and ln["y0"] < p["height"] * FOOTER_FRAC]
        if not ls:
            continue
        left = min(ln["x0"] for ln in ls)
        right = p["width"] - max(ln["x1"] for ln in ls)
        top = min(ln["y0"] for ln in ls)
        per_page.append({"pagina": p["index"], "izq": round(left, 1), "der": round(right, 1), "sup": round(top, 1)})
        if left < LR_MIN - TOL:
            viol["izquierdo"].append(p["index"])
        if right < LR_MIN - TOL:
            viol["derecho"].append(p["index"])
        if top < TOP_MIN - TOL:
            viol["superior"].append(p["index"])
    if per_page:
        med = {k: round(st.median(x[k] for x in per_page), 1) for k in ("izq", "der", "sup")}
        n_bad = sum(len(v) for v in viol.values())
        estado = OK if n_bad == 0 else (FALLA if any(len(v) > len(per_page) * 0.3 for v in viol.values()) else ALERTA)
        checks.append(check("margins", estado,
                            f"Mediana izq {med['izq']} pt ({med['izq']/CM:.2f} cm), der {med['der']} pt ({med['der']/CM:.2f} cm), sup {med['sup']} pt ({med['sup']/CM:.2f} cm). "
                            "El margen inferior no se mide (el pie lo contamina).",
                            umbral=f"izq/der ≥ {LR_MIN:.0f} pt, sup ≥ {TOP_MIN:.0f} pt (tolerancia {TOL} pt)",
                            violaciones={k: v[:60] for k, v in viol.items()}, mediana=med, paginas_medidas=len(per_page)))
    else:
        checks.append(check("margins", GRIS, "No hay páginas de cuerpo medibles"))

    # --- interlineado
    ratios = []
    for p in body:
        ls = [ln for ln in p["lines"] if is_body_size(ln["size"]) and ln["chars"] > 20]
        gaps = []
        for l1, l2 in zip(ls, ls[1:]):
            g = l2["baseline"] - l1["baseline"]
            if 0.8 * l1["size"] < g < 4 * l1["size"]:
                gaps.append(g / l1["size"])
        if len(gaps) >= 4:
            ratios.append((p["index"], round(st.median(gaps), 2)))
    if ratios:
        lows = [pg for pg, r in ratios if r < 1.9]
        med = st.median(r for _, r in ratios)
        estado = OK if not lows else (FALLA if len(lows) > len(ratios) * 0.3 else ALERTA)
        checks.append(check("line_spacing", estado,
                            f"Interlineado mediano {med:.2f}× el tamaño de fuente; {len(lows)} de {len(ratios)} páginas por debajo de 1,9×.",
                            umbral="doble: ≥ 1,9× (Word doble ≈ 2,3×; 1,5 líneas ≈ 1,7×)", paginas=lows[:60]))
    else:
        checks.append(check("line_spacing", GRIS, "No se pudo medir: no hay renglones de cuerpo en tamaño 12"))

    # --- tipografía
    fam, sizes, nontimes_pages = {}, {}, []
    for p in body:
        page_total, page_times = 0, 0
        for ln in p["lines"]:
            for f in ln["fonts"]:
                family = re.sub(r"[-,].*$", "", f["font"].split("+")[-1])
                fam[family] = fam.get(family, 0) + f["chars"]
                sizes[f["size"]] = sizes.get(f["size"], 0) + f["chars"]
                page_total += f["chars"]
                if "times" in f["font"].lower():
                    page_times += f["chars"]
        if page_total and page_times / page_total < 0.5:
            nontimes_pages.append(p["index"])
    total = sum(fam.values()) or 1
    times = sum(v for k, v in fam.items() if "times" in k.lower())
    size12 = sum(v for k, v in sizes.items() if is_body_size(k))
    share_t, share_12 = times / total, size12 / total
    top_fams = sorted(fam.items(), key=lambda kv: -kv[1])[:5]
    estado = OK if share_t >= 0.85 and share_12 >= 0.6 else (ALERTA if share_t >= 0.6 else FALLA)
    checks.append(check("fonts", estado,
                        f"Times New Roman: {share_t:.0%} de los caracteres del cuerpo; tamaño 12: {share_12:.0%}.",
                        familias=[{"fuente": k, "proporcion": round(v / total, 3)} for k, v in top_fams],
                        paginas_no_times=nontimes_pages[:60], umbral="Times ≥ 85 %"))

    # --- numeración
    body_idx = {p["index"] for p in body}
    seq = [(p["index"], int(p["printed"]["num"])) for p in pages if p["printed"] and p["index"] in body_idx]
    breaks = [{"pagina_pdf": b[0], "impresa": b[1], "anterior": a_[1]} for a_, b in zip(seq, seq[1:])
              if b[1] - a_[1] != b[0] - a_[0]]
    sin_num = sorted(body_idx - {i for i, _ in seq})
    caratula_num = bool(pages[0]["printed"])
    estado = OK if not breaks and len(sin_num) <= 2 and not caratula_num else ALERTA
    checks.append(check("page_numbers", estado if seq else GRIS,
                        f"{len(seq)} páginas de cuerpo con número impreso; {len(breaks)} saltos; {len(sin_num)} sin número."
                        + (" La carátula tiene número." if caratula_num else ""),
                        saltos=breaks[:30], sin_numero=sin_num[:60]))

    # --- anexos: "página X de Y"
    if sec["anexos"]:
        first = min(sec["anexos"].values())
        ann = [p for p in pages if p["index"] >= first]
        ok_xy = [p["index"] for p in ann if p["printed"] and p["printed"]["total"]]
        missing = [p["index"] for p in ann if p["index"] not in ok_xy]
        checks.append(check("annex_numbering", OK if not missing else ALERTA,
                            f"{len(ok_xy)} de {len(ann)} páginas de anexos con numeración 'X de Y'.",
                            paginas=missing[:60], anexos=sec["anexos"]))
    else:
        checks.append(check("annex_numbering", FALLA, "No se detectaron encabezados 'ANEXO I/II/III'.", anexos={}))

    # --- resumen
    if sec["resumen"]:
        words, started, pg = 0, False, sec["resumen"]
        stop = re.compile(r"^\s*([IÍ]NDICE|ABSTRACT|PALABRAS\s+CLAVE|KEYWORDS)\b", re.I)
        span_pages = []
        for p in pages[pg - 1: pg + 3]:
            if p["index"] in {v["title_page"] for v in sec["chapters"].values()}:
                break
            done = False
            for ln in p["lines"]:
                t = ln["text"].strip()
                if ln["y0"] < HEADER_ZONE or ln["y0"] > p["height"] * FOOTER_FRAC:
                    continue
                if not started:
                    if HEAD["resumen"].match(t):
                        started = True
                    continue
                if stop.match(t):
                    done = True
                    break
                words += len(t.split())
            span_pages.append(p["index"])
            if done:
                break
        checks.append(check("abstract_words", OK if words <= 600 else FALLA, f"Resumen: {words} palabras.",
                            valor=words, umbral="≤ 600", paginas=span_pages))
    else:
        checks.append(check("abstract_words", FALLA, "No se encontró el encabezado 'RESUMEN'."))

    # --- carátulas de capítulo
    found = sec["chapters"]
    missing = [r for r in ROMAN if r not in found]
    repeated = []
    for num, info in found.items():
        if info.get("title") and info["start"] <= len(pages):
            nxt = pages[info["start"] - 1]
            first_lines = " ".join(ln["text"] for ln in nxt["lines"][:4] if ln["y0"] > HEADER_ZONE)
            if norm(info["title"]) and norm(info["title"]) in norm(first_lines):
                repeated.append(num)
    checks.append(check("chapter_title_pages", OK if not missing and not repeated else ALERTA,
                        f"Carátulas detectadas: {len(found)} de 13."
                        + (f" No detectadas: {', '.join(missing)}." if missing else "")
                        + (f" Título repetido en la hoja siguiente: {', '.join(repeated)}." if repeated else ""),
                        detectadas={k: {"pagina": v["title_page"], "titulo": v.get("title")} for k, v in found.items()},
                        no_detectadas=missing, titulo_repetido=repeated,
                        nota="La detección es heurística: confirmar visualmente los capítulos 'no detectados' antes de observar."))

    # --- primera persona (Art. 21), excluyendo Cap. XII
    cap12 = set(range(found["XII"]["start"], found["XII"]["end"] + 1)) if "XII" in found else set()
    hits = []
    for p in body:
        if p["index"] in cap12:
            continue
        txt = " ".join(ln["text"] for ln in p["lines"])
        ms = FIRST_PERSON.findall(txt)
        if ms:
            hits.append({"pagina": p["index"], "n": len(ms), "ejemplos": sorted(set(m.lower() for m in ms))[:6]})
    total_fp = sum(h["n"] for h in hits)
    checks.append(check("first_person", OK if total_fp == 0 else ALERTA,
                        f"{total_fp} formas en primera persona en {len(hits)} páginas (fuera del Cap. XII).",
                        paginas=hits[:80]))

    write_artifact(a.id, "pdf_format.json", checks, meta={"paginas": len(pages), "paginas_cuerpo": len(body)}, sections=sec)
    print(f"[audit_pdf_format] {len(checks)} controles → artifacts/pdf_format.json")


if __name__ == "__main__":
    main()
