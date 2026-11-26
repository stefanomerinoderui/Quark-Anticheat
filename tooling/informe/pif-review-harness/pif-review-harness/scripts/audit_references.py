#!/usr/bin/env python3
"""Capa 1 — Existencia de las referencias (Crossref, OpenAlex, URLs).

Lee artifacts/referencias.json (de audit_apa_citations.py) y escribe artifacts/referencias_verificacion.json.

Estados:
  Verificada · Con discrepancias · No localizada · Fabricada (a confirmar) ·
  Accesible (contenido a verificar) · No verificada (sin red)

Reglas:
  - Antes de concluir que un DOI "no está registrado" se hace un control positivo con un DOI conocido.
    Si el control falla, ninguna conclusión negativa es válida: todo queda "No verificada (sin red)".
  - "Fabricada (a confirmar)" solo con evidencia concreta (DOI de otra obra, título real con otros autores).
    El Maker confirma o rebaja a "No localizada" con búsquedas web registradas.
  - Las respuestas HTTP se guardan en artifacts/http_cache/ para que la corrida sea reproducible.
"""
import argparse
import difflib
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import OK, ALERTA, FALLA, GRIS, artifacts, check, load_json, now_iso, save_json, strip_accents, write_artifact  # noqa: E402

CONTROL_DOI = "10.1038/nature14539"  # LeCun, Bengio & Hinton (2015), Deep learning, Nature
MAILTO = os.environ.get("HARNESS_MAILTO", "")
UA = f"pif-review-harness/2.0 (+docencia UCP{'; mailto:' + MAILTO if MAILTO else ''})"
SUSPICIOUS = re.compile(r"\b(enthusiast|expert|developer|admin|user|team|ai|gpt|chatgpt|bot|anonymous|unknown|author|writer|blogger|editor de contenido)\b", re.I)


