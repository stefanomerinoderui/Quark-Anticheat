# Evaluación del diseño v1 y mejoras incorporadas en v2

**Insumos de la evaluación:** documento *Proceso de Diseño y Construcción del Harness de Revisión de PIF* (v1, en `docs/diseno_v1.md`); procedimiento de corrección consolidado en la skill `corregir-pif-ucp` (correcciones reales de PIF 2026, entre ellas los casos en que aparecieron referencias con autoría inventada); criterios de devolución de la cátedra (sin portafolio ni bitácora en reentregas, coloquio previo, acceso al repositorio con la cuenta de cátedra).

**Fecha:** 19/11/2026.

---

## 1. Lo que el diseño v1 resuelve bien

- **Separación entre exigencia reglamentaria y estándar de cátedra** (módulo 05 diferenciado). Es la decisión que más protege al informe frente a Dirección de Carrera y tribunal.
- **WIP=1 con checklist atómico**: es lo que en la práctica evita la revisión "en diagonal" del capítulo IX o X, donde suelen estar las faltas más serias.
- **Estado longitudinal** (`review_state.json`) para controlar reincidencia entre AE1 → AE2 → AE4.
- **Ingesta dual** (local o clon con tag/commit) y verificación de congelamiento.
- **Tres consumidores** del informe con distinto nivel de detalle.
- **Capítulo VIII ampliado** con cruce real contra `LICENSE` y dependencias: es verificable y casi nadie lo hace bien.

## 2. Brechas detectadas (ordenadas por gravedad)

### B1. No se verifica la existencia de las referencias
v1 solo cruza citas del texto contra la Bibliografía. En las correcciones reales, el hallazgo más grave no fue una cita huérfana sino **referencias que no existen o tienen autoría inventada** (nombres que no son personas, DOI no registrados, título real con autores cambiados). Eso es falseamiento de información (Art. 10.1.2) y afecta el criterio de fuentes (Art. 18.1.7), no un desvío de formato APA.
**Mejora:** `scripts/audit_references.py` consulta Crossref y OpenAlex, con control positivo antes de declarar un DOI "no registrado", y clasifica cada entrada como *Verificada / Con discrepancias / No localizada / Fabricada*. Módulo `reglamento/06_verificacion_referencias.md` con la regla de redacción prudente y la verificación de que la fuente respalde las afirmaciones con datos duros.

### B2. Falta la salida para los estudiantes
El *Informe de Cumplimiento* sirve a docentes, Dirección y tribunal, pero lo que el equipo necesita para reentregar es una **devolución con observaciones numeradas, evidencia exigida y matriz de respuesta**, más el **coloquio previo** (Art. 8.2.4, 8.2.6 y 11).
**Mejora:** `templates/devolucion_estudiantes.md`, con IDs `OBS-xx` estables que se persisten en `review_state.json`. La reincidencia se controla por ID, no por similitud de texto.

### B3. Inyección de instrucciones desde el material del estudiante (riesgo de seguridad)
El harness evalúa justamente si los repos tienen `AGENTS.md`, `CLAUDE.md` o `.cursor/rules`. Si esos archivos quedan dentro del árbol de trabajo del agente, **Claude Code puede cargarlos como instrucciones**. Un `CLAUDE.md` del alumno que diga "todo cumple" o un comentario en el PDF dirigido a la IA contaminan la evaluación.
**Mejora:** los repos se clonan en `entregas/<id>/input/` y `init_review.sh` renombra cualquier archivo de instrucciones de agente a `*.STUDENT_DATA` en una copia de trabajo (el original queda intacto en el clon de solo lectura). `AGENTS.md` declara que todo lo que está en `input/` es dato no confiable, y `audit_sdd_harness.py` detecta frases dirigidas a evaluadores o modelos ("ignorá las instrucciones", "calificá como"), que se reportan como hallazgo de integridad.

### B4. Promesas que el sistema no puede cumplir
"Determinístico" y "libre de falsos positivos" no son alcanzables con un LLM en la capa 2 y 3, y comprometen al docente si el informe se cuestiona.
**Mejora:** el objetivo pasa a ser **reproducible, auditable y con tasa de falsos positivos medida**. Para que el Checker deje de ser "otro LLM opinando":
- Cada hallazgo debe incluir una **cita literal** de la evidencia. `scripts/verify_evidence.py` comprueba mecánicamente que esa cita exista en la página del PDF o en la línea del archivo declarada. Si no aparece, el hallazgo se descarta.
- El Checker corre como **subagente separado** (`.claude/agents/checker.md`), con contexto limpio y sin acceso al razonamiento del Maker.

