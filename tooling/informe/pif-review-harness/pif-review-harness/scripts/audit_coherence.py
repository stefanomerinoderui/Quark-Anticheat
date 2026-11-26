#!/usr/bin/env python3
"""Capa 1 — Candidatos de coherencia interna y datos (RR97 18.1.6, 22.1, 24.3.2).

No decide: lista candidatos con página para que el ítem COH-01 / DAT-01 / EST-01 los revise.
Salida: artifacts/coherence.json
"""
import argparse
import difflib
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.common import OK, ALERTA, FALLA, GRIS, artifacts, check, load_json, load_pages, norm, project_dir, write_artifact  # noqa: E402
from lib.survey import infer_n  # noqa: E402

CARATULA = {
    "universidad": "universidad de la cuenca del plata",
    "carrera": "ingenieria en sistemas de informacion",
    "denominacion": "proyecto integrador final",
}
TERMS_TECH = {
    "RAG": re.compile(r"\bRAG\b"),
    "pretotipo": re.compile(r"\bpretotip\w*", re.I),
    "big data": re.compile(r"\bbig\s+data\b", re.I),
    "blockchain": re.compile(r"\bblockchain\b", re.I),
    "machine learning / IA": re.compile(r"\b(machine learning|aprendizaje autom[aá]tico|inteligencia artificial)\b", re.I),
}
NON_SI = re.compile(r"\b(\d+[.,]?\d*)\s*(pulgadas?|inch(es)?|millas?|miles|mph|libras?|lbs?|pies|feet|ft|°F|onzas?|galones?)\b", re.I)
KEY_QTY = ["umbral", "precisi[oó]n", "exactitud", "accuracy", "latencia", "tiempo de respuesta", "usuarios concurrentes",
           "usuarios", "presupuesto", "costo total", "inversi[oó]n", "resoluci[oó]n", "dimensi[oó]n", "versi[oó]n",
           "disponibilidad", "uptime", "muestra", "encuestad"]
