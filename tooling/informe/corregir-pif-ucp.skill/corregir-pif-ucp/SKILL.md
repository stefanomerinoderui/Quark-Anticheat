---
name: "corregir-pif-ucp"
description: "Corregir un Proyecto Integrador Final (PIF) de Ing. en Sistemas UCP contra la RR 97/23, verificar sus citas y producir la devolución formal con observaciones, evidencia, matriz y coloquio previo."
---

# Corrección de PIF – Ingeniería en Sistemas de Información (UCP)

Skill para corregir cualquier Proyecto Integrador Final (PIF) presentado en la asignatura Proyecto Final de Grado, contra el Reglamento General del PIF (Resolución Rectoral 97/2023, en adelante RR 97/23), y producir una devolución formal para los estudiantes.

El docente responsable es Sergio Lapertosa. La cuenta de cátedra para acceso a repositorios es **lapertosasergio_cen@ucp.edu.ar**.

## Entradas

- Uno o más PDF del PIF (si hay varias versiones, se comparan).
- La RR 97/23 (si no se adjunta, usar el resumen de la sección "Lista de control – RR 97/23").
- Opcional: devoluciones anteriores, programa de la asignatura del ciclo vigente.

No inventar datos que no estén en los documentos. Si un dato no se puede verificar, decirlo.

## Flujo de trabajo

1. **Leer y extraer texto.**
   - `pdftotext -layout` y `pdftotext` (sin layout) para cada PIF; `pdfinfo` para páginas y metadatos (el productor, por ejemplo la versión del renderizador, ayuda a ordenar versiones).
   - Si la RR 97/23 está escaneada: `pdftoppm -r 200 -gray` + `tesseract -l spa`. Verificar visualmente la numeración de incisos antes de citarlos (el OCR puede desalinear números y textos).
2. **Identificar versiones** (si hay más de una): determinar cuál es la posterior por contenido (correcciones, secciones nuevas), no por el nombre del archivo. Diff de líneas normalizadas con `difflib.SequenceMatcher` (quitar números de página sueltos y espacios). Resumir qué mejoró y qué contradicciones introdujo la revisión.
3. **Verificar cumplimiento de la RR 97/23** con la lista de control, sobre la versión más reciente.
4. **Verificar formato** (Art. 20):
   - Fuentes: `pdffonts` (debe predominar Times New Roman).
   - Márgenes: `pdftotext -bbox` sobre varias páginas de cuerpo; en A4 (596×842 pt), 3 cm ≈ 85 pt y 2,5 cm ≈ 71 pt. El margen inferior incluye el pie, no usarlo como evidencia.
   - Interlineado y carátulas de capítulo: renderizar páginas con `pdftoppm -r 50` y mirarlas.
5. **Buscar inconsistencias internas** (Art. 18.1.6 evalúa la coherencia): valores técnicos repetidos con distinto valor (umbrales, dimensiones, versiones), arquitectura descripta distinto en distintos capítulos, numeración de RF/HU y su trazabilidad, numeración de figuras, metodología declarada en Cap. V vs. Cap. VI, clases de Niza, enlaces al repositorio, anexos mencionados que no existen.
6. **Verificar datos**:
   - Encuesta: ¿se declara n? Inferir n de los porcentajes (p. ej., 28,6 % = 10/35) y señalar si "representativa" no está sustentado.
   - Términos técnicos mal usados (p. ej., "RAG" sin paso de generación, "pretotipo" para un prototipo).
7. **Verificar las citas bibliográficas** con la sección "Verificación de citas bibliográficas" completa.
8. **Redactar la devolución** como documento (tipo Docs) con la estructura de la sección "Estructura de la devolución".
9. **Revisar** antes de entregar: cada artículo citado coincide con el texto de la RR; cada observación tiene evidencia exigida; numeración OBS correlativa y coincidente con la matriz; no se exigen portafolio ni bitácora; cada referencia marcada como "No localizada", "Con discrepancias" o "Fabricada" tiene registradas las búsquedas y la evidencia.

## Verificación de citas bibliográficas