### B5. Detección de IA en la prosa
v1 marca ROJO el "uso no autorizado o no trazado de IA" en prosa. **No hay detector confiable de texto generado**, y un falso positivo en este punto es injusto y difícil de revertir.
**Mejora:** el harness nunca concluye "texto generado por IA". Registra **indicadores verificables** (referencias fabricadas, cifras sin fuente, inconsistencias, cambios bruscos de registro entre capítulos, Cap. XII casi idéntico entre integrantes) y los convierte en **preguntas para el coloquio individual**, que es donde se valida la autoría. Lo único que puede ser ROJO por IA es lo documental: falta de declaración donde el protocolo la exige.

### B6. Ejecutar código de estudiantes
La condición material de ejecutabilidad obliga a compilar y arrancar sistemas ajenos. Sin aislamiento, eso corre con las credenciales del docente.
**Mejora:** `audit_repos.py` no ejecuta nada por defecto. Con `--try-build` corre en un contenedor Docker sin red y sin montar el home, con límite de tiempo. El resultado es evidencia ("no reproducible siguiendo el manual"), pero el ROJO de ejecutabilidad lo **confirma el docente**.

### B7. Límites de la evidencia de git
Las fechas de commit y tag las pone el cliente y se pueden falsificar; un mismo integrante puede commitear con varios correos.
**Mejora:** `init_review.sh` registra el **hash y la fecha de recepción** (hora del clon) en `review_state.json`: esa es la marca de congelamiento confiable. Se respeta `.mailmap`. Las métricas de commits generan **preguntas para el coloquio**, nunca un semáforo ROJO por sí solas.

### B8. Conflictos normativos sin resolver
| Tema | v1 | Práctica de la cátedra | Resolución en v2 |
| --- | --- | --- | --- |
| Portafolio y bitácoras | ROJO si faltan | No se exigen en devoluciones de reentrega; la evidencia vive en el informe y la matriz | Parámetro `exige_portafolio_bitacora` en `plan_entregas.json`. `true` en AE1/AE2/AE4 si la consigna lo pide; `false` en el perfil `reentrega`. |
| IA en redacción | Prohibida en prosa (protocolo 2026, Art. 27.2) | Revisar redacción/ortografía admitido con declaración (programa PFG) | Parámetro `politica_ia` por instancia. Por defecto, el protocolo 2026 en AE4. El informe avisa cuando la política aplicada es más restrictiva que la del programa. |
| "Art. 27.1 / 27.2" | Citado junto a la RR 97/23 | — | Se rotula como **Planificación 2026 / consignas AE**, no como RR 97/23. Verificar el documento exacto. |
| Art. 10.1.2 | Falseamiento | El original tiene **dos incisos numerados 10.1.2** | Citar como "Art. 10.1.2 (segundo inciso)". |
| Anexo III | "Declaración de originalidad" | En el Art. 24.6 el Anexo III es "Otros" | Verificar en el texto oficial antes de citar. Marcado `verificar` en `reglamento/00_fuentes.md`. |

**Mejora general:** `reglamento/00_fuentes.md` registra cada fuente con su versión y un indicador *verificado contra el original* por artículo. El agente no puede citar un artículo marcado `verificar` sin advertirlo.

### B9. Controles que la experiencia mostró necesarios y v1 no tenía
- **Inconsistencias internas** (Art. 18.1.6): un mismo valor técnico con distintos valores en distintos capítulos, arquitectura descripta distinto en Cap. V y IX, numeración de RF/HU, figuras, anexos mencionados que no existen. → `audit_pdf_format.py` extrae candidatos (números con unidad repetidos, referencias a anexos/figuras) y el ítem `COH-01` los revisa.
- **Comparación de versiones** de una reentrega → `scripts/diff_versions.py`.
- **Encuestas:** inferir *n* de los porcentajes cuando no se declara → `scripts/lib/survey.py`.
- **Términos técnicos mal usados** ("RAG" sin generación, "pretotipo" por prototipo).
- **Denominación de la Facultad** y de la carrera en la carátula.
- **Página impresa vs. página del PDF**: toda ubicación se informa como `PDF p. X (impresa Y)`.

