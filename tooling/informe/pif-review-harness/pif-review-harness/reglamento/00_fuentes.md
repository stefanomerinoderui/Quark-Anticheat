# 00 — Registro de fuentes normativas

Solo se pueden citar artículos o apartados que figuren en este registro. Estado:
- **ok**: cotejado contra el texto original (se indica página o sección).
- **corroborado**: confirmado por otra fuente oficial que lo cita, sin el original a la vista.
- **verificar**: no cotejado; citar con "(numeración a verificar)".

Originales en `reglamento/fuentes/` (no versionados). Texto extraído en `reglamento/fuentes/texto/` (DNI omitidos; la RR 97/23 es OCR de un escaneo). Cotejo completo: 19/11/2026.

## Alcance de la verificación (decisión de cátedra, 19/11/2026)

El harness trabaja con **dos regímenes**, según la instancia de `plan_entregas.json`:

| Régimen | Instancias | Qué se verifica | Qué no se verifica |
| --- | --- | --- | --- |
| **Entregas parciales del PIF en las AE** | AE1, AE2, AE4 (perfiles `ae1_entrega_parcial`, `ae2_entrega_parcial`, `ae4_entrega_integral`) | Contenido entregado del PIF (RR 97/23 + estándar de contenido de cátedra); **declaración de uso de IA** (cláusula CAT-IA); **Portafolio Digital y Bitácora Individual según la Guía de Evaluación Multimodal** (GD2 7, 8.1, 8.2 y el contenido que pide cada consigna) | Nota, cierre de la AE, regularidad, recuperatorios: los registra el docente |
| **Versión final del PIF** | FINAL, REENTREGA (perfiles `pif_final`, `reentrega`) | **RR 97/23** con las consideraciones elaboradas (estándar de cátedra como AMARILLO, cláusula CAT-IA) | Portafolio, bitácora y toda mecánica de las AE |

Reglas comunes:
- Las observaciones obligatorias y los ROJO de contenido se fundan en la RR 97/23 (o Ley 25.326). En las AE, la ausencia o insuficiencia de portafolio o bitácora se funda en GD2 7–8 (componente de cierre).
- Las exigencias de contenido de las consignas 2026 son **estándar de contenido de cátedra**: solo AMARILLO.
- IA: cláusula CAT-IA en todas las entregas, con el Art. 10.1.2 (segundo inciso) y el 18.1.7–18.1.8 de la RR 97/23.

## CAT-IA — Cláusula de cátedra: Declaración de uso de inteligencia artificial (texto del docente)

> Si utilizó herramientas de IA generativa, debe declararlo en un apartado final indicando para qué se usó y cómo se verificó la información obtenida. Se deben indicar los prompts utilizados y compartir el enlace a la conversación con la herramienta de IA Generativa seleccionada. El uso no declarado, o la incorporación de datos no verificables, se registra con las observaciones correspondientes a los reglamentos. Tenga presente que en todas las producciones entregadas se le podrá pedir que dé cuenta oralmente.

Elementos verificables: (1) apartado final de declaración; (2) para qué se usó; (3) cómo se verificó la información; (4) prompts utilizados; (5) enlace a la conversación. Consecuencias: uso no declarado o datos no verificables → observación fundada en la RR 97/23 (Art. 10.1.2 segundo inciso; 18.1.7; 18.1.8 "información completa y fehaciente"); posibilidad de pedir que se dé cuenta oralmente (Art. 8.2.4 y 11).

## Fuentes

| Código | Documento | Versión / fecha | Archivo | Estado |
| --- | --- | --- | --- | --- |
| RR97 | Resolución Rectoral UCP N.º 97/23 — Reglamento General del PIF (Anexo I) y Formularios N.º 1 y N.º 2 (Anexos II y III) | 11/05/2023 | `RR_97_23.pdf` (escaneado, 17 págs.) | ok |
| GD2 | Guía Docente — Parte II: Sistema de Evaluación Multimodal UCP (v.1, versión de trabajo institucional) | Agosto 2026 | `Guia_Docente_Parte_II_v1_2026.pdf` | ok |
| GD1 | Guía Docente — Parte I (v.2) | 2026 | *no disponible* | corroborado (citada por GD2 y AE26) |
| RR258 | Resolución Rectoral UCP N.º 258/26 — Régimen transitorio de Espacios Complementarios de Gestión Pedagógica Multimodal | 24/08/2026 | `RR_258_26.pdf` | ok |
| PLAN26 | Planificación de Actividades PFG 2026 (cronograma) | 2026 | `Cronograma_PFG_2026.docx` | ok |
| AE26-1 a AE26-4 | Consignas AE1, AE2, AE3 y AE4 2026 | 2.º cuatrimestre 2026 | `Consigna_AE[1-4]_2026.docx` | ok |
| CAT | Estándar técnico de cátedra (SDD, harness, higiene) — no reglamentario | 2026 | este repo, módulo 05 | n/a |
| CAT-IA | Cláusula de cátedra de declaración de uso de IA | 2026 | este archivo | ok (texto del docente) |

