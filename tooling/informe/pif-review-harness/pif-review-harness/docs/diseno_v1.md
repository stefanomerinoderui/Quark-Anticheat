# Proceso de Diseño y Construcción del Harness de Revisión de Proyectos Integradores Finales (PIF)

**Institución:** Universidad de la Cuenca del Plata (UCP) — Facultad de Ingeniería, Tecnología y Arquitectura  
**Carrera:** Ingeniería en Sistemas de Información  
**Asignatura:** Proyecto Final de Grado (PFG)  
**Entorno de ejecución objetivo:** Local, asistido por agentes de código (Claude Code o equivalentes)  
**Estado del proyecto:** Arquitectura cerrada y Fase 1 (núcleo normativo y orquestación) completada  

---

## 1. Resumen Ejecutivo y Propósito

El presente documento registra de manera exhaustiva el proceso de análisis, diseño e implementación inicial de un **Harness de Revisión de Proyectos Integradores Finales (PIF)** basado en los principios de **Harness Engineering** (tomando como referencia metodológica el repositorio `walkinglabs/learn-harness-engineering`).

El objetivo del sistema es reemplazar la revisión ad-hoc con modelos de lenguaje (subir un PDF a un chat y solicitar una corrección general) por un entorno de auditoría **determinístico, trazable, repetible y libre de falsos positivos** que garantice el respeto estricto al marco normativo institucional y a los estándares técnicos de la cátedra.

### Destinatarios de la salida del sistema
El artefacto final generado por el *harness* —un **Informe de Cumplimiento** con semáforos, observaciones, oportunidades de mejora, recomendaciones y guía de defensa— está diseñado para ser consumido de forma escalonada por tres actores:
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
* **Fase Checker (Auditor de Evidencia):** Audita lo producido por el Maker y descarta cualquier observación que carezca de cita normativa exacta, ubicación precisa (`PDF pág. X` o `repo_codigo/ruta:línea`) o que contradiga los reportes generados por los scripts.

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

### 3.2. Resolución Rectoral UCP N.º 258/26 (Gestión Pedagógica Multimodal)
Si bien su cuerpo principal regula el régimen transitorio de espacios complementarios y cargas horarias docentes, aporta el sustento institucional para la auditoría de trazabilidad en el *harness* (Anexo I, puntos 1 y 13):
* Consolida el **Aula Digital** y el **Sistema de Evaluación Multimodal UCP** como ámbitos para registrar **evidencias de proceso**, **trazabilidad de la evaluación** e **instancias de verificación de autoría**.
* Vincula explícitamente dichas evidencias con la **integridad académica** y el **uso ético de la Inteligencia Artificial**.

### 3.3. Planificación 2026 y Consignas de Actividades de Evaluación (AE1 a AE4)
El análisis del Cronograma 2026 y de las consignas de AE1, AE2, AE3 y AE4 permitió alinear el *harness* tanto para la **revisión final (prioridad inmediata)** como para el **seguimiento de entregas sucesivas durante el cursado**, respetando la flexibilidad de que cada estudiante/equipo pueda acordar variaciones sobre la propuesta inicial de la cátedra.

