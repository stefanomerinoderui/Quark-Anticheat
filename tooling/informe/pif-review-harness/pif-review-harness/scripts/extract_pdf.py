#!/usr/bin/env python3
"""Extrae texto paginado y geometría del PDF del PIF.

Salidas en entregas/<id>/artifacts/:
  pdf_text/page_NNNN.txt   texto plano por página (para citas literales)
  pdf_pages.json           líneas con bbox, fuente y tamaño; número de página impreso; metadatos
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import artifacts, save_json, sha256, now_iso  # noqa: E402

try:
    import pymupdf
except ImportError:  # versiones viejas
    import fitz as pymupdf  # type: ignore

PAGE_NUM_RE = re.compile(r"^\s*(?:p[aá]g(?:ina)?\.?\s*)?(\d{1,4})(?:\s*(?:de|/)\s*(\d{1,4}))?\s*$", re.I)


def detect_printed(lines, height):
    """Busca el número de página impreso en la franja superior (8 %) o inferior (12 %)."""
    cands = []
    for ln in lines:
        in_header = ln["y1"] < height * 0.08
        in_footer = ln["y0"] > height * 0.88
        if not (in_header or in_footer):
            continue
        m = PAGE_NUM_RE.match(ln["text"])
        if m:
            cands.append({"num": m.group(1), "total": m.group(2), "zona": "encabezado" if in_header else "pie", "text": ln["text"].strip()})
    return cands[-1] if cands else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out-name", default="pdf_pages.json", help="Para versiones anteriores: pdf_pages_prev.json")
    ap.add_argument("--text-dir", default="pdf_text")
    a = ap.parse_args()

    art = artifacts(a.id)
    tdir = art / a.text_dir
    tdir.mkdir(exist_ok=True)
    doc = pymupdf.open(a.pdf)
    pages = []
    for i, page in enumerate(doc, start=1):
        w, h = page.rect.width, page.rect.height
        text = page.get_text("text")
        (tdir / f"page_{i:04d}.txt").write_text(text, encoding="utf-8")
        lines = []
        d = page.get_text("dict")
        for block in d.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                spans = [s for s in line.get("spans", []) if s.get("text", "").strip()]
                if not spans:
                    continue
                txt = "".join(s["text"] for s in spans)
                # fuente y tamaño dominantes por cantidad de caracteres
                weight = {}
                for s in spans:
                    k = (s["font"], round(s["size"], 1))
                    weight[k] = weight.get(k, 0) + len(s["text"])
                (font, size), _ = max(weight.items(), key=lambda kv: kv[1])
                x0, y0, x1, y1 = line["bbox"]
                lines.append({
                    "x0": round(x0, 1), "y0": round(y0, 1), "x1": round(x1, 1), "y1": round(y1, 1),
                    "baseline": round(spans[0]["origin"][1], 1),
                    "font": font, "size": size, "chars": len(txt), "text": txt,
                    "fonts": [{"font": f, "size": s, "chars": c} for (f, s), c in weight.items()],
                })
        lines.sort(key=lambda ln: (ln["y0"], ln["x0"]))
        pages.append({
            "index": i, "width": round(w, 1), "height": round(h, 1),
            "words": len(text.split()), "printed": detect_printed(lines, h),
            "has_images": bool(page.get_images()), "lines": lines,
        })
    meta = dict(doc.metadata or {})
    out = {
        "generado_el": now_iso(), "archivo": Path(a.pdf).name, "sha256": sha256(Path(a.pdf)),
        "paginas": len(pages), "metadata": meta,
        "sin_texto": sum(1 for p in pages if p["words"] < 5),
        "pages": pages,
    }
    save_json(art / a.out_name, out)
    print(f"[extract_pdf] {len(pages)} páginas, {out['sin_texto']} sin texto → {art / a.out_name}")


if __name__ == "__main__":
    main()
