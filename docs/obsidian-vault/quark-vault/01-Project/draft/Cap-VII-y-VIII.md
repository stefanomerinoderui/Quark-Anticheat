# BORRADOR — Capítulos VII y VIII (no integrado al informe)

> Estado: borrador del 2026-11-25. Firma: `agent:claude-sonnet-5-5`. Fuente de la estructura: Art. 24.3.7 y 24.3.8 del RR-97-23. Lo no verificado se marca **UNVERIFIED**. Nada de lo que sigue afirma resultados de encuesta, búsquedas INPI ni contactos externos, porque no existen aún.

---

# CAPÍTULO VII — MARKETING DEL PROYECTO

## 7.1. Descripción de Producto/Experiencia

Quark Anticheat es un sistema anticheat nativo para GNU/Linux, de código abierto, compuesto por un módulo de kernel, un servicio en espacio de usuario y una API/SDK de integración para videojuegos (Cap. I, 1.5 y 1.6). El producto no se vende. Se ofrece como proyecto académico y comunitario, y su propuesta de valor es la transparencia: el código se publica y puede ser auditado por cualquier persona.

La experiencia se define por perfil:

- **Jugador en Linux.** Instala el sistema desde el repositorio, sin software propietario. Entiende qué se monitorea porque puede leer el código y la documentación. La condición de uso prevista es que la protección esté activa solo durante la sesión de juego (condición de adopción incluida en la encuesta diseñada).
- **Desarrollador de juegos open source.** Incorpora el SDK en su título, sin conocer el detalle del módulo de kernel (Cap. I, 1.6). El caso de referencia es un juego de código abierto, cuya comunidad es el primer público de validación (Beyond All Reason, vía RecoilEngine; la integración existe en el repositorio de trabajo según `vm/README.md`).
- **Comunidad de seguridad y académica.** Revisa el diseño, reproduce las pruebas y reporta fallas.

Estado del producto: prototipo académico; no hay versión estable publicada. **UNVERIFIED** cualquier afirmación de eficacia fuera de las capturas del vault.

## 7.2. Dinámicas de intercambio por perfil de interesado

| Perfil | Qué aporta | Qué recibe | Forma de intercambio |
|---|---|---|---|
| Jugadores GNU/Linux | Respuestas a la encuesta, reportes de compatibilidad, pruebas en distintas distribuciones | Un anticheat auditable; influencia en las prioridades | Encuesta, issues del repositorio |
| Desarrolladores de juegos open source | Feedback del SDK, casos de integración | SDK y documentación gratuitos y modificables | Issues, pull requests, encuesta breve para desarrolladores |
| Comunidad de seguridad | Revisión del código, análisis de evasiones | Un caso de estudio abierto; mención en los créditos | Issues, discusiones públicas del diseño |
| Moderadores y medios comunitarios | Autorización de difusión y alcance | Información veraz y verificable | Consulta previa de reglas, material en español e inglés |
| Cátedra y tutor | Evaluación y seguimiento | Evidencia del avance (Cap. VI) | Entregas y defensa |
| Equipo (Martínez, Merino De Rui) | Desarrollo y difusión | Validación del proyecto y portafolio | Repositorio público |

Objeción principal prevista: publicar el código facilita la evasión. La encuesta la mide de forma explícita con un ítem planteado a propósito en contra del proyecto (`docs/Quark_Encuesta_Diapositivas.txt`, diapositiva 04).

## 7.3. Estrategias de publicidad, promoción y engagement

Las estrategias no tienen presupuesto (Cap. III, 3.4, restricciones económicas) y se apoyan en contenido propio.

