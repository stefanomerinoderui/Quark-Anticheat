# Proceso de Diseño y Construcción del Harness de Revisión de Proyectos Integradores Finales (PIF)

**Institución:** Universidad de la Cuenca del Plata (UCP) — Facultad de Ingeniería, Tecnología y Arquitectura  
**Carrera:** Ingeniería en Sistemas de Información  
**Asignatura:** Proyecto Final de Grado (PFG)  
**Entorno de ejecución objetivo:** Local, asistido por agentes de código (Claude Code o equivalentes)  
**Estado del proyecto:** v2.4 (AE: contenido + IA + portafolio/bitácora; versión final: RR 97/23) — Fases 1 y 2 implementadas y probadas con un PIF sintético; Fase 3 parcial (plantillas y perfiles listos, piloto pendiente)  
**Versión del documento:** 2.0 (19/11/2026). Cambios respecto de la v1 en `docs/EVALUACION_Y_MEJORAS.md`.  

---

## 1. Resumen Ejecutivo y Propósito

El presente documento registra de manera exhaustiva el proceso de análisis, diseño e implementación inicial de un **Harness de Revisión de Proyectos Integradores Finales (PIF)** basado en los principios de **Harness Engineering** (tomando como referencia metodológica el repositorio `walkinglabs/learn-harness-engineering`).

El objetivo del sistema es reemplazar la revisión ad-hoc con modelos de lenguaje (subir un PDF a un chat y solicitar una corrección general) por un entorno de auditoría **reproducible, trazable, auditable y con tasa de falsos positivos medida** que garantice el respeto estricto al marco normativo institucional y a los estándares técnicos de la cátedra.

### Destinatarios de la salida del sistema
El *harness* genera dos artefactos: un **Informe de Cumplimiento** (semáforos, observaciones, valoración orientativa, guía de defensa) consumido de forma escalonada por los tres actores de abajo, y una **Devolución a los estudiantes** (observaciones OBS-xx con evidencia exigida, matriz de respuesta y coloquio previo):
1. **Equipo Docente (consumidor principal):** Acelera la corrección, aporta evidencia objetiva de formato y código, sugiere valoración en la rúbrica analítica y genera preguntas específicas para los coloquios individuales.
2. **Dirección de Carrera (consumidor secundario):** Brinda una vista ejecutiva del cumplimiento reglamentario (RR 97/23 y RR 258/26) y de la trazabilidad del proceso antes de habilitar instancias administrativas.
3. **Tribunal Evaluador (apoyo en instancia final):** Sirve como insumo estructurado de consulta sobre la coherencia del informe, el código entregado y las posibles tensiones técnicas a indagar en la defensa oral pública.

---

## 2. Fundamentación Metodológica: Los 5 Subsistemas del Harness

El diseño adopta la premisa central de *Harness Engineering*: **el modelo aporta capacidad de razonamiento, pero el arnés (*harness*) es el que garantiza confiabilidad**. Los cinco subsistemas del enfoque se tradujeron al dominio de la evaluación académica del siguiente modo:

| Subsistema | Principio en Harness Engineering | Implementación en el Harness de Revisión de PIF |
| :--- | :--- | :--- |
| **1. Instrucciones (*Progressive Disclosure*)** | Evitar un *mega-prompt* monolítico; usar un índice central y cargar reglas modulares bajo demanda (*Just-in-Time*). | Un orquestador principal (`AGENTS.md`) que carga únicamente el módulo de `reglamento/` correspondiente al criterio en evaluación. |
| **2. Alcance (*Scope* y `WIP=1`)** | Restringir al agente a una unidad atómica de trabajo por vez para evitar omisiones y revisiones superficiales. | Checklists atómicos en JSON (`profiles/ae4_final.json`, etc.) que obligan a evaluar y cerrar un criterio por vez. |
| **3. Verificación (*Quality Gates*)** | El agente no puede declarar cumplimiento sin pruebas ejecutables o evidencia verificable. | Doble capa: scripts determinísticos (Python/Bash) que miden formato, citas y repositorios antes del LLM + obligación de citar artículo y página/archivo en cada hallazgo. |
| **4. Estado (*State*)** | Persistencia en disco para retomar trabajo sin perder contexto entre sesiones. | Archivo `review_state.json` por proyecto que registra el historial de entregas (AE1 $\to$ AE2 $\to$ AE4) y controla si las observaciones previas fueron subsanadas o reinciden. |
| **5. Ciclo de vida (*Session Lifecycle*)** | Inicialización determinística, ejecución controlada y cierre limpio. | Script `init_review.sh` que prepara el espacio de trabajo, ingesta el PDF y los repositorios (locales o remotos), ejecuta las auditorías automáticas y habilita al agente. |