## RR97 — Reglamento General del PIF (cotejado; "p." = página del PDF)

| Art. | Contenido (literal o casi literal) | p. |
| --- | --- | --- |
| Res. Art. 2 | Aprueba el **Anexo II — Formulario N.º 1** (Registro de Orientación Disciplinar) y el **Anexo III — Formulario N.º 2** (Autorización para Publicación del PIF) | 1 |
| 1–2 | Objetivo; el PIF puede tratar selección, diseño, desarrollo, administración o implementación de un SI "considerando el marco de gestión de proyectos y su puesta en valor desde la mirada de negocios" | 2 |
| 3 | "Debe ser un trabajo completo" | 2 |
| 4 | El proyecto "podrá ser compartido por varios estudiantes, distribuyéndose en forma clara y expresa las actividades y responsabilidades de cada uno" | 2 |
| 5–7 | Cátedra PFG orienta; Dirección de Carrera coordina y garantiza "la calidad esperada" | 3 |
| 8.1 | Seguimiento efectivo para la culminación "en tiempo y forma"; evaluación conforme la normativa vigente | 3 |
| 8.2.1 | Recepcionar los temas; controlar requisitos formales y académicos del tema y del grupo; llevar registro | 3–4 |
| 8.2.2 | Clases: recibir material, "devolverá material con retroalimentaciones, dando las indicaciones correspondientes para que el estudiante instrumente las modificaciones necesarias"; sugerencias "para una redacción clara y precisa, con lenguaje técnico apropiado" | 4 |
| 8.2.3 | Dirigir en todas las etapas | 4 |
| 8.2.4 | "Evaluar el proceso de producción del PIF y la participación de cada estudiante, cuando se trate de un trabajo grupal" | 4 |
| 8.2.5 | Supervisar recolección de datos, análisis y resultados | 4 |
| 8.2.6 | "Recepcionar y evaluar el informe final de Proyecto en un plazo no mayor a veinte días" | 4 |
| 9 | Docentes disciplinares expertos; Formulario N.º 1 (Anexo II) | 4–5 |
| 10.1.1 | Coordinar con el profesor | 5 |
| 10.1.2 (primero) | Entregar los avances según la planificación | 5 |
| 10.1.2 (segundo) | "Responsabilizarse de cualquier falseamiento y/o adulteración **voluntaria** de la información" | 5 |
| 10.2 | Entregar al finalizar un ejemplar digital para Biblioteca | 5 |
| 10.3 | Rescisión del trabajo conjunto: comunicación escrita al profesor | 5 |
| 11 | "La aprobación del PIF estará a cargo de los docentes de la asignatura […] habilitándolo a la defensa oral" | 5 |
| 12 | Defensa: resto de las asignaturas aprobadas y PFG regular | 6 |
| 13 | Inscripción a mesa de turnos ordinarios o extraordinarios; mesa especial si es necesario | 6 |
| 14 | Cinco días hábiles antes, copia del PIF por correo a la Dirección de Carrera | 6 |
| 15 | Aprobación de la defensa con 6 como mínimo | 6 |
| 16 | Defensa pública, hasta 45 minutos, luego preguntas del tribunal | 6 |
| 17 | Tribunal: docentes de PFG + dos profesores de la carrera; designado por Disposición de la "Facultad de Ingeniería y Tecnología" | 6 |
| 18.1 | El tribunal "deberá considerar todo el proceso llevado a cabo por el estudiante" | 7 |
| 18.1.1 | Pertinencia del tema seleccionado | 7 |
| 18.1.2 | Claridad del tema | 7 |
| 18.1.3 | Objetivos descriptos de acuerdo al perfil del egresado de la carrera | 7 |
| 18.1.4 | Grado de aplicación de los conocimientos adquiridos | 7 |
| 18.1.5 | Habilidad para el manejo de los conceptos teóricos | 7 |
| 18.1.6 | Coherencia de los componentes del Proyecto y las conclusiones | 7 |
| 18.1.7 | Fuentes de información consultadas (bibliografía, profesionales, proveedores, empresas, entes oficiales, entre otros) | 7 |
| 18.1.8 | Presentación escrita (claridad, secuencia lógica, coherencia, información completa y fehaciente) | 7 |
| 18.1.9 | Presentación oral (capacidad de síntesis, claridad en la exposición, apertura y cierre, recursos didácticos) | 7 |
| 18.2 | "Dado que el estudiante aprobó la primera instancia", el tribunal califica entre 6 y 10; es la calificación definitiva de PFG | 7 |
| 18.3 | La defensa es la instancia final para el título | 7 |
| 19 | Tras la defensa, ejemplar digital para Biblioteca y autorización de publicación según el **Anexo III** (Formulario N.º 2) | 7–8 |
| 20 | A4; márgenes 2,5 / 2,5 / 3 / 3 cm; espaciado 2 líneas; Times New Roman; cuerpo 12, notas y citas al pie 10, títulos y encabezado/pie de libre elección; **tapa dura** con Universidad, Facultad, Carrera, "Proyecto Integrador Final", título, nombre del alumno, mes y año; numeración correlativa salvo anexos; láminas como una página y plegadas según IRAM; SIMELA y recomendaciones del SI; anexos "página X de Y"; bibliografía en normas APA; entrega digital con código fuente, tablero de gestión y demás datos digitales | 8 |
| 21 | Impersonal; verbos en presente y en afirmativo; criterio uniforme de formato (títulos, guionado, etc.); "No deberán exponerse desarrollos teóricos, ni plantearse discusiones o alternativas ajenas al desarrollo específico del tema del proyecto" | 9 |
| 22.1 | Carátula sin numerar: nombre y logo de la UCP, "Facultad de Ingeniería y Tecnología", Ingeniería en Sistemas de Información, título, autor/es, año | 9 |
| 22.2–22.3 | Resumen ≤ 600 palabras "que refleje el contenido del trabajo"; Índice de Capítulos, Anexos, Tablas y Figuras | 9 |
| 22.4 | Cada capítulo en hoja aparte, número romano y título en mayúscula, "centrados y en el centro de la hoja"; el texto empieza en hoja aparte "sin repetir el título"; 22.4.1 a 22.4.13 títulos de los 13 capítulos (XII: "Lecciones Aprendidas del Proyecto") | 9–10 |
| 22.5–22.7 | Conclusiones; Bibliografía; Anexos I (Datos relevados), II (Documentos del entorno o dominio), III (Otros) | 10 |
| 23.1–23.3 | Modalidades: Selección y Administración; Diseño y Desarrollo; Implementación | 10–11 |
| 24.1–24.6 | Temario: 24.3.1 a 24.3.13 contenidos mínimos de cada capítulo; 24.3.4 incluye "Definición de Negocios (Actividades, Mercado General y Tecnología)"; 24.3.5 MVP (23.2) o implementación (23.1/23.3); 24.6.3 "Otros Anexos" | 11–15 |
| Anexo III | Formulario N.º 2: autorización de publicación y **declaración de originalidad** ("la obra es original […] no se violaron o usurparon derechos de autor o de terceros") | 17 |