1. **Repositorio público como vitrina.** README claro en inglés y español, descripción de la arquitectura, instrucciones para reproducir la demostración y guía de contribución. Un repositorio sin documentación no genera interés técnico.
2. **Encuesta como instrumento de engagement y de validación.** La encuesta anónima diseñada convoca a la comunidad a opinar antes de publicar el producto. Valida dos supuestos (existe interés; el código abierto es un diferencial) y registra canales opcionales de seguimiento, desvinculados de las respuestas. Diseño vigente: encuesta principal recortada a unos 25 ítems, encuesta breve aparte para desarrolladores, prueba piloto con 5 a 10 personas y consulta previa a moderadores. Los resultados se publican de vuelta en cada comunidad. **No existen resultados aún.**
3. **Demostración reproducible.** Video o captura breve de una detección real, tomada de la evidencia del vault, con la salvedad de sus límites. Se muestran también los límites conocidos: la honestidad técnica es parte del posicionamiento.
4. **Entradas técnicas.** Notas sobre la investigación de anticheat en Proton y el diseño del módulo, a partir de las notas del vault (p. ej. la nota de investigación de anticheat en Proton).
5. **Participación comunitaria.** Respuesta pública a preguntas e issues; reconocimiento de contribuciones.

Indicadores propuestos (a medir, sin valores objetivo inventados): visitas y estrellas del repositorio, issues abiertos por terceros, respuestas completas a la encuesta, tasa de abandono, cantidad de desarrolladores que piden información del SDK.

## 7.4. Canales

| Canal | Uso | Condición |
|---|---|---|
| Repositorio público (GitHub) | Código, documentación, issues | Publicar solo con la licencia definida (Cap. VIII) |
| GamingOnLinux | Noticia/aviso a la comunidad de jugadores en Linux | Cumplir sus criterios editoriales; **UNVERIFIED** el procedimiento de envío |
| r/linux_gaming | Presentación del proyecto y encuesta principal | Consultar a los moderadores las reglas sobre encuestas y autopromoción |
| r/gamedev | Encuesta breve para desarrolladores | Ídem |
| Comunidad de Beyond All Reason (foros/Discord) | Juego de referencia; feedback de integración | Consultar a sus responsables antes de publicar; **UNVERIFIED** la aceptación |
| Presentaciones académicas (defensa del PIF) | Difusión institucional | Calendario de la cátedra |

Un mismo post por comunidad, en inglés y español, con enlace al repositorio y a la encuesta. La publicación de muchas encuestas puede causar problemas con los moderadores (diapositiva 04 de la encuesta), por lo que se limita a una por comunidad.

**Acciones futuras (no ejecutadas, sin contacto realizado).** Contactar a la comunidad del juego de referencia y, más adelante, evaluar un acercamiento a Valve (Steam) o a desarrolladoras. Estas acciones quedan fuera del alcance actual y no figuran como logros.

## 7.5. Limitaciones

No hay datos de mercado propios (Cap. II pendiente de encuesta). No hay presupuesto publicitario. La difusión depende de la aceptación de moderadores y editores, no controlable por el equipo.

---

# CAPÍTULO VIII — PROPIEDAD INTELECTUAL

## 8.1. Definición de Marca y activos a proteger

**Activos:**

| Activo | Situación | Protección prevista |
|---|---|---|
| Nombre "Quark Anticheat" | En uso en el proyecto y el repositorio | Registro de marca (8.2 a 8.4) |
| Logo | **No existe aún** | Se registra recién cuando exista un diseño definitivo; mientras tanto solo la marca denominativa |
| Código fuente (módulo de kernel, servicio, eBPF, SDK) | Autoría de Martínez y Merino De Rui; sin archivo LICENSE en el repositorio de trabajo (verificado: no hay `LICENSE*` en el árbol `Dev` ni en el repositorio de documentación) | Derecho de autor y licencia de software libre (8.5) |
| Documentación, informe e imágenes del vault | Autoría del equipo | Licencia de documentación a definir (p. ej. Creative Commons); **UNVERIFIED** decisión |

La autoría y el derecho de autor surgen sin registro formal; el registro de obra ante el organismo competente es opcional. No se atribuye derechos a la facultad.

## 8.2. Definición de clases internacionales a seleccionar

La Clasificación de Niza agrupa productos (clases 1 a 34) y servicios (35 a 45). Redacción oficial verificada (Niza, 12.ª edición, versión 2024, según la publicación de la USPTO del acuerdo; texto en inglés, traducción propia):