### Patrón Maker-Checker (Separación Generador / Auditor)
Para eliminar críticas subjetivas o alucinaciones normativas, cada ítem del checklist atraviesa un ciclo de dos pasos:
* **Fase Maker (Revisor):** Evalúa el entregable contra el módulo normativo y los resultados determinísticos, asigna un semáforo y redacta hallazgos y recomendaciones.
* **Verificación mecánica (`verify_evidence.py`):** cada hallazgo incluye una *cita literal*; el script comprueba que exista en la página del PDF o en la línea del archivo indicadas, corrige páginas corridas y descarta lo que no aparece.
* **Fase Checker (Auditor de Evidencia, subagente con contexto limpio):** audita lo que sobrevivió y descarta cualquier observación sin norma registrada en `reglamento/00_fuentes.md`, cuya cita no demuestre lo observado o que contradiga los reportes de los scripts.

---

## 3. Síntesis del Relevamiento y Marco Normativo Integrado

Durante el proceso se analizaron e integraron cinco fuentes normativas y pedagógicas, más dos requerimientos específicos definidos por la cátedra.

### 3.1. Resolución Rectoral UCP N.º 97/23 (Reglamento General del PIF)
Constituye la columna vertebral obligatoria del *harness*:
* **Finalidad y modalidades (Arts. 1 a 4 y 23):** Encuadre obligatorio del PIF en una de tres modalidades: *23.1 Selección y Administración*, *23.2 Diseño y Desarrollo* (exige MVP en Cap. V) o *23.3 Implementación* (exige descripción de implementación en Cap. V).
* **Aspectos formales (Art. 20):** Hoja A4; márgenes superior/inferior de $2{,}5\text{ cm}$ e izquierdo/derecho de $3\text{ cm}$; interlineado doble; tipografía Times New Roman tamaño 12 en cuerpo y 10 en notas/citas al pie; numeración correlativa en el cuerpo y numeración independiente (`página X de Y`) en anexos; unidades en SIMELA / SI; bibliografía en normas APA (especificada como **APA 7** por la cátedra); entrega digital incluyendo código fuente, tablero de gestión y documentación.
* **Redacción (Art. 21):** Redacción impersonal, verbos en presente y en afirmativo, criterio uniforme de formato y exclusión de desarrollos teóricos o deliberaciones ajenas al proyecto.
* **Estructura obligatoria (Arts. 22 y 24):** Carátula sin numerar con datos y logo institucional; Resumen de hasta $600$ palabras ($\le 600$); Índice de Capítulos, Anexos, Tablas y Figuras; 13 capítulos con carátula propia en hoja aparte (número romano y título en mayúsculas centrados) y texto en hoja siguiente; Conclusiones; Bibliografía; Anexos I, II y III.
* **Criterios de evaluación del Tribunal (Art. 18.1):** 9 criterios oficiales (18.1.1 a 18.1.9) que van desde la pertinencia y claridad del tema hasta la presentación escrita y oral.
* **Integridad y publicación (Art. 10.1.2 y Anexo III):** Responsabilidad del estudiante por falseamiento o adulteración de información y declaración de originalidad y derechos de autor.

### 3.2. Resolución Rectoral UCP N.º 258/26 y Guía Docente – Parte II
**RR 258/26 (24/08/2026):** aprueba el régimen transitorio de Espacios Complementarios de Gestión Pedagógica Multimodal (2C2026–1C2027). Aporta al harness: la trazabilidad de la evaluación y el uso ético de la IA como finalidades (Anexo I, 1); el Aula Digital como espacio de evidencias de proceso e instancias de verificación de autoría (Anexo I, 13); y la indelegabilidad de coloquios e intervenciones orales (Art. 8 y Anexo I, 10.3). **No contiene el protocolo de IA.**

