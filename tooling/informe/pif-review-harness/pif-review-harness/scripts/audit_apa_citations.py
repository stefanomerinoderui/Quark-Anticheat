#!/usr/bin/env python3
"""Capa 1 — Cruce citas en el texto ↔ Bibliografía y formato APA 7.

Salidas:
  artifacts/referencias.json     entradas de la Bibliografía estructuradas (insumo de audit_references.py)
  artifacts/apa_citations.json   checks de cruce y de formato
"""
import argparse
import difflib
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import OK, ALERTA, FALLA, GRIS, artifacts, check, load_json, load_pages, save_json, strip_accents, write_artifact  # noqa: E402

YEAR = r"(\d{4}[a-z]?|s\.\s?f\.|n\.\s?d\.)"
ENTRY_YEAR = re.compile(r"\(\s*" + YEAR + r"(?:,[^)]*)?\)")
DOI = re.compile(r"(10\.\d{4,9}/[^\s\"<>]+)", re.I)
URL = re.compile(r"(https?://[^\s<>\"]+)", re.I)
SHORT = re.compile(r"https?://(bit\.ly|tinyurl\.com|goo\.gl|t\.co|ow\.ly|is\.gd|buff\.ly|rb\.gy|cutt\.ly)/", re.I)
PAREN = re.compile(r"\(([^()]{2,250}?)\)")
CIT_ITEM = re.compile(r"^\s*(?:v[eé]ase\s+|cf\.\s+)?(.+?),\s*" + YEAR + r"(?:\s*,\s*p+\.\s*[\d\-–]+)?\s*$", re.I)
NARR = re.compile(r"([A-ZÁÉÍÓÚÑ][\wáéíóúñüÁÉÍÓÚÑÜ'\-]+(?:\s+(?:y|&|e)\s+[A-ZÁÉÍÓÚÑ][\wáéíóúñü\-]+)?(?:\s+et\s+al\.)?)\s+\(" + YEAR + r"\)")
STOP_WORDS = {"en", "de", "la", "el", "los", "las", "del", "segun", "según", "por", "con", "para", "como", "y"}


def key(name: str) -> str:
    name = re.sub(r"\bet\s+al\.?", "", name, flags=re.I).strip()
    name = re.split(r"\s+(?:y|&|e)\s+|,", name)[0].strip()
    toks = [t for t in re.split(r"\s+", name) if t]
    if not toks:
        return ""
    # autor corporativo (varias palabras con mayúscula) → nombre completo; persona → primer apellido
    k = name if len(toks) > 2 else toks[-1] if toks[0].lower() in STOP_WORDS else toks[0]
    return re.sub(r"[^a-z0-9 ]", "", strip_accents(k).lower()).strip()


def norm_year(y: str) -> str:
    y = y.lower().replace(" ", "")
    return "s.f." if y in ("s.f.", "n.d.") else y


def bib_lines(pages, sec):
    start = sec.get("bibliografia")
    if not start:
        return None, []
    ends = [v for v in sec.get("anexos", {}).values() if v > start]
    end = min(ends) - 1 if ends else len(pages)
    lines = []
    for p in pages[start - 1:end]:
        for ln in p["lines"]:
            t = ln["text"].strip()
            if ln["y0"] < 60 or ln["y0"] > p["height"] * 0.9 or not t:
                continue
            if re.match(r"^(BIBLIOGRAF[IÍ]A|REFERENCIAS)", t, re.I) and len(t) < 40:
                continue
            lines.append({**ln, "page": p["index"]})
    return (start, end), lines


def split_entries(lines):
    if not lines:
        return []
    min_x = min(ln["x0"] for ln in lines)
    indented = sum(1 for ln in lines if ln["x0"] > min_x + 12)
    entries, cur = [], None
    for ln in lines:
        t = ln["text"].strip()
        if indented >= len(lines) * 0.15:  # sangría francesa detectable
            new = ln["x0"] <= min_x + 4
        else:  # sin sangría: nueva entrada si la línea trae (año) en sus primeros 200 caracteres y la anterior cerró
            new = bool(ENTRY_YEAR.search(t[:200])) and (cur is None or cur["text"].rstrip().endswith((".", "/")) or URL.search(cur["text"][-80:] or ""))
        if new or cur is None:
            cur = {"text": t, "page": ln["page"]}
            entries.append(cur)
        else:
            joiner = "" if cur["text"].endswith(("-", "/")) else " "
            cur["text"] += joiner + t
    return entries