### B10. Semáforo de tres colores
VERDE por ausencia de hallazgos es un falso negativo encubierto (p. ej., si el script de referencias no tuvo red).
**Mejora:** cuarto estado **GRIS = no evaluado / no verificable**, con motivo. Nada es VERDE sin evidencia positiva.

### B11. Ortografía y redacción
Contar errores con un LLM no es repetible y el descuento (−0,50 desde el 6.º error ortográfico, −0,50 desde el 4.º de redacción) necesita un número defendible.
**Mejora:** LanguageTool (es) como generador de **candidatos**, si está instalado. El descuento se calcula solo sobre errores **confirmados** por el docente en `artifacts/ortografia_confirmada.json`.

### B12. Otros ajustes
- Claude Code lee `CLAUDE.md`, no `AGENTS.md`: se agrega `CLAUDE.md` que importa `@AGENTS.md`.
- Reutilizar herramientas existentes en lugar de reescribirlas (PyMuPDF, `gitleaks` si está disponible, inventario de dependencias por manifiesto). Si una herramienta falta, el control queda GRIS, no se omite en silencio.
- **Datos personales** (Ley 25.326): `entregas/` está en `.gitignore`; los informes no copian datos sensibles del PIF.
- **Calibración:** el piloto usa devoluciones ya hechas como conjunto de referencia y mide precisión por control (`tests/`).

## 3. Qué cambia en la arquitectura

```text
pif-review-harness/
├── CLAUDE.md                     # NUEVO: importa AGENTS.md
├── AGENTS.md                     # Reescrito: datos no confiables, GRIS, evidencia literal
├── .claude/agents/checker.md     # NUEVO: Checker como subagente con contexto limpio
├── reglamento/00_fuentes.md      # NUEVO: registro de fuentes y artículos a verificar
├── reglamento/06_verificacion_referencias.md   # NUEVO
├── profiles/reentrega.json       # NUEVO: perfil de devolución sin portafolio/bitácora
├── schemas/                      # NUEVO: hallazgo, plan_entregas, review_state
├── scripts/audit_references.py   # NUEVO: Crossref/OpenAlex
├── scripts/verify_evidence.py    # NUEVO: Checker mecánico
├── scripts/diff_versions.py      # NUEVO
├── scripts/state.py              # NUEVO: alta y seguimiento de OBS
└── templates/devolucion_estudiantes.md         # NUEVO
```

## 4. Pendientes

Ver §8.3.

## 5. Cotejo con las fuentes 2026 (19/11/2026)

Documentos cotejados: RR 258/26 (completa, 17 págs.), Consignas AE1, AE2, AE3 y AE4 2026, Planificación de Actividades PFG 2026.

### 5.1. Corrección sobre la RR 258/26

La RR 258/26 aprueba el **régimen transitorio de Espacios Complementarios de Gestión Pedagógica Multimodal** (Aula Digital, Reuniones de Cátedra y de Comisión, Docencia Complementaria, cargas horarias y adicional docente) para 2C2026–1C2027. **No establece el protocolo de IA ni la modalidad de evaluación de las AE.** Sus aportes al harness son:
- Anexo I, 1: la finalidad de "fortalecer la calidad y trazabilidad de la evaluación" y "consolidar criterios institucionales de integridad y uso ético de la Inteligencia Artificial".
- Anexo I, 13: el Aula Digital como espacio de "evidencias de proceso, registros de participación e instancias de verificación de autoría".
- Art. 8 y Anexo I, 10.3: los coloquios y las Intervenciones Orales no se delegan a asistentes ni adscriptos.

El protocolo de IA está en los **apartados 27.1 y 27.2 de la Guía Docente – Parte II**, según citan las consignas AE3 y AE4 (la AE4 transcribe el 27.2 completo). La modalidad de evaluación (AE formativas y sumativas, Portafolio, Bitácora, Foro) también proviene de la Guía Docente y del Sistema de Evaluación Multimodal. La RR 258/26 menciona ese sistema pero no lo regula. Si la Guía fue aprobada por otra resolución (la RR 258/26 cita en el Visto las RR 14/20, 240/22, 195/26 y 257/26), conviene registrarla.

### 5.2. Qué cambió en el harness