- **Clase 9**: "…recorded and downloadable media, computer software, blank digital or analogue recording and storage media…" y "computers and computer peripheral devices". Es el encabezado completo, que comienza con "Scientific, research, navigation, surveying, photographic, cinematographic, audiovisual, optical, weighing, measuring, signalling, detecting, testing, inspecting, life-saving and teaching apparatus and instruments;…".
- **Clase 42**: encabezado que incluye "design and development of computer hardware and software". Su nota explicativa incluye "computer and technology services for securing computer data and personal and financial information" y "software as a service (SaaS), platform as a service (PaaS)". Se excluye "installation, maintenance and repair of computer hardware (Cl. 37)".

El comienzo del encabezado de la clase 42 ("Scientific and technological services and research and design relating thereto; industrial analysis, industrial research and industrial design services; quality control and authentication services; design and development of computer hardware and software.") surge de la búsqueda en las ediciones WIPO, pero el texto completo oficial no se pudo recuperar en esta sesión: **UNVERIFIED**; debe cotejarse en la edición vigente de WIPO y en la versión en español usada por el INPI.

**Clases candidatas y justificación:**

| Clase | Justificación | Prioridad |
|---|---|---|
| 9 | Quark se distribuye como software descargable (módulo, daemon, SDK). El rubro "computer software" aplica de forma directa. La guía de WIPO pide precisar la función del software en lugar de usar "software" a secas (p. ej. "software anticheat para la detección de manipulación de procesos de videojuegos"); la redacción final es **UNVERIFIED**. | Alta |
| 42 | Diseño y desarrollo de software; servicios de seguridad informática; eventual servicio de verificación (atestación) en línea si se ofreciera. | Media; solo si hay servicios, hoy no |
| 41 (candidata) | Entretenimiento, si el producto se vinculara a juegos; **no se recomienda ahora** porque el producto no presta ese servicio. UNVERIFIED que aplique. | Descartada por ahora |

Recomendación del borrador: solicitar clase 9 y evaluar la 42 con el tutor. Cada clase adicional agrega tasa. **UNVERIFIED** el monto vigente.

## 8.3. Búsqueda de antecedentes en INPI

**La búsqueda no se ha realizado.** Este apartado describe el procedimiento y queda **pendiente de aportar por una persona** (integrante del equipo con acceso al sitio del INPI).

Procedimiento propuesto (sujeto a verificación en el sitio oficial, **UNVERIFIED** en pasos y nombres de pantallas):

1. Ingresar al buscador de marcas del Instituto Nacional de la Propiedad Industrial (INPI, Argentina).
2. Buscar la denominación exacta "Quark Anticheat" y sus componentes por separado: "Quark" y "Anticheat".
3. Repetir con variantes fonéticas y gráficas ("Quarc", "Kwark", "Quark Anti-Cheat") y con las clases 9, 42 (y 41 como control).
4. Registrar por cada hallazgo: denominación, titular, clase, estado, fecha y número de acta.
5. Capturar la pantalla con fecha y hora, y guardarla en el vault (zona de evidencia, append-only).
6. Analizar si hay marcas idénticas o confundibles en las mismas clases o en clases conexas.

Es esperable que "Quark" sea un término de uso extendido en varios rubros (incluido el software); esto no está verificado y debe resolverlo la búsqueda. **UNVERIFIED**. El resultado puede imponer agregar un elemento distintivo o descartar el registro.

Tabla a completar por una persona:

| Fecha | Término buscado | Clase | Resultados | Captura | Responsable |
|---|---|---|---|---|---|
| *pendiente* | | | | | |

## 8.4. Registro de la marca

Pasos previstos, tras la búsqueda: solicitud en el INPI, pago de tasa, publicación en boletín, plazo de oposición y concesión. Los plazos y costos no se citan porque no se verificaron. **UNVERIFIED**. Se cita como marco general la ley de marcas argentina (Ley 22.362); su articulado debe cotejarse antes de citarlo. **UNVERIFIED**. El registro de marca no es un requisito de aprobación del PIF; se plantea como decisión futura según resultado de búsqueda, costo y objetivos del equipo.