Fundamento: el tribunal evalúa las fuentes consultadas (Art. 18.1.7), la bibliografía debe seguir APA (Art. 20) y los estudiantes responden por el falseamiento de información (Art. 10.1.2). Una referencia inexistente es una falta grave, no un detalle de formato.

### 1. Extraer y estructurar

- Ubicar la sección Bibliografía en el texto extraído y separar cada entrada (una entrada empieza en un apellido o entidad seguido del año entre paréntesis: `(2020)`, `(s.f.)`, `(n.d.)`).
- Registrar cada entrada en una tabla de trabajo (CSV): autores, año, título, fuente (revista, editorial, sitio), edición, DOI, URL, ISBN si figura.
- Extraer las citas del cuerpo con dos patrones: `(Apellido, año)` / `(Apellido y Apellido, año)` / `(Apellido et al., año)` y `Apellido (año)`. Normalizar acentos y mayúsculas para comparar (Čermák = Cermak).

### 2. Cruce citas ↔ referencias

Informar por separado:
- Citas en el texto sin entrada en la bibliografía.
- Entradas en la bibliografía nunca citadas en el texto.
- Mismo autor con años distintos entre texto y lista (p. ej., Sommerville 2011 en el texto y 2016 en la lista).
- Autor citado en el texto con un nombre que no figura en la lista (p. ej., "Meta Open Source" citado y "Meta Platforms" en la lista).
- Diferencias de grafia en apellidos o en la cantidad de autores.
- Entradas duplicadas (misma obra en dos idiomas o ediciones).

### 3. Verificar la existencia de cada fuente

Verificar todas las referencias si son 40 o menos. Si son más: todas las académicas (artículos, libros, tesis, ponencias) y las web que sostienen datos, porcentajes o decisiones centrales del proyecto.

**Herramientas, en este orden de preferencia.** Revisar qué herramientas tiene la sesión (cargando con ToolSearch las diferidas) antes de empezar.

1. **Nimble (o un MCP equivalente de extracción web), si está disponible.** Es la opción preferida porque puede abrir cualquier URL, incluidas las API bibliográficas.
   - **Lote completo:** iniciar **una sola** ejecución del Web Search Agent (`nimble_agents_run`, `use_case: enrichment`, `effort: medium`) con las referencias como `input_data` (hasta 40 filas por ejecución) y un `output_schema` con: `existe` (Sí / No / Desconocido), `autores_reales`, `anio_real`, `titulo_real`, `fuente_real`, `edicion_real`, `doi_o_url_verificada`, `discrepancias`. En la `skill` del agente indicar: buscar primero en la fuente primaria (Crossref, OpenAlex, sitio de la revista o conferencia, catálogo de la editorial) y escribir "Desconocido" en lugar de adivinar. Consultar el resultado con `nimble_agents_run_status` hasta que termine. Si hay más de 40 referencias, priorizar las académicas y las que sostienen datos.
   - **Comprobación puntual de DOI** (para las referencias sospechosas que marque el agente, o si no se usa el agente): `nimble_extract` con `url = https://api.crossref.org/works/<DOI>`, `driver: vx6`, `output_format: plain_text`. Una respuesta JSON con `"status":"ok"` trae autores, año, revista y páginas; la respuesta `Resource not found.` significa que **el DOI no está registrado**. Antes de concluir sobre DOI no registrados, hacer un **control** con un DOI conocido de la misma lista: si el control devuelve metadatos, la respuesta negativa es confiable.
   - **Sin DOI:** `nimble_extract` sobre `https://api.crossref.org/works?query.bibliographic=<título+autor>&rows=3` o `https://api.openalex.org/works?search=<título>`.
   - **Páginas web citadas:** `nimble_extract` sobre la URL de la entrada para comprobar que existe y qué dice (con `driver: vx8` si la página necesita JavaScript).
2. **Sin Nimble: WebSearch + WebFetch.** WebFetch solo abre URL que hayan aparecido en resultados de búsqueda o que el usuario haya pasado; no abre directamente `api.crossref.org` ni `doi.org`. Por eso: buscar primero (título + autores, o el DOI entre comillas) y abrir con WebFetch solo los resultados. Un DOI que no aparece en ninguna búsqueda queda como indicio, no como prueba.
3. **Sin herramientas web:** marcar todas las referencias como "No verificadas" y exigir en la devolución DOI o URL completa para cada una.

