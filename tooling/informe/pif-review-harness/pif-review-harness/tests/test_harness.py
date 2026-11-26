#!/usr/bin/env python3
"""Prueba de punta a punta del harness con el PIF y el repo sintéticos.

Uso:  python3 tests/test_harness.py        (o pytest -q tests/test_harness.py)
Crea entregas/_test_fixture/ y lo borra al final (salvo con --keep).
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
PID = "_test_fixture"
P = ROOT / "entregas" / PID
A = P / "artifacts"


def sh(*args, check=True):
    r = subprocess.run(list(args), cwd=ROOT, capture_output=True, text=True)
    if check and r.returncode:
        raise AssertionError(f"{' '.join(args)}\n{r.stdout}\n{r.stderr}")
    return r


def chk(name, cid):
    d = json.loads((A / name).read_text(encoding="utf-8"))
    return next(c for c in d["checks"] if c["id"] == cid)


def setup(tmp):
    sh(sys.executable, "tests/make_fixture.py", str(tmp))
    shutil.rmtree(P, ignore_errors=True)
    P.mkdir(parents=True)
    plan = json.loads((tmp / "plan_entregas.json").read_text(encoding="utf-8"))
    plan["proyecto_id"] = PID
    (P / "plan_entregas.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    sh("bash", "scripts/init_review.sh", "--id", PID, "--instancia", "FINAL", "--pdf", str(tmp / "pif_prueba.pdf"),
       "--code-dir", str(tmp / "repo"), "--tag", "v-final", "--offline")


def test_capa1():
    m = json.loads((A / "manifest.json").read_text(encoding="utf-8"))
    assert all(v["estado"] != "error" for v in m["auditorias"].values()), m["auditorias"]
    # formato
    assert chk("pdf_format.json", "abstract_words")["valor"] > 600
    ct = chk("pdf_format.json", "chapter_title_pages")
    assert ct["no_detectadas"] == ["III"], ct["no_detectadas"]
    mg = chk("pdf_format.json", "margins")
    assert mg["violaciones"]["izquierdo"], "debió detectar el margen izquierdo de 50 pt"
    assert chk("pdf_format.json", "line_spacing")["paginas"], "debió detectar interlineado simple"
    assert chk("pdf_format.json", "fonts")["paginas_no_times"], "debió detectar la página en Helvetica"
    assert chk("pdf_format.json", "first_person")["paginas"], "debió detectar 'decidimos'"
    assert chk("pdf_format.json", "annex_numbering")["estado"] == "OK"
    # coherencia y datos
    assert 7 in chk("coherence.json", "survey_n")["inferencias"][0]["n_compatibles"]
    assert "umbral" in " ".join(chk("coherence.json", "key_values")["candidatos"].keys())
    assert "IV" in chk("coherence.json", "annex_refs")["mencionados_sin_existir"]
    assert "RAG" in chk("coherence.json", "tech_terms")["paginas"]
    assert chk("coherence.json", "cap12_similarity")["pares"][0]["similitud"] > 0.6
    assert any(x.get("problema") == "citada sin epígrafe" for x in chk("coherence.json", "figures_tables")["candidatos"])
    ai = chk("coherence.json", "ai_declaration")
    assert ai["estado"] == "ALERTA" and ai["elementos"]["enlace a la conversación"] is False and ai["elementos"]["prompts utilizados"], ai["detalle"]
    assert ai["archivos_agentes_repo"], "debió listar los archivos de agentes del repo como evidencia de uso"
    cm = chk("coherence.json", "content_markers")["por_capitulo"]
    assert "matriz de decisión ponderada" in cm["IX"]["ausentes"] and "umbral de decisión" in cm["XI"]["presentes"], cm.get("IX")
    # bibliografía
    assert [c["autor"] for c in chk("apa_citations.json", "citas_sin_entrada")["items"]] == ["Pérez"]
    assert chk("apa_citations.json", "anio_distinto")["items"][0]["anios_en_lista"] == ["2016"]
    nc = {i["autores"].split(",")[0] for i in chk("apa_citations.json", "entradas_no_citadas")["items"]}
    assert nc == {"Gómez", "Ministerio de Salud"}, nc
    fa = chk("apa_citations.json", "formato_apa")["items"]
    assert "url_acortada" in fa and "fecha_recuperacion" in fa
    # referencias sin red → GRIS, nunca "Verificada" ni "No localizada"
    assert chk("referencias_verificacion.json", "existencia")["estado"] == "GRIS"
    assert chk("referencias_verificacion.json", "senales")["items"], "debió señalar 'Enthusiast, A. C.'"
    # repo
    assert chk("repos.json", "license")["tipo"] == "MIT"
    assert chk("repos.json", "dependencies")["conflictos"][0]["nombre"] == "gpl-scheduler"
    cm = chk("repos.json", "commits")
    assert cm["sin_commits"] == ["Bruno Díaz"] and cm["proporcion_tardia"] > 0.4
    assert "Externo" in cm["detalle"]
    assert chk("repos.json", "deploy_manual")["estado"] == "FALLA"
    # seguridad
    assert (P / "input" / "repo_codigo" / "CLAUDE.md.STUDENT_DATA").exists()
    assert not (P / "input" / "repo_codigo" / "CLAUDE.md").exists()
    assert (P / "input" / "repo_codigo" / ".claude.STUDENT_DATA").is_dir()
    inj = chk("sdd_harness.json", "injection")["items"]
    assert {i["tipo"] for i in inj} == {"repo", "pdf"} and len(inj) == 2, inj
    assert any(s["tipo"] == "aws_access_key" for s in chk("sdd_harness.json", "secrets")["items"])
    assert {x["tipo"] for x in chk("sdd_harness.json", "pii_pdf")["items"]} >= {"dni", "email"}


def test_referencias_clasificacion():
    """Clasificación con respuestas simuladas de Crossref/OpenAlex (sin red)."""
    import audit_references as ar

    class FakeHttp:
        log = []

        def __init__(self, table):
            self.t = table

        def json(self, url):
            for k, v in self.t.items():
                if k in url:
                    return v
            return 404, None

        def get(self, url, accept_json=True):
            return {"status": 404, "final_url": url}

    lecun = {"message": {"title": ["Deep learning"], "author": [{"family": "LeCun"}, {"family": "Bengio"}, {"family": "Hinton"}],
                         "issued": {"date-parts": [[2015]]}, "container-title": ["Nature"], "DOI": "10.1038/nature14539"}}
    other = {"message": {"title": ["Protein folding at scale"], "author": [{"family": "Smith"}], "issued": {"date-parts": [[2019]]}, "DOI": "10.1/x"}}
    http = FakeHttp({"works/10.1038%2Fnature14539": (200, lecun), "works/10.1038/nature14539": (200, lecun), "works/10.5555": (200, other)})
    base = {"n": 1, "pagina": 30, "urls": []}
    ok = ar.classify({**base, "autores": "LeCun, Y., Bengio, Y., & Hinton, G", "anio": "2015", "titulo": "Deep learning", "doi": "10.1038/nature14539"}, http, True)
    assert ok["estado"] == "Verificada", ok
    yr = ar.classify({**base, "autores": "LeCun, Y., Bengio, Y., & Hinton, G", "anio": "2018", "titulo": "Deep learning", "doi": "10.1038/nature14539"}, http, True)
    assert yr["estado"] == "Con discrepancias" and any("año" in d for d in yr["discrepancias"]), yr
    au = ar.classify({**base, "autores": "García, M., & Torres, J", "anio": "2015", "titulo": "Deep learning", "doi": "10.1038/nature14539"}, http, True)
    assert au["estado"] == "Fabricada (a confirmar)", au
    wrong = ar.classify({**base, "autores": "Martínez, L", "anio": "2022", "titulo": "Sistemas inteligentes de turnos en hospitales públicos", "doi": "10.5555/abc"}, http, True)
    assert wrong["estado"] == "Fabricada (a confirmar)" and "otra obra" in " ".join(wrong["senales"]), wrong
    nf = ar.classify({**base, "autores": "Martínez, L", "anio": "2022", "titulo": "Sistemas inteligentes de turnos en hospitales públicos", "doi": "10.9999/rlim"}, http, True)
    assert nf["estado"] == "No localizada" and any("no registrado" in s for s in nf["senales"]), nf
    off = ar.classify({**base, "autores": "LeCun, Y", "anio": "2015", "titulo": "Deep learning", "doi": "10.1038/nature14539"}, http, False)
    assert off["estado"] == "No verificada (sin red)"


def write_findings(item, findings):
    (A / "findings").mkdir(exist_ok=True)
    (A / "findings" / f"{item}.maker.json").write_text(json.dumps(findings, ensure_ascii=False), encoding="utf-8")


def test_maker_checker_estado():
    """Simula al Maker: una cita correcta, una con página corrida, una inventada y un VERDE sin evidencia."""
    texts = {int(f.stem.split("_")[1]): f.read_text(encoding="utf-8") for f in (A / "pdf_text").glob("page_*.txt")}
    pg_survey = next(p for p, t in texts.items() if "28,6 %" in t)
    base = {"item_id": "DAT-01", "norma": [{"fuente": "RR97", "ref": "Art. 24.3.2"}], "destino": "ambos", "origen": "maker",
            "que_se_espera": "Declarar n y diseño muestral", "evidencia_a_presentar": "Tabla con n por pregunta en el Cap. II"}
    write_findings("DAT-01", [
        {**base, "clave": "DAT-01:n_no_declarado", "semaforo": "AMARILLO", "observacion": "No se declara n.",
         "ubicaciones": [{"tipo": "pdf", "pdf_page": pg_survey, "cita_literal": "La muestra es representativa de la población"}]},
        {**base, "clave": "DAT-01:pagina_corrida", "semaforo": "AMARILLO", "observacion": "Porcentajes sin n.",
         "ubicaciones": [{"tipo": "pdf", "pdf_page": pg_survey + 3, "cita_literal": "el 42,9 % entre 30 y 60 minutos"}]},
        {**base, "clave": "DAT-01:inventada", "semaforo": "ROJO", "observacion": "Datos inventados.",
         "ubicaciones": [{"tipo": "pdf", "pdf_page": pg_survey, "cita_literal": "el 99 % de los pacientes abandona"}]},
        {**base, "clave": "DAT-01:verde_sin_evidencia", "semaforo": "VERDE", "observacion": "Anonimización correcta.",
         "ubicaciones": [{"tipo": "artifact", "artifact": "sdd_harness.json"}]},
    ])
    write_findings("REPO-01", [
        {"item_id": "REPO-01", "clave": "REPO-01:secreto", "semaforo": "ROJO", "norma": [{"fuente": "LEY", "ref": "Ley 25.326"}], "destino": "ambos",
         "origen": "maker", "observacion": "Clave AWS en el código.", "que_se_espera": "Remover y rotar", "evidencia_a_presentar": "Commit que la elimina y constancia de rotación",
         "ubicaciones": [{"tipo": "repo", "path": "src/config.js", "line": 1, "cita_literal": "awsKey: 'AKIAABCDEFGHIJKLMNOP'"}]},
    ])
    sh(sys.executable, "scripts/verify_evidence.py", "--id", PID)
    v = json.loads((A / "findings" / "DAT-01.verified.json").read_text(encoding="utf-8"))
    est = {f["clave"]: f["verificacion_mecanica"]["estado"] for f in v}
    assert est == {"DAT-01:n_no_declarado": "valida", "DAT-01:pagina_corrida": "pagina_corregida",
                   "DAT-01:inventada": "descartada", "DAT-01:verde_sin_evidencia": "descartada"}, est
    assert next(f for f in v if f["clave"] == "DAT-01:pagina_corrida")["ubicaciones"][0]["pdf_page"] == pg_survey
    r = json.loads((A / "findings" / "REPO-01.verified.json").read_text(encoding="utf-8"))
    assert r[0]["verificacion_mecanica"]["estado"] == "valida", r[0]["verificacion_mecanica"]
    # el Checker (aquí simulado) aprueba todo lo que sobrevivió
    for item in ("DAT-01", "REPO-01"):
        data = json.loads((A / "findings" / f"{item}.verified.json").read_text(encoding="utf-8"))
        for f in data:
            f["checker"] = {"decision": "aprobado", "motivo": "test"}
        (A / "findings" / f"{item}.checked.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    sh(sys.executable, "scripts/state.py", "merge", "--id", PID, "--instancia", "FINAL")
    st = json.loads((P / "review_state.json").read_text(encoding="utf-8"))
    ids = {o["clave"]: o["id"] for o in st["observaciones"]}
    assert set(ids) == {"DAT-01:n_no_declarado", "DAT-01:pagina_corrida", "REPO-01:secreto"}, ids
    # segunda entrega: reaparece una, desaparece otra → reincidente / subsanada_a_confirmar; IDs estables
    st["entregas"].append({"instancia": "REENTREGA-1", "recibido_el": "x"})
    (P / "review_state.json").write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")
    keep = [f for f in json.loads((A / "findings" / "DAT-01.checked.json").read_text(encoding="utf-8")) if f["clave"] == "DAT-01:n_no_declarado"]
    (A / "findings" / "DAT-01.checked.json").write_text(json.dumps(keep, ensure_ascii=False), encoding="utf-8")
    (A / "findings" / "REPO-01.checked.json").write_text("[]", encoding="utf-8")
    sh(sys.executable, "scripts/state.py", "merge", "--id", PID, "--instancia", "REENTREGA-1")
    st2 = {o["clave"]: o for o in json.loads((P / "review_state.json").read_text(encoding="utf-8"))["observaciones"]}
    assert st2["DAT-01:n_no_declarado"]["estado"] == "reincidente"
    assert st2["DAT-01:n_no_declarado"]["id"] == ids["DAT-01:n_no_declarado"]
    assert st2["DAT-01:pagina_corrida"]["estado"] == "subsanada_a_confirmar"
    assert st2["REPO-01:secreto"]["estado"] == "subsanada_a_confirmar"
    out = sh(sys.executable, "scripts/state.py", "matriz", "--id", PID).stdout
    assert ids["DAT-01:n_no_declarado"] in out and "Uso de IA" in out
    # en la reentrega no se exige bitácora: pedirla debe generar advertencia
    write_findings("FMT-01", [{"item_id": "FMT-01", "clave": "FMT-01:margen", "semaforo": "AMARILLO", "norma": [{"fuente": "RR97", "ref": "Art. 20"}],
                               "destino": "ambos", "origen": "maker", "observacion": "Margen.", "que_se_espera": "3 cm",
                               "evidencia_a_presentar": "Registrar la corrección en la bitácora", "ubicaciones": [{"tipo": "artifact", "artifact": "pdf_format.json#margins"}]}])
    sh(sys.executable, "scripts/verify_evidence.py", "--id", PID)
    fm = json.loads((A / "findings" / "FMT-01.verified.json").read_text(encoding="utf-8"))[0]
    assert "pide_bitacora_no_exigida" in fm["verificacion_mecanica"]["advertencias"]


def test_proceso_ae(tmp):
    """Entrega parcial de AE: se verifican portafolio y bitácoras (GD2 7–8); en la versión final no."""
    assert chk("proceso.json", "alcance")["estado"] == "GRIS"  # instancia FINAL
    pid = PID + "_ae4"
    pd = ROOT / "entregas" / pid
    shutil.rmtree(pd, ignore_errors=True)
    pd.mkdir(parents=True)
    plan = json.loads((tmp / "plan_entregas.json").read_text(encoding="utf-8"))
    plan["proyecto_id"] = pid
    (pd / "plan_entregas.json").write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    try:
        sh("bash", "scripts/init_review.sh", "--id", pid, "--instancia", "AE4", "--pdf", str(tmp / "pif_prueba.pdf"),
           "--code-dir", str(tmp / "repo"), "--tag", "v-final", "--offline",
           "--portafolio-dir", str(tmp / "portafolio"), "--bitacoras-dir", str(tmp / "bitacoras"))
        d = json.loads((pd / "artifacts" / "proceso.json").read_text(encoding="utf-8"))
        c = {x["id"]: x for x in d["checks"]}
        assert "guion de la demostración y protocolo de contingencia" in [k for k, v in c["portafolio"]["elementos"].items() if not v]
        b = c["bitacoras"]["por_integrante"]
        assert b["Ana Pérez"]["propuesta"] == "COMPLETO", b["Ana Pérez"]
        assert b["Bruno Díaz"]["propuesta"].startswith("INCOMPLETO") and "no registra decisiones (¿crónica de reuniones?, GD2 8.2)" in b["Bruno Díaz"]["senales"]
    finally:
        shutil.rmtree(pd, ignore_errors=True)


def test_perfiles_y_esquemas():
    for f in (ROOT / "profiles").glob("*.json"):
        p = json.loads(f.read_text(encoding="utf-8"))
        ids = [i["id"] for i in p["items"]]
        assert len(ids) == len(set(ids)), f
        for i in p["items"]:
            if i["modulo"]:
                assert (ROOT / i["modulo"]).exists(), (f.name, i["modulo"])
                txt = (ROOT / i["modulo"]).read_text(encoding="utf-8")
                for s in i["secciones"]:
                    assert f"## {s}" in txt, (f.name, i["id"], s)
    try:
        import jsonschema
    except ImportError:
        return
    sch = json.loads((ROOT / "schemas" / "plan_entregas.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(json.loads((ROOT / "templates" / "plan_entregas.ejemplo.json").read_text(encoding="utf-8")), sch)


if __name__ == "__main__":
    keep = "--keep" in sys.argv
    with tempfile.TemporaryDirectory() as td:
        setup(Path(td))
        fails = 0
        for name, fn in [("capa1", test_capa1), ("referencias", test_referencias_clasificacion),
                         ("maker_checker_estado", test_maker_checker_estado), ("proceso_ae", lambda: test_proceso_ae(Path(td))),
                         ("perfiles", test_perfiles_y_esquemas)]:
            try:
                fn()
                print(f"OK    {name}")
            except AssertionError as e:
                fails += 1
                print(f"FALLA {name}: {e}")
    if not keep:
        shutil.rmtree(P, ignore_errors=True)
    sys.exit(1 if fails else 0)