NUM = r"(\d{1,3}(?:[.\s]\d{3})*(?:,\d+)?|\d+(?:[.,]\d+)?)\s*(%|ms|s\b|segundos|MB|GB|TB|px|USD|US\$|\$|ARS|usuarios|personas)?"
PCT = re.compile(r"(\d{1,3}(?:[.,]\d{1,2})?)\s?%")
N_DECL = re.compile(r"\b(?:n\s*=\s*(\d+)|(\d+)\s+(?:encuestad[oa]s|respuestas|participantes|personas encuestadas|respondentes))", re.I)
FIG_REF = re.compile(r"\b(Figura|Fig\.|Tabla|Gr[aá]fico)\s+(\d+(?:\.\d+)?)", re.I)
ANEXO_REF = re.compile(r"\bAnexo\s+(III|II|I|IV|V|[0-9]+)\b", re.I)
REQ = re.compile(r"\b(RF|RNF|HU|CU|RN)[-\s]?(\d{1,3})\b")
# Marcadores de contenido por capítulo (AE26). Indicio de presencia, no prueba de calidad.
MARKERS = {
    "I": {"línea de base": r"l[ií]nea\s+de\s+base", "criterio de éxito": r"criterio\s+de\s+[ée]xito", "ODS": r"\bODS\b|Objetivos\s+de\s+Desarrollo\s+Sostenible",
          "desencadenante": r"desencadenante"},
    "II": {"instrumento de relevamiento": r"encuest|entrevist|observaci[oó]n", "referente/contacto": r"referente|contacto", "implicancia decisoria": r"implicancia",
           "análisis del entorno": r"PESTEL|cinco\s+fuerzas|FODA|cadena\s+de\s+valor"},
    "III": {"alcance": r"alcance", "límites/exclusiones": r"l[ií]mite|exclu", "criterio de aceptación": r"criterios?\s+de\s+aceptaci[oó]n", "trazabilidad": r"trazabilidad"},
    "IV": {"lienzo": r"lienzo|canvas", "rivalidad amplificada": r"rivalidad|sustitut", "mapeo de competencia": r"competen"},
    "V": {"iteraciones": r"sprint|iteraci", "MVP": r"\bMVP\b|producto\s+m[ií]nimo\s+viable", "cronograma": r"cronograma",
          "pérdida de un integrante": r"(p[ée]rdida|ausencia|baja|salida)\s+de\s+(un|algún|alg[uú]n)\s+integrante"},
    "VI": {"definición de terminado": r"definici[oó]n\s+de\s+(terminado|hecho)|definition\s+of\s+done", "retrospectiva": r"retrospectiva",
           "gestión de la configuración": r"gesti[oó]n\s+de\s+(la\s+)?configuraci[oó]n", "plan de pruebas": r"plan\s+de\s+pruebas|casos?\s+de\s+prueba"},
    "VII": {"canales": r"canal", "perfiles de interesado": r"perfil"},
    "VIII": {"INPI": r"\bINPI\b|Instituto\s+Nacional\s+de\s+la\s+Propiedad", "clases de Niza": r"Niza|clases?\s+\d{1,2}\b", "licencia": r"licencia",
             "fecha de la búsqueda": r"\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4}|\d{1,2}\s+de\s+\w+\s+de\s+20\d\d"},
    "IX": {"matriz de decisión ponderada": r"matriz\s+de\s+decisi[oó]n|ponderad", "modelo de datos": r"modelo\s+de\s+datos", "licencia de terceros": r"licencia",
           "entornos de trabajo": r"entornos?\s+de\s+(trabajo|desarrollo|prueba|producci[oó]n)"},
    "X": {"recursos financieros con cifras": r"\$\s?\d|USD|ARS|pesos", "recursos humanos": r"recursos?\s+humanos"},
    "XI": {"escalabilidad": r"escalab", "supuestos": r"supuesto", "hipótesis": r"hip[oó]tesis", "métrica accionable": r"m[ée]trica",
           "umbral de decisión": r"umbral", "perseverar o pivotar": r"persever|pivot", "10× carga": r"10\s?[x×]|diez\s+veces",
           "sostenibilidad / responsabilidad social": r"sostenib|responsabilidad\s+social"},
    "XII": {"aspectos a mejorar": r"(aspectos?\s+a\s+mejorar|mejorar[ií]a|deb[ií]\s+haber|error)", "firma": r"\bfirma"},
    "XIII": {"etiqueta de versión": r"etiqueta|\btag\b|\bv\d", "repositorio": r"github|gitlab|bitbucket|repositorio", "manual de despliegue": r"despliegue|instalaci[oó]n"},
}
# Declaración de uso de IA (cláusula de cátedra CAT-IA)
AI_HEAD = re.compile(r"declaraci[oó]n\s+(de(l)?\s+)?uso\s+de\s+(la\s+)?(herramientas\s+de\s+)?(inteligencia\s+artificial|IA)\b", re.I)
AI_SHARE = re.compile(r"https?://(?:www\.)?(?:chatgpt\.com/share|chat\.openai\.com/share|claude\.ai/share|g\.co/gemini/share|gemini\.google\.com/share|"
                      r"copilot\.microsoft\.com/\S*share|(?:www\.)?perplexity\.ai/search|poe\.com/s|chat\.deepseek\.com/\S*share|grok\.com/share|x\.com/i/grok/share|"
                      r"aistudio\.google\.com/\S*|notebooklm\.google\.com/\S*|chat\.mistral\.ai/\S*share)[^\s)\]]*", re.I)
AI_TOOLS = re.compile(r"\b(ChatGPT|GPT-?\d|OpenAI|Claude|Anthropic|Gemini|Bard|Copilot|Perplexity|DeepSeek|Grok|Mistral|Llama|NotebookLM|Cursor|"
                      r"inteligencia\s+artificial\s+generativa|IA\s+generativa|modelo\s+de\s+lenguaje|LLM)\b", re.I)