**Guía Docente – Parte II** (v.1, agosto 2026, cotejada): apartado **27.1**, prohibición general de IA generativa en todas las AE (incluidas AE1/AE2, bitácoras y reelaboraciones) salvo autorización institucional expresa; apartado **27.2**, Protocolo de Uso Autorizado para el artefacto de software (transcripto en la consigna AE4); apartados 5.2 (incidencia de AE1/AE2) y 15 (recuperatorio TIFAS).

### 3.3. Planificación 2026 y Consignas de Actividades de Evaluación (AE1 a AE4)
El análisis del Cronograma 2026 y de las consignas de AE1, AE2, AE3 y AE4 permitió alinear el *harness* tanto para la **revisión final (prioridad inmediata)** como para el **seguimiento de entregas sucesivas durante el cursado**, respetando la flexibilidad de que cada estudiante/equipo pueda acordar variaciones sobre la propuesta inicial de la cátedra.

| Instancia | Carácter y Semana | Entregables Auditables por el Harness | Regla de IA Aplicable |
| :--- | :--- | :--- | :--- |
| **AE1** | Grupal, formativa (Sem. 4) | PDF (Resumen $\le 600$ pal., Caps. I y II), Prototipo v0 (maqueta navegable + validación), Portafolio (Instrumentos 1–22 + evidencia de contacto), Bitácoras individuales, Repo y Tablero. | Admitida con declaración obligatoria en bitácora (herramienta, fragmento y verificación). |
| **AE2** | Grupal, formativa (Sem. 8) | PDF (Caps. III, IV, V y X + Catálogo de requisitos verificables), Prototipo v1 (esqueleto ejecutable vertical + CI + etiqueta `v1`), Portafolio (matriz de trazabilidad, acta de validación), Bitácoras individuales. | Admitida con declaración obligatoria en bitácora + verificación de correcciones previas de AE1. |
| **AE3** | Individual, sumativa (Sem. 12) | Examen escrito sincrónico (Moodle Quiz con preguntas *Essay*). *No aplica al producto colectivo;* el harness solo audita opcionalmente la completitud del Portafolio AE3. | **Prohibida en cualquier caso.** |
| **AE4 / Final (TIFAS)** | Producto colectivo, acreditación individual (Sem. 15) | PDF consolidado (13 capítulos, Resumen, Índice, Conclusiones, Bibliografía APA 7, Anexos), Sistema ejecutable con etiqueta congelada, manual de despliegue, evidencia de CI, Tablero, **Cap. XII individual y firmado** por integrante, Bitácoras individuales (sem. 13–15) y Portafolio AE4. | **Protocolo GD2, apartado 27.2:** Prohibida en prosa académica (capítulos, conclusiones, Cap. XII, bitácora); admitida **solo en software** para tareas mecánicas, con declaración, trazabilidad e intervención humana verificable. |

#### Reglas operativas de alto rigor extraídas de las consignas 2026
1. **Condición material bloqueante:** En AE2 y AE4, un sistema que no compila, no arranca o carece de manual de despliegue reproducible impide declarar completo el Producto Final, sin importar la calidad del documento escrito.
2. **Rúbrica analítica de 6 Dimensiones (A–F):** Escala de 4 niveles ($3, 6, 8, 10$ puntos) mapeada directamente a los 9 criterios del Art. 18.1 de la RR 97/23.
3. **Cómputo de descuentos por Ortografía y Redacción:** Hasta $1{,}00$ punto sobre $10$: $-0{,}50$ a partir del $6.^\circ$ error ortográfico y $-0{,}50$ a partir del $4.^\circ$ error de redacción (incluyendo infracciones al Art. 21).
4. **Excepción controlada al Art. 21:** El **Capítulo XII (Lecciones Aprendidas)** debe ser individual, firmado por cada integrante y redactado en **primera persona** respecto del aporte propio, con autocrítica real.
5. **Exigencias de contenido específicas:** Problema con 5 componentes y línea de base numérica; regla de las 3 preguntas en todo dato estadístico; distinción entre sector del problema y sector de recursos; requisitos con criterio de aceptación comprobable; planificación resistente a la pérdida de un integrante; matriz de decisión ponderada en Cap. IX; experimentos de escalabilidad ($10\times$ carga) con métricas accionables (no vanidosas) y umbral perseverar/pivotar en Cap. XI; anonimización de datos personales sensibles.
6. **Control de integración y no reincidencia:** En AE4 el documento debe exhibir un registro uniforme de redacción (no una yuxtaposición de entregas previas) y no repetir observaciones formales ya señaladas en AE1 y AE2.

