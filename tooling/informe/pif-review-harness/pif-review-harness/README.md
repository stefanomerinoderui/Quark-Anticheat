# Harness de Revisión de PIF — UCP · Ingeniería en Sistemas de Información

Entorno local para revisar Proyectos Integradores Finales con un agente de código (Claude Code) de forma **reproducible, auditable y con evidencia verificable**, contra la RR 97/23, las consignas de cátedra 2026 y el estándar técnico de la cátedra.

- Diseño original: `docs/diseno_v1.md`
- Evaluación del diseño y cambios de la v2: `docs/EVALUACION_Y_MEJORAS.md`

## Requisitos

- Python 3.10+ y `pip install -r requirements.txt`
- git
- Windows: correr los `.sh` desde **Git Bash** (o WSL). Si el intérprete se llama `python`, anteponer `PYTHON=python`.
- Opcionales: Docker (para `sandbox_build.sh`), `gitleaks` (secretos), servidor local de LanguageTool (`LT_URL`) para candidatos de ortografía.

## Uso

```bash
# 1. Crear el plan del proyecto (una vez por equipo)
mkdir -p entregas/pif-2026-turnos
cp templates/plan_entregas.ejemplo.json entregas/pif-2026-turnos/plan_entregas.json
#    → completar equipo (con todos los correos de git de cada integrante), modalidad, instancias,
#      instancias (perfil y fecha) y variaciones acordadas.

# 2. Ingesta + Capa 1 (determinística)
scripts/init_review.sh --id pif-2026-turnos --instancia AE2 \
    --pdf ~/Descargas/PIF_Turnos_final.pdf \
    --code-url https://github.com/equipo/turnos --tag v1 \
    --portafolio-dir ~/Descargas/AE2/portafolio --bitacoras-dir ~/Descargas/AE2/bitacoras
#    versión final (sin portafolio ni bitácora):
#    --instancia FINAL --pdf PIF_final.pdf --code-url ... --tag v-final
#    reentrega con versión anterior:
#    --instancia REENTREGA-1 --pdf nueva.pdf --pdf-anterior vieja.pdf

# 3. (Opcional) Intento de construcción aislado
scripts/sandbox_build.sh --id pif-2026-turnos

# 4. Capas 2 y 3, en Claude Code desde la raíz de este repo:
#    "Revisá la entrega FINAL del proyecto pif-2026-turnos siguiendo AGENTS.md."
```

El agente recorre el perfil ítem por ítem, escribe `artifacts/findings/<ITEM>.maker.json`, corre `scripts/verify_evidence.py`, invoca al subagente `checker`, consolida con `scripts/state.py merge` y redacta:

- `informes/<INST>_informe_cumplimiento.md` — docentes, Dirección de Carrera, tribunal.
- `informes/<INST>_devolucion.md` — estudiantes: OBS-xx, evidencia exigida, matriz de respuesta y coloquio.

Para pasar a Word: `pandoc informes/FINAL_devolucion.md -o FINAL_devolucion.docx`.

## Cómo está armado

| Capa | Qué hace | Dónde |
| --- | --- | --- |
| 1 · Determinística | Mide formato, estructura, citas, existencia de referencias, repos, licencias, commits, secretos, inyección de instrucciones, datos personales | `scripts/` → `artifacts/*.json` + `manifest.json` |
| 2 · Normativa (Maker, WIP=1) | Evalúa cada ítem del perfil cargando solo su módulo de `reglamento/` | `AGENTS.md`, `profiles/` |
| 3 · Auditoría | Verificación mecánica de citas literales + Checker con contexto limpio | `scripts/verify_evidence.py`, `.claude/agents/checker.md` |
| Estado | Entregas, hashes, OBS estables, reincidencia | `entregas/<id>/review_state.json`, `scripts/state.py` |

**Semáforo:** ROJO (bloqueante) · AMARILLO (corregible) · VERDE (cumple, con evidencia positiva) · GRIS (no evaluado, con motivo).

**Dos regímenes:**
- **Entregas parciales del PIF en las AE** (`ae1_entrega_parcial`, `ae2_entrega_parcial`, `ae4_entrega_integral`): contenido entregado, declaración de uso de IA (cláusula de cátedra) y Portafolio y Bitácora según la Guía de Evaluación Multimodal. Ingresarlos con `--portafolio-dir` y `--bitacoras-dir` (una bitácora por integrante; el nombre del archivo debe contener su nombre o apellido).
- **Versión final del PIF** (`pif_final`, `reentrega`): RR 97/23 con las consideraciones de cátedra; sin portafolio ni bitácora.

En ningún caso se verifican nota, cierre, regularidad, rúbrica ni descuentos de las AE.

**Fuentes:** `reglamento/fuentes/` guarda los originales (no versionados) y `reglamento/fuentes/texto/` su texto extraído (con los DNI omitidos), para que el agente cite las consignas en forma literal.

## Seguridad y datos

- Los repos se clonan *bare* en `input/_git/` y la versión evaluada se exporta a `input/repo_codigo/` con `AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.claude/`, etc. renombrados a `*.STUDENT_DATA`, para que el agente no los cargue como instrucciones. `AGENTS.md` y `.claude/settings.json` refuerzan la regla.
- Las frases dirigidas al evaluador en el PDF o el repo se reportan (`sdd_harness.json#injection`).
- El código del estudiante solo se ejecuta en `sandbox_build.sh` (contenedor sin montajes del host, recursos limitados).
- `entregas/` está en `.gitignore`. LanguageTool solo con servidor local.
- La verificación de referencias consulta Crossref y OpenAlex (solo metadatos bibliográficos). Opcional: `export HARNESS_MAILTO=...` para el *polite pool* de Crossref.

## Pruebas

```bash
python3 tests/test_harness.py
```

Genera un PIF y un repo sintéticos con ~30 errores sembrados (margen, interlineado, tipografía, resumen largo, carátula faltante, citas huérfanas, año distinto, referencia con autor atípico, DOI inexistente, URL acortada, encuesta sin n, valores contradictorios, Cap. XII duplicado, datos personales, inyección de instrucciones, dependencia GPL, clave AWS, commits tardíos, integrante sin commits) y verifica que la Capa 1 los detecte, que la clasificación de referencias funcione con respuestas simuladas y que el ciclo Maker → verificación → estado asigne OBS estables y detecte reincidencia.

## Pendientes antes del piloto

Fuentes cotejadas: RR 97/23 (marco de evaluación), cláusula de cátedra de IA y, como contexto, Guía Docente – Parte II, RR 258/26, consignas y planificación 2026 (`reglamento/00_fuentes.md`). Falta el piloto con 2 o 3 PIF ya corregidos. Ver `docs/EVALUACION_Y_MEJORAS.md §7`.