| Instancia | Carácter y Semana | Entregables Auditables por el Harness | Regla de IA Aplicable |
| :--- | :--- | :--- | :--- |
| **AE1** | Grupal, formativa (Sem. 4) | PDF (Resumen $\le 600$ pal., Caps. I y II), Prototipo v0 (maqueta navegable + validación), Portafolio (Instrumentos 1–22 + evidencia de contacto), Bitácoras individuales, Repo y Tablero. | Admitida con declaración obligatoria en bitácora (herramienta, fragmento y verificación). |
| **AE2** | Grupal, formativa (Sem. 8) | PDF (Caps. III, IV, V y X + Catálogo de requisitos verificables), Prototipo v1 (esqueleto ejecutable vertical + CI + etiqueta `v1`), Portafolio (matriz de trazabilidad, acta de validación), Bitácoras individuales. | Admitida con declaración obligatoria en bitácora + verificación de correcciones previas de AE1. |
| **AE3** | Individual, sumativa (Sem. 12) | Examen escrito sincrónico (Moodle Quiz con preguntas *Essay*). *No aplica al producto colectivo;* el harness solo audita opcionalmente la completitud del Portafolio AE3. | **Prohibida en cualquier caso.** |
| **AE4 / Final (TIFAS)** | Producto colectivo, acreditación individual (Sem. 15) | PDF consolidado (13 capítulos, Resumen, Índice, Conclusiones, Bibliografía APA 7, Anexos), Sistema ejecutable con etiqueta congelada, manual de despliegue, evidencia de CI, Tablero, **Cap. XII individual y firmado** por integrante, Bitácoras individuales (sem. 13–15) y Portafolio AE4. | **Protocolo Art. 27.2:** Prohibida en prosa académica (capítulos, conclusiones, Cap. XII, bitácora); admitida **solo en software** para tareas mecánicas, con declaración, trazabilidad e intervención humana verificable. |

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
├── AGENTS.md                           # Orquestador principal (WIP=1, Progressive Disclosure, Maker-Checker)
├── reglamento/                         # Normativa modular (se carga bajo demanda)
│   ├── 01_formato_y_redaccion.md       # RR 97/23 Arts. 20, 21 + APA 7 + Descuentos
│   ├── 02_estructura_capitulos.md      # RR 97/23 Arts. 22–24 + AE1–AE4 + Cap. VIII ampliado
│   ├── 03_criterios_academicos.md      # Rúbrica 6 Dimensiones (A–F) + Art. 18.1 + Ejecutabilidad
│   ├── 04_etica_y_ia.md                # RR 97/23 + RR 258/26 + Protocolo IA Art. 27.2 + Datos
│   └── 05_ingenieria_sdd_harness.md    # Apartado especial: SDD, Harness Engineering y buenas prácticas
├── profiles/                           # Perfiles de evaluación por instancia
│   ├── ae1_diagnostico.json            # (Fase 3)
│   ├── ae2_formulacion.json            # (Fase 3)
│   └── ae4_final.json                  # Checklist atómico completo (13 ítems)
├── scripts/                            # Capa 1: Quality Gates determinísticos (Fase 2)
│   ├── init_review.sh                  # Ingesta PDF + repos (local o git clone con tag/commit)
│   ├── audit_pdf_format.py             # A4, márgenes, Times New Roman, numeración, resumen <= 600
│   ├── audit_apa_citations.py          # Cruce citas en texto vs. Bibliografía (APA 7)
│   ├── audit_repos.py                  # Dependencias, LICENSE, tag congelado, despliegue, CI, git log
│   └── audit_sdd_harness.py            # Detección de specs, AGENTS.md/CLAUDE.md, tests y secretos
├── templates/                          # Plantillas de salida (Fase 3)
│   └── informe_cumplimiento.md         # Semáforos, rúbrica A–F, apartado SDD y preguntas de defensa
└── entregas/                           # Estado persistente por proyecto/equipo
    └── <proyecto_id>/
        ├── plan_entregas.json          # Plan acordado (hereda base cátedra o custom del equipo)
        ├── review_state.json           # Memoria longitudinal entre entregas
        ├── input/                      # PDF + repo_codigo/ + repo_docs/
        ├── artifacts/                  # Reportes JSON determinísticos
        └── informes/                   # Informes generados por instancia
