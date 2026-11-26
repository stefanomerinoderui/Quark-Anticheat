<!--
PLANTILLA — Informe de Cumplimiento (consumidores: equipo docente, Dirección de Carrera, tribunal).
Marco: entregas parciales de AE = contenido + CAT-IA + Portafolio y Bitácora (GD2 7–8); versión final = RR 97/23 + CAT-IA. Nunca nota, cierre, regularidad ni rúbrica de las AE.
Fuente de datos: artifacts/findings_final_<INST>.json, artifacts/manifest.json, review_state.json, plan_entregas.json.
Reglas: no copiar datos personales del PIF; toda afirmación lleva el ID del hallazgo; GRIS se informa con motivo.
Convertir a Word si hace falta: pandoc <archivo>.md -o <archivo>.docx
-->

# Informe de Cumplimiento — {{instancia}}

| | |
| --- | --- |
| Proyecto | {{titulo}} (`{{proyecto_id}}`) |
| Equipo | {{integrantes}} |
| Modalidad declarada (Art. 23) | {{modalidad}} |
| Instancia / perfil | {{instancia}} / `{{perfil}}` |
| Versión evaluada | PDF `{{pdf_archivo}}` (sha256 `{{pdf_sha_corto}}`), repo `{{repo_ref}}` → `{{commit_corto}}`, recibido el {{recibido_el}} |
| Marco de evaluación | {{Entrega parcial de AE: contenido según RR 97/23, declaración de IA (cátedra), Portafolio y Bitácora (Guía de Evaluación Multimodal) · Versión final: RR 97/23 y declaración de IA (cátedra)}} |
| Variaciones acordadas | {{variaciones_o_ninguna}} |
| Fecha del informe | {{fecha}} |

## 1. Resumen ejecutivo

**Veredicto propuesto:** {{en condiciones / no en condiciones de aprobar el PIF y habilitar la defensa (Art. 11)}} · {{en un avance: observaciones a resolver en la próxima versión}}. *El veredicto es del docente; esta es una propuesta fundada en los hallazgos.*

| Semáforo | Cantidad | Ítems |
| --- | --- | --- |
| 🔴 ROJO | {{n}} | {{ids}} |
| 🟡 AMARILLO | {{n}} | {{ids}} |
| 🟢 VERDE | {{n}} | {{ids}} |
| ⚪ GRIS (no evaluado) | {{n}} | {{ids y motivo}} |

**Las 3 observaciones más graves:** {{OBS-xx — una línea cada una}}

**Referencias:** {{n}} verificadas · {{n}} con discrepancias · {{n}} no localizadas · {{n}} fabricadas · {{n}} no verificadas. Método: Crossref/OpenAlex (control positivo {{OK/falló}}) + búsquedas web registradas.

**Declaración de uso de IA (DIA-01):** {{completa / incompleta (faltan: …) / ausente con evidencia de uso / ausente sin evidencia / declara no uso}}.

## 2. Matriz de cumplimiento normativo (RR 97/23)

| Ítem | Criterio | Norma | Semáforo | Hallazgo principal | Ubicación | OBS |
| --- | --- | --- | --- | --- | --- | --- |
| {{GATE-01}} | {{…}} | {{RR97 Art. …}} | {{…}} | {{…}} | {{PDF p. X (impresa Y) / repo:ruta:línea}} | {{OBS-xx}} |

{{Las observaciones basadas en el estándar de contenido de cátedra se listan aparte, como AMARILLO.}}

## 3. Sistema de Información entregado

{{Resultado de GATE-01 según la modalidad (Art. 23): build.json (imagen, pasos, código de salida) o intento manual del docente siguiendo el manual. Si es ROJO, indicar "confirmado por el docente el …".}}

## 4. Seguimiento de observaciones previas

| OBS | Origen | Estado | Nota |
| --- | --- | --- | --- |
| {{OBS-xx}} | {{instancia}} | {{subsanada / parcial / reincidente / subsanada a confirmar}} | {{…}} |

{{Si hay versión anterior: resumen de diff_versiones.json — capítulos modificados, sin cambios y contradicciones nuevas.}}

## 5. Declaración de uso de IA (cláusula de cátedra)

| Elemento | Presente | Evidencia |
| --- | --- | --- |
| Apartado final de declaración | {{sí/no}} | {{PDF p. X}} |
| Para qué se usó | | |
| Cómo se verificó la información | | |
| Prompts utilizados | | |
| Enlace a la conversación | | {{enlaces listados para que el docente los abra}} |

