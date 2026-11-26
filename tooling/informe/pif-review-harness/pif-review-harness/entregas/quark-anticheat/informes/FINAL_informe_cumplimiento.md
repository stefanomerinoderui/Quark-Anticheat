# Informe de Cumplimiento — FINAL (autorrevisión)

| | |
| --- | --- |
| Proyecto | Quark Anticheat (`quark-anticheat`) |
| Equipo | G. S. Martinez Alarcón (autor, defiende); S. N. Merino De Rui (colaborador) |
| Modalidad declarada (Art. 23) | 23.2 Diseño y Desarrollo |
| Instancia / perfil | FINAL / `pif_final` |
| Versión evaluada | PDF `build/Informe-PIF-2026-11-25.pdf` (193 págs.); código `Dev@35c6031`; docs `dev/docs@ea676de` |
| Marco | RR 97/23 y cláusula CAT-IA. Sin portafolio ni bitácora |
| Variaciones acordadas | Ninguna |
| Fecha | 2026-11-25 · `agent:claude-sonnet-5-5` |

Autorrevisión hecha por el equipo con el harness para anticipar observaciones. No es una evaluación de la cátedra.

## 1. Resumen ejecutivo

**Veredicto propuesto:** no en condiciones de habilitar la defensa (Art. 11) en el estado actual. Hay 2 ROJO. La decisión es docente.

| Semáforo | Cantidad | Ítems |
| --- | --- | --- |
| ROJO | 2 | GATE-01, DIA-01 |
| AMARILLO | 13 hallazgos | COH-01, ENT-01, EST-01 (3), EST-02, EST-04, EST-06, FMT-01, FMT-02, REF-02, REPO-01, ENG-01 |
| VERDE | 2 | EST-06 (conclusiones), ETH-01 |
| GRIS | 9 | ACA-01, COH-01 (ADR-001), DAT-01, EST-03, EST-05, FMT-03, ORA-01, REF-01, REQ-01 |

**Observaciones más graves**
- OBS-02: sin declaración de uso de IA y con firmas `agent:claude-sonnet-5-5` en el PDF (p. 4 y 185).
- OBS-12: sin manual de despliegue en `Dev@35c6031`; no se ejecutó la construcción.
- OBS-03/OBS-11: el PDF se generó con "cambios sin commitear" y conserva bloques "Update" del vault.

**Referencias:** 1 verificada · 2 con discrepancias · 5 no localizadas · 0 fabricadas · 9 accesibles sin cotejo de contenido. Método: Crossref y OpenAlex automáticos, sin búsqueda manual. Varias discrepancias vienen de la extracción del PDF (nombres partidos, guiones). No se usa "Fabricada".

**Declaración de IA (DIA-01):** ausente, con evidencia de uso.

## 2. Matriz de cumplimiento (RR 97/23)

| Ítem | Semáforo | Hallazgo principal | Ubicación | OBS |
| --- | --- | --- | --- | --- |
| GATE-01 | ROJO | Sin manual de despliegue, sin CI | `repos.json#deploy_manual` | OBS-12 |
| DIA-01 | ROJO | Sin declaración CAT-IA | PDF p. 185; `coherence.json#ai_declaration` | OBS-02 |
| REPO-01 | AMARILLO | LICENSE solo en `dev/docs` | `repos.json#license` | OBS-14 |
| ENT-01 | AMARILLO | Versión sin commit publicado; 3 URL de repo | PDF p. 1 | OBS-03 |
| FMT-01 | AMARILLO | Fuente TeX Gyre Termes; márgenes ~2,9 cm | `pdf_format.json` | OBS-10 |
| FMT-02 | AMARILLO | Bloques "Update" con firma de agente | PDF p. 4, 185 | OBS-11 |
| EST-01 | AMARILLO | Carátula incompleta; `{#…}` en 16 págs.; Resumen 696 palabras | PDF p. 1, 7, 132 | OBS-04/05/06 |
| EST-02 | AMARILLO | Encuesta no publicada, sin n | PDF p. 19 | OBS-07 |
| EST-04 | AMARILLO | INPI incompleto; sin logotipo | PDF p. 97 | OBS-08 |
| EST-06 | AMARILLO / VERDE | Anexos sin "X de Y"; Conclusiones honestas | PDF p. 163, 158 | OBS-09 |
| COH-01 | AMARILLO / GRIS | Control negativo invalidado; ADR-001 sin cotejar | PDF p. 170, 6 | OBS-01 |
| REF-02 | AMARILLO | Fuentes con "URL pendiente" o "resumen de búsqueda" | PDF p. 161–162 | OBS-13 |
| ENG-01 | AMARILLO | Sin tests, CI ni quality gates detectables | `sdd_harness.json` | — |
| ETH-01 | VERDE | Sin inyección ni secretos por regex | `sdd_harness.json` | — |

## 3. Sistema de Información entregado
No se ejecutó la construcción (`sandbox_build.sh` no corrido). GATE-01 es ROJO por ausencia de manual, pendiente de confirmación docente.

## 4. Seguimiento de observaciones previas
No aplica: sin OBS previas.

## 5. Declaración de uso de IA

| Elemento | Presente | Evidencia |
| --- | --- | --- |
| Apartado final | no | — |
| Para qué se usó | no | — |
| Cómo se verificó | no | — |
| Prompts | no | — |
| Enlace | no | — |

Evidencia de uso: firmas `agent:claude-sonnet-5-5` en PDF p. 4 y 185; archivo de contexto de agentes en el repo (renombrado a `*.STUDENT_DATA`).

## 6. Solo informe docente
- **Commits (REPO-01, Art. 4):** `Dev` tiene 25 commits; 24 de S. Merino (94,5 % de líneas) y 1 de G. Martinez (5,5 %). Solo para coloquio: el Cap. V debe explicitar la distribución de responsabilidades. Verificar los emails de autoría, porque el commit de un integrante puede figurar bajo otra cuenta.
- **DAT-01:** teléfonos detectados por regex en p. 22, 168 y 169. Revisar si son de terceros (Ley 25.326).
- **Capítulos sin leer:** I, III–VII, IX–XIII no se evaluaron de fondo (EST-03, EST-05, REQ-01, ACA-01, ORA-01).
- **ENG-01:** las pruebas existen como scripts de VM que el detector no cuenta.

## 7. Controles en GRIS y límites
Ortografía (sin LanguageTool); cruce citas↔bibliografía (parser poco fiable); ADR-001; DAT-01; capítulos sin leer. gitleaks no instalado. Valoración 18.1 no hecha.

**Preguntas de coloquio (ORA-01):** ¿Cómo construyen y cargan el módulo desde cero en una VM limpia? ¿Qué partes se hicieron con IA y cómo las verificaron? ¿Qué evidencia propia sostiene H-D1 a H-D3? ¿Qué aportó cada integrante?