class Http:
    def __init__(self, cache_dir: Path, offline: bool):
        self.cache_dir, self.offline = cache_dir, offline
        cache_dir.mkdir(parents=True, exist_ok=True)
        self.log = []

    def get(self, url: str, accept_json=True):
        h = hashlib.sha1(url.encode()).hexdigest()[:16]
        f = self.cache_dir / f"{h}.json"
        if f.exists():
            r = json.loads(f.read_text(encoding="utf-8"))
            self.log.append({"url": url, "status": r["status"], "cache": True})
            return r
        if self.offline:
            return {"status": None, "error": "offline", "body": None}
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json" if accept_json else "*/*"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read(400_000).decode("utf-8", "replace")
                r = {"status": resp.status, "final_url": resp.geturl(), "body": body}
        except urllib.error.HTTPError as e:
            r = {"status": e.code, "final_url": url, "body": e.read(20_000).decode("utf-8", "replace")}
        except Exception as e:  # red, DNS, TLS, proxy
            r = {"status": None, "error": f"{type(e).__name__}: {e}", "body": None}
        r["url"], r["fecha"] = url, now_iso()
        if r["status"] is not None:
            f.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
        self.log.append({"url": url, "status": r["status"], "error": r.get("error")})
        time.sleep(0.25)
        return r

    def json(self, url):
        r = self.get(url)
        if r.get("status") == 200:
            try:
                return 200, json.loads(r["body"])
            except Exception:
                return 200, None
        return r.get("status"), None


def n(s):
    return re.sub(r"[^a-z0-9 ]", " ", strip_accents(s or "").lower()).split()


def sim(a, b):
    return difflib.SequenceMatcher(None, " ".join(n(a)), " ".join(n(b))).ratio()


def surnames(authors_str):
    parts = re.split(r",\s*(?:[A-ZÁÉÍÓÚÑ]\.\s*)+(?:,|&|\by\b)?|\s+&\s+|\s+y\s+", authors_str or "")
    out = []
    for p in parts:
        toks = [t for t in n(p) if len(t) > 1]
        if toks:
            out.append(toks[0])
    return out


def crossref_meta(msg):
    title = (msg.get("title") or [""])[0]
    fams = [strip_accents(a.get("family", a.get("name", ""))).lower() for a in msg.get("author", [])]
    year = None
    for k in ("issued", "published-print", "published-online", "created"):
        dp = (msg.get(k) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            year = str(dp[0][0])
            break
    return {"titulo": title, "autores": fams, "anio": year, "fuente": (msg.get("container-title") or [""])[0], "doi": msg.get("DOI")}


def openalex_meta(w):
    fams = [strip_accents((a.get("author") or {}).get("display_name", "").split()[-1]).lower() for a in w.get("authorships", []) if (a.get("author") or {}).get("display_name")]
    return {"titulo": w.get("title") or "", "autores": fams, "anio": str(w.get("publication_year") or ""), "fuente": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", ""), "doi": (w.get("doi") or "").replace("https://doi.org/", "")}


def compare(entry, meta):
    diffs = []
    ts = sim(entry["titulo"], meta["titulo"])
    if ts < 0.85:
        diffs.append(f"título: '{meta['titulo'][:120]}'")
    mine = surnames(entry["autores"])
    if meta["autores"] and mine:
        overlap = len(set(mine) & set(meta["autores"]))
        if overlap == 0:
            diffs.append(f"autores reales: {', '.join(meta['autores'][:6])}")
        elif overlap < min(len(mine), len(meta["autores"])):
            diffs.append(f"autores parcialmente distintos (reales: {', '.join(meta['autores'][:6])})")
    else:
        overlap = None
    if entry.get("anio") and meta.get("anio") and entry["anio"][:4] != meta["anio"][:4]:
        diffs.append(f"año real: {meta['anio']}")
    return ts, overlap, diffs


def classify(entry, http, control_ok):
    res = {"n": entry["n"], "autores": entry["autores"], "anio": entry["anio"], "titulo": entry["titulo"], "pagina_pdf": entry["pagina"],
           "doi": entry.get("doi"), "urls": entry.get("urls", []), "consultas": [], "senales": []}
    if SUSPICIOUS.search(entry["autores"] or ""):
        res["senales"].append(f"nombre de autor atípico: '{entry['autores'][:60]}'")
    if not control_ok:
        res["estado"] = "No verificada (sin red)"
        return res

    # 1) DOI
    if entry.get("doi"):
        doi = entry["doi"]
        url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        st, js = http.json(url)
        res["consultas"].append({"url": url, "status": st})
        if st == 200 and js:
            meta = crossref_meta(js.get("message", {}))
            res["metadatos_reales"] = meta
            ts, overlap, diffs = compare(entry, meta)
            if ts < 0.5 and len(entry.get("titulo") or "") < 15:
                res["estado"] = "Con discrepancias"
                res["discrepancias"] = diffs + ["título de la entrada no se pudo separar: cotejar a mano"]
            elif ts < 0.5:
                res["estado"] = "Fabricada (a confirmar)"
                res["senales"].append(f"el DOI corresponde a otra obra: '{meta['titulo'][:120]}' ({', '.join(meta['autores'][:3])}, {meta['anio']})")
            elif diffs:
                res["estado"] = "Con discrepancias"
                res["discrepancias"] = diffs
                if overlap == 0 and ts >= 0.85:
                    res["senales"].append("título real con autores que la obra no tiene")
                    res["estado"] = "Fabricada (a confirmar)"
            else:
                res["estado"] = "Verificada"
            return res
        if st == 404:
            res["senales"].append("DOI no registrado en Crossref (control positivo OK)")
        # si el DOI no sirve, seguir con búsqueda bibliográfica

    # 2) Búsqueda bibliográfica (Crossref + OpenAlex)
    if entry.get("titulo") and len(entry["titulo"]) > 12:
        q = f"{entry['titulo']} {' '.join(surnames(entry['autores'])[:2])}"
        best = None
        url = "https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(q)
        st, js = http.json(url)
        res["consultas"].append({"url": url, "status": st})
        for it in ((js or {}).get("message", {}).get("items", []) if st == 200 else []):
            m = crossref_meta(it)
            s = sim(entry["titulo"], m["titulo"])
            if not best or s > best[0]:
                best = (s, m, "Crossref")
        url = "https://api.openalex.org/works?per-page=3&search=" + urllib.parse.quote(entry["titulo"])
        st2, js2 = http.json(url)
        res["consultas"].append({"url": url, "status": st2})
        for w in ((js2 or {}).get("results", []) if st2 == 200 else []):
            m = openalex_meta(w)
            s = sim(entry["titulo"], m["titulo"])
            if not best or s > best[0]:
                best = (s, m, "OpenAlex")
        if best and best[0] >= 0.9:
            meta = best[1]
            res["metadatos_reales"] = {**meta, "base": best[2]}
            ts, overlap, diffs = compare(entry, meta)
            if entry.get("doi") and meta.get("doi") and meta["doi"].lower() != entry["doi"].lower():
                diffs.append(f"DOI real: {meta['doi']}")
            if overlap == 0:
                res["estado"] = "Fabricada (a confirmar)"
                res["senales"].append(f"el título existe con otros autores ({', '.join(meta['autores'][:4])})")
            elif diffs:
                res["estado"] = "Con discrepancias"
                res["discrepancias"] = diffs
            else:
                res["estado"] = "Verificada"
            return res

    # 3) URL
    for u in entry.get("urls", []):
        if "doi.org/" in u:
            continue
        r = http.get(u, accept_json=False)
        res["consultas"].append({"url": u, "status": r.get("status"), "final_url": r.get("final_url"), "error": r.get("error")})
        if r.get("status") and 200 <= r["status"] < 400:
            res["estado"] = "Accesible (contenido a verificar)"
            if r.get("final_url") and r["final_url"] != u:
                res["url_final"] = r["final_url"]
            return res
        if r.get("status") in (404, 410):
            res["senales"].append(f"URL devuelve {r['status']}")

    res["estado"] = "No localizada"
    res["nota"] = "No localizada en la búsqueda automática: el Maker debe buscar en la web y registrar las consultas antes de cerrar."
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    ap.add_argument("--offline", action="store_true", help="Usar solo la caché HTTP (reproducir una corrida)")
    ap.add_argument("--max", type=int, default=200)
    a = ap.parse_args()
    art = artifacts(a.id)
    refs = (load_json(art / "referencias.json", {}) or {}).get("entradas", [])
    http = Http(art / "http_cache", a.offline)

    st, js = http.json("https://api.crossref.org/works/" + CONTROL_DOI)
    control_ok = st == 200 and bool(js)
    checks = [check("control_positivo", OK if control_ok else GRIS,
                    "Crossref respondió el DOI de control" if control_ok else
                    "Crossref no respondió el DOI de control: sin red o bloqueado. Las referencias quedan 'No verificada (sin red)'.")]
    results = [classify(e, http, control_ok) for e in refs[: a.max]]
    order = {"Fabricada (a confirmar)": 0, "No localizada": 1, "Con discrepancias": 2, "No verificada (sin red)": 3, "Accesible (contenido a verificar)": 4, "Verificada": 5}
    results.sort(key=lambda r: (order.get(r["estado"], 9), r["n"]))
    tally = {}
    for r in results:
        tally[r["estado"]] = tally.get(r["estado"], 0) + 1
    bad = tally.get("Fabricada (a confirmar)", 0) + tally.get("No localizada", 0)
    est = GRIS if not control_ok else (FALLA if tally.get("Fabricada (a confirmar)") else (ALERTA if bad or tally.get("Con discrepancias") else OK))
    checks.append(check("existencia", est, "; ".join(f"{k}: {v}" for k, v in tally.items()) or "Sin referencias", conteo=tally))
    flagged = [r for r in results if r["senales"]]
    checks.append(check("senales", ALERTA if flagged else OK, f"{len(flagged)} referencias con señales de posible fabricación.", items=[{"n": r["n"], "senales": r["senales"]} for r in flagged]))
    write_artifact(a.id, "referencias_verificacion.json", checks, referencias=results, http_log=http.log[-400:],
                   meta={"control_doi": CONTROL_DOI, "fuentes": ["api.crossref.org", "api.openalex.org"], "offline": a.offline})
    print(f"[audit_references] {len(results)} referencias · {tally} → artifacts/referencias_verificacion.json")


if __name__ == "__main__":
    main()