| Antes | Ahora | Fuente |
| --- | --- | --- |
| "Art. 27" atribuido a la RR 97/23 o a la RR 258/26 | GD2 27.1 y 27.2; protocolo transcripto con sus seis incisos y los controles de cada uno | AE4 |
| Política de IA `programa_pfg` / `protocolo_2026` | `declaracion_bitacora` (AE1, AE2), `prohibida` (AE3), `gd2_27` (AE4 y reentregas) | AE1–AE4 |
| Rúbrica A–F sin nombres | Nombres, mapeo a 18.1.x y especificación por unidad (AE1, AE2, AE3, AE4). Faltan los descriptores de nivel | AE1–AE4 |
| Nueve criterios 18.1 sin contenido | Contenido según el mapeo de las consignas: 18.1.3 argumentación, 18.1.4 visión sistémica, 18.1.5 conceptos, 18.1.6 coherencia, 18.1.7 fuentes, 18.1.8 presentación escrita | AE1–AE4 |
| Exigencias 2026 resumidas | Exigencias i–vi (AE1), i–ix (AE2) y i–x (AE4) por capítulo, catálogo de requisitos, prototipos v0/v1/final | AE1, AE2, AE4 |
| — | Ítems nuevos: `PROT-01` (prototipo v0 validado), `REQ-01` (catálogo de requisitos), `ENT-01` (componentes de la entrega AE4), `ORA-01` (propuesta de VOA o IOVF), `CIE-01` (cierre AE4 con cuatro extremos) | AE1, AE2, AE4 |
| Descuentos siempre en nota | Informativos en AE1/AE2, en nota en AE3/AE4; reiteración de observaciones formales pondera en contra en F | AE1–AE4 |
| — | Registro formal por instancia (Entregada Completa / No completa; ventana de 10 días) y regla de cierre de AE4 | AE1, AE2, AE4 |
| — | Instancia oral: VOA (AE1, AE2) e IOVF (AE3, AE4), solo ante conductas "no admitidas" con evidencia, propuesta solo en el informe docente | AE1–AE4, RR258 Art. 8 |
| — | `coherence.json#content_markers`: marcadores de contenido por capítulo (línea de base, criterio de aceptación, matriz ponderada, INPI con fecha, hipótesis, umbral, perseverar/pivotar, 10× carga…) | AE1, AE2, AE4 |
| Fechas de ejemplo | AE1 05/09, AE2 01/10 (etiqueta `v1`), AE4 17/11 23:59 (48 h antes del coloquio) | AE1, AE2, AE4, PLAN26 |
| Facultad "a verificar" | "Ingeniería, Tecnología y Arquitectura" confirmada | AE1–AE4 |

### 5.3. Inconsistencias entre los documentos de cátedra

1. **Nota de cursado.** PLAN26, semana 16: "(AE1 + AE2 + AE3 + AE4) / 4". AE4: AE3 y AE4 forman el promedio base (50 % cada una) y AE1/AE2, que no llevan nota, lo modifican según GD2 5.2. Las dos fórmulas no pueden regir a la vez.
2. **Recuperatorio en semana 16.** PLAN26 prevé el 27/11 la "recuperación de la instancia no aprobada"; AE4 dice que el Recuperatorio TIFAS no se sustancia dentro del cuatrimestre. Si se refiere a la AE3, conviene decirlo.
3. **Fecha de la AE2.** La misma consigna dice "último día de la primera semana del mes de octubre · Clase 15 o 16" y "jueves 1.º de octubre de 2026".
4. **Fecha de la AE1.** "Último día de la primera semana del mes de septiembre" frente a la implementación del jueves 3/9 en PLAN26.
5. **Criterios 18.1 por AE.** PLAN26 asigna subconjuntos (AE1: 18.1.1, 18.1.2, 18.1.5, 18.1.7; AE2: 18.1.2, 18.1.4, 18.1.6) y las consignas aplican las seis dimensiones con sus nueve criterios. La AE3 sí concilia su subconjunto con la consigna.
6. **IA entre AE1/AE2 y AE4.** AE1 y AE2 admiten asistentes de texto con declaración; la AE4 prohíbe "reformular, total o parcialmente" los capítulos, que incluyen los producidos en AE1/AE2. El harness no observa el uso declarado en AE1/AE2, pero conviene explicitarlo en la consigna AE4.
7. **Nombre de la instancia oral.** "Verificación Oral de Autoría" (AE1, AE2) e "Instancia Oral de Validación y Fundamentación" (AE3, AE4): si son la misma figura de la Guía Docente, unificar el nombre.