**Aclaración Anexo III:** son dos cosas distintas. El Anexo III **de la Resolución** es el Formulario N.º 2 (con la declaración de originalidad). El Anexo III **del PIF** (Art. 22.7.3 / 24.6.3) es "Otros Anexos".

## GD2 — Guía Docente Parte II (cotejada; se citan apartados)

| Apartado | Contenido aplicable |
| --- | --- |
| 1 | Principios: cuatro AE; máximo dos AE grupales; AE3 siempre individual; AE4 con coloquio obligatorio; Portafolio como evidencia de proceso |
| 5.2 | Regularidad: **al menos una** de AE1/AE2 completa + AE3 y AE4 ≥ 6. Ambas completas: promedio AE3–AE4; solo una: promedio − 1; ninguna: Nota de Cursado 5, Libre |
| 7 | Cierre por componentes: COMPLETO ("presentado y reúne los mínimos requeridos; no significa excelencia") / INCOMPLETO; VALIDADA / NO VALIDADA; en AE3 y AE4, nota provisoria hasta validar la instancia oral |
| 8.1 | Portafolio = espacio de las Actividades de Proceso (borradores, versiones, registros de campo, decisiones, devoluciones y ajustes, pruebas) |
| 8.2 | "Toda AE grupal debe tener una evidencia individual correlativa": la Bitácora; no debe reducirse a "nos reunimos y repartimos tareas" |
| 9, 10 | AE1 grupal (pareja o trío), formativa, sin nota; AE2 formativa, individual o grupal; Bitácora si es grupal |
| 11 | Recuperatorio de AE1/AE2 = **Ventana de Mejora y Cumplimiento** (5 a 10 días según cronograma). **Feedback: logros + aspectos de mejora + sugerencias/reelaboración + dictamen completo / incompleto-reelaborar**. IOVF optativa |
| 12, 13 | AE3: escrito individual sincrónico; recuperatorio con IOVF obligatoria, tope 7 |
| 14 | AE4: individual o **en pareja; "nunca se realiza en Trío"**; coloquio obligatorio que valida la nota; regla: Producto ≥ 6 + Portafolio + Bitácora "cuando corresponda" + Foro en digital + Coloquio VALIDADO |
| 15 | Recuperatorio TIFAS en el primer llamado del turno ordinario siguiente: integral, nota 6 o 7, nuevo coloquio |
| 16 | IOVF en **todas** las AE: excepcional en AE1/AE2 "ante dudas sobre autoría, participación, proceso o fundamentación"; ante dudas fundadas en AE3 primer llamado; obligatoria en recuperatorio de AE3. 16.1: dar cuenta, fundamentar, profundizar. Duración: 5–10 min individual, hasta 15 grupal; preferentemente en tutoría |
| 17 | Grabación institucional de IOVF de AE3, IOVF en recuperatorios, coloquios de AE4, exámenes orales; identifica estudiante, asignatura, fecha, instancia, docente y resultado |
| 18 | Revisión de IOVF de AE3 o coloquio de AE4: solo sobre la grabación, pedido dentro de 48 h hábiles, dictamen escrito del tribunal de cátedra antes del fin del cursado |
| 22–24 | Matriz de componentes y checklists docentes de primer llamado (Completo/Incompleto + feedback por componente) y de recuperatorio |
| 26 | Síntesis: "AE4 grupal sólo admite Pareja"; "Toda AE grupal exige Bitácora Individual" |
| **27.1** | "Durante las Actividades de Evaluación queda prohibido utilizar IA generativa para resolver, redactar, elaborar, reformular o producir total o parcialmente las respuestas, argumentos o productos solicitados en las consignas, salvo autorización institucional expresa." Alcanza: productos escritos de **AE1 y AE2** cuando la consigna requiera producción propia; respuestas de AE3; fundamentaciones y decisiones; **Bitácoras**; foros; Producto Final de AE4; **reelaboraciones y recuperatorios**. Remite al Código de Conducta y Ética Profesional UCP |
| **27.2** | Excepción solo con una actividad diseñada para que la IA sea parte explícita del aprendizaje y con un **protocolo previamente autorizado y comunicado** que defina: herramienta, finalidad, límites, declaración de uso, evidencias de proceso y criterios de evaluación. Fuera de ese marco, el uso es no autorizado; la disponibilidad de la herramienta no implica autorización |
| 27.3 | Sentido: evitar la externalización del esfuerzo cognitivo. "EN LAS AE: PENSAMIENTO Y PRODUCCIÓN PROPIOS" |

