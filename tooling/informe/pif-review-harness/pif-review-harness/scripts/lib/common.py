"""Utilidades compartidas por los auditores del harness."""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENTREGAS = ROOT / "entregas"

OK, FALLA, ALERTA, GRIS = "OK", "FALLA", "ALERTA", "GRIS"


def now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).astimezone().isoformat(timespec="seconds")


def project_dir(pid: str) -> Path:
    d = ENTREGAS / pid
    if not d.is_dir():
        sys.exit(f"No existe entregas/{pid}. Corré primero scripts/init_review.sh")
    return d


def artifacts(pid: str) -> Path:
    d = project_dir(pid) / "artifacts"
    d.mkdir(exist_ok=True)
    return d


def load_json(path: Path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm(s: str) -> str:
    """Normaliza para comparar citas literales: sin acentos, minúsculas, sin guiones de corte, espacios simples."""
    s = s.replace("­", "")
    s = re.sub(r"-\s*\n\s*", "", s)           # palabra cortada con guion al final de línea
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = s.replace("–", "-").replace("—", "-")
    s = strip_accents(s).lower()
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def check(cid: str, estado: str, detalle: str = "", **extra) -> dict:
    d = {"id": cid, "estado": estado, "detalle": detalle}
    d.update(extra)
    return d


def write_artifact(pid: str, name: str, checks: list, meta: dict | None = None, **data) -> Path:
    out = {
        "generado_el": now_iso(),
        "script": Path(sys.argv[0]).name,
        "meta": meta or {},
        "resumen": {e: sum(1 for c in checks if c["estado"] == e) for e in (OK, ALERTA, FALLA, GRIS)},
        "checks": checks,
    }
    out.update(data)
    p = artifacts(pid) / name
    save_json(p, out)
    return p


def load_pages(pid: str) -> list[dict]:
    p = artifacts(pid) / "pdf_pages.json"
    data = load_json(p)
    if not data:
        sys.exit("Falta artifacts/pdf_pages.json. Corré scripts/extract_pdf.py")
    return data["pages"]


ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII"]