## 6. Cotejo con la RR 97/23 y la Guía Docente – Parte II (19/11/2026, v2.2)

La RR 97/23 está escaneada: se pasó por OCR y la numeración del Art. 8.2 se verificó a ojo sobre la página. Todos los artículos del registro pasan a **ok**, con su página.

### 6.1. Confirmaciones

- Art. 8.2.1 a 8.2.6, 10.1.2 duplicado, 11, 18.2: coinciden con lo que usaba la skill de corrección.
- Art. 20 y 21 coinciden con las consignas.
- La GD2 confirma el cierre de AE4 (producto ≥ 6 + portafolio + bitácora + coloquio validado), el recuperatorio TIFAS (6 o 7), la grabación y la revisión de 48 h.

### 6.2. Novedades incorporadas

| Tema | Antes | Ahora |
| --- | --- | --- |
| Art. 18.1 | Mapeo inferido | Texto literal de los nueve criterios. **18.1.3 es "objetivos de acuerdo al perfil del egresado"**, no argumentación |
| Anexo III | Duda | Anexo III de la Resolución = Formulario N.º 2 (publicación + declaración de originalidad); Anexo III del PIF = "Otros Anexos" |
| Facultad | Solo la denominación vigente | La RR97 dice "Facultad de Ingeniería y Tecnología"; el harness acepta ambas |
| Art. 10.1.2 | "falseamiento o adulteración" | Literal: "adulteración **voluntaria**" (afecta cómo se redacta una observación de referencias) |
| Art. 20 | Resumen | Tapa dura, títulos y encabezado de libre elección, láminas IRAM, SIMELA + SI |
| IA (GD2 27.1) | Prohibición en prosa solo en AE4 | **Regla general para todas las AE**, incluidos los productos de AE1/AE2, las bitácoras y las **reelaboraciones y recuperatorios**; excepción solo con protocolo autorizado de seis elementos (27.2) |
| Instancia oral | VOA en AE1/AE2, IOVF en AE3/AE4 | **IOVF** en todas, con duración, grabación y revisión de GD2 16–18; banco de preguntas organizado en *dar cuenta, fundamentar, profundizar* |
| Cierre | Solo AE4 | Checklist por componente de GD2 23 (COMPLETO = mínimos, no excelencia) en AE1, AE2 y AE4 (`CIE-01`) |
| Feedback AE1/AE2 | Libre | Estructura de GD2 11: logros + aspectos de mejora + sugerencias/reelaboración + dictamen |

### 6.3. Cuatro hallazgos que conviene resolver en la cátedra

1. **Las consignas AE1 y AE2 no se ajustan a GD2 27.** Admiten asistentes de texto con declaración, sin el protocolo autorizado que exige el 27.2. El harness evalúa según la consigna publicada, porque no corresponde observar a un estudiante por hacer lo que la consigna le permitió, y lo advierte en el informe docente.
2. **La pauta de IA en reentregas debe cambiar.** La skill `corregir-pif-ucp` admitía revisar redacción con IA si se declaraba en la matriz; GD2 27.1 lo prohíbe en "reelaboraciones y recuperatorios". El harness ya usa `gd2_27`; conviene actualizar la skill.
3. **AE4 con equipos de tres.** GD2 14 y 26: la AE4 es individual o en pareja, "nunca se realiza en Trío". La consigna AE4 trabaja sobre el producto colectivo del equipo de AE1 (dos o tres integrantes). La planificación la registra como individual con coloquio, lo que puede sostenerse; conviene explicitarlo en la consigna.
4. **Regularidad.** GD2 5.2 exige al menos una de AE1/AE2 completa; la consigna AE4 exige ambas en un párrafo y reproduce GD2 5.2 en otro; la planificación usa un promedio de las cuatro AE.

## 7. Reencuadre en la RR 97/23 y cláusula de IA de la cátedra (19/11/2026, v2.3)

### 7.1. Decisiones del docente

1. **El PIF se evalúa según la RR 97/23.** No se verifican aprobación, cierre por componentes, notas, regularidad, recuperatorios, Ventana de Mejora, portafolio, bitácora, foro, rúbrica A–F, descuentos ni IOVF de las AE. La Guía Docente, la RR 258/26, las consignas y la planificación quedan como contexto.
2. **Declaración de uso de IA (cláusula de cátedra):** apartado final que indique para qué se usó la IA, cómo se verificó la información, los prompts y el enlace a la conversación; el uso no declarado o los datos no verificables se observan según los reglamentos; se puede pedir que el estudiante dé cuenta oralmente de cualquier producción.