Qué buscar según el tipo de fuente:
- **Artículos y ponencias:** autores, año, revista o conferencia, volumen y páginas contra Crossref, OpenAlex o el sitio de la revista o conferencia (p. ej., CVF Open Access para WACV/CVPR, AIS eLibrary para revistas de AIS).
- **Libros:** título, autor, edición, idioma y año en la editorial o en catálogos de bibliotecas (WorldCat, catálogos universitarios). Verificar que la edición exista en el idioma citado.
- **Sitios web, documentación y notas periodísticas:** que la página exista, que la fecha y la URL coincidan y que trate lo que se le atribuye. Los acortadores (tinyurl, bit.ly) se resuelven y se pide la URL completa.
- **Software:** autor real del proyecto (no el usuario de GitHub) o autor corporativo.
- **Normativa** (leyes, resoluciones): número y año en el boletín oficial o el sitio del organismo.

No usar la memoria del modelo como evidencia de que una fuente existe o no existe: solo cuenta lo que devuelve una búsqueda o consulta real. Registrar para cada referencia observada la herramienta y la consulta usadas.

### 4. Señales de referencia fabricada (típicas de texto generado por IA)

- Lista de autores que no coincide con la de la obra real, o que mezcla nombres de áreas no relacionadas.
- Nombres que no parecen personas (p. ej., "Enthusiast, A. C.").
- URL o título que corresponden a una obra de otros autores.
- DOI no registrado en Crossref (`Resource not found.`, con control positivo) o que resuelve a otra obra.
- Título real con autores, año o revista cambiados.
- Páginas, volumen o edición inexistentes para esa revista o libro.
- URL plausible que devuelve 404 o una página sin relación.

### 5. Verificar que la fuente respalde lo afirmado

Para las afirmaciones con datos duros (porcentajes, métricas de precisión de modelos, cifras de mercado, estadísticas del dominio), abrir la fuente citada y comprobar que diga eso. Revisar al menos 5 afirmaciones, o todas si son menos. Registrar: afirmación, página del PIF, fuente citada y si la respalda (Sí / Sí, con reservas / Parcialmente / No / No verificable). Señalar cuando la fuente es una declaración de una empresa y no un dato estadístico.

### 6. Clasificar cada referencia

| Estado | Criterio |
| --- | --- |
| Verificada | Existe y autores, año, título y fuente coinciden. |
| Con discrepancias | Existe, pero difiere en autores, año, edición, título o URL. Indicar la diferencia y el dato correcto. |
| No localizada | No se encontró tras las búsquedas del punto 3. Registrar las búsquedas hechas y, si corresponde, que el DOI no está registrado. |
| Fabricada / Autoría inventada | Hay evidencia concreta de que la entrada combina datos falsos (p. ej., URL o DOI de otra obra, autores que la obra real no tiene). |

Redacción prudente: "No localizada" no es una acusación. "Fabricada" se usa solo con evidencia concreta, y se describe la evidencia, no la intención.

### 7. Formato APA 7

Controlar y listar: fechas de recuperación mal formadas (p. ej., "Recuperado Noviembre 23 2025 de"; en APA 7 solo para contenidos que cambian, con la forma "Recuperado el 23 de noviembre de 2025, de"), mezcla de s.f. y n.d., uso de "y" vs. "&" en referencias en español, URL acortadas, cursivas, orden alfabético, DOI en formato `https://doi.org/...`, iniciales de autores (cotejar con los metadatos de Crossref cuando estén disponibles).

### 8. Volcado a la devolución

