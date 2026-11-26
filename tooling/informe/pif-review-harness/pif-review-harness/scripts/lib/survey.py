"""Inferencia del tamaño de muestra (n) a partir de porcentajes redondeados."""
from __future__ import annotations

import math


def decimals(p: str) -> int:
    p = p.replace(",", ".")
    return len(p.split(".")[1]) if "." in p else 0


def compatible(n: int, pct: float, dec: int) -> bool:
    """¿Existe k entero tal que round(100k/n, dec) == pct? Tolera redondeo hacia arriba o abajo."""
    half = 0.5 * 10 ** (-dec)
    lo, hi = (pct - half) * n / 100, (pct + half) * n / 100
    k = math.ceil(lo - 1e-9)
    return k <= hi + 1e-9 and 0 <= k <= n


def infer_n(percentages: list[str], n_max: int = 2000) -> list[int]:
    """Devuelve los n (≤ n_max) compatibles con todos los porcentajes, de menor a mayor (los 5 primeros)."""
    vals = [(float(p.replace(",", ".")), decimals(p)) for p in percentages]
    vals = [(v, d) for v, d in vals if 0 < v < 100]
    if not vals:
        return []
    out = []
    for n in range(2, n_max + 1):
        if all(compatible(n, v, d) for v, d in vals):
            out.append(n)
            if len(out) == 5:
                break
    return out