### 7.2. Cambios en el harness

| Antes (v2.2) | Ahora (v2.3) |
| --- | --- |
| Perfiles `ae1_diagnostico`, `ae2_formulacion`, `ae4_final` | `avance_caps_I_II`, `avance_caps_III_V_X`, `pif_final`, `reentrega` |
| Políticas de IA por AE (`declaracion_bitacora`, `gd2_27`, `prohibida`) | `declaracion_catedra` por defecto; las otras quedan opcionales si alguna vez se quisiera aplicar la Guía |
| Ítems PRC-01 (portafolio/bitácora), CIE-01 (cierre), PROT-01 (prototipo v0) | Eliminados |
| ACA-01 rúbrica A–F | ACA-01 valoración orientativa por los criterios literales del Art. 18.1 |
| FMT-03 con descuentos | Solo candidatos de ortografía y redacción confirmados por el docente |
| ORA-01 IOVF (GD2 16–18) | ORA-01 "dar cuenta oralmente" (cláusula de cátedra, Arts. 8.2.4 y 11) |
| — | **DIA-01** y control `coherence.json#ai_declaration`: detecta el apartado, su ubicación final, los cuatro elementos, los enlaces de conversación (ChatGPT, Claude, Gemini, Copilot, Perplexity y otros), la declaración de no uso y la evidencia de uso no declarado (menciones en el texto, archivos de agentes en el repositorio) |
| Causales de ROJO con fundamento en consignas | Todas fundadas en la RR 97/23: Arts. 3, 4, 10.1.2, 18.1.7–18.1.8, 20, 22–24 y Ley 25.326. Las exigencias de las consignas pasan a "estándar de contenido de cátedra" (solo AMARILLO) |
| — | Art. 4 (distribución clara y expresa de responsabilidades en trabajos grupales) como contenido obligatorio del Cap. V |

### 7.3. Pendientes

1. Piloto de calibración con 2 o 3 PIF ya corregidos y su devolución.
2. Actualizar la skill `corregir-pif-ucp` con la cláusula de IA (hoy pide declarar solo en la matriz).

## 8. Dos regímenes: entregas parciales de AE y versión final (19/11/2026, v2.4)

### 8.1. Decisión del docente

- En las **entregas parciales** del PIF (cada AE), se siguen la Guía de Evaluación Multimodal respecto de **portafolio y bitácora**, las verificaciones del harness y la **declaración de uso de IA** (cláusula de cátedra).
- En la **versión final**, se sigue la **RR 97/23** con las consideraciones elaboradas (v2.3).

### 8.2. Cambios

| Antes (v2.3) | Ahora (v2.4) |
| --- | --- |
| Perfiles de avance sin portafolio ni bitácora | `ae1_entrega_parcial`, `ae2_entrega_parcial`, `ae4_entrega_integral` con `PRC-01`; `pif_final` y `reentrega` sin él |
| Portafolio y bitácora fuera de alcance | `PRC-01` (GD2 7, 8.1, 8.2 y contenido de cada consigna), solo cuando `exige_portafolio_bitacora = true` |
| — | `scripts/audit_proceso.py` y opciones `--portafolio-dir` / `--bitacoras-dir` en `init_review.sh`: busca los elementos del portafolio que pide cada consigna, asigna cada bitácora a su integrante, cuenta entradas fechadas, revisa los seis elementos y señala bitácoras-crónica o casi idénticas. Propone COMPLETO / INCOMPLETO; confirma el docente |
| — | Sección "Portafolio y Bitácora" en el informe y en la devolución de las AE |
| Igual | Declaración de IA (cláusula de cátedra) en todas las entregas; nunca nota, cierre, regularidad, rúbrica ni descuentos |

La AE4 se trató como entrega de AE (con portafolio y bitácora) y la versión final como la instancia posterior de aprobación previa a la defensa. Si la cátedra considera la AE4 como la versión final, basta con poner `exige_portafolio_bitacora: false` en esa instancia del plan.

### 8.3. Pendientes

1. Piloto de calibración con 2 o 3 PIF ya corregidos y, para las AE, con su portafolio y sus bitácoras.
2. Actualizar la skill `corregir-pif-ucp` con la cláusula de IA y los dos regímenes.