- Una observación en "Formato, redacción y bibliografía" para el formato APA (evidencia: cada referencia con DOI o URL completa y accesible).
- Si hay referencias "Con discrepancias", "No localizada" o "Fabricada", o afirmaciones no respaldadas: una observación **obligatoria** propia (Art. 10.1.2, 18.1.7 y 20). Evidencia exigida: para cada referencia observada, la fuente real (DOI, URL o datos de la edición consultada), o su eliminación y la reescritura del párrafo que se apoyaba en ella.
- Una sección **"Verificación de referencias"** (ver la estructura de la devolución), con: fecha y método de verificación; tabla `N.º | Referencia (autor, año) | Estado | Discrepancia o búsqueda realizada | Acción requerida`, ordenada con las fabricadas y no localizadas primero; tabla de afirmaciones verificadas; cruce citas ↔ lista (no citadas y duplicadas). Las referencias verificadas sin observaciones se nombran en una línea, y las no revisadas se remiten a la observación de formato APA.
- En la matriz de respuesta, una fila para la observación de referencias.
- En el coloquio previo, los estudiantes deben poder mostrar la fuente original de cada referencia observada.

## Lista de control – RR 97/23

**Carátula (22.1):** logo y nombre de la UCP, Facultad (verificar denominación vigente), carrera exacta "Ingeniería en Sistemas de Información", denominación "Proyecto Integrador Final", título, autores, año de presentación. Sin numerar.

**Resumen (22.2):** máximo 600 palabras; debe reflejar el trabajo completo (problema, relevamiento, modalidad, solución, resultados, conclusiones).

**Índice (22.3):** capítulos, anexos, tablas y figuras.

**Capítulos (22.4):** cada uno en hoja aparte, número romano y título en mayúscula, centrados; el texto empieza en la hoja siguiente sin repetir el título. Títulos y contenidos mínimos (Art. 24.3):

| Cap. | Título | Contenidos mínimos |
| --- | --- | --- |
| I | Definición del Proyecto | Origen; Misión, Visión y Objetivos; Necesidad o problema; ODS y diferenciales; descripción breve y detallada del SI |
| II | Relevamiento e Investigación de Mercado | Fuentes; instrumentos, dinámicas y alcance; datos; gráficos y variables; análisis; conclusiones |
| III | Entorno y Dominio del SI | Entorno; dominio; alcance (del SI y del proyecto); límites |
| IV | Modelo de Negocios del Proyecto | Definición de negocio; visión y misión; **análisis de rivalidad amplificada** (competencia actual, potenciales, sustitutos, proveedores, clientes); mapeo de competencia |
| V | Planificación del Proyecto | Iteraciones/sprints/etapas; entregables por etapa; organización del equipo; cronograma; MVP (23.2) o implementación (23.1/23.3) |
| VI | Metodologías de Gestión | Técnicas de ingeniería de software; trazabilidad; **gestión de la configuración**; testing |
| VII | Marketing del Proyecto | Producto/experiencia; dinámicas por perfil; publicidad, promoción y engagement; canales |
| VIII | Propiedad Intelectual | Marca/activos; clases internacionales; resultados de búsqueda INPI |
| IX | Diseño de la Solución | Arquitectura; diseño; modelo de datos; **infraestructura de comunicaciones y servidores**; **entornos de trabajo**; solución |
| X | Recursos del Proyecto | Humanos; físicos y materiales; **financieros (con cifras)**; tecnológicos; otros |
| XI | Oportunidades del Proyecto | CANVAS; oportunidades para escalar o innovar |
| XII | Lecciones Aprendidas | Aspectos positivos; aspectos a mejorar (del proceso, no un roadmap de funcionalidades) |
| XIII | Entregables | Código fuente; documentación |

**Conclusiones del Proyecto (22.5/24.4):** obligatorias; verificar que existan.

**Bibliografía (22.6/24.5):** APA; verificar con la sección "Verificación de citas bibliográficas".

**Anexos (22.7/24.6):** Anexo I Datos relevados; Anexo II Documentos del entorno o dominio; Anexo III Otros. Paginación independiente "página X de Y" (Art. 20).

**Modalidad (Art. 23):** debe declararse (23.1 Selección y Administración, 23.2 Diseño y Desarrollo, 23.3 Implementación).

**Formato (Art. 20):** A4; márgenes sup. 2,5 / inf. 2,5 / izq. 3 / der. 3 cm; interlineado 2 líneas; Times New Roman 12 (notas 10); páginas correlativas salvo anexos; unidades SIMELA; bibliografía APA. Entrega digital con código fuente, tablero de gestión y demás datos digitales.

