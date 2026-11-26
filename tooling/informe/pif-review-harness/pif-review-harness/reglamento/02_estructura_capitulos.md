# 02 — Estructura y contenido de capítulos

Ítems que cargan este módulo: `EST-01` a `EST-06`, `REQ-01`, `COH-01`, `DAT-01`. Cada ítem indica qué secciones (`§`) leer.

**Fundamento de las observaciones obligatorias:** RR97 Arts. 3, 4 y 20–24 (contenido mínimo). La columna "Estándar de contenido de cátedra" recoge exigencias de las consignas 2026: se observan como **AMARILLO** (profundidad o calidad), nunca como ROJO, y se citan como estándar de cátedra, no como reglamento.

## §estructura — Estructura obligatoria (RR97 22 y 24)

Orden: Carátula (sin numerar) → Resumen (≤ 600 palabras) → Índice (capítulos, anexos, tablas y figuras) → 13 capítulos → Conclusiones del Proyecto → Bibliografía (APA) → Anexos I, II y III con numeración independiente "página X de Y".

Cada capítulo comienza en **hoja aparte, con número romano y título en mayúscula, "centrados y en el centro de la hoja"**; el texto comienza en hoja aparte "sin repetir el título" (Art. 22.4). `pdf_format.json#chapter_title_pages` detecta las carátulas y si el título se repite en la hoja siguiente.

**Resumen (22.2):** ≤ 600 palabras (`pdf_format.json#abstract_words`), que "refleje el contenido del trabajo" (Art. 22.2).

**Documento único (estándar de cátedra; se apoya en Art. 21 "criterio uniforme de formato" y 18.1.8):** "El informe es un documento y no una acumulación de entregas": numeración, formato y terminología uniformes; "un informe en el que se advierten tres registros de redacción distintos no acredita integración". Los aspectos formales se verifican sobre el documento consolidado.

## §modalidad — Modalidades (RR97 23, a verificar)

23.1 Selección y Administración · 23.2 Diseño y Desarrollo (MVP en Cap. V) · 23.3 Implementación. Contrastar la declarada con `plan_entregas.json#modalidad` y con lo entregado.

## §caps — Contenido exigido por capítulo y por instancia

Columna "Estándar de contenido de cátedra": exigencias tomadas de las consignas 2026, además del contenido mínimo del Art. 24.3.