```

### 4.2. Modelo de Verificación en 3 Capas
1. **Capa 1 — Determinística (Scripts Python/Bash):** Mide con precisión matemática todo lo objetivamente verificable (geometría de página, fuentes, conteo de palabras, citas huérfanas, historial git, dependencias, existencia de `LICENSE`, secretos) y vuelca los hallazgos en `artifacts/*.json` antes de invocar al agente.
2. **Capa 2 — Normativa y Estructural (Agente en modo `WIP=1`):** Recorre el perfil activo ítem por ítem cargando únicamente el módulo de `reglamento/` pertinente y respetando las variaciones registradas en `plan_entregas.json`.
3. **Capa 3 — Semántica y Auditoría (*Maker-Checker*):** Evalúa coherencia cruzada (PDF $\leftrightarrow$ código $\leftrightarrow$ documentos $\leftrightarrow$ bitácoras), valida cada hallazgo contra evidencia verificable y produce el informe final + banco de preguntas personalizadas para el coloquio individual y el tribunal.

### 4.3. Ingesta Dual de Repositorios
El script de inicialización (`init_review.sh`) fue diseñado para operar en dos modalidades a elección del evaluador:
* **Modo local:** Referencia carpetas ya descargadas (`--code-dir`, `--docs-dir`).
* **Modo remoto:** Clona repositorios desde URL (`--code-url`, `--docs-url`) con soporte para fijar `--tag` o `--commit` y verificar que la marca temporal de congelamiento sea anterior al vencimiento de la entrega.

### 4.4. Matriz de Semáforos
* **ROJO (Bloqueante):** Incumplimiento grave que impide aprobar o habilitar la defensa (sistema no ejecutable, falta de capítulos o subtemas críticos del Art. 24, conflicto legal de licencias, citas inexistentes/fabricadas, uso no autorizado o no trazado de IA, datos sensibles expuestos, ausencia de Cap. XII individual, bitácoras o portafolio).
* **AMARILLO (Observación / Mejora requerida):** Desvíos formales o de profundidad corregibles (márgenes, interlineado, desvíos menores de APA 7, alertas de descuento de ortografía/redacción, subtemas incompletos, adopción parcial de SDD o *harness* de agentes).
* **VERDE (Cumple):** Validado con evidencia positiva por scripts y por la fase *Checker*.

---

## 5. Registro Cronológico del Proceso de Co-Diseño

El diseño del *harness* evolucionó de forma iterativa a través de seis hitos de decisión:

1. **Encuadre metodológico:** Se analizó el repositorio `walkinglabs/learn-harness-engineering` y se definieron los 5 subsistemas + patrón *Maker-Checker* aplicados a revisión académica, formulando las preguntas clave de relevamiento.
2. **Incorporación de la RR 97/23 y requisitos operativos:** Se analizaron las 17 páginas de la Resolución Rectoral N.º 97/23 y se definieron las entradas (PDF + repo de código + repo de documentos), el uso de APA 7, los consumidores del informe (docente, Dirección, tribunal), el artefacto con semáforos y la ejecución local en Claude Code.
3. **Definición de entregas flexibles, ingesta dual y apartado SDD/Harness:** Se incorporó el soporte para 4 entregas parciales adaptables por proyecto, la ingesta local o clonada de repositorios, las 3 reglas de la cátedra para IA Generativa (declaración, trazabilidad e intervención humana) y el apartado técnico especial de **Spec-Driven Development + Harness Engineering**.
4. **Incorporación de la RR 258/26:** Se revisaron las 28 páginas de la Resolución Rectoral N.º 258/26, extrayendo sus principios rectores de trazabilidad, evidencias de proceso, verificación de autoría e integridad académica en el Aula Digital.
5. **Integración del Cronograma 2026 y Consignas AE1–AE4:** Se analizaron los cinco documentos de cátedra 2026, incorporando al diseño el Protocolo de Uso Autorizado de IA (Art. 27.1 y 27.2), la rúbrica de 6 dimensiones (A–F), el sistema de descuentos por ortografía/redacción, la condición material de ejecutabilidad, el rol individual del Cap. XII y la preparación del coloquio individual.
6. **Ampliación del Capítulo VIII e implementación de la Fase 1:** Se sumó el apartado de modelos de software, licenciamiento de la solución, **licenciamiento de *datasets* y modelos de IA**, y cruce de compatibilidad con el Cap. IX y el repositorio. Con todas las definiciones cerradas, se redactaron los artefactos completos de la Fase 1.

---

## 6. Estado Actual: Artefactos Generados en Fase 1

La Fase 1 dejó completamente especificados y listos para desplegar los siguientes archivos del repositorio:

1. **`AGENTS.md`:** Orquestador con las 5 reglas innegociables (*Progressive Disclosure*, `WIP=1`, verificación determinística previa, evidencia obligatoria y respeto a `plan_entregas.json`) y el protocolo *Maker-Checker*.
2. **`reglamento/01_formato_y_redaccion.md`:** Reglas de Arts. 20, 21 y 22.1–22.4, excepción de primera persona en Cap. XII, cómputo de descuentos y validación APA 7.
3. **`reglamento/02_estructura_capitulos.md`:** Modalidades del Art. 23, temario obligatorio de los 13 capítulos (Art. 24 + AE1–AE4) y Capítulo VIII ampliado (Marca/INPI, modelo de software, licencias de solución, *datasets* y modelos de IA, y cruce con Cap. IX y repositorio).
4. **`reglamento/03_criterios_academicos.md`:** Rúbrica de 6 Dimensiones (A–F) mapeada a los 9 criterios del Art. 18.1 y regla bloqueante de ejecutabilidad.
5. **`reglamento/04_etica_y_ia.md`:** Prohibición de IA en prosa académica (Art. 27.1), protocolo de uso autorizado en software (Art. 27.2), protección de datos personales y trazabilidad de proceso (RR 258/26).
6. **`reglamento/05_ingenieria_sdd_harness.md`:** Estándar técnico de cátedra para SDD, *Harness Engineering*, trazabilidad de contribución humana e higiene de ingeniería.
7. **`profiles/ae4_final.json`:** Checklist atómico de 13 ítems (`GATE-01`, `FMT-01` a `FMT-03`, `EST-01` a `EST-06`, `ETH-01`, `ACA-01`, `ENG-01`), cada uno con su referencia normativa, artefactos determinísticos asociados e indicador de carácter bloqueante.

---

## 7. Hoja de Ruta Pendiente (Fases 2 y 3)

Para completar el *harness* operativo y validarlo en producción:

### Fase 2 — Quality Gates Determinísticos (`scripts/`)
* `scripts/init_review.sh`: Bootstrap del workspace por `<proyecto_id>`, clonación o vinculación de repositorios, extracción de texto paginado del PDF y ejecución en cadena de los auditores.
* `scripts/audit_pdf_format.py`: Auditoría automática de formato físico (A4, márgenes, Times New Roman 12/10, numeración, carátulas de capítulo y conteo de palabras del Resumen) mediante `PyMuPDF` / `pdfplumber`.
* `scripts/audit_apa_citations.py`: Extracción y cruce bidireccional entre citas en el cuerpo del texto y entradas de la sección Bibliografía.
* `scripts/audit_repos.py`: Verificación de etiqueta congelada y marca temporal, presencia de manual de despliegue y archivo `LICENSE`, inventario automático de dependencias (`package.json`, `requirements.txt`, etc.), evidencia de CI y distribución de commits por autor.
* `scripts/audit_sdd_harness.py`: Detección de carpetas de specs/ADRs, archivos de configuración de agentes (`AGENTS.md`, `CLAUDE.md`, `.cursor/rules`), cobertura básica de tests y escaneo de posibles secretos/credenciales expuestos.

### Fase 3 — Plantillas, Perfiles Parciales y Piloto
* `templates/informe_cumplimiento.md`: Plantilla final con resumen ejecutivo de semáforos, matriz de cumplimiento normativo, valoración orientativa de rúbrica A–F, tabla de descuentos, seguimiento de observaciones previas, apartado diferenciado de SDD/Harness y banco de preguntas personalizadas para coloquio individual y tribunal.
* `profiles/ae1_diagnostico.json` y `profiles/ae2_formulacion.json`: Perfiles base para las entregas formativas parciales.
* Esquema estándar de `plan_entregas.json` y `review_state.json`.
* **Prueba piloto:** Ejecución sobre un PIF de ciclos anteriores (o un proyecto de muestra) para calibrar umbrales de los scripts y verificar la tasa de falsos positivos del ciclo *Maker-Checker*.