**Redacción (Art. 21):** impersonal; verbos en presente y en afirmativo; formato uniforme; sin desarrollos teóricos ajenos al tema.

**Trabajo grupal (Art. 4):** distribución clara y expresa de actividades y responsabilidades de cada integrante.

## Estructura de la devolución

Documento formal, en español rioplatense ("ustedes"), tono profesional y directo. Secciones, en este orden:

1. **Encabezado:** frase inicial con el veredicto (si está o no en condiciones de ir a tribunal) + tabla: asignatura, título del proyecto, estudiantes, versión evaluada, marco normativo, modalidad que corresponde.
2. **Encuadre normativo:** por qué el PIF requiere la aprobación previa del equipo docente para ir a tribunal (ver "Fundamentación normativa").
3. **Valoración general:** fortalezas reales y avances respecto de la versión anterior, con ejemplos concretos.
4. **Observaciones obligatorias (RR 97/23):** tabla `N.º | Artículo | Observación | Qué se espera | Evidencia a presentar`. Numeración OBS-01, OBS-02… Incluye la observación de referencias no verificadas cuando corresponda.
5. **Inconsistencias internas:** lista numerada a continuación (OBS-xx), cada una con una sublínea "Evidencia:".
6. **Formato, redacción y bibliografía:** misma forma, cada una con "Evidencia:".
7. **Verificación de referencias:** ver "Verificación de citas bibliográficas", punto 8.
8. **Matriz de respuesta a observaciones:** pautas + tabla `N.º | Observación | Cambio realizado | Ubicación | Evidencia presentada | Responsable | Uso de IA`, con una fila por OBS y el resto vacío para los estudiantes. Sin la matriz completa la reentrega no se evalúa.
9. **Uso de IA generativa e integridad académica** (ver sección propia).
10. **Acceso y visibilidad del repositorio de código** (ver sección propia).
11. **Coloquio previo a la aceptación del PIF** (ver sección propia).
12. **Preguntas para preparar el coloquio y la defensa:** 5 a 8 preguntas técnicas y de negocio específicas del proyecto (validación de modelos, escalabilidad, seguridad y datos personales —Ley 25.326—, costos vs. ingresos, aporte de cada integrante).
13. **Próximos pasos y lista de control:** checklist con los rangos OBS, la matriz, la declaración de IA, el acceso al repositorio y la fecha del coloquio. Mencionar Art. 14 (copia a Dirección de Carrera 5 días hábiles antes de la defensa) y Art. 19 (ejemplar digital y Formulario N.º 2).

**Reglas para las observaciones:**
- Cada observación indica qué se espera y **qué evidencia debe quedar plasmada en la nueva versión** (página corregida, captura, anexo, enlace, commit, tabla con fuentes).
- **No exigir portafolio ni bitácora.** La evidencia vive en el informe y en la matriz.
- Siempre incluir una observación sobre el **repositorio y la estructura del código** (Art. 20 y 24.3.13): enlace correcto, acceso de la cátedra, árbol de directorios, módulos, dependencias, instrucciones de ejecución en el Cap. XIII, etiqueta de la versión entregada, commits de todos los integrantes.
- Citar artículos solo después de verificar su numeración.

## Fundamentación normativa (para el encuadre)

- **Art. 11:** la aprobación del PIF está a cargo de los docentes de la asignatura y es la que habilita la defensa oral ante el tribunal.
- **Art. 12:** para la defensa se requiere regularidad en Proyecto Final de Grado y las demás asignaturas aprobadas.
- **Art. 18.2:** "dado que el estudiante aprobó la primera instancia", el tribunal califica entre 6 y 10: no puede desaprobar, por lo que el control de calidad es previo y docente.
- **Art. 8.2.6:** el equipo docente recepciona y evalúa el informe final en no más de 20 días e informa el resultado para su presentación final.
- **Art. 8.1 y 8.2.1–8.2.5:** seguimiento efectivo "en tiempo y forma" (8.1); control de requisitos formales y académicos (8.2.1); retroalimentaciones e indicación de modificaciones (8.2.2); dirección en todas las etapas (8.2.3); evaluación del proceso y de la participación de cada estudiante en trabajos grupales (8.2.4); supervisión de datos, análisis y resultados (8.2.5).
- **Art. 3, 20, 21, 22 y 24:** trabajo completo, aspectos formales, redacción y estructura obligatoria.
- **Art. 10:** coordinar con el profesor (10.1.1), entregar avances (10.1.2) y responder por falseamiento o adulteración de información (segundo inciso numerado 10.1.2 en el original).
- **Art. 18.1.7:** el tribunal evalúa las fuentes de información consultadas.
- **Art. 7 y 14:** la Dirección de Carrera coordina para asegurar la calidad esperada y envía el PIF al tribunal.