### 3.4. Ampliación de Cátedra: Capítulo VIII (Propiedad Intelectual y Licenciamiento)
Por requerimiento expreso, el alcance original del Art. 24.3.8 de la RR 97/23 se amplió en cuatro ejes verificables con cruce directo hacia el Capítulo IX y el repositorio de código:
1. **Propiedad Industrial / Marca:** Definición de marca y activos, selección fundada de clases internacionales (Clasificación de Niza) y búsqueda de antecedentes en INPI con **fecha y constancia**.
2. **Modelo de Software y Licenciamiento de la Solución:** Modelo de explotación (propietario, SaaS, *open source*, *open core*, *dual licensing*) coherente con el Cap. IV; licencia adoptada (MIT, Apache 2.0, GPL/AGPL, EULA, etc.); encuadre de derechos de autor del software (Ley 11.723 / DNDA) y titularidad.
3. **Licenciamiento de Datasets y Modelos de IA:** Cuando el PIF entrena, ajusta o consume *datasets* o modelos de IA, debe declarar origen, licencia de cada *dataset* (CC-BY, ODbL, propietario, etc.), licencia o términos de uso de los modelos base o APIs, restricciones de uso comercial/derivado y cumplimiento de privacidad.
4. **Compatibilidad de Licencias (Cruce obligatorio):** Verificación de archivo `LICENSE` en el repositorio y consistencia legal entre la licencia de la solución (Cap. VIII), las bibliotecas de terceros declaradas (Cap. IX) y las dependencias reales del código fuente (detectando conflictos como librerías GPL en productos propietarios cerrados).