## RR258 — puntos aplicables (cotejados)

| Ref. | Contenido | Uso en el harness | p. |
| --- | --- | --- | --- |
| Anexo I, 1 | Fortalecer "la calidad y trazabilidad de la evaluación, consolidar criterios institucionales de integridad y uso ético de la Inteligencia Artificial" | Encuadre de ETH-01 | 11 |
| Anexo I, 13 | El Aula Digital organiza "evidencias de proceso, registros de participación e instancias de verificación de autoría" | Registro de devoluciones y evidencias | 26 |
| Art. 8; Anexo I, 10.3 | Tutorías disciplinares, Intervenciones Orales y Coloquios no se delegan a asistentes o adscriptos | El harness prepara el coloquio y la IOVF; no los sustituye | 6, 23 |

La RR 258/26 **no** contiene el protocolo de IA ni la modalidad de evaluación de las AE: están en la GD2.

## AE26 — consignas 2026 (cotejadas)

| Ref. | Contenido |
| --- | --- |
| Rúbrica A–F | Seis dimensiones, cuatro niveles (3/6/8/10), mapeadas por las consignas al Art. 18.1 (ver `03 §art18`). Descriptores de nivel: en el aula virtual (no disponibles) |
| Descuentos | Hasta 1,00/10 (ortografía −0,50 desde el 6.º error; redacción −0,50 desde el 4.º, incluye Art. 21). AE1/AE2: informativo. AE3/AE4: en nota. Las consignas lo atribuyen al "criterio institucional" (no figura en GD2; presumiblemente GD1) |
| Reiteración | Observaciones formales previas que reaparecen ponderan en contra en F |
| Política IA | AE1/AE2: "admitido con declaración obligatoria: asistentes de generación de texto o de código". AE3: prohibida. AE4: GD2 27.1 + Protocolo de Uso Autorizado para el software (27.2) transcripto en la consigna |
| No admitido | Trabajo ajeno; contactos, validaciones o búsquedas no realizadas; atribuir a una fuente un dato que no contiene; (AE4) declarar ejecutable un sistema que no lo es → instancia oral |
| Datos personales | Anonimizar u obtener consentimiento; datos sensibles fuera del repositorio (AE4: y de los anexos) |
| Ejecutabilidad | AE2 ix (prototipo v1); AE4 condición material e i |
| Congelamiento | AE4 x; etiqueta congelada en semana 14 |
| Cierre AE4 | Producto ≥ 6 + Portafolio + Bitácora de cada integrante + Coloquio VALIDADO (coincide con GD2 14) |