| Cap. | Título | Contenido mínimo (Art. 24.3) — obligatorio | Estándar de contenido de cátedra — AMARILLO |
| --- | --- | --- | --- |
| I | Definición del Proyecto | Origen; misión, visión y objetivos; necesidad o problema; ODS y diferenciales; descripción breve y detallada del SI | **AE1** i: problema con **cinco componentes** y **línea de base numérica**, "no con adjetivos"; de ella se deriva el **criterio de éxito**. ii: desencadenantes **jerarquizados**, cada uno con evidencia, con el principal declarado y la subordinación de los restantes |
| II | Relevamiento e Investigación de Mercado | Fuentes; instrumentos, dinámicas y alcance; datos; gráficos y variables; análisis; conclusiones | **AE1** iii: distinguir el **sector donde vive el problema** del **sector del cual provienen los recursos** ("el error más sancionado"); iv: **regla de las tres preguntas** junto a cada dato estadístico (quién lo produjo; con qué método y universo; para qué período de referencia); v: cada elemento del análisis del entorno declara su **implicancia decisoria**; vi: contacto con **persona identificada, canal concreto y motivo declarado** |
| III | Entorno y Dominio del SI | Entorno; dominio; alcance del SI y del proyecto; límites | **AE2** iii: límites por escrito (qué queda fuera y **quién validó esa frontera**); iv: cada entidad y regla de negocio remite a evidencia del relevamiento o a validación documentada. **Catálogo de requisitos** como apartado del Cap. III (ver §requisitos) |
| IV | Modelo de Negocios | Definición de negocios; visión y misión; rivalidad amplificada (competencia actual, potenciales y sustitutos, proveedores, clientes); mapeo de competencia | **AE2** v: el **lienzo** no es decorativo: de él se deriva la rivalidad amplificada y se declara su implicancia sobre el alcance; vi: el flujo de valor automatizado se justifica con evidencia de que allí se concentra el problema |
| V | Planificación | Iteraciones/sprints; entregables por etapa; **organización del equipo** (con la distribución clara y expresa de actividades y responsabilidades de cada integrante, Art. 4); cronograma; MVP (23.2) o implementación (23.1/23.3) | **AE2** vii: la planificación **resiste la pérdida de un integrante** (qué se posterga y cómo se redistribuye según el acta); viii: el MVP se describe por lo que hace: casos de uso incluidos y, expresamente, los excluidos |
| VI | Metodologías de Gestión | Técnicas de ingeniería de software; trazabilidad; gestión de la configuración; testing | **AE4** b: marco metodológico efectivamente aplicado, **definición de terminado**, ciclo de revisión y retrospectiva, gestión de la configuración y trazabilidad, **plan de pruebas y resultados obtenidos** |
| VII | Marketing | Producto/experiencia; dinámicas por perfil; publicidad, promoción y engagement; canales | **AE4** c: producto, experiencia, canales y dinámicas de intercambio por perfil de interesado |
| VIII | Propiedad Intelectual | Marca/activos; clases internacionales; búsqueda INPI | **AE4** d e iii: marca y activos; clases de Niza seleccionadas; resultado documentado de la búsqueda en INPI **con fecha y constancia**. Ampliación de cátedra: ver §cap8 |
| IX | Diseño de la Solución | Arquitectura; diseño; modelo de datos; infraestructura de comunicaciones y servidores; entornos de trabajo; solución | **AE4** e: arquitectura con su **matriz de decisión ponderada**; modelo de datos; infraestructura y entornos; **licencia, versión y motivo de elección de cada componente de terceros** |
| X | Recursos | Humanos; físicos y materiales; financieros; tecnológicos; otros | **AE2** d: con **justificación de cada asignación** |
| XI | Oportunidades | CANVAS; oportunidades para escalar o innovar | **AE4** f, iii y iv: plan de escalabilidad técnica y de negocio con **supuestos declarados** y experimentos; componente que cede primero ante **10× la carga** y medida que lo previene; tecnologías emergentes con distinción **necesidad acreditada / ornamento**; responsabilidad social y sostenibilidad. Experimento verificable: **hipótesis, métrica accionable, umbral de decisión, criterio de perseverar o pivotar**; "una métrica vanidosa (descargas, visitas, registros sin uso) no valida hipótesis alguna" |
| XII | Lecciones Aprendidas | Aspectos positivos y a mejorar | Ver §cap12 |
| XIII | Entregables | Código fuente; documentación | **AE4** h: **inventario** de código fuente y documentación, con **ubicación y etiqueta de versión de cada elemento** |

Además: Bibliografía en normas APA (Art. 20) y, en el informe final, Índice, Conclusiones y Anexos con numeración independiente.

**Capítulos esperados en revisiones de avance** (`plan_entregas.json#capitulos_esperados` puede ajustarlo): avance 1 = Resumen, I, II · avance 2 = III, IV, V, X · informe final y reentregas = los 13. En un avance no se observan los capítulos que todavía no corresponden.


## §requisitos — Catálogo de requisitos (`REQ-01`, estándar de cátedra)

Estándar de cátedra (no exigido por la RR 97/23; se observa como AMARILLO): cada requisito con **identificador, enunciado, tipo (RF/RNF), prioridad, criterio de aceptación comprobable y trazabilidad** al hallazgo de la AE1 que lo origina.
- i: "Un requisito sin criterio de aceptación comprobable no se computa, por bien redactado que esté."
- ii: distinción rigurosa RF/RNF. "El sistema debe ser rápido" no es un RNF; "el listado devuelve resultados en menos de dos segundos sobre diez mil registros", sí.
- `coherence.json#requirements` lista identificadores y huecos; `#content_markers` indica si aparecen "criterio de aceptación" y "trazabilidad" en el Cap. III.
- En el informe final, el catálogo debe seguir siendo trazable con lo construido (coherencia, Art. 18.1.6).

## §sistema — Sistema de Información entregado

Según la modalidad (Art. 23): en 23.2, componentes desarrollados y código fuente (Arts. 3, 20, 23.2, 24.3.13); en 23.1 y 23.3, evidencia de la selección o de la puesta en producción y su parametrización (Art. 23.1, 23.3, 24.3.5). Estándar de cátedra: repositorio con etiqueta de la versión entregada, README y manual de despliegue reproducible por un tercero, integración continua (ver `05 §repo`).