AI_ELEMENTS = {
    "para qué se usó": r"(se\s+(utiliz|us|emple)\w*|para\s+(revisar|redactar|generar|corregir|resumir|traducir|depurar|programar|buscar)|finalidad|tarea)",
    "cómo se verificó": r"verific|contrast|cotej|valid|comprob",
    "prompts utilizados": r"prompt|instrucci[oó]n(es)?\s+(dada|utilizada|enviada)|consulta\s+realizada|se\s+le\s+pidi",
    "enlace a la conversación": None,
}
NO_USE = re.compile(r"no\s+se\s+(utiliz|us|emple)\w*\s+(ninguna\s+)?(herramienta|inteligencia|IA)", re.I)
REPO_URL = re.compile(r"https?://(?:www\.)?(github\.com|gitlab\.com|bitbucket\.org)/[\w.\-]+/[\w.\-]+", re.I)


def page_chapter(sections):
    m = {}
    for num, info in sections.get("chapters", {}).items():
        for i in range(info["title_page"], info.get("end", info["title_page"]) + 1):
            m[i] = num
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True)
    a = ap.parse_args()
    pages = load_pages(a.id)
    fmt = load_json(artifacts(a.id) / "pdf_format.json", {}) or {}
    sections = fmt.get("sections", {"chapters": {}, "anexos": {}})
    chap_of = page_chapter(sections)
    plan = load_json(project_dir(a.id) / "plan_entregas.json", {}) or {}
    texts = {p["index"]: (artifacts(a.id) / "pdf_text" / f"page_{p['index']:04d}.txt").read_text(encoding="utf-8") for p in pages}
    checks = []

    # --- carátula
    t1 = norm(texts.get(1, ""))
    found = {k: (v in t1) for k, v in CARATULA.items()}
    fac_vigente = "facultad de ingenieria, tecnologia y arquitectura" in t1
    fac_2023 = "facultad de ingenieria y tecnologia" in t1
    found["facultad"] = fac_vigente or fac_2023
    year = re.search(r"\b20\d\d\b", t1)
    found["anio"] = bool(year)
    faltan = [k for k, v in found.items() if not v]
    checks.append(check("caratula", OK if not faltan else ALERTA,
                        "Carátula completa" if not faltan else f"No se encontró en la página 1: {', '.join(faltan)}",
                        encontrados=found, facultad_denominacion="vigente (2026)" if fac_vigente else ("RR97 (2023)" if fac_2023 else None),
                        nota="RR97 22.1 dice 'Facultad de Ingeniería y Tecnología'; la denominación vigente es 'Facultad de Ingeniería, Tecnología y Arquitectura'. Ambas se aceptan."))

    # --- figuras y tablas
    refs, caps = defaultdict(set), defaultdict(set)
    for i, t in texts.items():
        for ln in t.splitlines():
            m = FIG_REF.match(ln.strip())
            if m:
                caps[m.group(1).lower().rstrip(".")[:3]].add(m.group(2))
        for m in FIG_REF.finditer(t):
            refs[m.group(1).lower().rstrip(".")[:3]].add((m.group(2), i))
    fig_issues = []
    for kind, rs in refs.items():
        nums = {n for n, _ in rs}
        for n in sorted(nums - caps.get(kind, set())):
            fig_issues.append({"tipo": kind, "numero": n, "paginas": sorted({p for x, p in rs if x == n}), "problema": "citada sin epígrafe"})
        ints = sorted(int(n) for n in caps.get(kind, set()) if n.isdigit())
        if ints:
            gaps = sorted(set(range(1, ints[-1] + 1)) - set(ints))
            if gaps:
                fig_issues.append({"tipo": kind, "numeros_faltantes": gaps, "problema": "numeración salteada"})
    checks.append(check("figures_tables", OK if not fig_issues else ALERTA,
                        f"{len(fig_issues)} problemas de numeración o referencia de figuras/tablas.", candidatos=fig_issues[:50]))

    # --- anexos referenciados
    existing = set(sections.get("anexos", {}).keys())
    anx = defaultdict(set)
    for i, t in texts.items():
        for m in ANEXO_REF.finditer(t):
            anx[m.group(1).upper()].add(i)
    missing = {k: sorted(v) for k, v in anx.items() if k not in existing}
    checks.append(check("annex_refs", OK if not missing else ALERTA,
                        "Todos los anexos mencionados existen" if not missing else f"Anexos mencionados que no se detectaron: {', '.join(missing)}",
                        mencionados_sin_existir=missing, detectados=sorted(existing)))

    # --- requisitos
    reqs = defaultdict(lambda: defaultdict(set))
    for i, t in texts.items():
        for m in REQ.finditer(t):
            reqs[m.group(1)][int(m.group(2))].add(i)
    req_out = {}
    for kind, d in reqs.items():
        nums = sorted(d)
        gaps = sorted(set(range(1, nums[-1] + 1)) - set(nums)) if nums else []
        req_out[kind] = {"cantidad": len(nums), "max": nums[-1] if nums else 0, "huecos": gaps[:40]}
    checks.append(check("requirements", ALERTA if any(v["huecos"] for v in req_out.values()) else (OK if req_out else GRIS),
                        "Identificadores de requisitos detectados" if req_out else "No se detectaron identificadores RF/RNF/HU",
                        detalle_por_tipo=req_out))

    # --- valores clave repetidos con valores distintos
    qty = defaultdict(list)
    for i, t in texts.items():
        flat = re.sub(r"\s+", " ", t)
        for term in KEY_QTY:
            for m in re.finditer(term + r"[^.\d]{0,40}?" + NUM, flat, re.I):
                qty[re.sub(r"\\|\[|\]|\(|\)|\?", "", term)].append({"valor": (m.group(1) + (m.group(2) or "")).strip(), "pagina": i, "capitulo": chap_of.get(i), "contexto": m.group(0)[:90]})
    divergent = {k: v for k, v in qty.items() if len({x["valor"] for x in v}) > 1 and len({x["capitulo"] for x in v}) > 1}
    checks.append(check("key_values", ALERTA if divergent else OK,
                        f"{len(divergent)} magnitudes con valores distintos en distintos capítulos (candidatos, revisar contexto).",
                        candidatos={k: v[:12] for k, v in divergent.items()}))

    # --- unidades no SI
    nonsi = [{"pagina": i, "texto": m.group(0)} for i, t in texts.items() for m in NON_SI.finditer(t)]
    checks.append(check("units", OK if not nonsi else ALERTA, f"{len(nonsi)} unidades fuera de SIMELA/SI.", candidatos=nonsi[:40]))

    # --- términos técnicos a revisar
    terms = {}
    for name, rx in TERMS_TECH.items():
        pg = sorted({i for i, t in texts.items() if rx.search(t)})
        if pg:
            terms[name] = pg
    checks.append(check("tech_terms", ALERTA if ("RAG" in terms or "pretotipo" in terms) else OK,
                        "Términos que suelen usarse mal: revisar que el uso sea correcto (p. ej., RAG con paso de generación).",
                        paginas=terms))

    # --- enlaces a repositorio
    urls = defaultdict(set)
    for i, t in texts.items():
        for m in REPO_URL.finditer(t.replace("\n", "")):
            urls[m.group(0).rstrip(".,)").lower()].add(i)
    checks.append(check("repo_links", ALERTA if len(urls) > 2 else (OK if urls else FALLA),
                        f"{len(urls)} URL de repositorio distintas en el PDF." if urls else "El PDF no contiene enlaces a un repositorio.",
                        urls={k: sorted(v) for k, v in urls.items()}))

    # --- encuestas: n declarado e inferido (Cap. II y Anexo I)
    ch2 = sections.get("chapters", {}).get("II")
    target = set()
    if ch2:
        target |= set(range(ch2["start"], ch2["end"] + 1))
    if "I" in sections.get("anexos", {}):
        start = sections["anexos"]["I"]
        nxt = [v for v in sections["anexos"].values() if v > start]
        target |= set(range(start, (min(nxt) if nxt else len(pages) + 1)))
    if not target:
        target = set(texts)
    declared = sorted({int(m.group(1) or m.group(2)) for i in target for m in N_DECL.finditer(texts[i])})
    inferred = []
    for i in sorted(target):
        pcts = [p for p in PCT.findall(texts[i]) if "," in p or "." in p]
        if len(pcts) >= 2:
            ns = infer_n(pcts)
            inferred.append({"pagina": i, "porcentajes": pcts[:12], "n_compatibles": ns})
    estado = GRIS if not inferred else (OK if declared else ALERTA)
    checks.append(check("survey_n", estado,
                        ("n declarado: " + ", ".join(map(str, declared))) if declared else "No se encontró n declarado; ver n compatibles inferidos de los porcentajes.",
                        n_declarado=declared, inferencias=inferred[:30],
                        nota="El n inferido es el mínimo compatible con el redondeo; varios n son posibles. Usar como pregunta, no como dato."))

    # --- Cap. XII: similitud entre secciones individuales
    names = [m["nombre"] for m in plan.get("equipo", [])]
    ch12 = sections.get("chapters", {}).get("XII")
    if ch12 and len(names) >= 2:
        body = "\n".join(texts[i] for i in range(ch12["start"], ch12["end"] + 1) if i in texts)
        pos = []
        for n in names:
            m = re.search(re.escape(n.split()[0]) + r"[^\n]{0,40}\n", body, re.I)
            if m:
                pos.append((m.start(), n))
        pos.sort()
        segs = {n: body[s:(pos[k + 1][0] if k + 1 < len(pos) else len(body))] for k, (s, n) in enumerate(pos)}
        pairs = []
        ks = list(segs)
        for x in range(len(ks)):
            for y in range(x + 1, len(ks)):
                r = difflib.SequenceMatcher(None, norm(segs[ks[x]]), norm(segs[ks[y]])).ratio()
                pairs.append({"a": ks[x], "b": ks[y], "similitud": round(r, 2)})
        high = [p for p in pairs if p["similitud"] > 0.6]
        firmas = len(re.findall(r"\bfirma\b", body, re.I))
        checks.append(check("cap12_similarity", ALERTA if high or len(segs) < len(names) else OK,
                            f"Secciones individuales detectadas: {len(segs)} de {len(names)}; pares con similitud > 0,6: {len(high)}; menciones de 'firma': {firmas}.",
                            pares=pairs, detectadas=list(segs)))
    else:
        checks.append(check("cap12_similarity", GRIS, "Sin Cap. XII detectado o sin integrantes en plan_entregas.json"))

    # --- marcadores de contenido por capítulo detectado
    cm, missing_total = {}, 0
    for num, info in sections.get("chapters", {}).items():
        txt = " ".join(texts.get(i, "") for i in range(info["start"], info.get("end", info["start"]) + 1))
        txt = re.sub(r"\s+", " ", txt)
        found = {k: bool(re.search(rx, txt, re.I)) for k, rx in MARKERS.get(num, {}).items()}
        falt = [k for k, v in found.items() if not v]
        missing_total += len(falt)
        cm[num] = {"paginas": [info["start"], info.get("end")], "presentes": [k for k, v in found.items() if v], "ausentes": falt}
    checks.append(check("content_markers", ALERTA if missing_total else (OK if cm else GRIS),
                        f"{missing_total} marcadores de contenido ausentes en {sum(1 for v in cm.values() if v['ausentes'])} capítulos." if cm else "Sin capítulos detectados",
                        por_capitulo=cm, nota="Indicio de presencia por palabras clave (AE26). Confirmar leyendo el capítulo antes de observar."))

    # --- declaración de uso de IA (CAT-IA)
    n_pages = len(pages)
    head_pages = [i for i, t in texts.items() if any(AI_HEAD.search(ln) and len(ln.strip()) < 90 for ln in t.splitlines())]
    decl_text, decl_pages = "", []
    if head_pages:
        start = head_pages[-1]
        stop_rx = re.compile(r"^\s*(BIBLIOGRAF[IÍ]A|REFERENCIAS|ANEXO\s+[IVX0-9]+|CONCLUSIONES)\b", re.I)
        started = False
        for i in range(start, min(start + 3, n_pages + 1)):
            for ln in texts.get(i, "").splitlines():
                if not started:
                    if AI_HEAD.search(ln):
                        started = True
                    continue
                if stop_rx.match(ln) and decl_text:
                    break
                decl_text += ln + "\n"
            decl_pages.append(i)
    links = sorted({m.group(0).rstrip(".,;") for m in AI_SHARE.finditer(decl_text.replace("\n", ""))})
    elements = {}
    for k, rx in AI_ELEMENTS.items():
        elements[k] = bool(links) if rx is None else bool(re.search(rx, decl_text, re.I))
    declares_no_use = bool(NO_USE.search(decl_text))
    generic = bool(decl_text) and len(decl_text.split()) < 40 and not links
    # evidencia de uso fuera de la declaración
    mentions = []
    for i, t in texts.items():
        if i in decl_pages:
            continue
        for m in AI_TOOLS.finditer(t):
            ctx = re.sub(r"\s+", " ", t[max(0, m.start() - 60): m.end() + 60])
            mentions.append({"pagina": i, "termino": m.group(0), "contexto": ctx})
    export = project_dir(a.id) / "input" / "repo_codigo"
    agent_files = []
    if export.exists():
        agent_files = [str(x.relative_to(export)) for x in export.rglob("*") if x.name.endswith(".STUDENT_DATA")]
    evidence = bool(mentions) or bool(agent_files)
    final_part = bool(decl_pages) and (decl_pages[0] >= n_pages * 0.6)
    if decl_text and declares_no_use and not evidence:
        estado, det = OK, "Declara que no se utilizó IA y no hay evidencia en contrario."
    elif decl_text and declares_no_use and evidence:
        estado, det = FALLA, "Declara que no se utilizó IA, pero hay evidencia de uso (menciones o archivos de agentes en el repositorio)."
    elif decl_text:
        falt = [k for k, v in elements.items() if not v]
        estado = ALERTA if (falt or generic or not final_part) else OK
        det = ("Declaración presente" + ("" if final_part else " (no está en un apartado final)") +
               (f"; faltan: {', '.join(falt)}" if falt else "; con los cuatro elementos") + ("; declaración genérica" if generic else "") + ".")
    elif evidence:
        estado, det = FALLA, "No hay apartado de declaración de uso de IA y hay evidencia de uso: uso no declarado (CAT-IA)."
    else:
        estado, det = GRIS, "No hay declaración ni evidencia documental de uso. Preguntar en el coloquio."
    checks.append(check("ai_declaration", estado, det, paginas=decl_pages, en_apartado_final=final_part,
                        elementos=elements, enlaces=links, declara_no_uso=declares_no_use, extracto=decl_text[:1200],
                        menciones_fuera=mentions[:30], archivos_agentes_repo=agent_files[:20],
                        nota="Cláusula de cátedra CAT-IA. Los enlaces se listan para que el docente los abra; el harness no los descarga."))

    write_artifact(a.id, "coherence.json", checks)
    print(f"[audit_coherence] {len(checks)} controles → artifacts/coherence.json")


if __name__ == "__main__":
    main()