## 8.5. Licencia del software

**Hechos verificados en el código** (rama `Dev`, árbol de trabajo local, sujeto a revisión contra `origin/Dev`):

- `kernel/quark_kernel.c:37`: `MODULE_LICENSE("GPL")`.
- `quark_daemon/src/bpf/quark.bpf.c:31`: `char LICENSE[] SEC("license") = "GPL";`.
- No hay archivo `LICENSE` en el árbol.

**Consecuencias:**

- Un módulo de kernel que declara una licencia no compatible con GPL se marca como "tainted" y no puede usar los símbolos exportados solo para GPL. Los programas eBPF que usan ciertas funciones auxiliares (helpers) también exigen una licencia compatible con GPL. El código de este proyecto declara "GPL", por lo que el componente de kernel y el programa eBPF deben distribuirse bajo licencia GPL. (Regla general del kernel; **UNVERIFIED** contra la documentación vigente de kernel.org en esta sesión.)
- La declaración "GPL" en `MODULE_LICENSE` indica GPL v2 o posterior según la convención del kernel (**UNVERIFIED** contra la documentación oficial). El kernel Linux está bajo GPL-2.0 con excepción para las llamadas al sistema (**UNVERIFIED** en esta sesión).

**Propuesta para decisión del equipo (no tomada):**

| Componente | Licencia propuesta | Motivo |
|---|---|---|
| Módulo de kernel y programa eBPF | GPL-2.0-or-later (SPDX), con cabecera `SPDX-License-Identifier` | Coincide con lo declarado y es exigido por el kernel |
| Servicio en espacio de usuario | GPL-2.0-or-later | Coherencia con el resto; mantiene el código abierto |
| SDK/API enlazado por los juegos | **Pendiente**: GPL implicaría que el juego que lo enlace quede bajo licencia compatible; una licencia permisiva o LGPL facilitaría la integración. | La decisión afecta la adopción por desarrolladores; **UNVERIFIED** el análisis legal de compatibilidad con la licencia de cada juego (p. ej. RecoilEngine, que debe consultarse) |
| Documentación | Creative Commons u otra | A definir |

Acciones concretas: agregar el archivo `LICENSE`, las cabeceras SPDX en cada archivo y una sección de licencia en el README, **antes de publicar el repositorio** (Cap. VII). Estas acciones no se ejecutaron en este borrador.

La licencia libre es coherente con la propuesta de valor (transparencia y auditoría) y con el diferencial que mide la encuesta. No impide registrar la marca: la licencia cubre el código; la marca, su uso y el logo se protegen aparte, y puede fijarse una política de uso del nombre para forks. **UNVERIFIED** el alcance legal.

## 8.6. Limitaciones

No se consultó a un profesional de propiedad intelectual. Los datos legales, plazos y costos no se verificaron. El logo no existe. La búsqueda INPI queda pendiente.

---

## Referencias nuevas (APA 7)

United States Patent and Trademark Office. (2024). *Nice Agreement twelfth edition, version 2024: General remarks, class headings and explanatory notes*. https://www.uspto.gov/trademarks/trademark-updates-and-announcements/nice-agreement-twelfth-edition-version-2024-general

World Intellectual Property Organization. (s. f.). *Nice Classification*. https://www.wipo.int/classifications/nice/en/ (UNVERIFIED: fecha de consulta y edición a precisar al integrar).

World Intellectual Property Organization. (s. f.). *Filing international trademark applications: Classification of goods and services*. https://www.wipo.int/de/web/madrid-system/how_to/file/madrid-system-filing-international-trademark-applications-classification-of-goods-and-services

Fuentes internas: `docs/Quark_Encuesta_Diapositivas.txt`; `kernel/quark_kernel.c:37` y `quark_daemon/src/bpf/quark.bpf.c:31` (rama `Dev`, árbol local); `docs/RR-97-23-Reglamento-de-Proyecto-Integrador-Final.md` (Art. 24.3.7 y 24.3.8).

`agent:claude-sonnet-5-5` — 2026-11-25
