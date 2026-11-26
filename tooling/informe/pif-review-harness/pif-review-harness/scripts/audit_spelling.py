#!/usr/bin/env python3
"""Capa 1 (opcional) — Candidatos de ortografía y gramática con LanguageTool LOCAL.

Por privacidad (Ley 25.326) no se usa la API pública: hace falta un servidor local, por ejemplo
  docker run -d -p 8010:8010 erikvl87/languagetool
y la variable LT_URL=http://localhost:8010 .  Sin servidor, el control queda GRIS.

Salida: artifacts/languagetool.json  (candidatos; el docente confirma en ortografia_confirmada.json)
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import OK, ALERTA, GRIS, artifacts, check, load_json, write_artifact  # noqa: E402

SPELL_CATS = {"TYPOS", "CASING", "DIACRITICS", "CONFUSED_WORDS"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    url = os.environ.get("LT_URL")
    if not url:
        write_artifact(a.id, "languagetool.json", [check("languagetool", GRIS, "LT_URL no definido: sin servidor LanguageTool local.")])
        print("[audit_spelling] omitido (LT_URL no definido)")
        return
    art = artifacts(a.id)
    fmt = load_json(art / "pdf_format.json", {}) or {}
    sec = fmt.get("sections", {})
    stop = min([sec.get("bibliografia") or 10**6] + list((sec.get("anexos") or {}).values()))
    matches = []
    for f in sorted((art / "pdf_text").glob("page_*.txt")):
        pg = int(f.stem.split("_")[1])
        if pg == 1 or pg >= stop:
            continue
        text = f.read_text(encoding="utf-8")
        data = urllib.parse.urlencode({"text": text, "language": "es", "disabledCategories": "TYPOGRAPHY,WHITESPACE"}).encode()
        try:
            with urllib.request.urlopen(url.rstrip("/") + "/v2/check", data=data, timeout=60) as r:
                res = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            write_artifact(a.id, "languagetool.json", [check("languagetool", GRIS, f"LanguageTool no respondió: {e}")])
            return
        for m in res.get("matches", []):
            cat = m.get("rule", {}).get("category", {}).get("id", "")
            ctx = m.get("context", {})
            matches.append({"pdf_page": pg, "tipo": "ortografia" if cat in SPELL_CATS else "redaccion", "regla": m.get("rule", {}).get("id"),
                            "mensaje": m.get("message"), "fragmento": ctx.get("text", "")[ctx.get("offset", 0): ctx.get("offset", 0) + ctx.get("length", 0)],
                            "contexto": ctx.get("text"), "sugerencias": [r_["value"] for r_ in m.get("replacements", [])[:3]]})
    orto = sum(1 for m in matches if m["tipo"] == "ortografia")
    red = len(matches) - orto
    write_artifact(a.id, "languagetool.json", [check("languagetool", ALERTA if matches else OK,
                   f"Candidatos: {orto} ortográficos, {red} de redacción. El docente confirma los errores en ortografia_confirmada.json.",
                   ortografia=orto, redaccion=red)], candidatos=matches)
    print(f"[audit_spelling] {len(matches)} candidatos")


if __name__ == "__main__":
    main()