## §cap8 — Capítulo VIII ampliado (requerimiento de cátedra)

1. **Marca:** marca y activos; clases de Niza **con fundamento**; búsqueda INPI con **fecha y constancia** (AE26-4).
2. **Modelo de software y licencia de la solución:** modelo de explotación coherente con el Cap. IV; licencia adoptada; derechos de autor del software (Ley 11.723, DNDA) y titularidad.
3. **Datasets y modelos de IA** (si se usan): origen y licencia de cada dataset; términos de modelos y APIs; restricciones; privacidad.
4. **Compatibilidad:** `repos.json#license` ↔ Cap. VIII ↔ componentes de terceros declarados en el Cap. IX (licencia, versión, motivo: AE26-4 e) ↔ `repos.json#dependencies`. Conflicto real: ROJO. Licencia desconocida: GRIS.

## §cap12 — Capítulo XII (Art. 24.3.12) y aporte de cada integrante (Art. 4)

- Obligatorio (RR97): "Aspectos positivos del proyecto" y "Aspectos a mejorar para el proyecto". Lecciones del proceso, no un roadmap de funcionalidades.
- Obligatorio (RR97 Art. 4): en trabajos grupales, distribución "clara y expresa" de las actividades y responsabilidades de cada integrante (en el Cap. V y donde corresponda). Su ausencia es ROJO.
- Estándar de cátedra (AMARILLO): sección individual por integrante, firmada, en primera persona sobre el aporte propio, con autocrítica real ("un capítulo que sólo enumera aciertos no acredita el aprendizaje"). Señales a registrar: similitud alta entre integrantes (`coherence.json#cap12_similarity`), ausencia de firma, ausencia de aspectos a mejorar.

## §coherencia — Coherencia interna (RR97 18.1.6, Dimensión D)

Candidatos de `coherence.json`:
- La cadena problema → dominio → requisitos → planificación → arquitectura → construcción → explotación, y su relación con las conclusiones (Art. 18.1.6): ¿la línea de base del Cap. I reaparece en los criterios de éxito y en los experimentos del Cap. XI? ¿el MVP del Cap. V coincide con lo construido y con el inventario del Cap. XIII?
- Un mismo valor técnico con distintos valores en distintos capítulos (`#key_values`).
- Arquitectura descripta distinto en Caps. V, IX y XIII.
- Numeración y trazabilidad de RF/RNF/HU (`#requirements`).
- Figuras y tablas citadas que no existen o numeración salteada (`#figures_tables`); "uniformidad de tablas y figuras" (AE26-4 viii).
- Anexos mencionados que no existen (`#annex_refs`).
- Metodología del Cap. V distinta de la del Cap. VI.
- Enlaces al repositorio distintos entre capítulos (`#repo_links`).
- Términos mal usados (`#tech_terms`): "RAG" sin generación, "pretotipo" por prototipo; tecnología emergente como "ornamento" sin necesidad acreditada (AE26-4).
- Marcadores de contenido ausentes por capítulo (`#content_markers`): indicio, no prueba; confirmar leyendo el capítulo.

## §datos — Datos relevados (Cap. II y Anexo I)

- **Encuestas:** ¿se declara *n*? Si no, `coherence.json#survey_n` infiere el *n* mínimo compatible con los porcentajes. "Muestra representativa" sin diseño muestral es AMARILLO.
- **Regla de las tres preguntas** junto a cada dato estadístico (estándar de cátedra). Fundamento reglamentario: fuentes consultadas (18.1.7) e información "fehaciente" (18.1.8).
- Distinción entre demanda imaginada, declarada y revelada (PLAN26, sem. 2).
- **Anonimización** o consentimiento documentado; datos sensibles fuera del repositorio y de los anexos (Ley 25.326). Expuestos: ROJO. `sdd_harness.json#pii_pdf` lista candidatos.
- Contactos, entrevistas o validaciones sin constancia (persona, canal, motivo, fecha): AMARILLO con pedido de constancia. Si hay evidencia de que no se realizaron: ROJO (Art. 10.1.2, segundo inciso).