### 3.5. Apartado Especial de Cátedra: Buenas Prácticas, SDD y Harness Engineering
Dado que no forma parte del reglamento original (RR 97/23), se diseñó como un **módulo diferenciado** en el informe final para que Dirección de Carrera y Tribunal distingan exigencia reglamentaria de estándar técnico de cátedra. Evalúa cuatro dimensiones:
1. **Spec-Driven Development (SDD):** Presencia de especificaciones estructuradas (`specs/`, `.specify/`, `openspec/`, `docs/adr/`, RFCs), secuencia temporal en `git log` (specs previas o paralelas al código) y coherencia con Caps. III y IX.
2. **Harness Engineering para Agentes de Código:** Existencia y calidad de archivos de contexto (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules/`, skills), uso de *progressive disclosure* y presencia de *quality gates* reales (linters, formateadores, tests, CI/CD).
3. **Trazabilidad Humana vs. *Vibe-Coding*:** Distribución de commits por integrante y en el tiempo, detección de mega-commits tardíos, código muerto o sobre-ingeniería desconectada del documento del PIF.
4. **Higiene de Ingeniería:** `README.md` y manual de despliegue reproducibles desde máquina limpia, pruebas automatizadas ejecutables, lockfiles y ausencia de secretos o credenciales hardcodeadas.

---

## 4. Arquitectura del Sistema (`pif-review-harness/`)

### 4.1. Estructura de directorios
```text
pif-review-harness/
├── CLAUDE.md                           # Importa AGENTS.md (Claude Code lee CLAUDE.md)
├── AGENTS.md                           # Orquestador: datos no confiables, WIP=1, evidencia literal, GRIS
├── .claude/
│   ├── agents/checker.md               # Checker como subagente con contexto limpio
│   └── settings.json                   # Deniega leer input/_git y escribir en input/
├── reglamento/
│   ├── 00_fuentes.md                   # Registro de fuentes y artículos (ok / verificar) + conflictos
│   ├── 01_formato_y_redaccion.md       # Art. 20, 21, 22.1 + descuentos
│   ├── 02_estructura_capitulos.md      # Art. 22–24 + AE26 + Cap. VIII ampliado + coherencia + datos
│   ├── 03_criterios_academicos.md      # Causales de ROJO, Art. 18.1, rúbrica A–F, encuadre
│   ├── 04_etica_y_ia.md                # politica_ia por instancia, indicadores (no detección), datos, portafolio
│   ├── 05_ingenieria_sdd_harness.md    # Apartado de cátedra + repositorio oficial
│   ├── 06_verificacion_referencias.md  # Existencia, señales, estados, respaldo de afirmaciones
│   └── fuentes/                        # PDF oficiales (no versionados)
├── profiles/
│   ├── ae1_diagnostico.json · ae2_formulacion.json · ae4_final.json · reentrega.json
├── schemas/                            # finding, plan_entregas, review_state, profile
├── scripts/
│   ├── init_review.sh                  # Ingesta (bare clone + export saneado) → state.py register → run_audits.py
│   ├── run_audits.py                   # Corre la Capa 1 y escribe manifest.json
│   ├── extract_pdf.py                  # Texto por página + geometría (PyMuPDF)
│   ├── audit_pdf_format.py             # A4, márgenes, interlineado, fuentes, numeración, resumen, carátulas, 1.ª persona
│   ├── audit_coherence.py              # Carátula, figuras, anexos, requisitos, valores divergentes, encuestas (n), Cap. XII
│   ├── audit_apa_citations.py          # Citas ↔ lista, APA 7
│   ├── audit_references.py             # Crossref/OpenAlex/URL con control positivo y caché HTTP
│   ├── audit_repos.py                  # Ref congelada, LICENSE, README, despliegue, CI, dependencias, licencias, commits
│   ├── audit_sdd_harness.py            # Specs, contexto de agentes, gates, tests, secretos, inyección, datos personales
│   ├── audit_spelling.py               # LanguageTool local (opcional)
│   ├── diff_versions.py                # Comparación con la versión anterior
│   ├── sandbox_build.sh                # Construcción aislada en Docker
│   ├── verify_evidence.py              # Checker mecánico de citas literales
│   └── state.py                        # register / merge (OBS estables, reincidencia) / matriz / show
├── templates/
│   ├── informe_cumplimiento.md · devolucion_estudiantes.md · plan_entregas.ejemplo.json
├── tests/                              # PIF y repo sintéticos con errores sembrados + prueba de punta a punta
└── entregas/<proyecto_id>/             # (no versionado)
    ├── plan_entregas.json · review_state.json
    ├── input/  (_git/*.git, repo_codigo/, repo_docs/, PDF)
    ├── artifacts/  (*.json, pdf_text/, findings/, http_cache/, manifest.json)
    └── informes/
```

### 4.2. Modelo de Verificación en 3 Capas
1. **Capa 1 — Determinística (Scripts Python/Bash):** Mide con precisión matemática todo lo objetivamente verificable (geometría de página, fuentes, conteo de palabras, citas huérfanas, historial git, dependencias, existencia de `LICENSE`, secretos) y vuelca los hallazgos en `artifacts/*.json` antes de invocar al agente.
1b. **Material del estudiante = datos.** Los repos se clonan *bare* y la versión evaluada se exporta con los archivos de instrucciones para agentes (`AGENTS.md`, `CLAUDE.md`, `.cursor/`, `.claude/`) renombrados a `*.STUDENT_DATA`; el texto dirigido al evaluador se reporta como hallazgo.
2. **Capa 2 — Normativa y Estructural (Agente en modo `WIP=1`):** Recorre el perfil activo ítem por ítem cargando únicamente el módulo de `reglamento/` pertinente y respetando las variaciones registradas en `plan_entregas.json`.
3. **Capa 3 — Semántica y Auditoría (*Maker-Checker*):** Evalúa coherencia cruzada (PDF $\leftrightarrow$ código $\leftrightarrow$ documentos $\leftrightarrow$ bitácoras), valida cada hallazgo contra evidencia verificable y produce el informe final + banco de preguntas personalizadas para el coloquio individual y el tribunal.

### 4.3. Ingesta Dual de Repositorios
El script de inicialización (`init_review.sh`) fue diseñado para operar en dos modalidades a elección del evaluador:
* **Modo local:** Referencia carpetas ya descargadas (`--code-dir`, `--docs-dir`).
* **Modo remoto:** Clona repositorios desde URL (`--code-url`, `--docs-url`) con soporte para fijar `--tag` o `--commit` y verificar que la marca temporal de congelamiento sea anterior al vencimiento de la entrega.

### 4.4. Matriz de Semáforos
* **ROJO (Bloqueante, solo con fundamento en la RR 97/23):** sistema no entregado o no ejecutable según la modalidad (Arts. 3, 20, 23, 24.3.13; confirmado por el docente), partes o contenidos mínimos faltantes (Arts. 22 y 24), falseamiento o datos no verificables y uso de IA no declarado con evidencia (Art. 10.1.2 segundo inciso, 18.1.7–18.1.8, cláusula de cátedra), conflicto real de licencias, datos personales expuestos (Ley 25.326) y trabajo grupal sin distribución expresa de responsabilidades (Art. 4).
* **AMARILLO (Observación / Mejora requerida):** Desvíos formales o de profundidad corregibles (márgenes, interlineado, desvíos menores de APA 7, alertas de descuento de ortografía/redacción, subtemas incompletos, adopción parcial de SDD o *harness* de agentes).
* **VERDE (Cumple):** Validado con evidencia positiva por scripts y por la fase *Checker*.
* **GRIS (No evaluado):** el control no se pudo ejecutar o no aplica (sin red, PDF escaneado, herramienta ausente, variación acordada). Siempre con motivo: la ausencia de hallazgos no es VERDE.

Ajustes a la matriz: el uso de IA se evalúa por la cláusula de cátedra (declaración en apartado final), nunca por el estilo del texto; las exigencias de las consignas son estándar de contenido de cátedra (solo AMARILLO); las métricas de commits generan preguntas de coloquio, no semáforos; no se verifican portafolio, bitácora ni cierres de las AE.

---

## 5. Registro Cronológico del Proceso de Co-Diseño

El diseño del *harness* evolucionó de forma iterativa a través de seis hitos de decisión:

1. **Encuadre metodológico:** Se analizó el repositorio `walkinglabs/learn-harness-engineering` y se definieron los 5 subsistemas + patrón *Maker-Checker* aplicados a revisión académica, formulando las preguntas clave de relevamiento.
2. **Incorporación de la RR 97/23 y requisitos operativos:** Se analizaron las 17 páginas de la Resolución Rectoral N.º 97/23 y se definieron las entradas (PDF + repo de código + repo de documentos), el uso de APA 7, los consumidores del informe (docente, Dirección, tribunal), el artefacto con semáforos y la ejecución local en Claude Code.
3. **Definición de entregas flexibles, ingesta dual y apartado SDD/Harness:** Se incorporó el soporte para 4 entregas parciales adaptables por proyecto, la ingesta local o clonada de repositorios, las 3 reglas de la cátedra para IA Generativa (declaración, trazabilidad e intervención humana) y el apartado técnico especial de **Spec-Driven Development + Harness Engineering**.
4. **Incorporación de la RR 258/26:** Se revisaron las 28 páginas de la Resolución Rectoral N.º 258/26, extrayendo sus principios rectores de trazabilidad, evidencias de proceso, verificación de autoría e integridad académica en el Aula Digital.
5. **Integración del Cronograma 2026 y Consignas AE1–AE4:** Se analizaron los cinco documentos de cátedra 2026, incorporando al diseño el Protocolo de Uso Autorizado de IA (Guía Docente – Parte II, apartados 27.1 y 27.2), la rúbrica de 6 dimensiones (A–F), el sistema de descuentos por ortografía/redacción, la condición material de ejecutabilidad, el rol individual del Cap. XII y la preparación del coloquio individual.
6. **Ampliación del Capítulo VIII e implementación de la Fase 1:** Se sumó el apartado de modelos de software, licenciamiento de la solución, **licenciamiento de *datasets* y modelos de IA**, y cruce de compatibilidad con el Cap. IX y el repositorio. Con todas las definiciones cerradas, se redactaron los artefactos completos de la Fase 1.

---

7. **Evaluación contra la experiencia de corrección y v2 (19/11/2026):** se contrastó el diseño con el procedimiento consolidado en las correcciones reales de PIF 2026. Se incorporaron: verificación de existencia de referencias (Crossref/OpenAlex con control positivo), devolución a estudiantes con matriz y coloquio, aislamiento del material del estudiante frente a inyección de instrucciones, verificación mecánica de citas literales, Checker como subagente, estado GRIS, controles de coherencia interna y de encuestas, comparación de versiones, perfil de reentrega y registro de fuentes normativas con artículos a cotejar. Se implementó la Fase 2 completa y se probó de punta a punta con un PIF y un repositorio sintéticos.
8. **Cotejo con las fuentes 2026 (19/11/2026, v2.1):** se cotejaron la RR 258/26 y las consignas AE1–AE4 y la planificación 2026. Se corrigió la atribución del protocolo de IA (Guía Docente II, 27.1–27.2), se cargó la rúbrica A–F con su mapeo al Art. 18.1, se incorporaron las exigencias específicas de cada consigna, la regla de cierre de AE4, el registro formal de AE1/AE2, la instancia oral (VOA/IOVF) y se registraron siete inconsistencias entre documentos de cátedra (`docs/EVALUACION_Y_MEJORAS.md §5.3`).
9. **Cotejo con la RR 97/23 y la Guía Docente II (19/11/2026, v2.2):** la RR 97/23 (escaneada, por OCR) y la GD2 pasan a fuentes cotejadas. Se incorporaron el texto literal del Art. 18.1, la regla general de IA de GD2 27.1 (que alcanza a AE1, AE2, bitácoras y reelaboraciones), la IOVF unificada con grabación y revisión, el checklist de cierre por componentes y la estructura de feedback de la Ventana de Mejora; se registraron cuatro hallazgos para la cátedra (`docs/EVALUACION_Y_MEJORAS.md §6.3`).
10. **Reencuadre en la RR 97/23 (19/11/2026, v2.3):** por decisión docente, el PIF se evalúa solo contra la RR 97/23 y la cláusula de cátedra de declaración de IA; las mecánicas de las AE (cierre, notas, portafolio, bitácora, rúbrica, descuentos, IOVF) dejan de verificarse. Nuevos perfiles por avance y control automático del apartado de declaración de IA (`docs/EVALUACION_Y_MEJORAS.md §7`).
11. **Dos regímenes (19/11/2026, v2.4):** en las entregas parciales de AE se verifican el contenido, la declaración de IA y el portafolio y la bitácora según la Guía de Evaluación Multimodal (`audit_proceso.py`, `PRC-01`); en la versión final, la RR 97/23 (`docs/EVALUACION_Y_MEJORAS.md §8`).

---

## 6. Estado Actual

| Componente | Estado |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md`, `.claude/agents/checker.md`, `.claude/settings.json` | Implementado |
| `reglamento/00` a `06` | Implementado; todas las fuentes cotejadas salvo la Guía Docente – Parte I |
| `profiles/ae1_diagnostico`, `ae2_formulacion`, `ae4_final`, `reentrega` | Implementado |
| `schemas/` (hallazgo, plan, estado, perfil) | Implementado |
| `scripts/` Capa 1 (11 scripts) + `verify_evidence.py` + `state.py` | Implementado y probado (`tests/test_harness.py`) |
| `sandbox_build.sh` | Implementado; no probado con Docker activo |
| `templates/informe_cumplimiento.md`, `devolucion_estudiantes.md` | Implementado |
| Rúbrica A–F y Art. 18.1 | Dimensiones, mapeo y texto literal del 18.1 cargados; faltan los descriptores de nivel |
| Piloto con PIF reales | Pendiente |

---

## 7. Hoja de Ruta Pendiente

1. **Cotejo normativo:** completo (RR 97/23, GD2, RR 258/26, Planificación 2026 y consignas). Falta la Guía Docente – Parte I para el criterio institucional de descuentos.
2. **Rúbrica:** dimensiones A–F y mapeo al Art. 18.1 cargados; faltan los descriptores de los cuatro niveles (aula virtual).
3. **Piloto de calibración:** 2 o 3 PIF ya corregidos con su devolución como conjunto de referencia; medir por control precisión (falsos positivos) y cobertura (observaciones de la devolución humana que el harness no detectó); ajustar umbrales.
4. **Ejecutabilidad:** probar `sandbox_build.sh` con proyectos reales (Node, Python, Java) y documentar el procedimiento manual para despliegues con `docker compose`.
5. **Opcionales:** `gitleaks` y LanguageTool local; resolución de licencias de PyPI/Maven en el sandbox (`pip-licenses`, `license-checker`).