## Conflictos e inconsistencias conocidos (informativos: no se verifican en el PIF)

1. **IA en AE1 y AE2.** GD2 27.1 prohíbe la IA generativa en los productos de AE1 y AE2 y en las bitácoras "salvo autorización institucional expresa", y la excepción del 27.2 requiere un protocolo previamente autorizado con seis elementos. Las consignas AE1 y AE2 admiten asistentes de texto con declaración, sin ese protocolo. En el PIF rige la cláusula CAT-IA.
2. **IA en reentregas.** GD2 27.1 incluye "reelaboraciones y recuperatorios". Por decisión de cátedra, la verificación del PIF aplica la cláusula CAT-IA (uso declarado con prompts y enlace), no la prohibición de GD2.
3. **AE4 en trío.** GD2 14 y 26: AE4 individual o en pareja, "nunca se realiza en Trío". La consigna AE4 la define como "producción colectiva del equipo constituido en la AE1" (dos o tres integrantes) con acreditación individual; PLAN26 la registra como individual. Riesgo de objeción para equipos de tres.
4. **Regularidad.** GD2 5.2: basta **una** de AE1/AE2 completa (con −1 punto). La consigna AE4 exige en "Condiciones de regularidad" el cierre de **ambas**, y en "Incidencia académica" reproduce GD2 5.2: se contradice a sí misma. PLAN26 (sem. 16) usa además "(AE1 + AE2 + AE3 + AE4) / 4", que no coincide con ninguna.
5. **Criterio 18.1.3.** RR97 18.1.3 es "Objetivos descriptos de acuerdo al perfil del egresado"; las consignas le asignan la dimensión E (calidad de la argumentación). El resto del mapeo es consistente (A–18.1.7, B–18.1.4, C–18.1.5, D–18.1.1/18.1.2/18.1.6, F–18.1.8/18.1.9).
6. **Denominación de la Facultad.** RR97 (2023) dice "Facultad de Ingeniería y Tecnología" (Arts. 17 y 22.1); las consignas 2026, "Ingeniería, Tecnología y Arquitectura". El harness acepta ambas y sugiere la vigente.
7. **Nombre de la instancia oral.** GD2 la llama IOVF en todas las AE; las consignas AE1 y AE2 la llaman "Verificación Oral de Autoría". El harness usa IOVF.
8. **Recuperatorio en semana 16.** PLAN26 prevé el 27/11 la "recuperación de la instancia no aprobada"; AE4 y GD2 15 ubican el Recuperatorio TIFAS en el turno ordinario siguiente. Presumiblemente se refiere a AE3.
9. **Fechas de AE1 y AE2.** Ver `templates/plan_entregas.ejemplo.json` (se usan las fechas de implementación de PLAN26).
10. **Bitácora en AE4 individual.** GD2 14 pide Bitácora en AE4 solo "cuando corresponda" (en pareja); la consigna AE4 la hace componente de cierre para cada integrante. Es más exigente, no contradictorio, si la consigna lo declara (GD2 8).
