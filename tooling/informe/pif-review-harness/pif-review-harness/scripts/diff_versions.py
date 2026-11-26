#!/usr/bin/env python3
"""Compara la versión anterior del PIF (pdf_pages_prev.json) con la actual (pdf_pages.json).

Salidas: artifacts/diff_versiones.json (por capítulo) y artifacts/diff_versiones.md (líneas agregadas/quitadas).
Insumo de SEG-01: qué mejoró, qué no cambió y qué contradicciones nuevas pudo introducir la revisión.
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import ROMAN, artifacts, load_json, save_json  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_pdf_format import find_sections  # noqa: E402


def norm_lines(pages, rng=None):
    out = []
    for p in pages:
        if rng and not (rng[0] <= p["index"] <= rng[1]):
            continue
        for ln in p["lines"]:
            t = re.sub(r"\s+", " ", ln["text"]).strip()
            if not t or re.fullmatch(r"(p[aá]g(ina)?\.?\s*)?\d+(\s*(de|/)\s*\d+)?", t, re.I):
                continue
            out.append(t)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    art = artifacts(a.id)
    prev, cur = load_json(art / "pdf_pages_prev.json"), load_json(art / "pdf_pages.json")
    if not prev or not cur:
        sys.exit("Faltan pdf_pages_prev.json o pdf_pages.json")
    sp, sc = find_sections(prev["pages"]), find_sections(cur["pages"])
    chapters = []
    for r in ROMAN:
        a_, b_ = sp["chapters"].get(r), sc["chapters"].get(r)
        if not a_ and not b_:
            continue
        la = norm_lines(prev["pages"], (a_["start"], a_["end"])) if a_ else []
        lb = norm_lines(cur["pages"], (b_["start"], b_["end"])) if b_ else []
        sm = difflib.SequenceMatcher(None, la, lb, autojunk=False)
        added = sum(j2 - j1 for op, i1, i2, j1, j2 in sm.get_opcodes() if op in ("insert", "replace"))
        removed = sum(i2 - i1 for op, i1, i2, j1, j2 in sm.get_opcodes() if op in ("delete", "replace"))
        chapters.append({"capitulo": r, "en_anterior": bool(a_), "en_actual": bool(b_), "similitud": round(sm.ratio(), 3),
                         "lineas_agregadas": added, "lineas_quitadas": removed,
                         "paginas_actual": [b_["start"], b_["end"]] if b_ else None,
                         "estado": "nuevo" if not a_ else ("eliminado" if not b_ else ("sin cambios" if sm.ratio() > 0.98 else "modificado"))})
    la, lb = norm_lines(prev["pages"]), norm_lines(cur["pages"])
    diff = list(difflib.unified_diff(la, lb, "anterior", "actual", n=0, lineterm=""))
    (art / "diff_versiones.md").write_text("\n".join(diff[:5000]), encoding="utf-8")
    save_json(art / "diff_versiones.json", {"anterior": {"archivo": prev["archivo"], "paginas": prev["paginas"], "sha256": prev["sha256"]},
                                            "actual": {"archivo": cur["archivo"], "paginas": cur["paginas"], "sha256": cur["sha256"]},
                                            "similitud_global": round(difflib.SequenceMatcher(None, la, lb, autojunk=False).ratio(), 3),
                                            "capitulos": chapters, "checks": []})
    print(f"[diff_versions] {len(chapters)} capítulos comparados → artifacts/diff_versiones.json")


if __name__ == "__main__":
    main()