**Evidencia de uso fuera de la declaración:** {{menciones de herramientas en el texto; archivos de contexto de agentes en el repositorio}}. **Datos no verificables:** {{remitir a REF-02 y DAT-01}}.

## 5 bis. Portafolio y Bitácora (solo entregas parciales de AE — PRC-01)

| Componente | Propuesta | Elementos faltantes / señales | Evidencia a presentar |
| --- | --- | --- | --- |
| Portafolio Digital | {{COMPLETO / INCOMPLETO}} | {{…}} | {{…}} |
| Bitácora — {{integrante 1}} | {{COMPLETO / INCOMPLETO}} | {{…}} | {{…}} |
| Bitácora — {{integrante 2}} | | | |

*COMPLETO = presentado y con los mínimos requeridos; no significa excelencia (Guía de Evaluación Multimodal, 7). El registro definitivo es del docente.*

## 6. Ortografía y redacción (candidatos)

| Tipo | Candidatos (LanguageTool) | Confirmados por el docente | Páginas |
| --- | --- | --- | --- |
| Ortografía | {{n}} | {{n}} | {{…}} |
| Redacción (incluye Art. 21) | {{n}} | {{n}} | {{…}} |

## 7. Valoración orientativa por criterios del Art. 18.1 (solo docente)

| Art. | Criterio | Apreciación | Hallazgos | Pregunta abierta |
| --- | --- | --- | --- | --- |
| 18.1.1 | Pertinencia del tema seleccionado | {{sólido / suficiente / débil / no evaluable}} | {{IDs}} | {{…}} |
| 18.1.2 | Claridad del tema | | | |
| 18.1.3 | Objetivos de acuerdo al perfil del egresado | | | |
| 18.1.4 | Grado de aplicación de los conocimientos adquiridos | | | |
| 18.1.5 | Manejo de los conceptos teóricos | | | |
| 18.1.6 | Coherencia de los componentes y las conclusiones | | | |
| 18.1.7 | Fuentes de información consultadas | | | |
| 18.1.8 | Presentación escrita | | | |

*Orientativa. 18.1.9 (presentación oral) se aprecia en la defensa. No se propone nota.*

## 8. Apartado de cátedra — SDD, Harness Engineering y buenas prácticas

> No es exigencia de la RR 97/23: es estándar técnico de la cátedra.

| Dimensión | Semáforo | Evidencia |
| --- | --- | --- |
| Spec-Driven Development | {{…}} | {{carpetas, secuencia temporal}} |
| Harness para agentes de código | {{…}} | {{archivos de contexto, quality gates}} |
| Trazabilidad humana | {{…}} | {{distribución de commits — insumo del Art. 8.2.4; ver límites}} |
| Higiene de ingeniería | {{…}} | {{README, tests, lockfiles, secretos}} |

## 9. Integridad y pedido de dar cuenta oralmente (solo docente)

**Indicadores verificables** (ETH-01, REF-02, DAT-01, DIA-01 — no son conclusiones): {{lista con ubicación}}.

**Propuesta (ORA-01):** {{No se propone / Se propone pedir a {{integrante(s)}} que den cuenta oralmente de: {{puntos concretos}} — hallazgos {{IDs}}.}} Fundamento: cláusula de cátedra ("en todas las producciones entregadas se le podrá pedir que dé cuenta oralmente") y Arts. 8.2.4 y 11. Es decisión docente.

## 10. Banco de preguntas

**Coloquio previo (por integrante).** En tres planos: *dar cuenta* (qué hizo, qué aportó, qué cambió), *fundamentar* (por qué, con qué conceptos o autores, qué alternativa descartó), *profundizar* (consecuencias, límites, qué haría distinto; fragmentos asistidos por IA: qué pidió, qué aceptó, qué corrigió y cómo lo verificó). Cada integrante responde por todo el proyecto.
1. {{pregunta}} — *origen: {{ID}}*

**Tribunal:**
1. {{pregunta}} — *origen: {{ID}}*

## 11. Trazabilidad del informe

- Capa 1: `manifest.json` del {{fecha}} — auditorías con error u omitidas: {{lista}}.
- Hallazgos descartados por verificación mecánica: {{n}}; por el Checker: {{n}}.