def parse_entry(e, n):
    t = e["text"]
    m = ENTRY_YEAR.search(t)
    authors = t[: m.start()].strip().rstrip(".").strip() if m else ""
    year = norm_year(m.group(1)) if m else None
    rest = t[m.end():].lstrip(". ").strip() if m else t
    title = re.split(r"(?<=[.?!])\s+(?=[A-ZÁÉÍÓÚÑ¿\[])", rest, maxsplit=1)[0].strip().rstrip(".")
    source = rest[len(title):].strip(" .") if title else ""
    doi = DOI.search(t)
    urls = [u.rstrip(".,;)") for u in URL.findall(t)]
    return {
        "n": n, "pagina": e["page"], "texto": t, "autores": authors, "anio": year,
        "titulo": title[:300], "fuente": re.sub(URL, "", source)[:200].strip(" ."),
        "doi": doi.group(1).rstrip(".,;)") if doi else None,
        "urls": urls, "primer_autor_clave": key(authors),
    }


def extract_citations(pages, texts, exclude):
    cits = []
    for p in pages:
        i = p["index"]
        if i in exclude:
            continue
        t = re.sub(r"-\n", "", texts[i]).replace("\n", " ")
        for m in PAREN.finditer(t):
            for part in m.group(1).split(";"):
                mm = CIT_ITEM.match(part)
                if mm and re.search(r"[A-Za-zÁÉÍÓÚÑ]{2}", mm.group(1)) and not re.match(r"^\d", mm.group(1)):
                    cits.append({"autor": mm.group(1).strip(), "anio": norm_year(mm.group(2)), "pagina": i, "forma": "parentetica", "texto": m.group(0)[:120]})
        for m in NARR.finditer(t):
            cits.append({"autor": m.group(1).strip(), "anio": norm_year(m.group(2)), "pagina": i, "forma": "narrativa", "texto": m.group(0)[:120]})
    for c in cits:
        c["clave"] = key(c["autor"])
    return [c for c in cits if c["clave"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    pages = load_pages(a.id)
    art = artifacts(a.id)
    fmt = load_json(art / "pdf_format.json", {}) or {}
    sec = fmt.get("sections", {})
    texts = {p["index"]: (art / "pdf_text" / f"page_{p['index']:04d}.txt").read_text(encoding="utf-8") for p in pages}

    rng, lines = bib_lines(pages, sec)
    if not rng:
        write_artifact(a.id, "apa_citations.json", [check("bibliografia", FALLA, "No se encontró la sección Bibliografía / Referencias")])
        save_json(art / "referencias.json", {"entradas": []})
        print("[audit_apa_citations] sin Bibliografía")
        return
    entries = [parse_entry(e, n) for n, e in enumerate(split_entries(lines), start=1)]
    save_json(art / "referencias.json", {"paginas": list(rng), "entradas": entries})

    exclude = set(range(rng[0], rng[1] + 1)) | {1}
    if sec.get("indice"):
        first_ch = min([v["title_page"] for v in sec.get("chapters", {}).values()] or [sec["indice"] + 1])
        exclude |= set(range(sec["indice"], first_ch))
    cits = extract_citations(pages, texts, exclude)

    by_key = defaultdict(list)
    for e in entries:
        by_key[e["primer_autor_clave"]].append(e)
    checks = []

    # citas sin entrada / años distintos
    sin_entrada, anio_distinto = [], []
    for c in cits:
        cands = by_key.get(c["clave"])
        if not cands:
            fuzzy = difflib.get_close_matches(c["clave"], list(by_key), n=1, cutoff=0.85)
            if fuzzy:
                cands = by_key[fuzzy[0]]
                c["coincidencia_aproximada"] = fuzzy[0]
        if not cands:
            sin_entrada.append(c)
        elif c["anio"] not in {e["anio"] for e in cands}:
            anio_distinto.append({**c, "anios_en_lista": sorted({e["anio"] or "?" for e in cands})})
    dedup = lambda xs: list({(x["clave"], x["anio"]): x for x in xs}.values())  # noqa: E731
    sin_entrada, anio_distinto = dedup(sin_entrada), dedup(anio_distinto)
    checks.append(check("citas_sin_entrada", OK if not sin_entrada else ALERTA, f"{len(sin_entrada)} citas sin entrada en la Bibliografía.", items=sin_entrada[:80]))
    checks.append(check("anio_distinto", OK if not anio_distinto else ALERTA, f"{len(anio_distinto)} citas con año distinto al de la lista.", items=anio_distinto[:50]))

    cited_keys = {(c["clave"], c["anio"]) for c in cits} | {(c.get("coincidencia_aproximada"), c["anio"]) for c in cits}
    otro_anio = {c["clave"] for c in anio_distinto}
    no_citadas = [{"n": e["n"], "autores": e["autores"], "anio": e["anio"], "pagina": e["pagina"]} for e in entries
                  if (e["primer_autor_clave"], e["anio"]) not in cited_keys and e["primer_autor_clave"] not in otro_anio]
    checks.append(check("entradas_no_citadas", OK if not no_citadas else ALERTA, f"{len(no_citadas)} entradas nunca citadas en el texto.", items=no_citadas[:80]))

    # duplicados
    dups = []
    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            a_, b_ = entries[i], entries[j]
            same_doi = a_["doi"] and a_["doi"].lower() == (b_["doi"] or "").lower()
            sim = difflib.SequenceMatcher(None, a_["titulo"].lower(), b_["titulo"].lower()).ratio() if a_["titulo"] and b_["titulo"] else 0
            if same_doi or sim > 0.9:
                dups.append({"a": a_["n"], "b": b_["n"], "similitud_titulo": round(sim, 2), "mismo_doi": bool(same_doi)})
    checks.append(check("duplicados", OK if not dups else ALERTA, f"{len(dups)} pares de entradas posiblemente duplicadas.", items=dups))

    # formato APA 7
    fmt_issues = defaultdict(list)
    for e in entries:
        t = e["texto"]
        if re.search(r"\bRecuperado\b(?!\s+el\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4},\s+de)", t):
            fmt_issues["fecha_recuperacion"].append(e["n"])
        if SHORT.search(t):
            fmt_issues["url_acortada"].append(e["n"])
        if re.search(r"\bdoi:\s*10\.|dx\.doi\.org", t, re.I):
            fmt_issues["doi_formato"].append(e["n"])
        if not e["anio"]:
            fmt_issues["sin_anio"].append(e["n"])
        if " & " in e["autores"]:
            fmt_issues["usa_ampersand"].append(e["n"])
        if re.search(r",\s+y\s+[A-ZÁÉÍÓÚÑ]", e["autores"]):
            fmt_issues["usa_y"].append(e["n"])
    has_sf = any("s.f." in e["texto"].lower() for e in entries)
    has_nd = any("n.d." in e["texto"].lower() for e in entries)
    if has_sf and has_nd:
        fmt_issues["mezcla_sf_nd"] = [e["n"] for e in entries if "n.d." in e["texto"].lower() or "s.f." in e["texto"].lower()]
    if fmt_issues.get("usa_ampersand") and fmt_issues.get("usa_y"):
        fmt_issues["mezcla_y_ampersand"] = sorted(set(fmt_issues["usa_ampersand"] + fmt_issues["usa_y"]))
    fmt_issues.pop("usa_ampersand", None)
    fmt_issues.pop("usa_y", None)
    keys = [e["primer_autor_clave"] for e in entries]
    disorder = [entries[i]["n"] for i in range(1, len(keys)) if keys[i] and keys[i - 1] and keys[i] < keys[i - 1]]
    if disorder:
        fmt_issues["orden_alfabetico"] = disorder
    sin_id = [e["n"] for e in entries if not e["doi"] and not e["urls"]]
    checks.append(check("formato_apa", OK if not fmt_issues else ALERTA,
                        f"{sum(len(v) for v in fmt_issues.values())} desvíos de formato APA 7 en {len(fmt_issues)} categorías.",
                        items=dict(fmt_issues)))
    checks.append(check("sin_doi_ni_url", OK if not sin_id else ALERTA,
                        f"{len(sin_id)} entradas sin DOI ni URL (dificultan la verificación).", items=sin_id))
    checks.append(check("conteo", OK, f"{len(entries)} entradas en la Bibliografía (págs. {rng[0]}–{rng[1]}); {len(cits)} citas en el texto.",
                        entradas=len(entries), citas=len(cits)))

    write_artifact(a.id, "apa_citations.json", checks, citas=cits)
    print(f"[audit_apa_citations] {len(entries)} entradas, {len(cits)} citas → artifacts/apa_citations.json")


if __name__ == "__main__":
    main()