Cerrar con un párrafo de aplicación al caso: la devolución y el coloquio previo son los instrumentos de los Art. 8.2.2, 8.2.4 y 8.2.6, y su resultado es la aprobación del Art. 11.

## Uso de IA generativa

Base: Sistema de Evaluación Multimodal UCP (proceso y producto; dimensiones saber, saber hacer, saber ser, que incluye declarar autoría y herramientas auxiliares) y pautas éticas del programa de PFG (asistentes de texto y código admitidos con declaración; el estudiante responde por todo lo que firma).

Tabla de prácticas:
- Revisar redacción, ortografía o depurar código: admitido, declarado en la columna "Uso de IA" de la matriz.
- Interpretar observaciones o explorar alternativas: admitido con declaración; la decisión se describe con palabras propias.
- Generar datos, cifras, resultados de pruebas, citas o referencias: no admitido (falseamiento, Art. 10.1.2).
- Completar la matriz con texto generado: no admitido.
- Presentar contenido ajeno o generado sin declarar: excluido; impide validar el coloquio.

La declaración se hace en la matriz (herramienta, fragmento, verificación posterior) y en el informe, reemplazando cualquier descargo genérico por uno específico.

Antes de entregar, señalar al docente si la Guía Docente vigente para la AE en curso es más restrictiva que el programa de PFG.

## Acceso y visibilidad del repositorio

- Acceso para **lapertosasergio_cen@ucp.edu.ar** antes de la reentrega.
- Repositorio público: sin invitación; verificar que la URL abra sin iniciar sesión.
- Privado en cuenta personal: invitar como colaborador (Settings → Collaborators → Add people). En cuentas personales GitHub da lectura y escritura; la cátedra se compromete a usarlo solo para consulta.
- Privado en organización: invitar con rol Read.
- Condiciones: repositorio único y oficial coincidente con el Cap. XIII; etiqueta de la versión entregada; historial completo sin force push ni squash de lo publicado; autoría de commits identificable; README con estructura y ejecución; sin credenciales ni datos personales (`.env` en `.gitignore`; claves expuestas deben rotarse); acceso vigente hasta la defensa.
- Evidencia: URL y etiqueta; captura de colaboradores o de la visibilidad pública; captura del historial con aportes de todos los integrantes.

## Coloquio previo a la aceptación

- Fundamento: Art. 8.2.4, 11 y 8.2.6.
- Individual, duración orientativa 15 minutos por integrante, después de la reentrega con la matriz completa; fecha a acordar.
- Contenido: dar cuenta (recorrer la matriz y mostrar la evidencia elegida por el docente), fundamentar decisiones y alternativas descartadas, demostrar (navegar el código en el repositorio y mostrar la aplicación funcionando), explicar fragmentos asistidos por IA y mostrar la fuente original de las referencias observadas.
- Resultado Validado / No validado por integrante. Validado: se acepta el PIF y se habilita la inscripción a la defensa (Art. 12 y 13). No validado: la cátedra indica qué reforzar y fija nueva fecha. No reemplaza la defensa ante el tribunal.

## Al terminar

Entregar el documento con una línea de resumen al docente: veredicto, cantidad de observaciones, cantidad de referencias verificadas / con discrepancias / no localizadas / fabricadas, herramienta usada para verificar (Nimble, WebSearch o ninguna) y las 2 o 3 observaciones más graves. No repetir el contenido del documento en el chat.