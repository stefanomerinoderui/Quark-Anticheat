---
title: "Informe PIF (avance)"
tags: [proyecto, informe]
source: TPI-GP-Avance_Proyecto_Final_Grado-Martinez_Merino.md
status: snapshot
---

# **Quark Anticheat: análisis de viabilidad técnica e implementación**  **de un sistema anticheat nativo para GNU/Linux**

## 

## Universidad de la Cuenca del Plata

## 

## Facultad de Ingeniería y Tecnología

## 

## Ingeniería en Sistemas de Información

## 

## PROYECTO INTEGRADOR FINAL

# 

**Autor (presenta y defiende):** Martínez Alarcón, Gabriel Sebastián

**Colaborador:** Merino De Rui, Stefano Nahuel (colabora con atribución; no presenta ni defiende este PIF)

**Cátedra de Proyecto Final de Grado:** Ing. Sergio Lapertosa, Ing. Augusto Portillo, Ing. Martin Jones

**Noviembre de 2026** (defensa en febrero, en el turno de examen que fije la Dirección de Carrera; la fecha exacta no consta en el Reglamento y queda por confirmar)

#

# **Resumen**

El presente proyecto aborda una limitación técnica que afecta a los usuarios de distribuciones GNU/Linux que utilizan su equipo para jugar videojuegos en línea. Un conjunto significativo de títulos multijugador requiere, como condición obligatoria de ejecución, la presencia de un sistema anticheat2 de nivel de kernel3. Dado que estos sistemas se diseñan principalmente para Windows y operan en el nivel de máximo privilegio (Ring 0), resultan incompatibles con el modelo de kernel de Linux; en esta plataforma el anticheat, cuando existe, opera en espacio de usuario sobre capas de compatibilidad y, según información pública reciente, mediante programas BPF-LSM sin módulo de kernel, lo que condiciona el acceso a dichos títulos con independencia de que el juego en sí sea compatible.

La solución consiste en el diseño y desarrollo de un sistema anticheat de nivel de kernel orientado a entornos GNU/Linux, compuesto por tres elementos: un módulo de kernel, escrito en C, que deniega a cualquier otro proceso el acceso a la memoria de un proceso protegido mediante `ptrace`, `/proc/<pid>/mem` y `process_vm_readv/writev`; un servicio en espacio de usuario, escrito en Rust, que registra los procesos protegidos, ordena su protección al módulo por un canal autenticado, carga programas eBPF/BPF-LSM de protección y telemetría y vigila las variables que el juego declara; y una interfaz de integración (API4/SDK5) en C que permite incorporar el sistema en videojuegos y que falla de forma cerrada si el kernel no confirma la protección. El uso de C en el módulo, y no de Rust, responde a la contingencia prevista para el riesgo R2 (bindings de Rust for Linux insuficientes), que se materializó y se ejecutó.

El desarrollo se declara en espiral; la ejecución real es un prototipado evolutivo guiado por riesgo, decisión propuesta en la ADR-001 y adoptada por el autor en este informe, con seis ciclos reconstruidos desde el historial de git (Capítulos V y VI). Como pauta general del informe, ante un conflicto entre lo planeado en origen y lo ocurrido, prevalece lo ocurrido en la rama `Dev` (commit `35c6031`, 2026-11-05).

Los resultados alcanzados son un prototipo funcional integrado con RecoilEngine (motor del juego de código abierto Beyond All Reason) y una validación en máquina virtual con el build de pruebas: con el módulo cargado, el ataque por `/proc/<pid>/mem` es denegado en 10 de 10 repeticiones sobre un juego simulado, y hay una verificación sobre el motor real. El impacto en el rendimiento, las tasas de detección y de falsos positivos y la resistencia a evasión no se midieron y se declaran como trabajo pendiente. El proyecto aporta una base abierta y documentada para el estudio de mecanismos de seguridad en GNU/Linux y demuestra la viabilidad técnica del enfoque dentro del alcance indicado.

**Índice**

Resumen · Capítulos I a XIII (secciones numeradas dentro de cada capítulo) · Conclusiones del Proyecto · Bibliografía · Anexos I a III. El índice completo, con numeración de páginas, de capítulos, secciones, tablas y figuras, se genera automáticamente en la versión impresa (`sh tooling/build_informe.sh`).

**Índice de figuras.** Figura 2.1: participación de Linux en la Steam Survey (2016–2024). Figura 2.2: Windows, Linux, macOS y distribuciones Linux visibles (2016–2024). Figura 2.3: reparto de la Steam Survey por idioma (2016–2024).

**Índice de tablas.** Capítulo II: tablas 2.1 a 2.3. Capítulo IV: IV-1, IV-2, IV-3. Capítulo V: V-1 a V-11. Capítulo VI: VI-1. Capítulo IX: tablas de la sección 9. Capítulo XI: XI-1. Capítulo XIII: XIII-1. Conclusiones: C-1. Anexo III: III.1 a III.4.

#

#

#

# **CAPÍTULO I — DEFINICIÓN DEL PROYECTO**

## **1.1. Origen del Proyecto**

El proyecto surge a partir de la identificación de una limitación concreta que afecta a los usuarios de distribuciones GNU/Linux que utilizan sus equipos para jugar videojuegos en línea. Una parte significativa de los títulos multijugador más populares implementa sistemas anticheat de nivel de kernel como dependencia obligatoria de ejecución. Estos sistemas operan en el espacio del kernel (Ring 0), el nivel de máximo privilegio del procesador, lo que les otorga acceso amplio a los recursos del sistema para detectar modificaciones no autorizadas (Wikipedia, 2026a). Como se diseñaron principalmente para Windows, los usuarios de Linux quedan excluidos: en esta plataforma el anticheat, cuando se habilita a través de capas de compatibilidad como Proton, funciona en espacio de usuario y no mediante un controlador de kernel (GamingOnLinux, 2026).

El contexto de aplicación es a la vez técnico y social: técnico, porque la brecha existe por una limitación arquitectónica real entre los modelos de kernel de ambos sistemas operativos; social, porque afecta a una comunidad de usuarios en crecimiento que ha optado por plataformas libres y abiertas. El proyecto se enmarca en el contexto académico de la carrera de Ingeniería en Sistemas de Información de la Universidad de la Cuenca del Plata, donde representa una oportunidad de aplicar conocimientos de sistemas operativos, seguridad y desarrollo de software de bajo nivel sobre un problema con impacto real y verificable.

## **1.2. Misión, Visión y Objetivos**

**Misión.** Demostrar, mediante el diseño y desarrollo de un prototipo funcional, la viabilidad técnica de un sistema anticheat de nivel de kernel nativo para GNU/Linux que preserve la integridad del entorno de ejecución de videojuegos; su impacto en el rendimiento se mide y se informa en las Conclusiones, y hasta contar con esa medición no se afirma bajo impacto.

**Visión.** Contribuir a reducir la brecha que excluye a los usuarios de GNU/Linux del ecosistema de videojuegos multijugador competitivos, aportando una base técnica abierta sobre mecanismos de seguridad a nivel de kernel en esta plataforma.

**Objetivo general.** Analizar, diseñar y desarrollar un sistema anticheat de nivel de kernel para distribuciones GNU/Linux, capaz de detectar y prevenir comportamientos maliciosos que comprometan la integridad del entorno de ejecución de videojuegos, evaluando su viabilidad técnica, su impacto en el rendimiento del sistema anfitrión y los riesgos de seguridad asociados al uso de privilegios de kernel.

**Objetivos específicos.**

1. Definir la arquitectura del sistema propuesto, produciendo un documento de diseño que cubra el módulo de kernel, el servicio en espacio de usuario y la interfaz de integración.  
2. Identificar y documentar un mínimo de cinco vectores de ataque comunes utilizados por software de trampas en videojuegos multijugador.  
3. Implementar una interfaz de integración (API/SDK) funcional, verificada mediante su incorporación en un videojuego de código abierto seleccionado como caso de prueba.  
4. Validar el sistema desarrollado mediante la ejecución de casos de prueba basados en los vectores de ataque identificados, registrando tasas de detección y falsos positivos para cada uno.  
5. Medir el impacto del sistema en el rendimiento del equipo anfitrión, cuantificando el overhead introducido en CPU y memoria RAM durante la ejecución del videojuego.

**Tabla 1.1. Estado de los objetivos específicos al 2026-11-25** (detalle y fuentes en Conclusiones, C.2)

| N° | Estado |
| :---- | :---- |
| 1 | Parcial: la arquitectura existe en el código y en la documentación de `Dev`; se documenta en el Capítulo IX. |
| 2 | Parcial: los vectores cubiertos son `ptrace` *attach*, `/proc/<pid>/mem`, `process_vm_readv/writev`, carga de BPF de *tracing* y escritura de variables vigilada; la clasificación formal de cinco vectores no consta como documento. |
| 3 | Cumplido en lo esencial: SDK en C integrado en RecoilEngine (Beyond All Reason). |
| 4 | Parcial: un vector validado con control negativo (10/10); no se calculan tasas de detección ni falsos positivos. |
| 5 | No medido: no existe medición de overhead. |

## **1.3. Necesidad o Problema que responde**

Los sistemas anticheat de nivel de kernel disponibles en el mercado se desarrollaron principalmente para Windows. Esta decisión de diseño los hace incompatibles con las distribuciones GNU/Linux, ya que dependen de interfaces internas del kernel de Windows que no tienen equivalente directo en Linux; las diferencias en los requisitos de firma de controladores, las políticas de módulos de kernel y la naturaleza descentralizada de las distribuciones complican el despliegue de controladores propietarios en Linux frente al modelo centralizado de Windows (Wikipedia, 2026a). Como resultado, los videojuegos que incorporan estos sistemas como dependencia obligatoria resultan inaccesibles para los usuarios de Linux, sin que exista una solución de nivel de kernel abierta y documentada equivalente para dicha plataforma; los proveedores comerciales anuncian para Linux un servicio con programas BPF-LSM (información pública, sin verificación propia; Capítulo II).

El problema es de naturaleza técnica. Su causa radica en una incompatibilidad arquitectónica entre los mecanismos de kernel sobre los que se construyen los anticheats existentes y el modelo de kernel de Linux. No existe un componente organizacional o institucional que lo origine; es consecuencia directa de decisiones de desarrollo tomadas por la industria del videojuego orientadas al ecosistema Windows. El impacto, no obstante, trasciende lo técnico: la exclusión resultante afecta a un segmento de usuarios que ve limitado su acceso a productos de entretenimiento por razones ajenas a la capacidad de su hardware o a la compatibilidad del software en sí.

## **1.4. ODS asociadas y Diferenciales**

**ODS asociadas.** El proyecto se vincula principalmente con el Objetivo de Desarrollo Sostenible 9 (Industria, Innovación e Infraestructura), en tanto promueve la innovación tecnológica y el desarrollo de infraestructura de software abierta y resiliente. De forma secundaria se vincula con el ODS 10 (Reducción de las desigualdades), al reducir la brecha de acceso que excluye a una comunidad de usuarios de una plataforma libre. *(Asociación propuesta, a validar en la cátedra de Proyecto Final de Grado.)*

**Diferenciales.** El primer diferencial es su carácter abierto y documentado, frente al carácter cerrado y propietario de los anticheats comerciales (GamingOnLinux, 2026). El segundo es la combinación de un módulo de kernel en C con un servicio en Rust y programas BPF-LSM, que cubren lo que un LSM clásico no puede registrar desde fuera del árbol del kernel. El tercero es su orientación académica y la trazabilidad de cada afirmación del informe. El carácter «nativo de kernel» deja de ser diferencial exclusivo, porque la industria converge hacia BPF-LSM sin módulo de kernel (Capítulo II).

## **1.5. Descripción breve del Sistema**

Un sistema anticheat es una solución de seguridad cuyo propósito es detectar y prevenir el uso de software de trampas en videojuegos, preservando la integridad del entorno de ejecución y garantizando condiciones de juego equitativas. El presente sistema constituye una implementación de este concepto a nivel de kernel, orientada a distribuciones GNU/Linux. Se compone de tres elementos que operan de forma coordinada: un módulo de kernel, un servicio en espacio de usuario y una interfaz de integración. El sistema opera en tiempo real durante la ejecución del videojuego, con privilegios elevados que le permiten acceder a información del sistema no accesible desde el espacio de usuario convencional.

## **1.6. Descripción detallada del Sistema**

El **módulo de kernel** deniega el acceso de nivel *attach* a la memoria de los procesos protegidos y registra cada intento en el log del kernel. Opera con privilegios de kernel mediante un `kretprobe` sobre `ptrace_may_access`, de modo que resiste técnicas de evasión que explotan las limitaciones del espacio de usuario. La capacidad de mediación se completa con programas BPF-LSM, que exponen ganchos de seguridad del kernel desde eBPF sin requerir un módulo LSM compilado en el kernel (The kernel development community, 2024a); la telemetría de eventos la generan programas eBPF cargados por el servicio, máquina virtual interna del kernel que ejecuta programas verificados con bajo overhead (New Relic, 2025). Un LSM clásico no puede registrarse desde un módulo fuera del árbol, porque `security_add_hooks()` solo existe durante la inicialización y no se exporta.

El **servicio en espacio de usuario** registra los procesos protegidos, ordena su protección al módulo por un canal autenticado (Netlink con firma ECDSA), carga los programas BPF, registra la telemetría y termina el proceso del juego ante una discrepancia en las variables vigiladas.

La **interfaz de integración** expone una API/SDK que permite a los desarrolladores de videojuegos incorporar el sistema en sus títulos sin requerir conocimiento de los detalles internos del módulo ni del servicio. La política es de fallo cerrado: `quark_sdk_init()` falla si el kernel no confirma la protección y un *watchdog* termina el juego si el servicio deja de responder.

# **CAPÍTULO II — RELEVAMIENTO E INVESTIGACIÓN DE MERCADO**

## **2.1. Objetivo y alcance del relevamiento**

El relevamiento responde tres preguntas del proyecto: (a) cuál es el tamaño y la evolución del público potencial de un anticheat nativo para GNU/Linux; (b) cuál es el estado de la oferta existente; y (c) qué hipótesis de demanda sostienen el proyecto y qué las refutaría. El alcance es la investigación documental de fuentes públicas (2.2), el análisis de dos series estadísticas de la Steam Hardware & Software Survey (2.4) y el diseño de una encuesta anónima a *stakeholders* (2.3). La encuesta se diseña y no se publica; el capítulo no presenta resultados de ella, y los resultados de la encuesta los debe aportar una persona del equipo tras su aplicación.

## **2.2. Fuentes de datos**

**Tabla 2.1. Fuentes del relevamiento**

| Fuente | Tipo | Dato que aporta | Fecha |
|---|---|---|---|
| Compilación de panke de la Steam Hardware & Software Survey, pestaña de sistema operativo (`docs/steam-historic-hardware-survey-os.tsv`) | Secundaria, de procedencia débil | Participación mensual de Windows, macOS y Linux (y de algunas distribuciones) entre 2016-ene y 2024-jun para Linux | Nota del 2024-12-08 |
| Compilación de panke, pestaña de idioma (`docs/steam-historic-hardware-survey.tsv`) | Secundaria, de procedencia débil | Reparto de la encuesta por idioma, 2016-ene a 2024-nov | Nota del 2024-12-08 |
| Steam Hardware & Software Survey, octubre de 2026 (Valve) | Secundaria, estadística pública | Participación de sistemas operativos entre usuarios de Steam | Consulta 2026-11-25 |
| Cifras de usuarios de Steam (Valve, vía prensa) | Secundaria | Usuarios activos mensuales (fin de 2021) y récord de usuarios simultáneos (2026) | Consulta 2026-11-25 |
| AreWeAntiCheatYet | Secundaria, base colaborativa | Estado de compatibilidad de juegos con anticheat en Linux | Consulta 2026-11-25 |
| Phoronix; GamingOnLinux; It's FOSS | Secundaria, prensa especializada | Anuncio de Easy Anti-Cheat (EAC) para Linux v2 | Consulta 2026-11-25 |
| Repositorio propio `proton-anticheats` y nota `Proton-Anticheat-Research` | Primaria, análisis técnico propio | Funcionamiento de EAC y BattlEye bajo Proton | Commit `cc5078e`, 2026-11-13 |
| Encuesta a *stakeholders* (Reddit) | Primaria, instrumento diseñado | Interés, adopción y objeciones | No aplicada |

**Procedencia de la compilación de panke.** Las dos series 2016–2024 provienen de una compilación publicada por panke en una nota de note.com del 2024-12-08 (panke, 2024). Según la propia nota, los datos se copiaron de Reddit y el autor de este informe no los verificó contra la fuente de Valve; desde julio de 2024 la compilación se carga manualmente y su actualización estaba prevista hasta aproximadamente febrero de 2025. Es un dato secundario de procedencia débil y así se usa: como indicio de orden de magnitud y tendencia, no como medición. La verificación de alineación efectuada para este informe consiste en que, en cada mes con datos de los tres sistemas, Windows + macOS + Linux suman 100 % ± 0,3 pp. La serie de Linux tiene dato hasta junio de 2024 (92 de 97 meses de la tabla); julio a noviembre de 2024 están vacíos, y esas celdas se tratan como dato faltante, no como cero.

**Dos fuentes distintas.** La compilación de panke (2016–2024) y la lectura de la encuesta de octubre de 2026 (Valve, 2026) son fuentes independientes, con método de obtención diferente. No se combinan en una sola serie; se presentan por separado y solo se las compara de forma cualitativa.

**Limitaciones de las fuentes.** La Steam Hardware Survey mide a los usuarios de Steam que aceptan participar y no a todos los jugadores de PC; el sesgo de muestra no se cuantifica aquí. AreWeAntiCheatYet es colaborativa y la fecha de actualización varía por fila (las observadas, entre 2022 y 2024). Las notas de prensa sobre EAC v2 reproducen un anuncio de Epic Games, y el funcionamiento interno de EAC v2 no es público.

## 2.3. Instrumento: encuesta anónima a *stakeholders*

**Estado: diseñada, no publicada.** Fuente del diseño: `docs/Quark_Encuesta_Diapositivas.txt`. No existen respuestas, por lo que este apartado documenta el método y no datos.

**Población objetivo.** Usuarios de Linux, jugadores y desarrolladores de juegos. **Canal previsto:** subreddits afines, con consulta previa a moderadores en versiones en inglés y en español (varios subreddits limitan las encuestas). El muestreo es por conveniencia y autoselección; no es probabilístico y sus resultados no se extrapolan a la población (limitación metodológica declarada de antemano).

**Supuestos a validar.** (1) Existe interés en un anticheat nativo para Linux. (2) El código abierto es un diferencial.

**Estructura en cinco bloques.**

| Bloque | Contenido |
|---|---|
| 01 Perfil | Nivel técnico, años usando Linux, motivos, uso exclusivo de Linux |
| 02 Interés | Escala Likert sobre cada característica de Quark y sobre los anticheats de kernel |
| 03 Adopción | Probabilidad de instalación según condiciones; cambio de uso de Windows |
| 04 Propuestas | Qué agregarían, qué los haría rechazarlo, qué trampas contemplar |
| 05 Contacto | Canales de seguimiento, desvinculados de las respuestas |

**Preguntas clave.**

1. «Confiaría más en un anticheat de kernel de código abierto que en uno cerrado.» Valida el diferencial.
2. «Publicar el código de un anticheat facilita que los tramposos lo evadan.» Mide la objeción principal; se incluye a propósito para no sesgar a favor del proyecto.
3. Condiciones de instalación: repositorios de la distribución, carga solo durante el juego, Secure Boot, auditoría independiente. Orienta el diseño.
4. «Si estos juegos funcionaran en Linux, dejaría de usar Windows por completo.» Mide el impacto potencial; es hipotética y se presenta como **intención declarada, no como predicción de conducta**.

**Variables.** Independientes (perfil): nivel técnico, antigüedad en Linux, uso exclusivo de Linux, rol (usuario, jugador, desarrollador). Dependientes: nivel de acuerdo en escala Likert por característica, confianza en código abierto, percepción del riesgo de evasión, probabilidad de instalación y condiciones, intención de abandonar Windows. El diseño permite cruzar perfil con interés y adopción en la misma persona, razón por la que se descarta dividir la encuesta por etapas (al ser anónima, las etapas no se vinculan).

**Decisión de recorte.** El borrador contiene ~50 preguntas e ítems (cada persona ve entre 40 y 45 según su lógica condicional), ~33 en escala Likert, y una estimación de 10–12 minutos frente a los 8 anunciados. Se decide: una encuesta principal de ~25 ítems (6 a 7 minutos); características de 9 a 6 (se unifican canal firmado con atestación, y fallo cerrado con monitoreo); 5 condiciones de adopción; 2 preguntas abiertas; una encuesta breve aparte para desarrolladores de juegos (integración y verificación del servidor), difundida en r/gamedev; prueba piloto con 5 a 10 personas para medir el tiempo real. La decisión final queda sujeta a la opinión del tutor (pendiente de aportar). Las cifras de tiempo son estimaciones del equipo, no mediciones (UNVERIFIED hasta el piloto).

**Limitaciones.** Sesgo de autoselección (responde quien ya usa Linux y le interesa el tema); muestra pequeña de desarrolladores; tasas de abandono altas en Reddit; baterías Likert largas inducen respuestas automáticas; la anonimidad impide verificar duplicados o perfil; posible rechazo de moderadores. **El texto final del cuestionario, su fecha de publicación y las respuestas son pendiente de aportar.**

## **2.4. Presentación de datos**

### 2.4.1. Participación de Linux entre usuarios de Steam: serie histórica (compilación de panke)

**Figura 2.1. Participación de Linux en la Steam Survey, 2016-ene a 2024-jun** (compilación de panke; los huecos son meses sin dato)

![Participación de Linux en la Steam Survey por mes, 2016-2024](docs/figuras/steam-linux.png){width=90%}

Lectura: la participación de Linux pasa de 0,95 % en enero de 2016 a 2,08 % en junio de 2024, último mes con dato. El mínimo de la serie es 0,49 % (julio de 2018) y el máximo 2,32 % (mayo de 2024). En el mismo período, Windows va de 95,39 % a 96,61 % y macOS de 3,55 % a 1,31 % (enero de 2016 y junio de 2024). La serie tiene 92 meses con dato de 97; julio a noviembre de 2024 están vacíos para Linux aunque Windows y macOS sí tienen valores (dato faltante, sin interpolar). Entre las distribuciones con fila propia, Arch Linux pasa de 0,09 % (septiembre de 2019) a 0,17 % (junio de 2024) y Manjaro de 0,05 % (diciembre de 2018) a 0,06 % (junio de 2024); Ubuntu y Linux Mint aparecen fragmentadas por versión, con pocos meses cada una, por lo que su suma subestima el total.

**Figura 2.2. Sistemas operativos y distribuciones Linux visibles, 2016–2024** (compilación de panke; Ubuntu y Mint como suma de versiones visibles)

![Windows, Linux, macOS y distribuciones Linux visibles](docs/figuras/steam-so.png){width=100%}

### 2.4.2. Participación de Linux entre usuarios de Steam: dato de octubre de 2026 (lectura de la fuente de Valve)

**Tabla 2.2. Sistema operativo en la Steam Survey de octubre de 2026** (Valve, 2026)

| Sistema operativo | Participación | Variación mensual |
|---|---|---|
| Windows | 93,70 % | −1,33 pp |
| Linux | 3,95 % | +0,90 pp |
| macOS | 2,35 % | +0,43 pp |

Lectura: Linux alcanza 3,95 % en octubre de 2026, con un aumento mensual de +0,90 pp, el mayor entre los tres sistemas. Es una observación puntual obtenida de otra fuente y de otro modo que la serie de panke: no se anexa a ella. La comparación cualitativa indica que el valor de octubre de 2026 es superior a todos los valores de la compilación (máximo 2,32 %), con la reserva de que son fuentes distintas, de método y procedencia diferentes, y de que entre junio de 2024 y octubre de 2026 no hay dato. Los valores de Valve se extrajeron de la página con una herramienta automática de lectura; no hay captura archivada.

### 2.4.3. Reparto de la encuesta por idioma

La misma compilación de panke incluye el reparto por idioma de las cuentas encuestadas. Se usa para justificar los idiomas de la encuesta a *stakeholders* y de la difusión (Capítulo VII), no para dimensionar el mercado Linux.

**Figura 2.3. Reparto de la Steam Survey por idioma, 2016-ene a 2024-nov** (compilación de panke; español = Spanish hasta 2018-sep, luego España + Latinoamérica; portugués de Brasil empalmado de igual modo)

![Participación por idioma en la Steam Survey](docs/figuras/steam-idiomas.png){width=90%}

Lectura: el inglés va de 45,62 % (enero de 2016) a 33,18 % (noviembre de 2024); el chino simplificado, de 5,99 % a 30,25 %; el ruso, de 17,56 % a 9,55 %; el español (España más Latinoamérica), de 5,44 % a 4,52 %; el portugués de Brasil, de 3,86 % a 3,64 %. Hay 97 meses con dato de 107 columnas; las vacías son dato faltante. La compilación anota posibles datos anómalos en el chino simplificado, por lo que ese idioma se toma solo como contexto. Para el proyecto, el inglés sigue siendo el idioma de mayor peso individual y el español y el portugués de Brasil suman 8,16 % en noviembre de 2024, lo que justifica una encuesta y una difusión en inglés y en español y deja el portugués y el ruso como idiomas candidatos si el equipo cuenta con capacidad.

### 2.4.4. Estado de compatibilidad de anticheats en Linux

AreWeAntiCheatYet lista 1.167 juegos, con la siguiente clasificación (AreWeAntiCheatYet, 2026):

**Tabla 2.3. Juegos por estado en AreWeAntiCheatYet** (consulta 2026-11-25)

| Estado | Juegos | Participación |
|---|---|---|
| Supported | 196 | 17 % |
| Running | 280 | 24 % |
| Planned | 2 | 0 % |
| Broken | 636 | 54 % |
| Denied | 53 | 5 % |

Según el mismo sitio, *Supported* son los juegos que corren en Linux porque el desarrollador habilitó el anticheat o porque funciona sin cambios bajo Wine/Proton; *Running*, los que corren sin impacto en el juego en línea pero requieren pasos manuales; *Planned*, aquellos cuyo desarrollador declaró que planea habilitarlo; *Broken*, los que no corren en línea por el anticheat desplegado; y *Denied*, aquellos cuyo desarrollador declaró que no lo habilitará.

Lectura: el 54 % de los títulos listados figura como *Broken* y el 5 % como *Denied*; entre los *Denied* se cuentan Fortnite, Apex Legends y Valorant. El 41 % figura como *Supported* o *Running*. La lista incluye juegos sin anticheat activo o con filas sin actualizar (las filas observadas se actualizaron entre 2022 y 2024), por lo que las proporciones indican el orden de magnitud y no un estado vigente. Los conteos provienen de la cabecera de la página, leída con una herramienta automática y verificada manualmente.

### 2.4.5. Oferta existente: EAC y BattlEye bajo Proton

Los hallazgos de la investigación propia (Martínez Alarcón & Merino De Rui, 2026) se resumen en la sección D del Anexo III.6 y en `Proton-Anticheat-Research`: EAC bajo Proton es un cliente nativo (`easyanticheat_x64.so`) que incluye el desarrollador del juego y funciona en espacio de usuario; BattlEye distribuye un cliente empaquetado y virtualizado. Ambos dependen de la decisión de cada desarrollador y ninguno actúa como anticheat de kernel en Linux.

### 2.4.6. Movimiento de la industria: EAC para Linux v2

Epic Games anunció el 2026-10-14 la reconstrucción de EAC para Linux («EAC Linux v2»). Según la prensa especializada, no instala ni carga un módulo de kernel; usa un servicio de systemd que se ejecuta mientras corre un juego protegido y programas eBPF sobre BPF-LSM que restringen el acceso de otros procesos a la memoria del juego. Los requisitos informados incluyen kernel y módulos firmados, atestación de Secure Boot, arranque medido, IOMMU, *lockdown* en modo *integrity*, kexec deshabilitado y BPF-LSM activo. Fortnite es el piloto previsto, y luego se ofrecería a otros desarrolladores; no se informó fecha de lanzamiento (Phoronix, s. f.; It's FOSS, 2026). Alcance: información de prensa sobre un anuncio; el funcionamiento interno de EAC v2 no es público y no puede observarse; se describe según la documentación pública y la investigación interna del proyecto (`proton-anticheats`).

## **2.5. Análisis**

1. **Demanda potencial.** La serie de panke muestra a Linux entre 0,49 % y 2,32 % de los usuarios de Steam entre 2016 y junio de 2024, con tendencia creciente en la segunda mitad del período; la lectura de octubre de 2026 informa 3,95 %. Son dos fuentes distintas y la tendencia entre ambas no se afirma. Se trata de un segmento minoritario en términos relativos y creciente en las dos fuentes.
2. **Brecha de oferta.** La mayoría de los títulos con anticheat listados en AreWeAntiCheatYet no funciona en Linux (*Broken* 54 %, *Denied* 5 %). La disponibilidad de anticheat es una barrera de acceso, con la reserva sobre la vigencia de las filas (2.4.4).
3. **Dirección de la industria.** El anuncio de EAC v2 va hacia BPF-LSM sin módulo de kernel, el mismo mecanismo que la capa BPF-LSM de Quark. La línea técnica del proyecto se alinea con la industria; el diferencial pasa a ser la apertura del código y la documentación académica.
4. **Oportunidad.** Un segmento creciente, una oferta que depende de cada desarrollador y una solución de referencia (EAC v2) aún sin lanzamiento constituyen una oportunidad para una alternativa abierta. Esta lectura es una inferencia del equipo y se contrasta con la encuesta una vez aplicada.
5. **Lo que el relevamiento no permite concluir.** Tamaño de mercado en dinero, disposición a adoptar Quark y confianza en el código abierto, que dependen de la encuesta (no aplicada). El tamaño del segmento Linux se estima en el Capítulo IV (4.5) como rango con supuestos explícitos.

### 2.5.1. Hipótesis de demanda (provisional)

Se formula una hipótesis de demanda provisional, no estática: se revisa cuando se apliquen la encuesta y cualquier dato nuevo, y se construye con lo relevado en la sección D del Anexo III.6, en `Proton-Anticheat-Research`, en AreWeAntiCheatYet y en Steam.

**H-D1.** Existe una demanda insatisfecha de jugadores de Linux, porque el acceso a los títulos con anticheat depende de la decisión de cada desarrollador: en AreWeAntiCheatYet el 54 % de los juegos listados figura como *Broken* y el 5 % como *Denied*, y el cliente nativo de EAC bajo Proton y el cliente de BattlEye son opcionales por título (`proton-anticheats`).

**H-D2.** El segmento es minoritario pero creciente: 3,95 % en octubre de 2026 (+0,90 pp mensual) y entre 0,49 % y 2,32 % en la compilación 2016–2024, con la serie de Linux en su valor más alto de la compilación en mayo de 2024.

**H-D3.** Un anticheat abierto y auditable agrega valor frente a uno cerrado para una comunidad que eligió plataformas libres, y el diferencial real del proyecto es la apertura y la documentación, no el mecanismo, porque la industria converge hacia BPF-LSM (EAC v2).

**Supuestos.** (S1) La Steam Survey es una muestra representativa de los jugadores de PC en Linux, lo que no se verificó. (S2) La compilación de panke refleja los datos de Valve (procedencia débil, sin verificar). (S3) Los títulos *Broken* o *Denied* son relevantes para los jugadores de Linux. (S4) Los usuarios de Linux valoran la apertura; es el supuesto que la encuesta diseñada mide con una pregunta planteada a propósito en contra del proyecto.

**Qué refutaría la hipótesis.** (R1) Una cuota de Linux en Steam estancada o decreciente en lecturas posteriores. (R2) Que los desarrolladores de los títulos *Broken* habiliten EAC v2 o BattlEye para Linux y el acceso deje de ser una barrera, de modo que el proyecto pierda el nicho. (R3) Respuestas de la encuesta en las que la mayoría rechace instalar un componente de kernel de terceros o considere que publicar el código facilita la evasión. (R4) La ausencia de desarrolladores interesados en integrar el SDK.

## **2.6. Conclusiones del capítulo**

- Linux pasa de 0,95 % (2016-ene) a 2,08 % (2024-jun) de los usuarios de Steam según la compilación de panke (fuente débil), y alcanza 3,95 % en octubre de 2026 según la lectura de Valve (2026); son fuentes distintas, no se combinan en una sola serie.
- La compatibilidad de anticheats en Linux es parcial: 17 % *Supported* y 24 % *Running* sobre 1.167 juegos listados (AreWeAntiCheatYet, 2026), con filas de antigüedad variable.
- La industria incorpora BPF-LSM en EAC v2, lo que respalda la dirección técnica de Quark.
- La demanda se sostiene como hipótesis provisional (2.5.1) con supuestos y criterios de refutación explícitos; su validación con usuarios reales depende de la encuesta, diseñada y no publicada.

# **CAPÍTULO III — ENTORNO Y DOMINIO DEL SISTEMA**

## **3.1. Entorno del Sistema**

El sistema opera en equipos de escritorio o portátiles con distribuciones GNU/Linux instaladas, destinados a la ejecución de videojuegos en línea. El entorno de ejecución es heterogéneo: las distribuciones varían en versión de kernel, configuración de módulos habilitados, gestor de paquetes y políticas de seguridad activas. El sistema no asume una configuración uniforme del entorno.

Para el desarrollo y las pruebas se toma como entorno vigente Nobara Linux 43 (derivada de Fedora, con ajustes orientados al rendimiento en gaming), kernel 7.0.9, en una máquina virtual QEMU/KVM6 (`docs/vm_test_environment.md`). Una VM con CachyOS (kernel 7.3.1, compilado con clang) se menciona solo como propuesta a futuro (`vm/README.md`). El sistema opera de forma simultánea con el proceso del videojuego y con otros procesos del sistema operativo, por lo que el impacto en el rendimiento del equipo constituye una variable relevante del entorno que el diseño considera.

## **3.2. Dominio del Sistema (Variables)**

**Variables endógenas** (internas, bajo control directo del proyecto):

* **Arquitectura del módulo de kernel:** decisiones de diseño sobre qué interfaces del kernel se utilizan (`kretprobe`, Netlink, BPF-LSM7 y eBPF8) y cómo se estructuran los mecanismos de detección.  
* **Políticas de seguridad:** criterios definidos por el sistema para clasificar un comportamiento como anómalo y determinar la acción correspondiente.  
* **Rendimiento del sistema:** overhead introducido por el módulo de kernel y el servicio en espacio de usuario, ajustable mediante decisiones de implementación.  
* **Cobertura de detección:** conjunto de técnicas de trampa que el sistema es capaz de identificar, determinada por lo implementado: bloqueo de acceso de nivel *attach* (`ptrace`, `/proc/<pid>/mem`, `process_vm_readv/writev`), bloqueo de BPF de *tracing*, autoprotección del servicio, vigilancia de variables y telemetría. Límites: una DLL o `LD_PRELOAD` que escribe sin llamadas al sistema no es observable; `/proc/<pid>/maps` es legible por root (kernel ≥ 6.x); el máximo es de 16 procesos protegidos; el `kretprobe` usa `maxactive = 64`; los PID se resuelven con `task_tgid_vnr()`, sin soporte entre *namespaces* de PID.  
* **Interfaz de integración:** diseño y contrato de la API/SDK expuesta a los videojuegos, definido por el equipo de desarrollo.

**Variables exógenas** (externas, sin control directo del proyecto):

* **Versión y configuración del kernel de Linux del equipo anfitrión:** determina qué interfaces están disponibles y con qué comportamiento.  
* **Distribución GNU/Linux utilizada por el usuario:** afecta la disponibilidad de herramientas, módulos y configuraciones de seguridad por defecto.  
* **Evolución del ecosistema de soporte de Rust para módulos de kernel:** condiciona la migración futura del módulo de C a Rust; el proyecto no depende de ella en su versión actual, porque la madurez de los bindings fue insuficiente (riesgo R2). El soporte de Rust se incorporó al kernel principal en la versión 6.1 y dejó de considerarse experimental en 2025, aunque su cobertura de abstracciones internas sigue ampliándose de forma progresiva (Ojeda, 2025; The kernel development community, 2024b).  
* **Técnicas de trampa utilizadas por el software adversario:** el proyecto identifica y cubre un conjunto acotado; pueden surgir nuevas técnicas fuera del alcance.  
* **Videojuego seleccionado como caso de prueba:** sus características técnicas condicionan la forma de implementar y validar la interfaz de integración.

## **3.3. Alcance (del Sistema y del Proyecto)**

**El sistema incluye:**

* Un módulo de kernel para GNU/Linux que deniega a otros procesos el acceso a la memoria de un proceso protegido mediante `ptrace`, `/proc/<pid>/mem` y `process_vm_readv/writev`.  
* Un servicio en espacio de usuario que gestiona la comunicación entre el módulo de kernel y el videojuego, recolecta eventos y aplica políticas de seguridad.  
* Una interfaz de integración (API/SDK) que permite incorporar el sistema en videojuegos.  
* Un conjunto de pruebas (scripts de VM y 11 pruebas `#[test]` del servicio) ejecutadas sobre un juego simulado y verificadas sobre un videojuego de código abierto.  
* Documentación del diseño, la implementación y los resultados obtenidos.

**Quedan fuera del alcance del proyecto:**

* El desarrollo de un videojuego propio.  
* La compatibilidad con sistemas operativos distintos de GNU/Linux.  
* La detección de trampas mediante hardware externo o modificaciones de firmware.  
* La distribución o comercialización del sistema (el resultado es un prototipo funcional con fines académicos e investigativos).  
* La integración con plataformas de distribución de videojuegos o con anticheats de terceros.  
* El SDK del lado servidor, la prueba cliente↔servidor de punta a punta y la validación del build de *release* en hardware físico.  
* Todo lo posterior a la defensa, incluida cualquier continuación por parte del colaborador.

## **3.4. Límites y Restricciones**

* **Técnicas:** el sistema opera sobre el kernel de Linux. Las interfaces disponibles para módulos de kernel (`kretprobe`, Netlink) y para eBPF/BPF-LSM establecen límites sobre los eventos interceptables y su granularidad; Netfilter no se utiliza. El soporte de Rust para módulos de kernel presenta una madurez menor a la de C y ciertas APIs internas no cuentan con bindings estables (Ojeda, 2025), razón por la cual el módulo está en C. Las pruebas con privilegios elevados requieren entornos virtualizados para preservar la integridad de los equipos de desarrollo, y el build de producción se niega a proteger dentro de una VM: toda la validación disponible corresponde al build de pruebas.  
* **Económicas:** el proyecto se desarrolla sin financiamiento externo. Los recursos disponibles son los equipos personales de los integrantes y herramientas de software libre o de acceso gratuito. No se contempla la contratación de infraestructura en la nube ni la adquisición de licencias.  
* **Temporales:** el proyecto está acotado a los plazos del plan de estudios para el Proyecto Integrador Final, lo que delimita la profundidad alcanzable en algunas funcionalidades.  
* **Organizacionales:** el desarrollo lo realizan dos personas, el autor y un colaborador, que no presenta este PIF, lo que limita el trabajo paralelo y exige una distribución de tareas precisa. El proyecto está sujeto a las evaluaciones periódicas de los docentes de Gestión de Proyectos y Proyecto Final de Grado, que constituyen puntos de control obligatorios.

# **CAPÍTULO IV — MODELO DE NEGOCIOS DEL PROYECTO**

## **4.1. Definición de negocios**

**Actividades.** El proyecto diseña, desarrolla y documenta un sistema anticheat para GNU/Linux compuesto por un módulo de kernel (C, `kernel/quark_kernel.c`), un demonio en espacio de usuario (Rust, `quark_daemon/`) con programas eBPF, y un SDK en C (`sdk/`) que un juego integra para exigir la protección (Anexo III.6, §A). Las actividades de valor son: (a) el desarrollo y mantenimiento del código abierto; (b) la documentación técnica y de las decisiones de diseño; (c) la investigación comparada de los anticheats comerciales bajo Proton (Anexo III.6, §D); (d) la integración con motores de juego de código abierto (RecoilEngine, motor de *Beyond All Reason*).

**Mercado general.** El mercado es el de los videojuegos multijugador en línea que exigen un anticheat de nivel de kernel como condición de ejecución, y dentro de él el segmento de jugadores que usan GNU/Linux. Los anticheats comerciales se desarrollan principalmente para Windows (Wikipedia, 2026a), y en Linux su disponibilidad es optativa por título (ver 4.4); la oferta actual en esa plataforma funciona en espacio de usuario o, según información pública reciente, con BPF-LSM sin módulo de kernel. El tamaño del segmento Linux se estima en este proyecto como rango y su participación en cada título no se midió: **estimado** con fórmula y supuestos explícitos en 4.5.

**Tecnología.** Protección en Ring 0 mediante un `kretprobe` sobre `ptrace_may_access`, BPF-LSM y telemetría eBPF cargados desde el demonio, canal Netlink autenticado (uid, SHA-256 del ejecutable, firma ECDSA P-256 y nonce) y política de fallo cerrado en el SDK (Features §1–§3). El alcance validado es una máquina virtual con build de *testing* y un juego simulado, más una validación sobre el motor real (Anexo III.6, §C).

**Modelo de negocio en clave de adopción.** El proyecto no se comercializa (Cap. III, 3.3). No hay ingresos, precios ni clientes pagantes, y no se plantean. El "negocio" se define como la generación y sostenimiento de valor público: un componente abierto, auditable y reutilizable. El modelo se expresa en el CANVAS del Cap. XI.

## **4.2. Definiciones estratégicas**

**Misión y visión.** Se adoptan las del Cap. I, 1.2.

**Propuesta de valor estratégica.** A partir del relevamiento de mercado, el diferencial pasa de "nativo a nivel de kernel" a **abierto, académico y documentado** (Anexo III.6, §D): la industria converge hacia BPF-LSM sin módulo de kernel, de modo que la ventaja sostenible reside en la apertura del código, la trazabilidad de las afirmaciones (Claims-Ledger) y la documentación del diseño, no en un mecanismo exclusivo.

**Objetivos estratégicos de adopción** (derivados de los objetivos del Cap. I; ninguna meta numérica de adopción se fija, **pendiente de definir por el equipo**):
1. Publicar el repositorio bajo licencia GNU GPLv3 (Cap. VIII).
2. Mantener la integración con al menos un motor de juego de código abierto (hoy: RecoilEngine, PR #1).
3. Completar la medición pendiente (overhead, detección, falsos positivos) antes de cualquier afirmación de rendimiento (Anexo III.6, §C).

## **4.3. Análisis de rivalidad amplificada**

Se aplica el esquema de cinco fuerzas ampliado (competidores actuales, entrantes potenciales, sustitutos, proveedores, clientes) adaptado a un proyecto no comercial. Las valoraciones son cualitativas y se apoyan en las fuentes citadas; no se midió cuota de mercado alguna.

| Fuerza | Análisis | Fuente |
|---|---|---|
| Competencia actual | Easy Anti-Cheat (Epic), BattlEye, VAC (Valve) y Vanguard (Riot) dominan el segmento. En Linux, EAC y BattlEye funcionan bajo Proton solo si el desarrollador los habilita; VAC corre igual en Linux; Vanguard no se ofrece en Linux. | 4.4 |
| Competidores potenciales | Epic anunció (2026-10-14, según fuentes públicas secundarias) Easy Anti-Cheat para Linux v2 con servicio systemd y programas BPF-LSM, sin módulo de kernel. Es el mismo mecanismo que usa la capa BPF-LSM de Quark. Su funcionamiento interno no es público y no puede observarse; se describe según la documentación pública y la investigación interna del proyecto. | Anexo III.6, §D; `EAC_BPF_LSM_Service.md` |
| Sustitutos | (a) Detección del lado del servidor, que no depende del cliente; (b) no ofrecer el título en Linux; (c) juegos sin anticheat de kernel (ej. VAC en espacio de usuario). | Informe, Cap. XI previsto; GamingOnLinux (2026) |
| Proveedores | Kernel de Linux (interfaces LSM, eBPF, Netlink, kprobes), toolchain Rust/libbpf, distribuciones. Dependencia alta de la estabilidad de interfaces internas del kernel (riesgo R7) y de la configuración del usuario (BPF-LSM requiere `bpf` en `lsm=`; Features §1.5). | Informe, Cap. V 5.7; Known-Limitations |
| Clientes / adoptantes | Desarrolladores de juegos (integran el SDK; hoy un motor de código abierto) y jugadores Linux (instalan módulo y demonio). Los estudios comerciales dependen de proveedores con servicio, soporte y respaldo de servidor, que Quark no ofrece. | Anexo III.6, §A, §E |
| Barreras de entrada | Altas en lo técnico (kernel, detección, atestación) y para obtener confianza (ver Riot: Linux no permite atestar el estado de arranque ni los módulos de kernel). | GamingOnLinux (2024) |

**Lectura de rivalidad.** Quark no compite hoy por clientes comerciales: carece de SDK del lado servidor, de prueba de punta a punta cliente-servidor y de atestación verificada por servidor (Features §5; Anexo III.6, §E). Su espacio es el de la alternativa abierta, estudiable y reproducible.

## **4.4. Mapeo de competencia**

**Tabla IV-1. Mapeo de competencia (información pública, consultada el 2026-11-25).** La columna "Linux" describe el soporte según las fuentes citadas; no se midió el comportamiento de estos productos salvo donde se indica.

| Solución (proveedor) | Naturaleza técnica según fuentes | Soporte en Linux | Modelo de licenciamiento / distribución | Fuente |
|---|---|---|---|---|
| Easy Anti-Cheat (Epic Games) | Anticheat comercial, disponible gratis a través de Epic Online Services en todas las plataformas de PC (según Epic). Bajo Proton el *runtime* es un puente y el cliente nativo (`easyanticheat_x64.so`) lo aporta el juego (análisis estático propio). | Funciona vía Wine/Proton si el desarrollador lo activa en el portal de Epic (Epic, 2021). Análisis dinámico propio: un juego, sin partida en línea. | Propietario, cerrado | Epic Online Services (2021); GamingOnLinux (2021a); Wikipedia (2026b); `EAC.md` |
| BattlEye (BattlEye Innovations) | Anticheat comercial. El *runtime* de Proton distribuye el cliente real (`BEClient_x64.so`), empaquetado y virtualizado; solo legible en parte en el volcado propio. | Opt-in: el desarrollador debe solicitarlo a BattlEye (GamingOnLinux, 2021a, 2021b). Un juego puede incluir BattlEye sin habilitar Proton (GamingOnLinux, 2024b). | Propietario, cerrado | GamingOnLinux (2021a, 2021b, 2024b); `BattlEye.md` |
| VAC (Valve) | Sistema de Valve que detecta cheats en la PC del usuario con una base de cheats conocidos, similar a un antivirus; reportado como de espacio de usuario, no de kernel (descripción de terceros; Valve no publica el detalle interno). Los bans se aplican vía API de Steamworks. | La versión de Linux es idéntica a la de Windows (Valve Developer Community, s. f.). | Propietario, ligado a Steam/Steamworks | Valve Corporation (s. f.); Valve Developer Community (s. f.) |
| Vanguard (Riot Games) | Anticheat con driver; Riot afirma que necesita verificar el entorno y atestar estado de arranque y módulos de kernel. | No soportado; Riot declara que Linux no permite atestar el estado de arranque ni los módulos de kernel, y que rechaza emulación y VM. | Propietario, cerrado, ligado a títulos de Riot | GamingOnLinux (2024a) |
| Easy Anti-Cheat para Linux v2 (Epic) | Servicio systemd + programas BPF-LSM, sin módulo de kernel; ocho requisitos de plataforma (BPF-LSM, *lockdown*, Secure Boot, TPM 2.0, IOMMU, entre otros). Se describe según documentación pública y la investigación interna; su funcionamiento no es público y no puede observarse. | Nativo Linux con requisitos estrictos | Propietario | `EAC_BPF_LSM_Service.md` §0–§3; Phoronix (s. f.); It's FOSS (2026) |
| **Quark Anticheat** | Módulo de kernel (C) + BPF-LSM/eBPF + demonio (Rust) + SDK (C). Bloquea localmente `ptrace`, `/proc/<pid>/mem` y `process_vm_*` en Ring 0; bloquea BPF de *tracing*; autoprotege al demonio (Features §1). | Nativo Linux. Validado en VM, build de *testing*, juego simulado y motor real. | **Abierto**, académico, documentado (GNU GPLv3, Cap. VIII) | Features; Anexo III.6, §A, §C |

**Tabla IV-2. Comparación cualitativa de capacidades.** «Sí/No/No público» según información pública; la comparación con EAC es contra información pública y documentación, no contra su comportamiento medido (que no es público).

| Capacidad | EAC (Proton) | BattlEye (Proton) | VAC | Vanguard | Quark |
|---|---|---|---|---|---|
| Código auditable por terceros | No | No | No | No | Sí (GNU GPLv3) |
| Funciona en Linux | Si el juego lo activa | Si el juego lo activa | Sí | No | Sí (prototipo) |
| Bloqueo local de acceso a memoria en Ring 0 en Linux | No público (EAC v2 anuncia BPF-LSM) | No público | No (reportado espacio de usuario) | No aplica | Sí, validado solo en VM/build de pruebas |
| Atestación verificada por servidor | No público | No público | No público | Sí declarado necesario (Riot) | No (brecha identificada) |
| Servicio y soporte comercial | Sí | Sí | Sí | Sí | No |
| Overhead medido | No medido (decisión de alcance) | No medido | No medido | No medido | No medido (pendiente, H5) |

**Decisión de alcance: no se mide el overhead de los competidores.** Los competidores son de espacio de usuario o de funcionamiento no público, no ofrecen la misma protección y medirlos de forma comparable es inabarcable para este proyecto; por eso la fila de overhead no se completa y la comparación es cualitativa.

**Otros competidores.** Otros productos (por ejemplo FACEIT Anti-Cheat, Ricochet, XIGNCODE) quedan fuera del alcance del mapeo por decisión de alcance; no se identificó, en este relevamiento, un anticheat de nivel de kernel abierto para Linux equivalente, y la búsqueda no fue exhaustiva.

**Conclusión del mapeo.** Los competidores existentes son cerrados y, salvo VAC, requieren el consentimiento del estudio para operar en Linux; la industria avanza hacia BPF-LSM. Quark ocupa el nicho de alternativa abierta y documentada, con brechas explícitas frente a la industria (atestación por servidor, SDK de servidor, canal de mensajes, reporte tipado).

## **4.5. Estimación del segmento Linux (best-effort)**

El tamaño del segmento se estima como rango con una fórmula simple, usando solo datos citados. No es una medición.

**Fórmula.** Segmento ≈ U × s, donde U son los usuarios mensuales de Steam y s es la participación de Linux en la Steam Survey.

- **s = 3,95 %** (octubre de 2026; Valve, 2026). La compilación 2016–2024 (panke, 2024) es otra fuente y no se mezcla en la fórmula.
- **U, escenario bajo = 132 millones**: usuarios activos mensuales a fin de 2021 (GamingOnLinux, 2022, que reproduce el informe anual de Valve).
- **U, escenario alto ≈ 210 millones**: el escenario bajo escalado por la razón entre el récord de usuarios simultáneos de octubre de 2026 (43,5 millones; Dot Esports, 2026) y el de 2021 (27,4 millones; GamingOnLinux, 2022): 132 × 43,5 / 27,4 ≈ 210 millones.

**Resultado.** Escenario bajo: 132 × 0,0395 ≈ 5,2 millones. Escenario alto: 210 × 0,0395 ≈ 8,3 millones. Rango: **entre 5 y 8 millones de usuarios mensuales de Steam en Linux**, redondeado.

**Supuestos.** (a) La Steam Survey es representativa de todos los usuarios de Steam, lo que no se verificó. (b) Los usuarios mensuales crecen en proporción al pico de usuarios simultáneos, supuesto fuerte porque no hay un dato oficial reciente de usuarios mensuales. (c) La participación de la encuesta de octubre de 2026 se aplica al total, con la variación mensual de +0,90 pp que sugiere volatilidad; un valor distinto en otro mes cambia el resultado de forma proporcional.

**Lo que la estimación no cubre.** La fracción de esos usuarios que juega títulos con anticheat de kernel no tiene cifra citable, por lo que se expresa solo como una fracción desconocida f (0 ≤ f ≤ 1) y el mercado direccionable es f × (5 a 8 millones). No se estiman unidades vendidas ni ingresos, porque el proyecto no se comercializa.

**Qué la refutaría.** Un dato oficial de Valve de usuarios mensuales actuales, un sesgo demostrado de la encuesta o una participación de Linux sustancialmente distinta en lecturas posteriores.

# **CAPÍTULO V — PLANIFICACIÓN DEL PROYECTO**

## **5.1. Definición de Etapas**

El proyecto se organiza en cuatro etapas secuenciales:

* **Etapa 1: Análisis técnico (meses 5 y 6).** Estudio de las interfaces de programación del kernel de GNU/Linux orientadas a la telemetría y monitorización de procesos en tiempo real. Identificación y clasificación de técnicas de trampa y vectores de ataque comunes en videojuegos multijugador. Modelización del sistema real para comprender las variables exógenas que afectan el rendimiento del juego, garantizando que la monitorización a nivel de kernel no introduzca latencia perceptible.  
* **Etapa 2: Diseño arquitectónico (meses 6 y 7).** Definición formal de la arquitectura del módulo, incluyendo la especificación de los hooks de seguridad y los puntos de intercepción dentro del espacio del kernel. Diseño del modelo de comunicación entre el espacio de usuario y el kernel. Elaboración de los diagramas de arquitectura que documenten dependencias entre componentes, interfaces expuestas y restricciones de seguridad.  
* **Etapa 3: Desarrollo del módulo (meses 7, 8, 9 y 10).** Codificación en C del módulo de kernel, del SDK y de los programas eBPF, y en Rust del servicio en espacio de usuario. Ejecución de pruebas de integración en entornos controlados y aislados mediante QEMU/KVM con scripts y herramientas de ataque propias; las pruebas de carga, condiciones de carrera y entradas malformadas quedan pendientes.  
* **Etapa 4: Validación y soporte (meses 10 y 11).** Etapa en curso al 2026-11-25. Cumplido: integración y verificación sobre RecoilEngine (Beyond All Reason). Falta: medición del impacto sobre el rendimiento, tasas de detección y falsos positivos. Los resultados alimentan el ciclo siguiente del modelo en espiral, permitiendo identificar vectores no contemplados y ajustar los mecanismos de detección. Incluye la preparación de la documentación final y la defensa del PIF.

**Ejecución real (reconstruida desde git).** Como pauta del informe, lo ocurrido prevalece sobre lo planeado. El historial de `Dev` muestra seis ciclos, reconstruidos a posteriori y no registrados en su momento ([[Cycle-Log]]):

**Tabla V-1. Ciclos de ejecución real** (fuente: historial de git, reconstrucción)

| Ciclo | Fecha | Contenido | Commit de referencia |
| :---- | :---- | :---- | :---- |
| C1 | 2026-06-11 | Primer prototipo | `9b9aa22` |
| C2 | 2026-06-25 | Protección en Ring 0 (`kretprobe`) | `174e467` |
| — | 2026-06-26 a 2026-08-27 | Sin commits; la causa no consta (UNVERIFIED) | — |
| C3 | 2026-08-27/28 | Integración con el motor real | `6b05ad7` |
| C4 | 2026-08-29/31 | Endurecimiento: fallo cerrado, detección de VM, canal autenticado | `2624ae4`, `333bbe2`, `48cc3f6`, `2216684` |
| C5 | 2026-09-30 a 2026-10-05 | BPF-LSM y telemetría | `e497dbf` |
| C6 | 2026-11-05/06 | Linter e instalador | `35c6031` (Dev); `2b088ab` (rama sin integrar) |

## **5.2. Entregables por etapa**

**Tabla V-2. Entregables por etapa y estado al 2026-11-25**

| Etapa | Entregable principal | Estado |
| ----- | ----- | ----- |
| 1 — Análisis técnico | Documento de diseño preliminar (E1.4): decisión sobre bindings de Rust, vectores de ataque, videojuego de prueba | La decisión de R2 (C en el módulo), la elección de RecoilEngine/BAR y los vectores cubiertos constan en fuentes dispersas; el documento E1.4 como tal no consta |
| 2 — Diseño arquitectónico | Diagramas de arquitectura (E2.3): hooks, modelo de comunicación kernel↔usuario, dependencias e interfaces | El Capítulo IX documenta la arquitectura real, con tablas de flujos e interfaces |
| 3 — Desarrollo del módulo | Módulo de kernel compilado (v0.4.0) y operativo en VM, servicio de espacio de usuario, API/SDK y pruebas (E3.1–E3.4) | Cumplido en lo esencial; sin SDK de servidor |
| 4 — Validación y soporte | Informe de validación (tasas de detección y falsos positivos), medición de overhead de CPU/RAM, documentación final y defensa (E4.1–E4.4) | En curso: integración con motor real lograda; mediciones pendientes |

## **5.3. Organización del Equipo**

El proyecto lo desarrollan dos personas con roles diferenciados, pero la presentación y la defensa del PIF corresponden a una sola.

* **Martínez Alarcón, Gabriel Sebastián — autor, líder de proyecto y analista.** Responsable de la planificación, el seguimiento, la gestión de riesgos, la redacción del informe y la defensa, que realiza en febrero; participa además en el desarrollo.
* **Merino De Rui, Stefano Nahuel — colaborador, analista y desarrollador.** Colabora con atribución en la arquitectura técnica y la implementación del código y es titular del repositorio de trabajo; no presenta ni defiende este PIF porque adeuda materias para ser elegible.
* **Cátedra de Proyecto Final de Grado:** Ing. Sergio Lapertosa, Ing. Augusto Portillo e Ing. Martin Jones.

El equipo se comunica de forma asincrónica y realiza reuniones de seguimiento para la revisión de hitos. Todo lo posterior a la defensa queda fuera del alcance del informe.

## **5.4. Cronograma (Gantt)**

El cronograma planificado se estructura en cuatro etapas distribuidas entre mayo y noviembre de 2026, con un horizonte total de siete meses; la ejecución real se resume en la Tabla V-1. Las etapas de análisis técnico y diseño arquitectónico se solapan parcialmente en junio. El desarrollo del módulo concentra la mayor parte del esfuerzo, de julio a octubre, con las pruebas corriendo en paralelo. La validación se inicia en octubre solapada con el cierre del desarrollo, dejando noviembre para pruebas finales, medición de rendimiento, documentación y defensa.

**Tabla V-3. Cronograma Gantt planificado** (■ = mes planificado de la etapa; el detalle por actividad se infiere del orden y las dependencias)

| N° | Actividad | Dependencias | May | Jun | Jul | Ago | Sep | Oct | Nov |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| E1 | Etapa 1: Análisis técnico |  | ■ | ■ |  |  |  |  |  |
| E1.1 | Estudio de API Kernel | \- |  |  |  |  |  |  |  |
| E1.2 | Identificación y clasificación de técnicas de trampa | \- |  |  |  |  |  |  |  |
| E1.3 | Modelización del sistema y variables exógenas | E1.1, E1.2 |  |  |  |  |  |  |  |
| E1.4 | Producción del documento de diseño preliminar | E1.3 |  |  |  |  |  |  |  |
| E2 | Etapa 2: Diseño arquitectónico |  |  | ■ | ■ |  |  |  |  |
| E2.1 | Especificación de hooks de seguridad e intercepción | E1 |  |  |  |  |  |  |  |
| E2.2 | Diseño del modelo de comunicación kernel/usuario | E2.1 |  |  |  |  |  |  |  |
| E2.3 | Elaboración de diagramas de arquitectura | E2.2 |  |  |  |  |  |  |  |
| E3 | Etapa 3: Desarrollo del módulo |  |  |  | ■ | ■ | ■ | ■ |  |
| E3.1 | Implementación del módulo de kernel (C) | E2 |  |  |  |  |  |  |  |
| E3.2 | Implementación del servicio en espacio de usuario (Rust) | E3.1 |  |  |  |  |  |  |  |
| E3.3 | Implementación de la API/SDK de integración (C) | E3.2 |  |  |  |  |  |  |  |
| E3.4 | Pruebas de integración (QEMU/KVM) | E3.1 |  |  |  |  |  |  |  |
| E4 | Etapa 4: Validación y soporte |  |  |  |  |  |  | ■ | ■ |
| E4.1 | Integración con videojuego open source | E3 |  |  |  |  |  |  |  |
| E4.2 | Ejecución de casos de prueba y registro de resultados | E4.1 |  |  |  |  |  |  |  |
| E4.3 | Medición de impacto en rendimiento (CPU/RAM) | E4.1 |  |  |  |  |  |  |  |
| E4.4 | Documentación final y preparación de defensa | E4.2, E4.3 |  |  |  |  |  |  |  |

## **5.5. Análisis PERT/CPM**

El análisis PERT identifica trece actividades distribuidas en cuatro etapas, con duraciones estimadas mediante la ponderación de tiempos optimistas, más probables y pesimistas. El camino crítico recorre las actividades E1.1/E1.2 → E2.1/E2.2 → E3.1 → E4.1 → E4.2 → E4.4, con una duración total esperada de 19 semanas. Las actividades E1.3, E2.3 y E4.3 presentan holgura y no condicionan el plazo final. La actividad de mayor varianza es E3.1 (desarrollo del módulo de kernel, Var \= 2,25), lo que la identifica como el principal factor de riesgo sobre el cronograma.

**Tabla V-4. Tiempos PERT del proyecto** (tiempos en semanas)

| ID | Precedente | T. optimista | T. medio | T. pesimista | T. esperado | Varianza |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| E1.1 | \- | 1 | 2 | 4 | 2,2 | 0,25 |
| E1.2 | \-  | 1 | 2 | 4 | 2,2 | 0,25 |
| E1.3 | E1.1, E1.2 | 0,5 | 1 | 2 | 1,1 | 0,06 |
| E2.1 | E1.1, E1.2 | 1 | 2 | 4 | 2,2 | 0,25 |
| E2.2 | E1.1, E1.2 | 1 | 2 | 3 | 2,0 | 0,11 |
| E2.3 | E1.3 | 0,5 | 1 | 2 | 1,1 | 0,06 |
| E3.1 | E2.1, E2.2 | 5 | 8 | 14 | 8,5 | 2,25 |
| E3.2 | E2.1, E2.2 | 2 | 4 | 7 | 4,2 | 0,69 |
| E3.3 | E3.2 | 2 | 4 | 7 | 4,2 | 0,69 |
| E4.1 | E3.1, E3.3, E2.3 | 1 | 2 | 3 | 2,0 | 0,11 |
| E4.2 | E4.1 | 1 | 2 | 4 | 2,2 | 0,25 |
| E4.3 | E4.1 | 1 | 1,5 | 3 | 1,7 | 0,11 |
| E4.4 | E4.2, E4.3 | 1 | 2 | 3 | 2,0 | 0,11 |

**Figura 1. Grafo PERT con CPM del proyecto.** Los precedentes de cada actividad constan en la Tabla V-4 y el camino crítico se describe arriba (E1.1/E1.2 → E2.1/E2.2 → E3.1 → E4.1 → E4.2 → E4.4; 19 semanas). La lámina gráfica del grafo original no se incorpora a esta versión; la reconstrucción visual a partir de la Tabla V-4 es una tarea editorial pendiente de una persona.

## **5.6. Estimación de Tamaño y Esfuerzo**

### **Estimación SLOC por componente (planificación)**

Para proyectos de complejidad similar en el ecosistema Linux, la estimación de origen fue la siguiente:

**Tabla V-5. Estimación de SLOC por componente (planificación de origen)**

| Componente | Descripción | SLOC estimado |
| :---- | :---- | :---- |
| Módulo de kernel (C + Rust) | Supervisión de procesos, memoria, eBPF, hooks LSM | 3.000 – 4.500 |
| Servicio en espacio de usuario | Daemon, comunicación kernel↔juego, políticas | 2.000 – 3.000 |
| API/SDK de integración | Interfaz para videojuego, protocolo, bindings | 1.000 – 1.500 |
| Suite de pruebas | Casos de prueba, scripts, mocks | 800 – 1.200 |
| Total |  | 6.800 – 10.200 |

El valor central adoptado fue **8.000 SLOC**. Esa estimación se conserva como referencia de planificación.

### **Tamaño real medido (Dev@35c6031)**

Como pauta general, prevalece lo ocurrido: el tamaño real se mide en el árbol de `Dev` en el commit `35c6031`. Comando: `python tooling/sloc.py ../quark-wt/Dev`. SLOC = líneas no vacías y no solo comentario (`//`, `/* */` y `#` en shell), contadas con la heurística de `tooling/sloc.py`. Exclusiones: `Cargo.lock`, `Makefile`, la documentación, el submódulo `RecoilEngine`, el código de terceros y las 11 pruebas `#[test]` del servicio, que están dentro de `main.rs` y `bpf.rs` y no se separan. No se usó `cloc` ni `tokei` porque no están instalados en el entorno de medición.

**Tabla V-6. SLOC real por componente (Dev@35c6031)**

| Componente | Archivos | SLOC |
| :---- | :---- | :---- |
| Módulo de kernel (C) | `kernel/quark_kernel.c` (417), `kernel/quark_pubkey.h` (4) | 421 |
| Servicio en espacio de usuario (Rust) | `main.rs` (481), `bpf.rs` (366), `build.rs` (18) | 865 |
| Programas eBPF (C) | `quark.bpf.c` (240), `quark_events.h` (25) | 265 |
| Cliente de control `quark_cli` (C) | `quark_cli.c` | 197 |
| SDK (C) | `quark_sdk.c` (210), `quark_sdk.h` (19) | 229 |
| Subtotal del producto | | 1.977 |
| Pruebas y harness (C, Bash) | `game.c` (88), `cheat.c` (65), `run_test*.sh` (345), `capture.sh` (287) | 785 |
| Total | | 2.762 |

El tamaño real (2,762 KSLOC con pruebas; 1,977 KSLOC solo el producto) es menor que la estimación de origen (8 KSLOC); el módulo de kernel no contiene Rust. La comparación es entre un prototipo y una estimación de planificación y no implica sobreestimación ni subestimación de esfuerzo.

### **Story Points del módulo de kernel**

Para el componente de kernel, que no se mide bien con SLOC puro, la planificación aplicó estimación por Story Points:

**Tabla V-7. Estimación en Story Points del módulo de kernel (planificación de origen)**

| Historia / Tarea | Complejidad | SP |
| :---- | :---- | :---- |
| Configuración del entorno de desarrollo de módulos kernel | Media | 5 |
| Implementación de hooks LSM básicos | Alta | 13 |
| Supervisión de procesos con eBPF | Muy alta | 21 |
| Detección de accesos anómalos a memoria | Muy alta | 21 |
| Canal de comunicación kernel ↔ userspace (Netlink) | Alta | 13 |
| Manejo de errores y estabilidad del módulo | Alta | 13 |
| Integración con Rust for Linux | Alta | 13 |
| Total módulo de kernel |  | 99 SP |

El ítem «Integración con Rust for Linux» no se ejecutó; el esfuerzo se reasigna a BPF-LSM y al canal autenticado. No hay registro de Story Points reales, por lo que no se informan.

### **Ajuste de complejidad COCOMO II**

Se mantiene la metodología: el modelo utiliza factores de escala y multiplicadores de esfuerzo (cost drivers) para ajustar la estimación (Boehm et al., 2000).

**Tabla V-8. Factores de costo COCOMO II (sin cambios respecto de la planificación)**

| Factor | Descripción | Nivel | Multiplicador |
| :---- | :---- | :---- | :---- |
| RELY | Fiabilidad requerida | Alto (fallo = kernel panic) | 1,10 |
| CPLX | Complejidad del producto | Muy alto (desarrollo de kernel) | 1,34 |
| ACAP | Capacidad del equipo | Bajo | 1,19 |
| PCAP | Experiencia en el dominio | Muy bajo | 1,29 |
| AEXP | Experiencia en la plataforma | Bajo | 1,13 |
| PLEX | Experiencia en el entorno | Bajo | 1,09 |
| LTEX | Experiencia en lenguaje/herramienta | Bajo (eBPF, Rust, C de kernel) | 1,20 |
| TOOL | Uso de herramientas de desarrollo | Nominal | 1,00 |
| SCED | Restricción de cronograma | Nominal | 1,00 |

**Factor de ajuste compuesto (EAF).** EAF = 1,10 × 1,34 × 1,19 × 1,29 × 1,13 × 1,09 × 1,20 × 1,00 × 1,00 ≈ **3,34**. La versión de origen informaba 3,76; el producto de los mismos multiplicadores es 3,34, por lo que se corrige el valor.

### **Estimación del esfuerzo (recalculada con el tamaño real)**

Fórmula aplicada, sin cambios: **Esfuerzo = A × (KSLOC)^B × EAF**, con A = 3,0, B = 1,12 y EAF = 3,34. Cambian las entradas: KSLOC pasa de 8,0 (estimado) a 2,762 (medido, con pruebas, comparable con el 8,0 de origen, que incluía la suite de pruebas) y a 1,977 (solo producto).

* Con 2,762 KSLOC: (2,762)^1,12 ≈ 3,12; esfuerzo = 3,0 × 3,12 × 3,34 ≈ **31,3 personas-mes** en forma pura; con el factor de reducción de 0,15 para un proyecto académico de alcance acotado, ≈ **4,7 personas-mes**; con el mes académico de 80 h/persona, ≈ **376 horas-persona**.
* Con 1,977 KSLOC: (1,977)^1,12 ≈ 2,14; esfuerzo ≈ 21,5 personas-mes en forma pura, ≈ 3,2 con reducción, ≈ 258 horas-persona.
* Referencia de origen: 8,0 KSLOC con EAF = 3,76 dio ≈ 116 personas-mes puras y ≈ 1.392 horas-persona; con el EAF corregido, ≈ 103 personas-mes puras y ≈ 1.236 horas-persona.

**Tabla V-9. Resumen de la estimación de esfuerzo**

| Métrica | Origen (planificación) | Recalculado (tamaño real, con pruebas) |
| :---- | :---- | :---- |
| KSLOC | 8,0 (estimado) | 2,762 (medido) |
| EAF | 3,76 (con error de cálculo) | 3,34 |
| Esfuerzo puro (personas-mes) | ≈ 116 (≈ 103 con EAF corregido) | ≈ 31,3 |
| Esfuerzo con reducción 0,15 (personas-mes) | ≈ 17,4 (≈ 15,5 con EAF corregido) | ≈ 4,7 |
| Horas-persona equivalentes (80 h/mes) | ≈ 1.392 (≈ 1.236) | ≈ 376 |
| Story Points del módulo de kernel | 99 SP | sin registro de SP reales |

**Significado.** El resultado dice cuánto esfuerzo requeriría construir, con la productividad del modelo y el perfil de equipo declarado, un producto del tamaño real medido; no dice cuántas horas se trabajaron. No hay registro de horas reales (Capítulo XII), por lo que no se atribuye ninguna hora real al proyecto ni se contrasta el cálculo con una ejecución medida.

*Nota metodológica: las constantes A = 3,0 y B = 1,12 corresponden a la calibración del modo semi-detached del COCOMO intermedio (Boehm, 1981). La versión COCOMO II reemplaza el exponente fijo por uno derivado de cinco factores de escala y emplea constantes nominales A = 2,94 y B = 0,91 (Boehm et al., 2000). Se mantiene el cálculo original del proyecto y se deja constancia de la distinción para una eventual recalibración.*

## **5.7. Gestión de Riesgos**

Se identifican catorce riesgos: los siete primeros se planificaron y los siete restantes se observaron durante el desarrollo ([[Risk-Register]]).

**Tabla V-10. Identificación de riesgos y estado al 2026-11-25**

| ID | Riesgo | Categoría | Prob. | Impacto | Estado |
| :---- | :---- | :---- | :---- | :---- | :---- |
| R1 | Inestabilidad del módulo de kernel durante el desarrollo (kernel panics frecuentes) | Técnico | Alta | Alto | Vigente; sin registro de panics por sesión |
| R2 | Madurez insuficiente de los bindings de Rust for Linux para las APIs requeridas | Técnico | Alta | Alto | Materializado; contingencia aplicada: módulo en C, servicio en Rust, BPF-LSM con `libbpf-rs` |
| R3 | Subestimación del esfuerzo en el módulo de kernel | Planificación | Media | Alto | Vigente; sin registro de esfuerzo real |
| R4 | Incompatibilidad con versiones de kernel distintas a la de referencia | Técnico | Media | Medio | Vigente; solo se probó el kernel 7.0.9 |
| R5 | Disponibilidad reducida de algún integrante | Organizacional | Media | Alto | Vigente |
| R6 | Limitaciones del videojuego open source que dificulten la integración | Técnico | Baja | Medio | Mitigado: integración lograda con RecoilEngine/BAR |
| R7 | Cambios en interfaces internas del kernel | Externo | Baja | Alto | Vigente |
| R8 | Procedencia del build de validación no registrada (causa probable `2624ae4`) | Técnico | n/d | n/d | Residual: no se registró `git_commit` en las capturas |
| R9 | Deriva de repositorios de la VM que rompe builds | Técnico | n/d | n/d | Observado |
| R10 | Socket de control sin autenticar | Seguridad | n/d | n/d | Mitigado; residual: `SocketMode=0666` |
| R11 | La validación solo puede hacerse con build de pruebas (el de release se niega a proteger en una VM) | Técnico | Alta | Alto | Vigente |
| R12 | Documentación que contradice al código | Calidad | Alta | Medio | Corregido en esta versión del informe |
| R13 | Divergencia de ramas | Configuración | Alta | Medio | Vigente |
| R14 | Overhead sin medir con poco tiempo restante | Técnico | Alta | Alto | Vigente |

**Planes preventivos y contingentes**

* **R1 — Inestabilidad del módulo de kernel.** *Preventivo:* todo el desarrollo y prueba se realiza en entornos virtualizados (QEMU/KVM); se adopta una estrategia de incrementos mínimos. *Contingente:* si la tasa de panics impide el avance, se reduce el alcance al conjunto mínimo, a saber, el `kretprobe` sobre `ptrace_may_access`, y se posponen las funcionalidades eBPF de mayor complejidad. En la ejecución real ocurrió lo inverso: eBPF/BPF-LSM se implementó. Salvedad: la validación en VM usa el build de pruebas (R11).
* **R2 — Madurez insuficiente de Rust for Linux.** *Preventivo:* se evalúa el estado de los bindings por API, determinando qué se implementa en Rust y qué requiere C, coherente con la naturaleza progresiva del soporte de Rust en el kernel (Ojeda, 2025). *Contingente:* los componentes sin bindings estables se implementan en C. *Estado:* materializado y contingencia ejecutada; además, un LSM clásico no puede registrarse desde un módulo fuera del árbol, por lo que la capa LSM se obtiene con BPF-LSM.
* **R3 — Subestimación del esfuerzo.** *Preventivo:* la estimación de 99 SP se revisa al cierre de cada iteración; si la velocidad sostenida cae por debajo de 6 SP/semana durante dos semanas consecutivas, se activa una revisión de alcance. *Contingente:* se define un conjunto de funcionalidades prescindibles que pueden eliminarse del prototipo sin comprometer la demostración de viabilidad.
* **R4 — Incompatibilidad entre versiones de kernel.** *Preventivo:* el módulo se compila contra los *headers* del equipo; los kernels de prueba son 7.0.9 (Nobara 43) y, como propuesta futura, 7.3.1 (CachyOS). El soporte de otras versiones no se verificó y no se fija una versión mínima. *Contingente:* las incompatibilidades detectadas se documentan como limitaciones conocidas.
* **R5 — Disponibilidad reducida de un integrante.** *Preventivo:* las reuniones de seguimiento reducen la dependencia crítica. *Contingente:* se renegocia el alcance con los docentes en la revisión de hito más próxima, priorizando el núcleo funcional.
* **R6 — Limitaciones del videojuego seleccionado.** *Estado:* mitigado; la integración con RecoilEngine/Beyond All Reason se logró. El plan de evaluar al menos dos candidatos no consta como ejecutado.
* **R7 — Cambios en interfaces internas del kernel.** *Preventivo:* se evitan las interfaces experimentales y se documentan los kernels de prueba. *Contingente:* si una actualización rompe funcionalidades, el entorno se fija en la versión estable y no se actualiza hasta el cierre.

## **5.8. Hitos de Control**

**Tabla V-11. Hitos de control y estado al 2026-11-25**

| Hito | Descripción | Fecha estimada | Entregable asociado | Estado al 2026-11-25 |
| :---- | :---- | :---- | :---- | :---- |
| H1 | Cierre de Etapa 1: análisis técnico completo | Fin de junio 2026 | Documento de diseño preliminar (E1.4) | El documento E1.4 como tal no consta |
| H2 | Cierre de Etapa 2: arquitectura definida | Fin de julio 2026 | Diagramas de arquitectura (E2.3) | Arquitectura documentada en el Capítulo IX |
| H3 | Módulo de kernel funcional en entorno virtualizado | Fin de agosto 2026 | Módulo compilado (E3.1) | Cumplido el 2026-06-25 (`174e467`), antes de lo planificado |
| H4 | Sistema completo integrado y probado | Fin de octubre 2026 | Suite de pruebas ejecutada (E3.4) | Cumplido en lo esencial (motor real 2026-08-28/31; BPF-LSM 2026-10-05); el criterio de 75 % de casos aprobados no se calculó |
| H5 | Validación sobre videojuego y documentación final | Mediados de noviembre 2026 | Informe final y defensa (E4.4) | Abierto; defensa en febrero |

**Criterios de aprobación por hito.** H1: documento de diseño preliminar aprobado por la cátedra; ICC ≥ 80 %. H2: diagramas completos y revisados; desvío de esfuerzo ≤ 20 %. H3: el módulo carga sin errores en QEMU/KVM y registra al menos un evento de supervisión; 0 kernel panics no controlados (sin registro de panics). H4: al menos el 75 % de los casos de prueba aprobados; velocidad de SP sostenida. H5: integración con videojuego funcionando, documentación completa y defensa realizada en fecha.

## **5.9. Descripción del MVP**

El Producto Mínimo Viable es un prototipo funcional compuesto por el módulo de kernel (C), el servicio en espacio de usuario (Rust) y el SDK (C), integrado con RecoilEngine. Impide el acceso externo a la memoria del proceso protegido por `ptrace`, `/proc/<pid>/mem` y `process_vm_*`, bloquea la carga de programas BPF de *tracing* y se autoprotege. Se valida en una VM con el build de pruebas. No incluye SDK de servidor ni medición de rendimiento. El MVP se congela en `Dev@35c6031`; la rama `feature/gameStartProtection` (`2b088ab`) es trabajo adicional sin integrar. Su descripción detallada está en el Capítulo IX y en el Anexo III.

# **CAPÍTULO VI — METODOLOGÍAS DE GESTIÓN**

## **6.1. Técnicas y Prácticas de Ingeniería de Software**

Se declara el **modelo en espiral** como metodología de origen, con prácticas de **SCRUM** (Boehm, 1988; Schwaber & Sutherland, 2020). El modelo en espiral organiza el desarrollo en ciclos sucesivos guiados por el riesgo; cada ciclo atraviesa las fases de determinación de objetivos, identificación y resolución de riesgos, desarrollo y validación, y planificación de la siguiente iteración. La elección respondió a la naturaleza del dominio: el desarrollo de un módulo de kernel exige rigor estructural y trazabilidad, y la naturaleza evolutiva de las amenazas hace inviable un modelo lineal.

**Ejecución real.** El historial de git muestra prototipos sucesivos cada vez más realistas, integrados por *pull request* en `Dev`, en seis ciclos reconstruidos (Tabla V-1), sin *sprints* ni análisis de riesgo escrito por ciclo. La decisión ADR-001, aceptada por el autor, establece presentar el proceso como **prototipado evolutivo guiado por riesgo**: el modelo en espiral queda como declaración de origen y los ciclos C1–C6 son una reconstrucción desde git, no un registro de la época. La línea de aceptación en la ADR, que forma parte de la zona de evidencia, queda por agregarse. Como pauta general, ante un conflicto entre lo planeado en origen y lo ocurrido, prevalece lo ocurrido. No se registran *sprints*.

## **6.2. Trazabilidad del Proyecto**

El historial de git (29 commits en `Dev` y 3 *pull requests* integrados) registra el avance real; el repositorio de trabajo es del colaborador. Los mensajes de commit no mencionan identificadores de actividad del Gantt y no existe registro de horas, por lo que los indicadores de cumplimiento de cronograma y de desvío de esfuerzo no pueden calcularse con datos de la época. El tablero Kanban del vault complementa el seguimiento.

## **6.3. Gestión de la Configuración**

La gestión de la configuración se apoya en el sistema de control de versiones del repositorio, que conserva el historial de cambios del módulo de kernel, el servicio de usuario, la API/SDK y la suite de pruebas. La documentación técnica registra los kernels de prueba (7.0.9 en Nobara 43; 7.3.1 en CachyOS como propuesta futura) y no fija una versión mínima soportada; el módulo se compila contra los *headers* de cada equipo y `vmlinux.h` se genera por equipo, con relocalizaciones CO-RE (ver R4 y R7, Capítulo V). El control de versiones usa ramas con integración por *pull request*; el estado de las ramas está en el Anexo III.

## **6.4. Testing del Proyecto**

Las pruebas se ejecutan en una VM QEMU/KVM con el build de pruebas del módulo. Comprenden scripts de escenario (`run_test.sh`, `run_test_kernel.sh`, `run_test_kernel_release.sh`, `run_test_no_quark.sh`, `capture.sh`), 11 pruebas `#[test]` en el servicio (9 en `bpf.rs` y 2 en `main.rs`; una exige root) y la tabla de verificación de `docs/vm_test_environment.md`, sobre un juego simulado y sobre RecoilEngine/BAR. Las tasas de detección y de falsos positivos no se midieron. El harness tiene defectos conocidos (`results.csv` malformado, `summary.txt` que solo reporta la condición B). La cita de New Relic (2025) respalda una afirmación general sobre eBPF y no una medición de Quark. Las pruebas de carga, condiciones de carrera y entradas malformadas quedan pendientes.

## **6.5. Indicadores de Seguimiento**

Se definen cinco indicadores distribuidos en las dimensiones de tiempo, costo y calidad.

1. **Cumplimiento de Cronograma (ICC) — Tiempo.** ICC \= (Actividades completadas en fecha / Actividades planificadas) × 100\. Meta: ≥ 80 % en cada punto de control. Frecuencia: al cierre de cada etapa.  
2. **Velocidad de Desarrollo en Story Points — Tiempo/Esfuerzo.** Velocidad \= SP completados / semanas transcurridas en E3. Meta: ≥ 6 SP/semana promedio. Frecuencia: semanal durante la Etapa 3\.  
3. **Desvío de Esfuerzo (DE) — Costo.** DE \= ((Horas reales acumuladas − Horas planificadas acumuladas) / Horas planificadas acumuladas) × 100\. Meta: ≤ ±20 % en cada punto de control. Frecuencia: mensual.  
4. **Tasa de Detección en Pruebas (TDP) — Calidad.** TDP \= (Casos de prueba aprobados / Casos ejecutados) × 100\. Meta: ≥ 75 % al cierre de E4.2. Frecuencia: por suite de pruebas.  
5. **Estabilidad del Módulo de Kernel — Calidad.** Cantidad de kernel panics o fallos críticos durante las sesiones de prueba en QEMU/KVM. Meta: 0 kernel panics no controlados al cierre de E3.4. Frecuencia: por sesión de prueba.

El seguimiento previsto es una reunión de sincronización semanal y una revisión formal por hito, que mide los indicadores, los compara contra las metas y decide continuar, ajustar o recuperar el plan.

**Tabla VI-1. Indicadores: meta y valor al 2026-11-25**

| Indicador | Meta | Valor al 2026-11-25 |
| :---- | :---- | :---- |
| ICC | ≥ 80 % | Sin registro |
| Velocidad en SP | ≥ 6 SP/semana | Sin registro |
| Desvío de esfuerzo | ≤ ±20 % | Sin registro de horas |
| TDP | ≥ 75 % | No medido |
| Estabilidad del módulo | 0 panics no controlados | Sin registro de panics por sesión |

No existen revisiones por hito documentadas en su momento; los resultados que se disponen se recogen en el Capítulo XII.

# **CAPÍTULO VII — MARKETING DEL PROYECTO**

## **7.1. Descripción de Producto/Experiencia**

Quark Anticheat es un sistema anticheat nativo para GNU/Linux, de código abierto, compuesto por un módulo de kernel, un servicio en espacio de usuario y una API/SDK de integración para videojuegos (Cap. I, 1.5 y 1.6). El producto no se vende. Se ofrece como proyecto académico y comunitario, y su propuesta de valor es la transparencia: el código se publica y puede ser auditado por cualquier persona.

La experiencia se define por perfil:

- **Jugador en Linux.** Instala el sistema desde el repositorio, sin software propietario. Entiende qué se monitorea porque puede leer el código y la documentación. La condición de uso prevista es que la protección esté activa solo durante la sesión de juego (condición de adopción incluida en la encuesta diseñada).
- **Desarrollador de juegos open source.** Incorpora el SDK en su título, sin conocer el detalle del módulo de kernel (Cap. I, 1.6). El caso de referencia es un juego de código abierto, cuya comunidad es el primer público de validación (Beyond All Reason, vía RecoilEngine; la integración existe en el repositorio de trabajo, según `docs/vm_test_environment.md`).
- **Comunidad de seguridad y académica.** Revisa el diseño, reproduce las pruebas y reporta fallas.

Estado del producto: prototipo académico; no hay versión estable publicada. **UNVERIFIED** cualquier afirmación de eficacia fuera de las capturas del vault.

## **7.2. Dinámicas de intercambio por perfil de interesado**

| Perfil | Qué aporta | Qué recibe | Forma de intercambio |
|---|---|---|---|
| Jugadores GNU/Linux | Respuestas a la encuesta, reportes de compatibilidad, pruebas en distintas distribuciones | Un anticheat auditable; influencia en las prioridades | Encuesta, issues del repositorio |
| Desarrolladores de juegos open source | Feedback del SDK, casos de integración | SDK y documentación gratuitos y modificables | Issues, pull requests, encuesta breve para desarrolladores |
| Comunidad de seguridad | Revisión del código, análisis de evasiones | Un caso de estudio abierto; mención en los créditos | Issues, discusiones públicas del diseño |
| Moderadores y medios comunitarios | Autorización de difusión y alcance | Información veraz y verificable | Consulta previa de reglas, material en español e inglés |
| Cátedra y tutor | Evaluación y seguimiento | Evidencia del avance (Cap. VI) | Entregas y defensa |
| Autor y colaborador (Martínez Alarcón, Merino De Rui) | Desarrollo y difusión | Validación del proyecto y portafolio | Repositorio público |

Objeción principal prevista: publicar el código facilita la evasión. La encuesta la mide de forma explícita con un ítem planteado a propósito en contra del proyecto (`docs/Quark_Encuesta_Diapositivas.txt`, diapositiva 04).

## **7.3. Estrategias de publicidad, promoción y engagement**

Las estrategias no tienen presupuesto (Cap. III, 3.4, restricciones económicas) y se apoyan en contenido propio.

1. **Repositorio público como vitrina.** README claro en inglés y español, descripción de la arquitectura, instrucciones para reproducir la demostración y guía de contribución. Un repositorio sin documentación no genera interés técnico.
2. **Encuesta como instrumento de engagement y de validación.** La encuesta anónima diseñada convoca a la comunidad a opinar antes de publicar el producto. Valida dos supuestos (existe interés; el código abierto es un diferencial) y registra canales opcionales de seguimiento, desvinculados de las respuestas. Diseño vigente: encuesta principal recortada a unos 25 ítems, encuesta breve aparte para desarrolladores, prueba piloto con 5 a 10 personas y consulta previa a moderadores. Los resultados se publican de vuelta en cada comunidad. **No existen resultados aún; los debe aportar una persona tras publicar la encuesta.**
3. **Demostración reproducible.** Video o captura breve de una detección real, tomada de la evidencia del vault, con la salvedad de sus límites. Se muestran también los límites conocidos: la honestidad técnica es parte del posicionamiento.
4. **Entradas técnicas.** Notas sobre la investigación de anticheat en Proton y el diseño del módulo, a partir de las notas del vault (p. ej. la nota de investigación de anticheat en Proton).
5. **Participación comunitaria.** Respuesta pública a preguntas e issues; reconocimiento de contribuciones.

Indicadores propuestos (a medir, sin valores objetivo inventados): visitas y estrellas del repositorio, issues abiertos por terceros, respuestas completas a la encuesta, tasa de abandono, cantidad de desarrolladores que piden información del SDK.

## **7.4. Canales**

| Canal | Uso | Condición |
|---|---|---|
| Repositorio público (GitHub) | Código, documentación, issues | Publicar solo con la licencia GNU GPLv3 declarada (Cap. VIII) |
| GamingOnLinux | Noticia/aviso a la comunidad de jugadores en Linux | Cumplir sus criterios editoriales; **UNVERIFIED** el procedimiento de envío |
| r/linux_gaming | Presentación del proyecto y encuesta principal | Consultar a los moderadores las reglas sobre encuestas y autopromoción |
| r/gamedev | Encuesta breve para desarrolladores | Ídem |
| Comunidad de Beyond All Reason (foros/Discord) | Juego de referencia; feedback de integración | Consultar a sus responsables antes de publicar; **UNVERIFIED** la aceptación |
| Presentaciones académicas (defensa del PIF, en febrero) | Difusión institucional | Calendario de la cátedra |

Un mismo post por comunidad, en inglés y español (los idiomas elegidos con apoyo de la Figura 2.3 del Capítulo II), con enlace al repositorio y a la encuesta. La publicación de muchas encuestas puede causar problemas con los moderadores (diapositiva 04 de la encuesta), por lo que se limita a una por comunidad.

**Acciones futuras (no ejecutadas, sin contacto realizado).** Contactar a la comunidad del juego de referencia y evaluar un acercamiento a Valve (Steam) o a desarrolladoras. No se toman contactos externos en este PIF; estas acciones quedan fuera del alcance y no figuran como logros.

## **7.5. Limitaciones**

No hay datos de mercado propios (Cap. II pendiente de encuesta). No hay presupuesto publicitario. La difusión depende de la aceptación de moderadores y editores, no controlable por el equipo.

# **CAPÍTULO VIII — PROPIEDAD INTELECTUAL**

## **8.1. Definición de Marca y activos a proteger**

**Activos:**

| Activo | Situación | Protección prevista |
|---|---|---|
| Nombre "Quark Anticheat" | En uso en el proyecto y el repositorio | Registro de marca (8.2 a 8.4) |
| Logo | **No existe aún** | Se registra recién cuando exista un diseño definitivo; mientras tanto solo la marca denominativa |
| Código fuente (módulo de kernel, servicio, eBPF, SDK) | Autoría del autor y del colaborador; sin archivo LICENSE en el repositorio de trabajo (verificado: no hay `LICENSE*` en el árbol `Dev` ni en el repositorio de documentación) | Derecho de autor y licencia GNU GPLv3 (8.5) |
| Documentación, informe e imágenes del vault | Autoría del autor y del colaborador | Licencia GNU GPLv3, decisión del autor para todo el proyecto |

La autoría y el derecho de autor surgen sin registro formal; el registro de obra ante el organismo competente es opcional. No se atribuye derechos a la facultad.

## **8.2. Definición de clases internacionales a seleccionar**

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

Recomendación: solicitar clase 9 y evaluar la 42 con el tutor. Cada clase adicional agrega tasa. **UNVERIFIED** el monto vigente.

## **8.3. Búsqueda de antecedentes en INPI**

El autor realizó la búsqueda de las denominaciones **"quark"** y **"quark anticheat"** en el buscador de marcas del Instituto Nacional de la Propiedad Industrial (INPI, Argentina) y aportó el listado de registros **no vencidos** para "quark". La búsqueda de **"quark anticheat" no arrojó registros**; la denominación completa se mantiene como **"Quark Anticheat"**. Se transcribe sin modificaciones de contenido; se omiten los datos de identificación fiscal de los titulares y los nombres de personas humanas, y se conserva el número de acta para trazabilidad.

**Tabla 8.1. Marcas "quark" no vencidas (búsqueda aportada por el autor, 2026-11-25)**

| Acta | Fecha | Clase | Denominación | Tipo | Estado (según fuente) | Vencimiento |
|---|---|---|---|---|---|---|
| 3580141 | 10/02/2017 | 42 | QUARK ENGINEERING Q | Mixta | C | 15/06/2028 |
| 3606184 | 23/05/2017 | 41 | QUARK RECORDS | Mixta | C | 17/10/2028 |
| 3626590 | 26/07/2017 | 35 | QUARKS SOLUCIONES CON ENERGIA | Mixta | C | 28/03/2032 |
| 3626591 | 26/07/2017 | 36 | QUARKS SOLUCIONES CON ENERGIA | Mixta | C | 12/09/2032 |
| 4322188 | 29/12/2023 | 5 | QUARKS | Mixta | NU | sin dato |
| 4331433 | 07/02/2024 | 35 | QUARKS | Mixta | C | 27/08/2034 |
| 4331474 | 07/02/2024 | 32 | QUARKS | Mixta | C | 27/08/2034 |
| 4336628 | 28/02/2024 | 30 | QUARKS | Mixta | NU | sin dato |
| 4545571 | 24/07/2025 | 5 | QUARKS | Mixta | C | 08/01/2036 |
| 4545572 | 24/07/2025 | 30 | QUARKS | Mixta | C | 08/01/2036 |
| 4596199 | 25/10/2025 | **9** | QUARK TOP | Mixta | C | 10/03/2036 |
| 4670316 | 12/03/2026 | 10 | QUARK | Denominativa | C | 08/05/2036 |
| 4689161 | 05/04/2026 | 43 | QUARK'S CAFE BRUNCH GRAB & GO | Mixta | C | 08/06/2036 |
| 4784131 | 09/09/2026 | 35 | QUARK | Mixta | C | 04/11/2036 |

Los códigos de estado "C" y "NU" se transcriben como figuran en la fuente; su significado no se verificó (**UNVERIFIED**).

**Lectura de los resultados.** La denominación "Quark" (o su plural "Quarks") figura en 14 registros vigentes, en las clases 5, 9, 10, 30, 32, 35, 36, 41, 42 y 43. Para las clases candidatas del apartado 8.2:

- **Clase 9:** un registro mixto, QUARK TOP (acta 4596199, vigente hasta 2036). Es la clase de prioridad alta para Quark Anticheat.
- **Clase 42:** un registro mixto, QUARK ENGINEERING Q (acta 3580141, vigente hasta 2028).
- Las clases 35, 41 y 43 no son candidatas; los registros allí listados no se analizan.
- La denominación completa "Quark Anticheat" no tiene registros no vencidos idénticos (búsqueda de "quark anticheat" sin resultados) y ningún registro de la lista contiene el término "anticheat". Los registros de "Quark" en las clases 9 y 42 son antecedentes del primer término; si la diferencia alcanza para descartar confusión **no se determinó**: es una valoración del examinador del INPI y, en su caso, de un profesional de propiedad intelectual (**UNVERIFIED**; no es asesoramiento legal).

**Alcance y límites de la búsqueda.** Se buscó "quark" y "quark anticheat". No se buscaron "anticheat" solo, variantes fonéticas ni clases conexas, y no hay captura de pantalla con fecha y hora en el vault. Esas tareas quedan pendientes de una persona (ver Tabla 8.2). La ausencia de esos pasos limita cualquier conclusión sobre la registrabilidad.

**Procedimiento de repetición** (sujeto a verificación en el sitio oficial; **UNVERIFIED** en pasos y nombres de pantallas):

1. Ingresar al buscador de marcas del INPI.
2. Buscar "Quark Anticheat" y, por separado, "Anticheat".
3. Repetir con variantes fonéticas y gráficas ("Quarc", "Kwark", "Quark Anti-Cheat") y con las clases 9 y 42.
4. Registrar por cada hallazgo: denominación, titular, clase, estado, fecha y número de acta.
5. Capturar la pantalla con fecha y hora y guardarla en el vault (zona de evidencia, append-only).

**Tabla 8.2. Estado de las búsquedas**

| Término | Clases | Estado | Captura |
|---|---|---|---|
| quark | todas | realizada (resultado en Tabla 8.1) | pendiente |
| quark anticheat | todas | realizada: sin registros | pendiente |
| anticheat | 9, 42 | pendiente | pendiente |
| variantes fonéticas | 9, 42 | pendiente | pendiente |

El logotipo no existe aún y lo debe aportar una persona.

## **8.4. Registro de la marca**

Pasos previstos, tras la búsqueda: solicitud en el INPI, pago de tasa, publicación en boletín, plazo de oposición y concesión. Los plazos y costos no se citan porque no se verificaron. **UNVERIFIED**. Se cita como marco general la ley de marcas argentina (Ley 22.362); su articulado debe cotejarse antes de citarlo. **UNVERIFIED**. El registro de marca no es un requisito de aprobación del PIF; se plantea como decisión futura según resultado de búsqueda, costo y objetivos del equipo.

## **8.5. Licencia del software**

**Decisión del autor: GNU General Public License versión 3 (GPLv3) para todo el proyecto**, es decir, módulo de kernel, servicio en espacio de usuario, programas eBPF, SDK/API, herramientas de prueba y documentación. La licencia es coherente con la propuesta de valor (transparencia y auditoría) y con el diferencial que mide la encuesta. No impide registrar la marca: la licencia cubre el código; la marca, su uso y el logo se protegen aparte, y puede fijarse una política de uso del nombre para *forks*.

**Hechos verificados en el código** (rama `Dev`, árbol de trabajo local):

- `kernel/quark_kernel.c:37`: `MODULE_LICENSE("GPL")`.
- `quark_daemon/src/bpf/quark.bpf.c:31`: `char LICENSE[] SEC("license") = "GPL";`.
- Se agregó el archivo `LICENSE` con el texto oficial de la GNU GPL versión 3 (29 de junio de 2007, publicado por la Free Software Foundation en https://www.gnu.org/licenses/gpl-3.0.txt) en la raíz del repositorio de documentación. En el repositorio de código (rama `Dev`) no hay archivo `LICENSE`; copiarlo allí y agregar las cabeceras SPDX es una acción pendiente, previa a publicar el repositorio (Cap. VII), porque `Dev` está congelada para esta entrega.

**Aviso de licencia por archivo.** La propia GPLv3 recomienda anteponer a cada archivo fuente el siguiente aviso (texto de la sección "How to Apply These Terms to Your New Programs"), con el nombre del programa y el año:

```
<nombre del programa y una línea con su propósito>
Copyright (C) <año>  <nombre del autor>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```

Los programas que interactúan por terminal pueden mostrar al iniciar un aviso breve ("This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'. This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details."). La definición de titulares del *copyright* (autor y colaborador) y, si corresponde, la declaración de renuncia de la institución, queda a definir. Dado que el aviso usa la fórmula "o (a su elección) cualquier versión posterior", la declaración es GPL-3.0-or-later.

**Nota a revisar (no bloqueante).** `MODULE_LICENSE("GPL")` en el kernel indica, por convención del kernel, una licencia compatible con GPLv2; el kernel Linux se distribuye bajo GPL-2.0. La compatibilidad entre una licencia GPLv3 declarada para el proyecto y un módulo cargado en un kernel GPLv2, y el efecto de la declaración `"GPL"` sobre el uso de símbolos exportados solo para GPL y de *helpers* eBPF, quedan como tema a revisar con la cátedra o con asesoramiento legal. No se trata como bloqueante para la entrega y no se verificó contra la documentación vigente de kernel.org en esta redacción (UNVERIFIED).

## **8.6. Limitaciones**

No se consultó a un profesional de propiedad intelectual. Los datos legales, plazos y costos no se verificaron. El logo no existe. La búsqueda INPI cubrió "quark" y "quark anticheat" y no tiene captura.

# **CAPÍTULO IX — DISEÑO DE LA SOLUCIÓN**

**Alcance de la evidencia.** El código descrito se leyó (no se ejecutó) en el worktree de solo lectura `quark-wt/Dev`, commit `35c6031` (`origin/Dev`, 2026-11-05). Toda referencia `archivo:línea` apunta a ese commit. Lo medido en la máquina virtual proviene de `docs/vm_test_environment.md` de ese mismo commit y se cita como tal. Lo inferido sin lectura directa se marca **UNVERIFIED**. La rama `feature/gameStartProtection` (commit `2b088ab`) no está integrada y se describe aparte (§9.9).

Este capítulo cubre los puntos del Art. 24.3.9 del Reglamento: arquitectura del sistema de información (§9.1), diseño de solución (§9.2 y §9.3), modelo de datos (§9.4), infraestructura de comunicaciones y servidores (§9.5), entornos de trabajo (§9.6) y solución (§9.7 a §9.9).

## **9.1. Arquitectura del sistema de información**

### **9.1.1. Componentes**

El sistema se compone de cuatro piezas de código propio más dos binarios de apoyo, escritos en tres lenguajes.

| Componente | Lenguaje | Ruta | Función |
|---|---|---|---|
| Módulo de kernel `quark_kernel` v0.4.0 | C | `kernel/quark_kernel.c:42,44` | Autoridad sobre qué PID está protegido; bloquea accesos de nivel *attach* con un `kretprobe`; recibe órdenes por Netlink. |
| Demonio `quark_daemon` | Rust (edición 2024) | `quark_daemon/src/main.rs`, `quark_daemon/Cargo.toml:4` | Atiende al juego por socket Unix, ordena la protección al kernel, supervisa variables, carga los programas eBPF. |
| Programas eBPF | C | `quark_daemon/src/bpf/quark.bpf.c` | 12 programas BPF-LSM y de tracepoint (ver §9.3.3); se cargan con `libbpf-rs` 0.27 (`quark_daemon/Cargo.toml:14`). |
| Cargador/esqueleto BPF | Rust | `quark_daemon/src/bpf.rs`, `quark_daemon/build.rs:15` | Compila el objeto BPF en tiempo de build (`libbpf-cargo` 0.27, `Cargo.toml:18`) y lo carga y adjunta en el arranque. |
| `quark_cli` | C | `quark_daemon/quark_cli.c` | Firma las órdenes y las envía por Netlink al kernel. |
| SDK | C | `sdk/quark_sdk.c`, `sdk/quark_sdk.h` | Biblioteca enlazada en el juego; API pública y *watchdog*. |

El juego de prueba (`game_target/game.c`), la herramienta de ataque (`cheat/cheat.c`) y el motor RecoilEngine (submódulo) son entornos de validación, no componentes del producto.

### **9.1.2. Arquitectura y canales**

El sistema se organiza en dos espacios, de usuario y de kernel, comunicados por los canales de la Tabla 9.1. Los diagramas se describen en forma tabular porque la versión impresa no incorpora gráficos de diagramas.

**Tabla 9.1. Componentes y canales**

| Origen | Destino | Canal | Autenticación o efecto | Referencia |
|---|---|---|---|---|
| Juego + SDK C | `quark_daemon` (Rust) | Socket Unix `/tmp/quark.sock` | `SO_PEERCRED`: pid real del par | `sdk/quark_sdk.c:11`; `main.rs:110-133` |
| `quark_daemon` | `quark_cli` (C) | `fork` + `exec` con `sudo` | Firma ECDSA P-256 de cada orden | `main.rs:202-204` |
| `quark_cli` | `quark_kernel.ko` (C) | Netlink protocolo 31: solicitud firmada, respuesta de 20 B | uid root, SHA-256 del ejecutable, firma, nonce | `quark_cli.c:16,145`; `quark_kernel.c:46,612` |
| `quark_daemon` | Programas eBPF (BPF-LSM y tracepoints) | `libbpf`: carga, *attach*, mapas `quark_protected`, `quark_config`, `quark_events` (*ring buffer*) | Solo el demonio accede a los objetos | `bpf.rs:184-269` |
| Programas eBPF | `quark_daemon` | *Ring buffer*, eventos de 96 bytes | Sin firma ni persistencia | `bpf.rs:233-255` |
| Atacante (`cheat`, `gdb`, `bpftrace`, `process_vm_*`) | Kernel / eBPF | Acceso *attach*, BPF de *tracing*, objetos Quark | Denegado (`EACCES`, `-EPERM`) | `quark_kernel.c:489-499`; `quark.bpf.c:163-254` |
| systemd | `quark_daemon` y `quark_kernel.ko` | `quark.socket` (fd 3), `quark.service`, `quark-kernel.service` (`insmod`/`rmmod`) | Activación por socket | `main.rs:25-42`; `quark-kernel.service:26-27` |

### **9.1.3. Principio de autoridad dividida**

El módulo de kernel decide qué PID está protegido. El mapa BPF `quark_protected` es un espejo que el demonio escribe solo después de que el kernel confirma con `ok=1` (`quark_daemon/src/bpf.rs:1-6`, `quark.bpf.c:21-24`, `main.rs:250-264`). El juego solo recibe la confirmación a través del demonio.

## **9.2. Diseño de la solución: flujos**

### **9.2.1. Flujo de protección (arranque protegido)**

**Tabla 9.2. Secuencia del arranque protegido** (el orden es el del código; cada paso cita su fuente)

1. El juego conecta a `/tmp/quark.sock` (`sdk/quark_sdk.c`; `quark.socket:5`).
2. systemd arranca `quark.service` y le pasa el socket como fd 3 (`LISTEN_FDS`) (`main.rs:16,25-42`). El módulo ya fue cargado por `quark-kernel.service`.
3. El demonio ejecuta `sudo quark_cli 3 <pid_demonio>` para registrarse como monitor de confianza (`main.rs:549-569`).
4. `quark_cli` envía el comando 3 firmado por Netlink (`quark_cli.c:120-259`).
5. El kernel verifica la orden y responde `{ok}` (`quark_kernel.c:591-595`).
6. El demonio carga y adjunta los programas eBPF con `load_and_attach(daemon_tgid)` (`main.rs:575-585`; `bpf.rs:184-269`).
7. El juego envía `CMD_REGISTER_GAME` con su pid declarado (`sdk/quark_sdk.c:133-139`).
8. El demonio toma el pid real de `SO_PEERCRED` y descarta el declarado (`main.rs:110-133,181-197`).
9. El demonio ejecuta `sudo quark_cli 1 <pid_real>` (`main.rs:202-204`).
10. `quark_cli` envía `{pid, nonce, firma}` por Netlink, tipo 1 (`quark_kernel.c:557-580`).
11. El kernel verifica uid root, SHA-256 de `/proc/pid/exe`, nonce fresco y firma ECDSA (`quark_kernel.c:220-271,557-578`).
12. `quark_protect_pid()` rechaza si hay hipervisor en el build *release* (`quark_kernel.c:334-349`).
13. El kernel responde `{ok, is_testing_build, version}` (`quark_kernel.c:354-390`).
14. `quark_cli` devuelve `QUARK_OK`, `QUARK_VERSION` y `QUARK_TESTING_BUILD` por stdout (`quark_cli.c:255-259`; `main.rs:213-234`).
15. El demonio refleja la protección en el mapa BPF: `quark_protected[pid]=1` y `quark_protected_count` (`main.rs:254-264`; `bpf.rs:272-282`).
16. El demonio responde al juego con el ack de 19 bytes `[ok][testing][version16][bpf_lsm_active]` (`main.rs:51-67,272`).
17. `quark_sdk_init()` exige `ok=1` e inicia el *watchdog* (`sdk/quark_sdk.c:147-187`).
18. Un hilo monitor del demonio lee `/proc/pid/mem` cada 50 ms (`main.rs:290-303,422-506`).

Decisiones observables en el flujo:

- El PID usado contra el kernel proviene de `SO_PEERCRED`, no del *payload*; si difiere, solo se registra una nota (`main.rs:181-197`).
- Si `quark_cli` falla (módulo ausente o rechazo), el demonio envía el ack con `ok=0` y corta la conexión (`main.rs:236-241,272,284-288`); el SDK devuelve `-1` y el juego debe negarse a continuar (`sdk/quark_sdk.c:149-157`, `sdk/quark_sdk.h:26-29`).
- La carga eBPF es de mejor esfuerzo: si falla, el demonio continúa con solo el `kretprobe` y reporta `bpf_lsm_active=0` (`main.rs:571-585,254-264`; `sdk/quark_sdk.c:169-173`).

### **9.2.2. Flujo de comandos firmados (canal de control)**

Tres órdenes cambian estado y pasan por la misma puerta (`quark_kernel.c:513-523`): `1` proteger, `2` desproteger, `3` registrar el monitor de confianza (`quark_cli.c:120-143`). Secuencia de verificación en el kernel (`quark_nl_recv_msg`, `quark_kernel.c:524-600`):

1. Tipo de mensaje válido (1, 2 o 3) y carga útil de tamaño suficiente (`:533-548`).
2. `quark_check_sender()`: uid del emisor tomado de `NETLINK_CREDS(skb)`, no del campo `nlmsg_pid`; debe ser root; se abre `/proc/<pid>/exe`, se calcula SHA-256 (tope 1 MiB, `:49,181-205`) y se compara con `quark_cli_expected_sha256` (`:220-271`).
3. `quark_nonce_is_fresh()`: el nonce debe ser estrictamente mayor que `last_nonce` (`:158-166`).
4. `quark_verify_signature()`: ECDSA P-256 (`crypto_alloc_sig("x962(ecdsa-nist-p256)")`) sobre SHA-256 de `{comando(1 B), pid(4 B), nonce(8 B)}` (`:127-152,566-571`) con la clave pública compilada (`kernel/quark_pubkey.h:9`, 65 bytes SEC1).
5. Solo entonces avanza el nonce (`:170-177,580`) y se ejecuta la orden (`:582-599`).

Las respuestas existen solo para 1 y 3; la 2 no tiene respuesta (`:537-540`, `quark_cli.c:223-227`). El nonce del cliente es la hora en nanosegundos (`quark_cli.c:176-178`). La firma se genera con OpenSSL EVP y la clave privada de `/opt/quark-anticheat/keys/quark_signing_key.pem` (`quark_cli.c:21,56-103`); el par de claves de prueba lo crea `tooling/keys/generate-testing-key.sh`. El hash de `quark_cli` se regenera en cada build (`Makefile:85-89`), por lo que el `.ko` queda atado al binario compilado en ese momento.

### **9.2.3. Flujo de bloqueo en el kernel**

`ptrace_may_access` se engancha con un `kretprobe` (`quark_kernel.c:506-511,620-621`). El *entry handler* guarda `task` y `mode` desde los registros `di` y `si` (`:427-438`, solo `CONFIG_X86_64`). El *return handler* fuerza `regs->ax = 0` (acceso denegado) cuando se cumplen simultáneamente (`:489-499`):

- el objetivo es un PID protegido (`is_pid_protected`, `:470`);
- el llamador no es el propio proceso ni `trusted_monitor_pid` (comparación por `tgid`, `:467-468,489`);
- el modo incluye `PTRACE_MODE_ATTACH` (`:491`).

Los accesos de solo lectura (`PTRACE_MODE_READ`) pasan sin alteración (`:409-417,484-488`). No existe exención general para root (`:476-483`).

### **9.2.4. Flujo de telemetría y autoprotección (eBPF)**

Los eventos se escriben en el *ring buffer* `quark_events` (`quark.bpf.c:83-86,138-155`); un hilo del demonio los consume cada 250 ms y los imprime como líneas `[QUARK-BPF]` (`bpf.rs:233-255,101-140`). Las acciones bloqueantes devuelven `-EPERM` (§9.3.3). Los programas de ejecución y de carga de módulos se omiten si `quark_protected_count == 0` (`quark.bpf.c:166-167,360-361,375-376`).

### **9.2.5. Flujo de supervisión de variables (capa suplementaria)**

Tras el ack, el SDK puede registrar variables (`CMD_REGISTER_VAR`) y declarar actualizaciones legítimas (`CMD_UPDATE_VAR`). El hilo monitor del demonio compara cada 50 ms el valor de `/proc/<pid>/mem` con el esperado; ante diferencia imprime la alerta y ejecuta `kill -9` sobre el proceso (`main.rs:462-497`, en particular `:463,480,490`). Esta capa lee memoria protegida y por eso depende de que el demonio esté registrado como monitor de confianza (`main.rs:540-569`).

### **9.2.6. Flujo de fin de sesión**

Cuando el cliente cierra el socket, el demonio ejecuta `quark_cli 2 <pid>` y retira el PID del espejo BPF (`main.rs:404-417`). Además, el tracepoint `sched_process_exit` borra la entrada si el líder de grupo termina (`quark.bpf.c:388-402`), lo que evita que un PID reutilizado herede protección. Del lado del SDK, el *watchdog* sondea el socket cada 1 s y llama a `_exit(137)` si el demonio se cae (`sdk/quark_sdk.c:18,63-111`).

## **9.3. Diseño de solución: interfaces**

### **9.3.1. Interfaz Netlink (kernel ↔ `quark_cli`)**

- Familia `AF_NETLINK`, `SOCK_RAW`, protocolo **31** (`NETLINK_QUARK`), definido en `kernel/quark_kernel.c:46` y `quark_daemon/quark_cli.c:16`; el kernel crea el socket con `netlink_kernel_create` (`quark_kernel.c:604-617`).
- `nlmsg_type` ∈ {1, 2, 3} (`quark_cli.c:204`; `quark_kernel.c:531-533`).
- Solicitud `struct quark_netlink_request` (`quark_kernel.c:55-60`; espejo manual en `quark_cli.c:30-35`):

| Campo | Tipo | Significado |
|---|---|---|
| `pid` | `s32` | PID objetivo (o PID del demonio para el comando 3) |
| `nonce` | `u64` | Hora en ns; estrictamente creciente |
| `sig_len` | `u16` | Longitud real de la firma DER, ≤ 72 |
| `sig` | `u8[72]` | Firma ECDSA P-256 DER |

- Respuesta `struct quark_protect_response` (`quark_kernel.c:68-73`; `quark_cli.c:38-43`): `ok:u8`, `is_testing_build:u8`, `reserved[2]`, `version[16]`. El kernel responde por `nlmsg_unicast` al `nlmsg_pid` del solicitante (`:354-390`). `quark_cli` espera como máximo 3 s (`quark_cli.c:49,162-169`) y traduce la respuesta a líneas `QUARK_OK:`, `QUARK_VERSION:`, `QUARK_TESTING_BUILD:` en la salida estándar (`:255-257`), que el demonio extrae (`main.rs:217-223`).
- Tamaño de la solicitud en memoria: 96 bytes por alineación natural de `u64` (cálculo propio, no medido con `sizeof`; **UNVERIFIED**). El mensaje firmado ocupa 13 bytes sin relleno (`quark_kernel.c:528`).
- Código de retorno de `quark_cli`: 0 si `ok=1`; 1 en cualquier otro caso (`quark_cli.c:259`).

### **9.3.2. Interfaz de socket Unix (SDK ↔ demonio)**

- Ruta `/tmp/quark.sock` (`sdk/quark_sdk.c:11`; `main.rs:509`), `SOCK_STREAM`, modo `0666` impuesto por systemd (`quark.socket:9`).
- Trama: cabecera de 8 bytes `[command:u32][payload_len:u32]` en *endianness* nativo, más *payload* (`sdk/quark_sdk.c:35-56`; `main.rs:153-168`).

| Comando | Valor | Payload | Respuesta |
|---|---|---|---|
| `CMD_REGISTER_GAME` | 1 | `pid:i32` (4 B) | ack de 19 B |
| `CMD_REGISTER_VAR` | 2 | `address:u64`, `size:u32`, `name:char[32]` (44 B) | ninguna |
| `CMD_UPDATE_VAR` | 3 | `address:u64`, `new_value:u64` (16 B) | ninguna |

Fuentes: `main.rs:45-47,171-397`; `sdk/quark_sdk.c:13-15,189-232`.

- Ack de registro, 19 bytes: `[ok:1][is_testing_build:1][version:16][bpf_lsm_active:1]` (`main.rs:49-67`; `sdk/quark_sdk.c:31-33,159-162`). El mismo diseño se mantiene a mano en ambos extremos.
- El demonio autentica al cliente con `SO_PEERCRED` (`main.rs:105-133`); el socket es escribible por cualquier usuario, de modo que el PID declarado en el *payload* no es confiable (`main.rs:138-144`).

### **9.3.3. Interfaz eBPF (demonio ↔ programas)**

Doce programas, enumerados en `quark.bpf.c` (conteo de `SEC("...")` sin licencia ni mapas):

| Tipo | Sección | Línea | Efecto |
|---|---|---|---|
| Bloqueo | `lsm/bpf_prog_load` | 163 | Deniega cargar BPF de tracing (kprobe, tracepoint, perf_event, raw_tracepoint, tracing, LSM, ext) con PID protegido, salvo el demonio |
| Bloqueo | `lsm/bpf_map` | 191 | Deniega fd de mapas de Quark a terceros |
| Bloqueo | `lsm/bpf_prog` | 205 | Ídem para programas |
| Bloqueo | `lsm/bpf` (`BPF_LINK_GET_FD_BY_ID`) | 223 | Ídem para enlaces |
| Bloqueo + telemetría | `lsm/ptrace_access_check` | 254 | Deniega todo acceso al demonio; reporta intentos *attach* a PID protegidos |
| Telemetría | `tp/syscalls/sys_enter_process_vm_readv` y `..._writev` | 289, 301 | `PROCESS_VM_ACCESS` |
| Telemetría | `lsm/file_mprotect` | 319 | `EXEC_MPROTECT` (anónimo + `PROT_EXEC`, sin bloqueo) |
| Telemetría | `lsm/task_kill` | 338 | `TASK_KILL` |
| Telemetría | `tp/module/module_load` | 358 | `MODULE_LOAD` |
| Telemetría | `tp/sched/sched_process_exec` | 373 | `EXEC` |
| Mantenimiento | `tp/sched/sched_process_exit` | 388 | Borra el PID del mapa |

El demonio verificó en la VM la carga de 12 programas, 4 mapas y 12 enlaces (`docs/vm_test_environment.md` §15.4, ejecución del 2026-09-30, núcleo 7.0.9 con `vmlinux.h` generado en otro núcleo).

Orden de arranque de la autoprotección (`bpf.rs:178-232`): se cargan los objetos; se leen ids de mapas y programas; se escribe `quark_config`; se adjunta; se consultan los ids de enlaces y se reescribe `quark_config`. El orden garantiza que `quark_bpf_map` conozca qué proteger antes de entrar en servicio (`bpf.rs:182-183`).

### **9.3.4. API pública del SDK (`sdk/quark_sdk.h`)**

| Función | Línea (.h) | Comportamiento |
|---|---|---|
| `int quark_sdk_init(void)` | 31 | Conecta, registra el PID, exige `ok=1` y lanza el *watchdog*; `-1` ante cualquier falla (`sdk/quark_sdk.c:113-187`) |
| `int quark_sdk_register_var(void*, uint32_t, const char*)` | 40 | Opta una variable por monitoreo; nombre de hasta 31 caracteres (`sdk/quark_sdk.c:189-213`) |
| `int quark_sdk_update_var(void*, uint64_t)` | 48 | Declara una escritura legítima (`:215-232`) |
| `int quark_sdk_is_active(void)` | 59 | 1 si el socket sigue abierto (`:234-239`) |
| `int quark_sdk_is_testing_build(void)` | 71 | 1 si el módulo es de *testing* (`:241-247`) |
| `int quark_sdk_is_bpf_lsm_active(void)` | 84 | 1 si los ganchos BPF-LSM cubren el proceso (`:249-255`) |
| `int quark_sdk_get_version(char*, size_t)` | 94 | Versión del módulo (`:257-275`) |
| `void quark_sdk_close(void)` | 99 | Cierra la conexión (`:277-285`) |

Los valores devueltos por `is_*` son calculados en el proceso del cliente. Un cliente adulterado puede falsificarlos (Informe, Anexo III.6 §E; no hay atestación verificada por servidor, `docs/features.md:254-256`).

## **9.4. Modelo de datos**

El sistema no usa base de datos ni persistencia. Todo el estado reside en memoria y se pierde al descargar el módulo o terminar el demonio (`quark_kernel.c:155-157`). Se distinguen cuatro grupos.

### **9.4.1. Estado del módulo de kernel**

| Dato | Declaración | Notas |
|---|---|---|
| `protected_pids[16]`, `protected_pids_count` | `quark_kernel.c:274-275` (tope en `:47`) | Protegido por `quark_lock` (`:276`). Alta rechazada con aviso si se llena (`:319-322`) |
| `trusted_monitor_pid` | `:283` | Una sola ranura, inicial `-1` |
| `last_nonce`, `quark_nonce_lock` | `:88-89` | Anti-repetición; se reinicia al recargar el módulo |
| `quark_pubkey[65]` | `kernel/quark_pubkey.h:9` | Clave pública ECDSA P-256 compilada |
| `quark_cli_expected_sha256[32]` | generado (`Makefile:85-89`), no versionado | Hash esperado del emisor |

### **9.4.2. Mapas y variables BPF**

| Objeto | Tipo | Clave → valor | Capacidad | Línea |
|---|---|---|---|---|
| `quark_protected` | `BPF_MAP_TYPE_HASH` | `u32` tgid → `u8` | 16 | `quark.bpf.c:53-58` |
| `quark_config` | `BPF_MAP_TYPE_ARRAY` | `u32` 0 → `struct quark_config` | 1 | `:66-81` |
| `quark_events` | `BPF_MAP_TYPE_RINGBUF` | — | 256 KiB | `:83-86` |
| `quark_protected_count` | variable global (`.bss`) | `u32` | — | `:93` |

`struct quark_config` (`:66-74`) contiene `daemon_tgid`, `map_ids[8]`, `map_id_count`, `prog_ids[16]`, `prog_id_count`, `link_ids[16]`, `link_id_count`. Los topes se repiten en Rust (`bpf.rs:23-27`) y la compilación falla si no coinciden con el tipo generado. El demonio es el único escritor de `quark_protected_count`; el BPF solo lo decrementa al salir un proceso (`bpf.rs:297-306`; `quark.bpf.c:397-400`).

### **9.4.3. Estado del demonio**

`QuarkState { pid, variables: HashMap<u64, MonitoredVar>, is_active }` y `MonitoredVar { address, size, name, expected_value }` (`main.rs:69-81`), uno por conexión y compartido entre el hilo del cliente y el monitor mediante `Arc<Mutex<…>>` (`main.rs:150-151,290-299`). Del lado BPF mantiene `HashSet<u32>` con los PID espejados (`bpf.rs:167-170`).

### **9.4.4. Formato de eventos**

Definido en `quark_daemon/src/bpf/quark_events.h` y duplicado a mano en Rust (`bpf.rs:29-55`; el encabezado lo declara en `quark_events.h:1-7`).

```c
struct quark_event {                       // quark_events.h:27-35
    unsigned long long timestamp_ns;       // bpf_ktime_get_ns()
    unsigned int type;                     // enum quark_event_type
    unsigned int pid;                      // tgid del actor
    unsigned int target_pid;               // tgid protegido, 0 si no aplica
    unsigned int aux;                      // modo ptrace / señal / tipo de prog BPF / prot / id
    char comm[16];                         // QUARK_COMM_LEN
    char modname[56];                      // QUARK_MODNAME_LEN, solo MODULE_LOAD
};
```

Tamaño: 8 + 4×4 + 16 + 56 = **96 bytes** (`bpf.rs:42-43`; el parseo rechaza registros más cortos, `bpf.rs:68-71`). Desplazamientos usados en el lector: `comm` en 24, `modname` en 40 (`bpf.rs:72-73`).

Tipos de evento (`quark_events.h:12-22`): 1 `EXEC`, 2 `PTRACE_ATTEMPT`, 3 `PROCESS_VM_ACCESS`, 4 `EXEC_MPROTECT`, 5 `TASK_KILL`, 6 `MODULE_LOAD`, 7 `BPF_PROG_DENIED`, 8 `BPF_OBJ_DENIED`, 9 `DAEMON_ACCESS_DENIED`. El significado de `aux` por tipo se declara en `quark_events.h:32`; el demonio lo presenta en texto en `bpf.rs:102-140`. Formato de salida: una línea `[QUARK-BPF] <TIPO>: …` por evento (p. ej. `bpf.rs:106-109`); el catálogo completo de mensajes está en `docs/log_messages.md`.

Los eventos no se persisten, no se firman y no se envían a un servidor: se imprimen en la salida estándar del demonio (`bpf.rs:237`), que en el servicio systemd va al *journal* (`docs/vm_test_environment.md` §3.2).

## **9.5. Infraestructura de comunicaciones y servidores**

El sistema opera de forma local, sin servidores propios. Los canales son tres, todos dentro del equipo del jugador:

| Canal | Mecanismo | Autenticación |
|---|---|---|
| SDK ↔ demonio | Socket Unix de flujo, `/tmp/quark.sock`, `0666` | `SO_PEERCRED` (pid real del par) |
| demonio → kernel | `quark_cli` + Netlink proto 31 | uid root, SHA-256 del ejecutable, firma ECDSA, nonce |
| demonio ↔ eBPF | `bpf()` por `libbpf-rs`; ring buffer | Solo el demonio tiene acceso a los objetos (`lsm/bpf_*`) |

Servicios systemd (`quark_daemon/systemd/`):

- `quark.socket`: `ListenStream=/tmp/quark.sock`, `SocketMode=0666`, `RemoveOnStop=true`, instalado en `sockets.target` (`quark.socket:5,9,10,13`).
- `quark.service`: `Requires=`/`After=quark.socket`, `Type=simple`, `ExecStart=/opt/quark-anticheat/quark_daemon/target/release/quark_daemon`, `User=root` (`quark.service:3-4,7,9,13`). No tiene sección `[Install]` propia: se arranca por activación del socket (`quark.service:15-18`, comentario; `main.rs:14-42`).
- `quark-kernel.service`: `Type=oneshot`, `RemainAfterExit=yes`, `insmod` idempotente en `ExecStart` y `rmmod` en `ExecStop` (`quark-kernel.service:15-16,26-27`). No impone orden respecto del socket; la falla de carga queda cubierta por el protocolo de ack (`quark-kernel.service:3-13`).

Limitaciones de infraestructura observables en el código:

- El demonio atiende **un cliente a la vez**: `handle_client` se invoca de forma síncrona dentro del bucle `incoming()` (`main.rs:587-592`) y retorna solo cuando el cliente se desconecta (`main.rs:155-168,404-419`). El efecto sobre un segundo juego concurrente no se midió (**UNVERIFIED**); el tope de 16 PID del kernel no es alcanzable con un único cliente activo. `quark_cli` documenta la misma restricción (`quark_cli.c:45-48`).
- Las rutas `./quark_daemon/quark_cli` y `/opt/quark-anticheat/keys/quark_signing_key.pem` están fijas en el código (`main.rs:203,411,551`; `quark_cli.c:21`). El demonio invoca `sudo` aunque corre como root (`main.rs:202`).
- No hay empaquetado DKMS: el módulo se compila contra el núcleo en uso (`docs/vm_test_environment.md` §3.1; `kernel/Makefile:3`).

## **9.6. Entornos de trabajo**

### **9.6.1. Entorno de pruebas (VM)**

Según `docs/vm_test_environment.md` §1: máquina virtual local **QEMU/KVM** accesible por SSH, con **Nobara Linux 43 (KDE Plasma)**, núcleo `7.0.9-200.nobara.fc43.x86_64`, partición raíz de 23 GB, usuarios `quark` y `root`. La distribución se declara referencia del proyecto (`docs/contexto_proyecto.md`, citada allí) y es el entorno vigente de pruebas. El equipo anfitrión usa Arch Linux y solo construye contenedores desechables Fedora 44 para compilar los plugins de IA (`vm_test_environment.md` §1, §6; `tooling/recoil-fedora-build/`).

Entorno vigente: **Nobara Linux 43** (`docs/vm_test_environment.md`). `vm/README.md:1-11` describe otra VM, **CachyOS** con núcleo `7.3.1-1-cachyos` compilado con clang (commit `38d49cd`), que se menciona solo como propuesta a futuro; el Makefile del módulo cubre ambos casos agregando `LLVM=1` si el núcleo se compiló con clang (`kernel/Makefile:6-8`; commit `2058e28`).

La VM obliga a usar el módulo de *testing*: el build de *release* rechaza proteger bajo un hipervisor porque lee el bit CPUID de hipervisor (`quark_kernel.c:79-86,334-349`; `kernel/Makefile:21-22`; `Makefile:98-100`). El build de *testing* se declara a sí mismo con `is_testing_build=1` (`quark_kernel.c:362-366`). Toda la evidencia de la VM corresponde por lo tanto a un build de *testing*.

### **9.6.2. Requisitos de ejecución**

- BPF-LSM requiere `bpf` en `/sys/kernel/security/lsm` (parámetro de arranque `lsm=`) (`docs/vm_test_environment.md` §15.1; `quark_daemon/src/main.rs:571-585`).
- `vmlinux.h` se genera con `bpftool` desde el BTF del equipo de compilación y no se versiona; las relocalizaciones CO-RE permiten usar el objeto en otro núcleo (`Makefile:25-29`; `build.rs:10-14`; verificado en la VM, §9.3.3).
- La compilación del módulo exige encabezados del núcleo en uso (`kernel/Makefile:3`, `docs/vm_test_environment.md` §2.1).

### **9.6.3. Construcción**

`make daemon` (`Makefile:16-18`) construye `quark_cli` (enlaza `-lcrypto`, `Makefile:33-35`) y `cargo build --release`. `make kernel` y `make kernel-testing` generan `kernel/quark_cli_hash.h` y compilan el módulo (`Makefile:85-100`). El linter (`make lint`) ejecuta `clang-tidy` sobre el código C del SDK, `quark_cli`, el módulo y los programas de prueba (`Makefile:72-79`).

## **9.7. Decisiones de diseño**

| Decisión | Motivo documentado | Fuente |
|---|---|---|
| Módulo de kernel en C, no Rust | Contingencia del riesgo R2 (bindings insuficientes), prevista en §5.7 del informe | Informe, Anexo III.6 §B |
| `kretprobe` en lugar de gancho LSM en el módulo | Un módulo fuera del árbol no puede registrar LSM: `security_add_hooks()` es `__init` y no se exporta | `quark.bpf.c:7-9` |
| Ganchos LSM mediante BPF-LSM desde el demonio | Única forma de obtener LSM reales; además cubre BPF de tracing, que no pasa por `ptrace_may_access` | `quark.bpf.c:3-15` |
| Bloquear solo `PTRACE_MODE_ATTACH` | Los accesos de lectura saturaban `dmesg` y afectaban `ps`/`htop` sin impedir lecturas de memoria | `quark_kernel.c:409-417` |
| Compara `tgid`, no `pid` de hilo | Un hilo no líder o el hilo monitor del demonio fallaban la comparación | `quark_kernel.c:459-468` |
| Una única ranura de monitor de confianza, sin exención a root | Una exención general de root dejó pasar al `cheat` en una prueba real | `quark_kernel.c:476-483` |
| Mensajes firmados con nonce, hash del emisor y uid | Se hallaron dos fallas de escalada local durante el desarrollo | `docs/features.md:155-163` |
| El espejo BPF solo se actualiza tras el `ok=1` del kernel | Una sola fuente de verdad | `bpf.rs:1-6` |
| Falla cerrada | `quark_sdk_init()` exige confirmación; el *watchdog* termina el proceso | `sdk/quark_sdk.h:11-31`; `sdk/quark_sdk.c:63-111` |
| Build de *release* sin camino de bypass compilado | Un build de prueba no puede hacerse pasar por *release* | `quark_kernel.c:326-333` |
| Activación por socket de systemd | El demonio solo corre mientras se usa, como `docker.socket` | `main.rs:14-24` |
| Eventos de telemetría no bloqueantes (`EXEC_MPROTECT`) | Los JIT legítimos también cambian `PROT_EXEC` | `quark.bpf.c:313-318` |

## **9.8. Límites del diseño**

Declarados en el código o en `docs/features.md`; ninguno fue medido por esta redacción más allá de lo citado.

1. **Lecturas de nivel *read* por root.** `/proc/<pid>/{environ,maps,auxv}` quedan legibles para cualquier proceso con `CAP_PERFMON`, porque `mm_access()` los concede después de que `ptrace_may_access()` se niega. Se expone el diseño de memoria (ASLR). No puede anularse desde un módulo (`docs/features.md:44-53`; `quark.bpf.c:248-253`; `vm_test_environment.md` §15.5).
2. **Escrituras sin llamada al sistema.** Una inyección por `LD_PRELOAD` o DLL que no use `ptrace`/`/proc/mem` no se observa; `EXEC_MPROTECT` es solo un indicador (Informe, Anexo III.6 §B).
3. **BPF-LSM de mejor esfuerzo.** Si el usuario arranca sin `bpf` en `lsm=`, quedan solo el `kretprobe` y el SDK lo informa con `bpf_lsm_active=0` (`main.rs:571-585`; `sdk/quark_sdk.h:73-84`). El motor RecoilEngine aún no aplica política sobre ese valor (`docs/features.md:260-262`).
4. **Atestación del cliente.** `quark_sdk_is_*` se calculan en el cliente; no existe SDK de servidor ni prueba cliente-servidor de punta a punta (`docs/features.md:252-259`).
5. **Capacidad.** 16 PID en el kernel y en `quark_protected` (`quark_kernel.c:47`; `quark.bpf.c:55`), 8/16/16 objetos propios en `quark_config` (`quark.bpf.c:47-49`) y un cliente activo por vez en el demonio (§9.5).
6. **Efectos colaterales mientras hay un PID protegido.** `bpftrace`, `perf trace` con BPF y la carga de programas de tracing fallan (`docs/features.md:125-127`; `quark.bpf.c:157-187`).
7. **Pérdida de estado.** Al recargar el módulo se reinician `protected_pids` y `last_nonce` (`quark_kernel.c:155-157`); no hay persistencia.
8. **Arquitectura.** El *entry handler* solo extrae argumentos en x86_64; en otras arquitecturas deja `task = NULL` y no bloquea nada (`quark_kernel.c:430-436`).
9. **Clave de firma.** El par de claves es de prueba, sin almacenamiento seguro, rotación ni distribución; la raíz de confianza para una versión productiva es un problema abierto (`tooling/keys/generate-testing-key.sh:1-15`; Informe, Anexo III.6 §E).
10. **Lecturas de memoria del propio demonio.** El hilo monitor no puede leer un proceso si el demonio no corre como root (`main.rs:437-459`). Un comentario de ese bloque (`main.rs:447-450`) todavía menciona una exención a root que el kernel ya no aplica (`quark_kernel.c:476-483`): discrepancia de documentación, sin efecto en la ejecución.
11. **Documentación desactualizada.** `docs/funcionamiento_codigo.md:13` atribuye al módulo ganchos LSM sobre `ptrace_access_check`, y `docs/funcionamiento_codigo.md:9-11` describe solo el prototipo de espacio de usuario; el código real usa `kretprobe` y canal firmado. Para este capítulo se tomó el código (R12 del registro de riesgos).
12. **Sobrecarga.** No se midió el costo en rendimiento de los ganchos (R14 del Informe).

## **9.9. Solución: estado e integración**

Estado de las ramas al 2026-11-13 (Informe, Update §F): la solución descrita está integrada en `Dev@35c6031`. La rama `feature/gameStartProtection` (`2b088ab`, 4 commits sobre `35c6031`) no está integrada y agrega, según `git diff --stat`: `tooling/install.sh` (instalador que copia a `/opt/quark-anticheat` y habilita las unidades; avisa si falta BPF-LSM, `tooling/install.sh:1-22`), un cambio en `game_target/game.c` para que el juego de prueba se niegue a iniciar si `quark_sdk_init()` falla o si `quark_sdk_is_bpf_lsm_active()` es 0, y una reescritura de `run_test_no_quark.sh`. Esa política de rechazo no existe en `Dev`, donde el juego de prueba continúa sin protección (`game_target/game.c:40-43` en `Dev`). Dado que la rama no está integrada, queda fuera de la solución descrita arriba.

Validación respaldada por documentación (no repetida por esta redacción; alcance: VM, build de *testing*): bloqueo del `cheat` con RecoilEngine real y control negativo con el módulo descargado (`docs/vm_test_environment.md` §7); *watchdog* con retardo observado de ~5,5 s (§8); 12 programas BPF cargados y comprobaciones de autoprotección (§15.4). Falta medir tasa de detección, falsos positivos y sobrecarga.

# **CAPÍTULO X — RECURSOS DEL PROYECTO**

## **10.1. Recursos humanos**

* **Martínez Alarcón, Gabriel Sebastián** — autor, líder de proyecto y analista; presenta y defiende el PIF en febrero.
* **Merino De Rui, Stefano Nahuel** — colaborador, analista y desarrollador, con atribución; no presenta ni defiende este PIF y adeuda materias para ser elegible.
* **Cátedra:** Ing. Sergio Lapertosa, Ing. Augusto Portillo e Ing. Martin Jones.

El esfuerzo planificado ascendía a ≈ 696 horas por integrante a lo largo de 8 meses (≈ 22 h/semana) según la estimación original (sección 5.6). Esa cifra proviene del EAF de origen (3,76) y de 8 KSLOC estimadas; recalculada con el tamaño real (2,762 KSLOC) y el EAF corregido (3,34), la estimación equivale a ≈ 376 horas-persona totales. **Las horas reales no se registran**, por lo que no se informa esfuerzo real.

## **10.2. Recursos físicos y materiales**

* Equipos personales del autor y del colaborador, para el desarrollo y la ejecución de máquinas virtuales de prueba.
* VM QEMU/KVM con Nobara Linux 43 (kernel 7.0.9), accesible por SSH, con disco de 23 GB (`docs/vm_test_environment.md`, §1).
* Propuesta a futuro: VM CachyOS (kernel 7.3.1, 4 CPU, 7,7 GiB de RAM, disco de 26 GiB; `vm/README.md`).
* Equipo anfitrión con Arch Linux y contenedores Docker (Fedora 44) para compilar los plugins de IA de RecoilEngine (`tooling/recoil-fedora-build/`).

## **10.3. Recursos financieros**

El proyecto se desarrolla sin financiamiento externo. No se contempla la contratación de infraestructura en la nube ni la adquisición de licencias (ver restricciones económicas, Capítulo III). El costo principal son las horas de trabajo de las personas involucradas, no registradas en dinero.

## **10.4. Recursos tecnológicos**

* **Lenguajes:** C (módulo de kernel, SDK, `quark_cli`, programas eBPF, juego simulado y atacante); Rust, edición 2024 (servicio); C++ (RecoilEngine, componente de terceros).
* **Bibliotecas:** `libbpf-rs` 0.27, `libbpf-cargo` 0.27 (compilación), `libc` 0.2; OpenSSL `libcrypto` (`quark_cli`); API criptográfica del kernel (`crypto_alloc_sig("x962(ecdsa-nist-p256)")`).
* **Interfaces del kernel:** `kretprobe`, Netlink protocolo 31, BPF-LSM y tracepoints; Netfilter no se utiliza.
* **Herramientas:** GCC, clang/LLVM (para módulos en kernels compilados con clang), `bpftool` (genera `vmlinux.h`), `clang-tidy` (`make lint`), `cargo`, systemd (`quark.socket`, `quark.service`, `quark-kernel.service`), Docker, QEMU/KVM, git y GitHub, pandoc y tectonic (generación del informe).
* **Distribución de pruebas:** Nobara Linux 43; CachyOS como propuesta a futuro.
* La licencia del proyecto es GNU GPLv3 (Capítulo VIII). Las licencias de las herramientas auxiliares usadas en pruebas no se verificaron (UNVERIFIED).

## **10.5. Otros recursos del proyecto**

El vault de Obsidian (documentación y registro de evidencia), la investigación propia `proton-anticheats` y el juego de código abierto Beyond All Reason, vía RecoilEngine, como caso de integración.

# **CAPÍTULO XI — OPORTUNIDADES DEL PROYECTO**

## **11.1. CANVAS del proyecto**

Se adapta el Business Model Canvas (Osterwalder & Pigneur, 2010) a un proyecto de código abierto sin comercialización: la columna de ingresos se reemplaza por sostenibilidad y no se declara ninguna cifra.

**Tabla XI-1. CANVAS de Quark Anticheat**

| Bloque | Contenido |
|---|---|
| **Segmentos de clientes / usuarios** | Desarrolladores de juegos de código abierto o independientes que quieran integrar un anticheat en Linux; jugadores de GNU/Linux; comunidad de seguridad e investigadores; cátedra y estudiantes (uso académico). Tamaño del segmento Linux: estimación en el Capítulo IV (4.5); el de los demás segmentos no se estimó. |
| **Propuesta de valor** | Anticheat abierto, auditable y documentado para Linux; protección local en Ring 0 (bloqueo de `ptrace`, `/proc/<pid>/mem`, `process_vm_*`) reforzada con BPF-LSM; SDK con política de fallo cerrado; trazabilidad de cada afirmación (Claims-Ledger). |
| **Canales** | Repositorio público y documentación; divulgación en comunidades de gaming en Linux (Cap. VII); integración vía pull request en motores de código abierto (PR #1 en RecoilEngine); defensa y bibliografía académica. |
| **Relación con clientes** | Soporte comunitario por issues y pull requests; documentación técnica; ayuda de integración a proyectos adoptantes (alcance pendiente de definir por el equipo). |
| **Fuentes de ingresos / sostenibilidad** | No hay ingresos ni comercialización (Cap. III). Sostenibilidad: tiempo voluntario de los autores, contribuciones de la comunidad, uso académico. Financiamiento externo (becas, fondos para software libre): no explorado, sin datos. |
| **Recursos clave** | El autor y un colaborador (esfuerzo en Cap. V 5.6); código (kernel, demonio, SDK); vault de documentación; equipos personales y VM QEMU/KVM; investigación `proton-anticheats`. |
| **Actividades clave** | Desarrollo y pruebas del módulo, demonio y SDK; medición de overhead y tasas de detección (pendiente); investigación comparada; documentación; integración con motores. |
| **Socios clave** | Proyectos de juegos de código abierto (Beyond All Reason / RecoilEngine); comunidad del kernel de Linux (interfaces LSM, eBPF, Rust for Linux); la universidad (cátedra). No se tomaron contactos externos ni hay compromisos formales de socios. |
| **Estructura de costos** | Sin financiamiento externo (Cap. III, 3.4); costo principal: horas de trabajo de los integrantes; infraestructura sin costo (software libre, equipos personales). Cualquier costo monetario: no registrado. |

## **11.2. Oportunidades de escalabilidad e innovación**

Cada oportunidad indica su fuente y su estado. Ninguna está implementada hoy salvo indicación contraria (Features §5).

1. **Atestación verificada por servidor.** Hoy `quark_sdk_is_active()` y similares devuelven valores calculados por el cliente, falsificables con `LD_PRELOAD`. La firma debería originarse en el kernel. Queda abierto el problema de la raíz de confianza (clave por máquina, confianza en el primer uso, clave del proveedor o cita TPM 2.0). Es la brecha de mayor valor y la que Riot menciona como motivo de su negativa (GamingOnLinux, 2024a). Fuente: `EAC_bridge_and_quark_takeaways.md` §3.
2. **SDK del lado servidor y prueba cliente-servidor de punta a punta.** No implementados (Features §5). Habilitan que un estudio decida con base en la atestación.
3. **Canal de mensajes del anticheat por la red del propio juego** y **reporte tipado de violaciones.** Fuente: `EAC_bridge_and_quark_takeaways.md` §3.
4. **Gancho `lsm/mmap_file`** para mapeos ejecutables de archivos ajenos, que `EXEC_MPROTECT` no cubre. Fuente: `EAC_BPF_LSM_Service.md` §7.
5. **Ampliación de la cobertura de detección** a nuevos vectores (Cap. I, objetivo 2) y límites hoy declarados: DLL o `LD_PRELOAD` que escribe sin llamadas al sistema no es observable; `/proc/<pid>/maps` legible por root (Anexo III.6, §B).
6. **Soporte multi-distribución y de versiones de kernel** más allá de Nobara 43 y del entorno de VM, con una VM CachyOS (kernel 7.3.1, compilado con clang) como propuesta a futuro (`vm/README.md`); hoy solo hay validación en VM y el build de *release* no se probó en hardware físico (Anexo III.6, §C).
7. **Migración progresiva de C a Rust** a medida que maduran los bindings del kernel; el soporte de Rust dejó de considerarse experimental en 2025 (Ojeda, 2025). El módulo actual está escrito en C por la contingencia del riesgo R2.
8. **Detección basada en comportamiento del lado del servidor** como complemento de la observación a nivel de kernel (Cap. XI previsto en el avance de mayo).
9. **Integración con más motores de código abierto** y distribución como paquete de distribución (instalador `tooling/install.sh`, rama `feature/gameStartProtection` sin integrar al 2026-11-13).
10. **Alineación con la tendencia de la industria.** EAC v2 adopta BPF-LSM (información pública secundaria); la convergencia valida la dirección técnica y abre la posibilidad de contraste reproducible cuando exista un juego con EAC v2 disponible (captura bloqueada hoy).
11. **Línea académica.** El material (vault, Claims-Ledger, investigación de anticheats bajo Proton) es reutilizable como caso de estudio de seguridad en Linux. Publicación académica o uso en cátedra: no acordado. La continuación del desarrollo por parte del colaborador, posterior a la defensa, es una oportunidad fuera del alcance de este PIF.

**Riesgos de las oportunidades.** La dependencia de interfaces internas del kernel (R7), la ausencia de medición de rendimiento (R14) y la configuración exigida al usuario (BPF-LSM, Secure Boot, TPM) limitan la escalabilidad real. Ninguna oportunidad se presenta como viable sin validación propia.

# **CAPÍTULO XII — LECCIONES APRENDIDAS DEL PROYECTO**

## **12.1. Alcance y fuentes**

Este capítulo recoge lo que el historial del repositorio y las notas del vault permiten afirmar sobre la ejecución del proyecto. No existen revisiones por hito escritas en su momento (ver 12.3.1), por lo que las lecciones se derivan de una reconstrucción desde git ([[Cycle-Log]], entrada 2026-11-11, rotulada como no contemporánea) y de los registros de riesgos, pruebas y afirmaciones. Trello, las reuniones semanales y los registros semanales de avance no se revisaron para esta versión (UNVERIFIED; [[Process-Recommendation]], "Limitaciones de esta evaluación").

## **12.2. Aspectos positivos**

**12.2.1. La contingencia del riesgo R2 se ejecuta y resulta viable.** El plan contingente de R2 (componentes sin bindings estables en C) estaba escrito antes del desarrollo (§5.7). El módulo de kernel resulta en C (`kernel/quark_kernel.c`), el demonio en Rust y los programas eBPF en C cargados con `libbpf-rs` (Anexo III.6, B; [[Risk-Register]] Update 2026-11-11; [[Claims-Ledger]] fila 12). La decisión por componente, que la sección 5.7 exigía documentar, queda sustentada por una restricción técnica concreta: un LSM clásico no se registra desde un módulo fuera del árbol porque `security_add_hooks()` solo existe durante la inicialización y no se exporta; la capa LSM se obtiene mediante BPF-LSM desde el demonio ([[Features]] §1.5; [[Claims-Ledger]] fila 13).

**12.2.2. Los hallazgos de seguridad propios se corrigen en el desarrollo.** Durante el diseño del canal de control se encuentran dos fallas de escalada local: (1) cualquier proceso local podía abrir un socket Netlink (protocolo 31) y ordenar desproteger el PID de otro; (2) el socket Unix del demonio (`/tmp/quark.sock`, `SocketMode=0666`) confiaba en el `pid` declarado por el cliente, de modo que el propio demonio, con privilegios de root, desprotegía a la víctima (`docs/vm_test_environment.md:610-624`, `docs/features.md:157-163`). La corrección se hace en capas (pid real por `SO_PEERCRED`, emisor root verificado por el kernel, hash SHA-256 de `quark_cli`, firma ECDSA P-256 con nonce creciente; commit `48cc3f6`; [[Features]] §2). El documento de la VM deja asentado que corregir solo la primera falla habría sido insuficiente porque la segunda produce el mismo efecto (`docs/vm_test_environment.md:623-624`). Estado de la verificación: DOCUMENTED, sin reverificar ([[Claims-Ledger]] fila 7). Queda un residual declarado: `SocketMode=0666` ([[Risk-Register]] Update 2026-11-11, R10).

**12.2.3. Las pruebas realimentan el diseño.** El hallazgo en la VM de que Cheat Engine leía memoria sin error tras un reinicio sin módulo cargado ([[VM-test-environment]] §11) produce el comportamiento de fallo cerrado (`2624ae4`: el SDK no informa éxito sin confirmación del kernel) y luego la detección de VM con build *testing* y atestación (`333bbe2`) ([[Cycle-Log]], "Lazo de retroalimentación observable"). La cronología también corrige una lectura previa: `2624ae4` (03:14 UTC) es anterior a las capturas formales del 2026-08-29 (03:33 UTC), por lo que estas no motivaron ese arreglo.

**12.2.4. La validación distingue causa de correlación.** El resultado principal está acotado por un control negativo: con el módulo cargado, el ataque por `/proc/<pid>/mem` falla con `EACCES` en 10 de 10 repeticiones; sin defensa funciona en 5 de 5; al descargar el módulo vuelve a funcionar sobre el mismo PID, lo que atribuye el bloqueo a Quark y no a Yama ([[Capture-findings-2026-08-29]] §2; [[Test-Status]]). Alcance: VM, build de *testing*, juego simulado; además hay una validación sobre el motor real ([[VM-test-environment]] §7).

**12.2.5. La integración con un juego real se logra.** El SDK se incorpora a RecoilEngine (*Beyond All Reason*), que impide iniciar una partida protegida si Quark no confirma la protección (PR #1; [[VM-test-environment]] §6.5, §7). El riesgo R6 pasa a estado mitigado ([[Risk-Register]]).

**12.2.6. La práctica de afirmar solo con evidencia se instala.** El [[Claims-Ledger]] clasifica cada afirmación como SUPPORTED, DOCUMENTED, NOT MEASURED o CONTRADICTED, y [[Working-Guidelines]] §6 define cuándo una afirmación está lista para el informe. Esta práctica permite declarar con precisión lo no medido (filas 10, 11, 14, 15) en lugar de repetir la formulación aspiracional del README.

**12.2.7. El análisis de la competencia aporta una validación de rumbo.** El relevamiento sobre Easy Anti-Cheat y BattlEye bajo Proton, y la información pública sobre EAC para Linux v2 basada en BPF-LSM, indican que la industria converge hacia el mecanismo que Quark usa en su capa BPF-LSM (Anexo III.6, D). Alcance: información pública y análisis estático; el comportamiento de EAC v2 no se observó.

## **12.3. Aspectos a mejorar**

**12.3.1. Falta de registro contemporáneo del proceso.** El informe declara modelo en espiral con prácticas SCRUM (§6.1), pero el historial muestra prototipos sucesivos integrados por *pull request* sin análisis de riesgo escrito por ciclo, planificación del ciclo siguiente, *sprints* ni velocidad ([[Cycle-Log]], "Lo que NO muestra el historial"; [[Process-Recommendation]], contexto). Los indicadores de la sección 6.5 (ICC, velocidad en SP, desvío de esfuerzo) no se calcularon con datos de la época (UNVERIFIED: ningún documento revisado los contiene). Los ciclos C1–C6 son interpretación posterior. Lección: la puerta de riesgo por iteración de [[Working-Guidelines]] §2 (objetivo, alcance, tres riesgos, criterio de salida, decisión GO/NO-GO/PIVOT) se aplica desde el inicio de cada ciclo y no al final. La desviación se declara así: modelo en espiral declarado; ejecución real, prototipado evolutivo guiado por riesgo (ADR-001, aceptada por el autor; la línea de aceptación en la ADR queda por agregarse).

**12.3.2. Trabajo en ráfagas.** Los commits se concentran en junio, fines de agosto, octubre y noviembre; entre 2026-06-26 y 2026-08-27 no hay commits y la causa no consta (UNVERIFIED) ([[Cycle-Log]]; Anexo III.6, F). Frente a una estimación de ≈ 22 h/semana por integrante (§5.6), el historial no permite contrastar horas reales, porque no hay registro de horas en las fuentes revisadas (UNVERIFIED). Lección: registrar horas y tareas semanalmente, como ya preveía la sección 6.2, para que el riesgo R5 (disponibilidad) y R3 (esfuerzo) tengan datos.

**12.3.3. Documentación que contradice al código.** El README de `Dev` y el informe original afirman un módulo "en Rust" y el uso del "framework LSM"; el módulo es C y la capa LSM es BPF-LSM ([[Claims-Ledger]] filas 12 y 13, CONTRADICTED). El README de `Dev` es aspiracional respecto del overhead (`contexto_proyecto.md`, según [[Test-Status]] Update 2026-11-11). El Resumen y el Cap. X decían "Rust como lenguaje principal"; se corrigieron en esta versión del informe. Esto se registra como R12 ([[Risk-Register]]). Lección: actualizar la documentación en el mismo *pull request* que cambia la decisión técnica, y no dejar la corrección en un bloque `Update` al final del informe.

**12.3.4. Divergencia de ramas.** `main` queda en el commit del 2026-06-11 más un cambio de `.gitignore`; la integración real ocurre en `Dev`. `feature/gameStartProtection` (4 commits, sin PR) hace que el juego simulado exija demonio y BPF-LSM para arrancar, con lo que el control negativo "sin Quark" deja de funcionar tal cual; `dev/docs` tampoco está integrada ([[Risk-Register]] R13; Anexo III.6, F; [[Plan-Inmediato-2026-11-25]], "Congelamiento del MVP"). Lección: un solo prototipo vivo, `main` actualizada solo con versiones congeladas y etiquetadas (`rc-1`, pendiente), y revisión del impacto sobre los scripts de prueba antes de cada *merge*.

**12.3.5. Procedencia de las capturas y defectos del harness.** Las capturas del 2026-08-29 se hicieron sin registrar `git_commit` ni `git_branch` en `environment.txt`, por lo que el commit probado no se puede demostrar y la correspondencia con `2624ae4` es probable pero UNVERIFIED ([[Test-Status]] Update 2026-11-11; [[Risk-Register]] R8). El harness presenta `results.csv` malformado y `summary.txt` que solo reporta la condición B; `quark_cli` informa éxito sin confirmación del kernel en el binario capturado ([[Capture-findings-2026-08-29]] §7.1, §7.6). Se asume sin corregir `capture.sh` (UNVERIFIED). Lección: fijar y registrar la revisión antes de capturar y tratar el harness como código sujeto a pruebas.

**12.3.6. Validación postergada hacia el final.** El overhead de CPU/RAM, las tasas de detección y falsos positivos, los intentos de evasión y el build de *release* en hardware físico no se midieron ([[Claims-Ledger]] filas 10, 11, 14, 15; [[Risk-Register]] R11 y R14). Medir esos aspectos corresponde a la etapa 4 del cronograma, pero la dependencia (el build de *release* se niega a proteger en una VM) era previsible desde el desarrollo de la detección de VM y no se anticipó en el registro de riesgos hasta noviembre. Lección: elegir tempranamente el entorno de medición y planificar la medición como parte de cada ciclo, no como actividad final.

**12.3.7. Estimación sin recalibración.** La estimación COCOMO usa constantes del modelo intermedio y un factor de reducción de 0,15 aplicado por criterio (§5.6, nota metodológica); además, el EAF de origen (3,76) tenía un error de cálculo (el producto de los multiplicadores es 3,34). Recién en esta versión el código real se contrasta con la estimación (2.762 SLOC medidas frente a 8.000 estimadas); no hay SP reales. Lección: comparar estimado y real al cierre de cada iteración, como establece el plan preventivo de R3.

**12.3.8. Encuesta y datos de mercado.** El instrumento de encuesta del Cap. II está diseñado y sin resultados; además, la serie histórica de Steam proviene de una compilación de procedencia débil. Lección: publicar el instrumento al inicio del cronograma, ya que depende de respuestas de terceros.

# **CAPÍTULO XIII — ENTREGABLES**

## **13.1. Código fuente del proyecto**

Módulo de kernel (C, `kernel/`), servicio en espacio de usuario (Rust, `quark_daemon/`), SDK (C, `sdk/`), programas eBPF (C, `quark_daemon/src/bpf/`), cliente de control `quark_cli` (C), herramientas de prueba (juego simulado `game_target/`, atacante `cheat/`, scripts de VM), unidades systemd (`quark_daemon/systemd/`) y scripts de instalación (`tooling/install.sh`, solo en la rama `feature/gameStartProtection`, sin integrar). Se alojan en el repositorio `Quark-Anticheat`, rama `Dev` (commit `35c6031`); el submódulo `RecoilEngine` contiene la integración con el motor. El repositorio, la titularidad y las ramas se detallan en el Anexo III.

**Repositorio oficial y versión entregada.** Repositorio `https://github.com/stefanomerinoderui/Quark-Anticheat`: código en la rama `Dev`, versión congelada en el commit `35c6031` (2026-11-05); documentación y licencia GNU GPLv3 (archivo `LICENSE`) en la rama `dev/docs`. La versión entregada se identifica por commit y no por etiqueta (UNVERIFIED que exista una etiqueta). El procedimiento de construcción, instalación y arranque consta en el Anexo III.5, que cumple la función de manual de despliegue porque `Dev` no contiene uno propio. El submódulo `RecoilEngine` apunta a `https://github.com/Billones142/RecoilEngine.git`.

## **13.2. Documentación**

**Tabla XIII-1. Documentación entregable y estado al 2026-11-25**

| Entregable | Estado | Ubicación |
| :---- | :---- | :---- |
| Documento de diseño preliminar (E1.4) | Parcial: las decisiones constan en fuentes dispersas; el documento como tal no consta | Vault (`Risk-Register`, `Features`), `docs/contexto_proyecto.md` |
| Diagramas y diseño de arquitectura (E2.3) | Existe, en forma tabular | Capítulo IX; `Architecture-Overview` |
| Prototipo funcional integrado con un videojuego de código abierto (MVP) | Existe; alcance VM y build de pruebas | `Dev@35c6031`; Anexo III |
| Informe de validación con tasas de detección y falsos positivos | No existe; existe el informe de capturas con 10/10, 5/5 y control negativo | `Capture-findings-2026-08-29` |
| Medición del overhead de CPU y RAM | No existe | — |
| Documentación técnica | Existe | `docs/features.md`, `docs/vm_test_environment.md`, `docs/log_messages.md`, `docs/funcionamiento_codigo.md` (en `Dev`); vault |
| Investigación comparada de anticheats bajo Proton | Existe | Repositorio `proton-anticheats`; `Proton-Anticheat-Research` |
| Informe del PIF (este documento) | Presente, con los apartados pendientes declarados | `Informe-PIF-Avance.md`; `sh tooling/build_informe.sh` |
| Material de defensa | En curso | — |

# **CONCLUSIONES DEL PROYECTO**

Las conclusiones son de carácter **parcial**: el proyecto no cierra todas las mediciones comprometidas en el Capítulo I. Cada conclusión indica alcance y fuente.

## **C.1. Frente al objetivo general**

El objetivo general comprometía analizar, diseñar y desarrollar un anticheat de nivel de kernel para GNU/Linux y evaluar su viabilidad técnica, su impacto en el rendimiento y los riesgos de seguridad asociados a los privilegios de kernel. Se logra un prototipo funcional de tres piezas (módulo de kernel v0.4.0, demonio, SDK en C) y se muestra, dentro de una VM, con build de *testing* y juego simulado, que un módulo de kernel reforzado con BPF-LSM impide el acceso externo a la memoria de un proceso protegido y que el mecanismo se integra en un motor real (Anexo III.6, A y G; [[Test-Status]]). **No se evalúa el impacto en el rendimiento**, por lo que la parte del objetivo y de la misión referida a "sin degradar la experiencia del usuario" **no tiene respaldo medido**. No se afirma bajo impacto de rendimiento ([[Claims-Ledger]] fila 10, NOT MEASURED). Los riesgos de seguridad de los privilegios de kernel se abordan en parte: se encuentran y corrigen dos fallas propias de escalada local (12.2.2), y quedan límites declarados en [[Known-Limitations]].

## **C.2. Frente a los objetivos específicos**

**Tabla C-1. Cumplimiento de los objetivos específicos**

| N° | Objetivo (Cap. I, 1.2) | Estado | Evidencia |
|---|---|---|---|
| 1 | Definir la arquitectura (kernel, servicio, interfaz) en un documento de diseño | Parcial. La arquitectura existe en código y en la documentación de `Dev` ([[Features]]); el Cap. IX se redacta a partir de ella. Entregable E1.4/E2.3 como documento formal: UNVERIFIED | Anexo III.6, A–B |
| 2 | Identificar y documentar al menos cinco vectores de ataque | Parcial. El diseño cubre ptrace, `/proc/<pid>/mem`, `process_vm_readv/writev` y carga de BPF de *tracing*; con `EXEC_MPROTECT` como indicador. Eso suma cuatro vectores bloqueados o cubiertos más un indicador. La clasificación formal de cinco vectores no consta en las fuentes revisadas (UNVERIFIED) | [[Features]] §1.1, §1.5; Anexo III.6, A–B |
| 3 | Implementar la API/SDK y verificarla en un juego de código abierto | Logrado en lo esencial: SDK en C integrado en RecoilEngine/BAR; el motor no inicia una partida protegida sin confirmación. Faltan SDK de servidor y prueba cliente↔servidor | PR #1; [[VM-test-environment]] §6.5, §7; [[Features]] §5 |
| 4 | Validar con casos de prueba por vector, registrando tasas de detección y falsos positivos | Parcial. Un vector (`/proc/<pid>/mem`) con 10/10 de bloqueo y control negativo; `process_vm_*` y `ptrace` documentados sin reverificar. **No se calculan tasas de detección ni falsos positivos** | [[Test-Status]]; [[Claims-Ledger]] filas 1–3, 8, 11 |
| 5 | Medir el overhead de CPU y RAM | **No cumplido.** No existe medición | [[Claims-Ledger]] fila 10; [[Test-Status]] |

## **C.3. Lo que no se midió ni se probó**

- Overhead de CPU y RAM (Objetivo 5); plan: tres configuraciones, al menos 10 repeticiones, media y desviación ([[Working-Guidelines]] §3).
- Tasa de detección y falsos positivos; el KPI TDP ≥ 75 % (§6.5) no se calcula.
- Intentos de evasión o *bypass*: no hay pruebas. La inyección por DLL o `LD_PRELOAD` sin llamadas al sistema no es observable y `EXEC_MPROTECT` es solo un indicador ([[Claims-Ledger]] fila 14).
- Build de *release* en hardware físico: toda la validación usa build de *testing* en VM porque el de *release* se niega a proteger dentro de una VM ([[Claims-Ledger]] fila 15; R11).
- Latencia de detección de la verificación en espacio de usuario y comportamiento del *watchdog* con captura (sonda inconclusa) ([[Test-Status]]).
- Resultados de la encuesta del Cap. II (instrumento sin aplicar).

## **C.4. Limitaciones del resultado**

La conclusión es válida para: VM, build de *testing*, kernel de la distribución de referencia en la versión capturada (kernel y distribución de generaciones Fedora distintas, [[Capture-findings-2026-08-29]] §7.5), un juego simulado y un motor real. El diseño no cubre `/proc/<pid>/maps` legible por root, un máximo de 16 procesos protegidos y BPF-LSM *best-effort*: sin `bpf` en `lsm=` queda solo el `kretprobe` ([[Features]] §1.1, §1.5; [[Known-Limitations]]). No hay atestación verificada por servidor: `quark_sdk_is_active()` y similares devuelven valores calculados por el cliente (Anexo III.6, E).

## **C.5. Sobre el diferencial**

El relevamiento muestra que Easy Anti-Cheat para Linux v2 adopta BPF-LSM sin módulo de kernel (información pública secundaria; no observado). El diferencial de Quark pasa de "nativo de kernel" a "abierto, académico y documentado", con la ventaja de bloquear localmente en Ring 0 `ptrace`, `/proc/<pid>/mem` y `process_vm_*`. Esa ventaja se compara contra información pública, no contra el comportamiento medido de EAC (Anexo III.6, D–E).

## **C.6. Trabajo pendiente**

1. Congelar un candidato a versión (`rc-1`) y registrar `git_commit` y `git_branch` en cada captura; decidir las ramas `feature/gameStartProtection` y `dev/docs`.
2. Corregir el harness y re-capturar.
3. Medir el overhead y calcular detección y falsos positivos sobre una lista cerrada de casos (ataque por `/proc/pid/mem`, `ptrace`, `process_vm_*`, carga de BPF, `LD_PRELOAD`, lecturas legítimas como `ps` y `htop`).
4. Probar evasión y el build de *release* en hardware físico.
5. Implementar el SDK de servidor y la prueba cliente↔servidor ([[Features]] §5).

La defensa puede sostener que el prototipo demuestra viabilidad técnica *en el alcance indicado*; no puede sostener bajo overhead, tasas de detección ni resistencia a evasión hasta contar con esas mediciones.

# **Notas al pie de página**

1. GNU/Linux es un sistema operativo libre basado en el kernel Linux, creado por Linus Torvalds en 1991 e integrado con herramientas del proyecto GNU. Su código abierto permite acceder, modificar y distribuir el software. ↩

2. Un sistema anticheat es un conjunto de herramientas diseñadas para detectar y prevenir trampas en videojuegos competitivos, como bots, aimbots y modificaciones no autorizadas. ↩

3. El kernel es el núcleo central del sistema operativo que gestiona la comunicación entre el hardware y las aplicaciones de software. ↩

4. Una API (Interfaz de Programación de Aplicaciones) define las reglas para que diferentes software se comuniquen entre sí. ↩

5. Un SDK (Kit de Desarrollo de Software) proporciona herramientas, librerías y documentación para implementar esa comunicación, facilitando la integración de funcionalidades externas en nuevas aplicaciones. ↩

6. QEMU/KVM es una solución de virtualización que combina QEMU (emulador de código abierto) con KVM (aceleración por hardware del kernel Linux). Permite ejecutar múltiples máquinas virtuales simultáneamente con rendimiento cercano al nativo. ↩

7. LSM (Linux Security Modules) es un framework de seguridad que proporciona ganchos en el kernel para insertar módulos de control de acceso, base de implementaciones como SELinux y AppArmor; BPF-LSM permite adjuntar programas eBPF a esos ganchos. ↩

8. eBPF (Extended Berkeley Packet Filter) es una máquina virtual dentro del kernel que ejecuta bytecode verificado para monitoreo, análisis de tráfico y seguridad, cargable en tiempo de ejecución. ↩

# **Declaración de uso de inteligencia artificial**

Este apartado cumple la cláusula de cátedra sobre uso de IA generativa y el Art. 10.1.2 del Reglamento.

**Herramientas.** Claude Code (Anthropic), con los modelos que cada sesión registra (en este repositorio, `claude-sonnet-5-5`). Las sesiones de agente firman sus entradas como `agent:<modelo>`.

**Para qué se usó.**

1. Redacción e integración del informe: lectura de `origin/Dev` y del vault, armado de los Capítulos I a XIII, de las Conclusiones y de los Anexos a partir de las fuentes del repositorio, cálculo de SLOC y de COCOMO con herramientas del repositorio, y generación del PDF con `tooling/build_informe.sh`.
2. Redacción de notas del vault (`Claims-Ledger`, `Test-Status`, `Cycle-Log`, ADR) bajo la guía de trabajo del repositorio.
3. Desarrollo del código: 11 commits de la rama `Dev` (2026-08-27 a 2026-08-31, cuenta `Billones142`) llevan el trailer `Claude-Session` con la sesión de Claude Code citada más abajo. Cubren, entre otros, la autenticación del canal Netlink (`48cc3f6`), el rechazo de la protección en una VM con omisión de pruebas (`333bbe2`), el watchdog y la validación contra el motor real (`6b05ad7`).
4. Autorrevisión del informe con el harness de revisión de PIF de la cátedra y corrección de las observaciones resultantes (2026-11-25 y 2026-11-26).

**Cómo se verificó.**

- Cada afirmación sobre el código lleva `archivo:línea` o commit y se leyó de `Dev@35c6031`; lo inferido se marca `UNVERIFIED`.
- Los resultados de pruebas (10/10, 5/5, control negativo) provienen de capturas reproducibles y constan en el `Claims-Ledger`, con su alcance (VM, build de pruebas, juego simulado).
- El tamaño del código se midió con `tooling/sloc.py`.
- Las citas bibliográficas se contrastaron con las fuentes cuando fue posible; las que no se consultaron directamente quedan declaradas en la Bibliografía.
- Los autores revisan y responden por lo incluido, y pueden dar cuenta oralmente de cada parte.

**Prompts.** Las instrucciones permanentes dadas a los agentes están versionadas en `AGENTS.md`, en `Working-Guidelines.md` y en `Append-Only-Standard.md` del vault. Los pedidos de cada sesión se registran de forma resumida, no textual, en `docs/obsidian-vault/quark-vault/06-Cycles/AI-Prompt-Log.md`: qué se pidió y qué se produjo, y, cuando el pedido remite a un archivo, un resumen de las instrucciones de ese archivo. Los pedidos de la sesión de desarrollo de agosto de 2026 son UNVERIFIED (no se conserva la transcripción).

**Enlaces a las conversaciones.**

- Desarrollo del código: `https://claude.ai/code/session_01JeTq4KYFDuzr41fQnUoCfQ` (trailer `Claude-Session` de los 11 commits indicados).
- Sesiones de redacción del informe y de autorrevisión (2026-11-25 y 2026-11-26): sesiones de terminal local, sin enlace compartible; su contenido consta en el registro resumido indicado arriba.

**Alcance de la declaración.** Se declara el uso de Claude Code. UNVERIFIED si los integrantes usaron otras herramientas de IA generativa; en ese caso los autores las agregan aquí.

# **Bibliografía**

AreWeAntiCheatYet. (2026). *Are We Anti-Cheat Yet?* Recuperado el 25 de noviembre de 2026, de [https://areweanticheatyet.com/](https://areweanticheatyet.com/)

Boehm, B. W. (1981). *Software engineering economics*. Prentice-Hall.

Boehm, B. W. (1988). A spiral model of software development and enhancement. *Computer, 21*(5), 61–72. [https://doi.org/10.1109/2.59](https://doi.org/10.1109/2.59)

Boehm, B. W., Abts, C., Brown, A. W., Chulani, S., Clark, B. K., Horowitz, E., Madachy, R., Reifer, D. J., & Steece, B. (2000). *Software cost estimation with COCOMO II*. Prentice Hall.

Dot Esports. (2026, octubre). *Steam all-time record 43.5 million concurrent users* \[Título tomado de la URL; autor y día no verificados\]. Recuperado el 25 de noviembre de 2026, de [https://dotesports.com/general/news/steam-all-time-record-43-5-million-concurrent-users](https://dotesports.com/general/news/steam-all-time-record-43-5-million-concurrent-users)

Epic Online Services. (2021, 23 de septiembre). *Epic Online Services launches anti-cheat support for Linux, Mac and Steam Deck*. [https://onlineservices.epicgames.com/en-US/news/epic-online-services-launches-anti-cheat-support-for-linux-mac-and-steam-deck](https://onlineservices.epicgames.com/en-US/news/epic-online-services-launches-anti-cheat-support-for-linux-mac-and-steam-deck) (contenido tomado de resúmenes de búsqueda; la página exigió autenticación)

GamingOnLinux. (2021a, 24 de septiembre). *BattlEye confirms Linux support for Steam Deck will be opt-in like Easy Anti-Cheat*. [https://www.gamingonlinux.com/2021/09/battleye-confirms-linux-support-for-steam-deck-will-be-opt-in-like-easy-anti-cheat](https://www.gamingonlinux.com/2021/09/battleye-confirms-linux-support-for-steam-deck-will-be-opt-in-like-easy-anti-cheat)

GamingOnLinux. (2021b, 6 de noviembre). *Supporting Linux, Proton and the Steam Deck with BattlEye is just an email away*. [https://gamingonlinux.com/2021/11/supporting-linux-proton-and-the-steam-deck-with-battleye-is-just-an-email-away/](https://gamingonlinux.com/2021/11/supporting-linux-proton-and-the-steam-deck-with-battleye-is-just-an-email-away/)

GamingOnLinux. (2022, marzo). *Steam had a massive year in 2021 with 132 million monthly players*. [https://www.gamingonlinux.com/2022/03/steam-had-a-massive-year-in-2021-with-132-million-monthly-players/](https://www.gamingonlinux.com/2022/03/steam-had-a-massive-year-in-2021-with-132-million-monthly-players/)

GamingOnLinux. (2024a, 11 de abril). *Riot Games talk Vanguard anti-cheat for League of Legends and why it's a no for Linux*. [https://www.gamingonlinux.com/2024/04/riot-games-talk-vanguard-anti-cheat-for-league-of-legends-and-why-its-a-no-for-linux](https://www.gamingonlinux.com/2024/04/riot-games-talk-vanguard-anti-cheat-for-league-of-legends-and-why-its-a-no-for-linux)

GamingOnLinux. (2024b, septiembre). *Grand Theft Auto V gets BattlEye anti-cheat, breaks online play on Steam Deck / Linux*. [https://www.gamingonlinux.com/2024/09/grand-theft-auto-v-gets-battleye-anti-cheat-breaks-online-play-on-steam-deck-linux/](https://www.gamingonlinux.com/2024/09/grand-theft-auto-v-gets-battleye-anti-cheat-breaks-online-play-on-steam-deck-linux/) (descripción tomada del resumen de búsqueda)

GamingOnLinux. (2026, mayo). *Anti-cheat check — which competitive games actually work on Linux?* [https://www.gamingonlinux.com/guides/view/anticheat-check-which-competitive-games-actually-work-on-linux/](https://www.gamingonlinux.com/guides/view/anticheat-check-which-competitive-games-actually-work-on-linux/)

It's FOSS. (2026). *Epic Games wants Linux gamers. It's rebuilding EAC for Fortnite.* Recuperado el 25 de noviembre de 2026, de [https://itsfoss.com/news/epic-games-linux-anti-cheat-fortnite/](https://itsfoss.com/news/epic-games-linux-anti-cheat-fortnite/)

Martínez Alarcón, G. S., & Merino De Rui, S. N. (2026). *proton-anticheats* \[Repositorio de investigación\]. URL: pendiente de aportar.

New Relic. (2025, 3 de junio). *What is eBPF, and why does it matter for observability?* [https://newrelic.com/blog/observability/what-is-ebpf](https://newrelic.com/blog/observability/what-is-ebpf)

Ojeda, M. (2025, 12 de diciembre). *rust: conclude the Rust experiment* \[Mensaje en lista de correo\]. Linux Kernel Mailing List. [https://lkml.iu.edu/hypermail/linux/kernel/2512.1/06411.html](https://lkml.iu.edu/hypermail/linux/kernel/2512.1/06411.html)

Osterwalder, A., & Pigneur, Y. (2010). *Business model generation*. Wiley.

panke. (2024, 8 de diciembre). *Compilación de la Steam Hardware & Software Survey, 2016–2024* \[Nota; título y URL exactos: pendiente de aportar\]. note.com. (Datos copiados de Reddit sin verificación; carga manual desde julio de 2024.)

Phoronix. (s. f.). *Epic Games to improve Easy Anti-Cheat on Linux with anti-cheat systemd service & eBPF.* Recuperado el 25 de noviembre de 2026, de [https://phoronix.com/news/Easy-Anti-Cheat-Better-Linux](https://phoronix.com/news/Easy-Anti-Cheat-Better-Linux)

Schwaber, K., & Sutherland, J. (2020). *The Scrum Guide: The definitive guide to Scrum — The rules of the game.* [https://scrumguides.org/](https://scrumguides.org/)

The kernel development community. (2024a). *Linux Security Modules: General security hooks for Linux.* The Linux Kernel documentation. [https://www.kernel.org/doc/html/latest/security/lsm.html](https://www.kernel.org/doc/html/latest/security/lsm.html)

The kernel development community. (2024b). *Rust.* The Linux Kernel documentation. [https://www.kernel.org/doc/html/latest/rust/](https://www.kernel.org/doc/html/latest/rust/)

United States Patent and Trademark Office. (2024). *Nice Agreement twelfth edition, version 2024: General remarks, class headings and explanatory notes*. [https://www.uspto.gov/trademarks/trademark-updates-and-announcements/nice-agreement-twelfth-edition-version-2024-general](https://www.uspto.gov/trademarks/trademark-updates-and-announcements/nice-agreement-twelfth-edition-version-2024-general)

Valve Corporation. (s. f.). *Anti-cheat and game bans*. Steamworks Documentation. [https://partner.steamgames.com/doc/features/anticheat/vac_integration](https://partner.steamgames.com/doc/features/anticheat/vac_integration)

Valve Corporation. (2026). *Steam Hardware & Software Survey: October 2026.* Recuperado el 25 de noviembre de 2026, de [https://store.steampowered.com/hwsurvey/](https://store.steampowered.com/hwsurvey/)

Valve Developer Community. (s. f.). *Valve Anti-Cheat*. [https://developer.valvesoftware.com/wiki/Valve_Anti-Cheat](https://developer.valvesoftware.com/wiki/Valve_Anti-Cheat) (contenido tomado de resumen de búsqueda)

Wikipedia. (2026a). *Kernel-level anti-cheat.* [https://en.wikipedia.org/wiki/Kernel-level\_anti-cheat](https://en.wikipedia.org/wiki/Kernel-level_anti-cheat)

Wikipedia. (2026b). *Easy Anti-Cheat.* [https://en.wikipedia.org/wiki/Easy\_Anti-Cheat](https://en.wikipedia.org/wiki/Easy_Anti-Cheat)

World Intellectual Property Organization. (s. f.-a). *Nice Classification*. [https://www.wipo.int/classifications/nice/en/](https://www.wipo.int/classifications/nice/en/)

World Intellectual Property Organization. (s. f.-b). *Filing international trademark applications: Classification of goods and services*. [https://www.wipo.int/de/web/madrid-system/how_to/file/madrid-system-filing-international-trademark-applications-classification-of-goods-and-services](https://www.wipo.int/de/web/madrid-system/how_to/file/madrid-system-filing-international-trademark-applications-classification-of-goods-and-services)

#

# **Anexos**

*Las hojas de los anexos se numeran de forma independiente, indicando "página X de Y".*

## **Anexo I — Datos relevados**

*Numeración propia: «página X de Y».*

### I.1. Cuestionario (versión de diseño)

La estructura de bloques y las preguntas clave están en 2.3. Material de origen: `docs/Quark_Encuesta_Diapositivas.txt`, presentación de diseño que no es el cuestionario final. El texto del cuestionario final de unos 25 ítems, su fecha de publicación y las respuestas deben aportarse por una persona del equipo tras definirlos con la cátedra.

### I.2. Datos de fuentes secundarias

**Tabla I.1. Datos puntuales**

| Dato | Valor | Fuente | Consulta |
|---|---|---|---|
| Linux, Steam Survey, oct. 2026 | 3,95 % (+0,90 pp) | Valve (2026) | 2026-11-25 |
| Windows, ídem | 93,70 % (−1,33 pp) | Valve (2026) | 2026-11-25 |
| macOS, ídem | 2,35 % (+0,43 pp) | Valve (2026) | 2026-11-25 |
| Linux, jun. 2024 (último mes con dato) | 2,08 % | panke (2024) | `docs/steam-historic-hardware-survey-os.tsv` |
| Linux, mínimo / máximo de la serie | 0,49 % (2018-jul) / 2,32 % (2024-may) | panke (2024) | ídem |
| Arch Linux, 2019-sep / 2024-jun | 0,09 % / 0,17 % | panke (2024) | ídem |
| Manjaro, 2018-dic / 2024-jun | 0,05 % / 0,06 % | panke (2024) | ídem |
| Juegos listados | 1.167 | AreWeAntiCheatYet (2026) | 2026-11-25 |
| Supported / Running / Planned / Broken / Denied | 196 / 280 / 2 / 636 / 53 | AreWeAntiCheatYet (2026) | 2026-11-25 |
| Usuarios activos mensuales de Steam, fin de 2021 | 132 millones | GamingOnLinux (2022), que reproduce el informe anual de Valve | 2026-11-25 |
| Récord de usuarios simultáneos, oct. 2026 | 43,5 millones (SteamDB, según prensa) | Dot Esports (2026) | 2026-11-25 |

### I.3. Series y gráficos

Los datos crudos están en `docs/steam-historic-hardware-survey-os.tsv` y `docs/steam-historic-hardware-survey.tsv` (compilación de panke, sin editar). Los gráficos se generan con `python tooling/grafico_steam_so.py` y `python tooling/grafico_steam_idiomas.py`, que escriben en `docs/figuras/`. Las celdas vacías son dato faltante y no se interpolan. La serie de Linux termina en 2024-jun.

### I.4. Respuestas de la encuesta

Sin datos: la encuesta no se publicó. Las respuestas exportadas sin editar, el tamaño de muestra, la tasa de finalización y el tiempo medio se anexan aquí cuando existan y los aporta una persona del equipo.

### I.5. Registro de método

Los valores de Valve y AreWeAntiCheatYet se obtuvieron el 2026-11-25 mediante lectura automática de las páginas; no hay captura de pantalla archivada. Las cifras de usuarios de Steam provienen de notas de prensa y no de la fuente primaria de Valve.

## **Anexo II — Documentos del entorno o dominio del Proyecto**

*Numeración propia: «página X de Y».*

### II.1. Planificación

Las tablas de planificación del Capítulo V (cronograma Gantt, tiempos PERT, entregables, hitos y riesgos) constituyen el detalle del cronograma. El grafo PERT con CPM no se incorpora como lámina; sus precedentes y el camino crítico constan en la Tabla V-4 y en 5.5.

### II.2. Medición de tamaño (SLOC)

Comando: `python tooling/sloc.py ../quark-wt/Dev` (worktree de solo lectura en `Dev@35c6031`). El script cuenta líneas no vacías y no solo comentario. Salida registrada:

| Componente | SLOC |
| :---- | :---- |
| Módulo de kernel (C): `quark_kernel.c` 417; `quark_pubkey.h` 4 | 421 |
| Servicio (Rust): `main.rs` 481; `bpf.rs` 366; `build.rs` 18 | 865 |
| Programas eBPF (C): `quark.bpf.c` 240; `quark_events.h` 25 | 265 |
| `quark_cli` (C) | 197 |
| SDK (C): `quark_sdk.c` 210; `quark_sdk.h` 19 | 229 |
| Pruebas y harness: `game.c` 88; `cheat.c` 65; `run_test.sh` 69; `run_test_kernel.sh` 102; `run_test_kernel_release.sh` 110; `run_test_no_quark.sh` 64; `capture.sh` 287 | 785 |
| TOTAL | 2.762 |

### II.3. Documentos de dominio

Documentación técnica de `Dev` (`docs/features.md`, `docs/vm_test_environment.md`, `docs/log_messages.md`, `docs/funcionamiento_codigo.md`), registro de afirmaciones y de pruebas del vault (`Claims-Ledger`, `Test-Status`, `Capture-findings-2026-08-29`), investigación `proton-anticheats` y reglamento de referencia (`docs/RR-97-23-Reglamento-de-Proyecto-Integrador-Final.md`).

### II.4. Scripts de generación

`tooling/build_informe.sh` (documento), `tooling/grafico_steam_so.py` y `tooling/grafico_steam_idiomas.py` (figuras del Capítulo II) y `tooling/sloc.py` (tamaño).

## **Anexo III — Otros anexos**

### **III.1. Estado del producto mínimo viable congelado**

El prototipo se congela en el commit `35c6031` de la rama `Dev` del repositorio `Quark-Anticheat` (2026-11-05, 19:33 -03:00). El estado se describe a partir de la lectura del código y de la documentación; no se ejecutó ninguna prueba para redactar este anexo. La rama `feature/gameStartProtection` (`2b088ab`, 2026-11-06) contiene cuatro commits adicionales sin integrar.

**Tabla III.1. Commits por rama remota** (fuente: `git log` y `git rev-list --count` sobre los remotos, 2026-11-25)

| Rama remota | Último commit | Fecha | Relación con `Dev` |
|---|---|---|---|
| `origin/Dev` | `35c6031` | 2026-11-05 | Rama de integración; 29 commits, primero `a0700dd` (2026-06-11); integra PR #1 (`5401750`), #2 (`0710fc6`) y #3 (`e258e2e`) |
| `origin/feature/gameStartProtection` | `2b088ab` | 2026-11-06 | 4 commits por delante, sin PR: `9741595`, `69cdab6`, `04b9f58`, `2b088ab` |
| `origin/feat/bpf-lsm-telemetry` | `e497dbf` | 2026-10-05 | Integrada en `Dev` (PR #2) |
| `origin/dev/linter` | `8116604` | 2026-06-26 | Integrada en `Dev` (PR #3) |
| `origin/dev/docs` | `7604129` | 2026-11-14 | 6 commits por delante de `Dev`: vault, estándar de escritura, README corregido, generación del PDF |
| `origin/main` | `989693f` | 2026-11-13 | Contiene el commit inicial del 2026-06-11 y un cambio de `.gitignore`; no incluye el desarrollo de `Dev` |

**Contenido de `feature/gameStartProtection`** (`git diff --stat Dev..2b088ab`: 5 archivos, +234 −86): `tooling/install.sh` (instalador que advierte si BPF-LSM no está activo), cambios en `game_target/game.c` (el juego simulado se niega a correr sin el demonio ni BPF-LSM), `run_test_no_quark.sh`, `docs/features.md` y `vm/README.md`. Esta rama modifica el control negativo «sin Quark» (el juego deja de arrancar sin demonio), por lo que invalida ese caso tal como está escrito ([[Test-Status]] Update 2026-11-11).

**Tabla III.2. Módulos del prototipo** (líneas físicas `wc -l`, `Dev@35c6031`)

| Módulo | Lenguaje | Ruta | Líneas | Función | Fuente |
|---|---|---|---|---|---|
| Módulo de kernel v0.4.0 | C | `kernel/quark_kernel.c`, `kernel/quark_pubkey.h` | 648 + 11 | `kretprobe` sobre `ptrace_may_access`; deniega acceso *attach* a hasta 16 PID protegidos; canal Netlink (proto 31) con uid verificado, hash SHA-256 de `quark_cli`, firma ECDSA P-256 y nonce creciente; detección de VM por CPUID; build *release* y *testing* | `docs/features.md:11-68, 155-237` |
| Demonio | Rust | `quark_daemon/src/main.rs`, `bpf.rs`, `build.rs` | 622 + 455 + 26 | Socket Unix con `SO_PEERCRED`, orden de protección, monitor de variables cada 50 ms con `kill -9`, carga de BPF-LSM y telemetría con `libbpf-rs` | `features.md:70-153` |
| Programas eBPF | C | `quark_daemon/src/bpf/quark.bpf.c` | 402 | 12 programas: `bpf_prog_load`, `bpf_map`, `bpf_prog`, `bpf`, `ptrace_access_check`, `file_mprotect`, `task_kill`, tracepoints de `process_vm_*`, `module_load`, `exec`, `exit` | `features.md:93-153`; `vm_test_environment.md:818-830` |
| Cliente de control | C | `quark_daemon/quark_cli.c` | 260 | Firma y envía comandos por Netlink | `features.md:185-197` |
| SDK | C | `sdk/quark_sdk.c`, `quark_sdk.h` | 285 + 105 | `quark_sdk_init` (falla si el kernel no confirma), vigilancia de variables, *watchdog*, atestación | `features.md:85-91, 239-250` |
| Juego simulado y atacante | C | `game_target/game.c`, `cheat/cheat.c` | 115 + 83 | Objetivo y herramienta de ataque de las pruebas | `Makefile` |
| Integración con motor real | C++ | submódulo `RecoilEngine` | n/d | Motor de *Beyond All Reason*; impide iniciar partida protegida si Quark no confirma | `vm_test_environment.md:36-60, 353-372`; `features.md:260-262` |
| Unidades systemd | — | `quark_daemon/systemd/` | n/d | `quark.socket`, `quark.service`, `quark-kernel.service` | [[Architecture-Overview]] Update |
| Pruebas | Bash, Rust | `run_test*.sh`, `capture.sh`, `#[test]` en `bpf.rs` (9) y `main.rs` (2) | n/d | Escenarios de VM y pruebas del demonio (una exige root, `bpf.rs:408-409`) | `Makefile`, `quark_daemon/src` |

### **III.2. Qué se probó y con qué alcance**

Alcance común: **máquina virtual QEMU/KVM, build de pruebas del módulo** (`is_testing_build=1`), juego simulado o RecoilEngine/BAR. Los resultados marcados «documentado» provienen de la documentación de `Dev`; no se reverificaron.

**Tabla III.3. Validación** (fuentes: [[Claims-Ledger]], [[Test-Status]], [[Capture-findings-2026-08-29]], `docs/vm_test_environment.md`)

| Afirmación | Estado | Alcance y resultado | Fuente |
|---|---|---|---|
| El módulo impide la escritura externa por `/proc/<pid>/mem` | SUPPORTED | 10 de 10 repeticiones con `EACCES` en `open()` y valor del juego intacto (100); 2 réplicas independientes; juego simulado | Capturas §2.3; ledger fila 1 |
| Sin defensa el ataque funciona | SUPPORTED | 5 de 5 | Capturas §2.1; fila 2 |
| El bloqueo se debe al módulo y no a Yama | SUPPORTED | Con el módulo descargado, el mismo ataque sobre el mismo PID funciona | Capturas §2.4; fila 3 |
| Funciona sobre un juego real | SUPPORTED | RecoilEngine/BAR en VM: ataque bloqueado, control negativo con `rmmod` exitoso, motor sin daños | `vm_test_environment.md:379-398`; fila 4 |
| *Watchdog* del SDK termina el juego si cae el demonio | DOCUMENTED | Sonda de captura inconclusa | `vm_test_environment.md:400-433`; fila 6 |
| Canal autenticado (ECDSA, hash de `quark_cli`) | DOCUMENTED | Sin reverificar | `vm_test_environment.md:608-695`; fila 7 |
| BPF-LSM bloquea BPF de tracing y protege al demonio | DOCUMENTED | 2026-09-30: 12 programas, 4 mapas, 12 enlaces cargados en kernel 7.0.9; `bpftrace` denegado, `process_vm_readv` → `EPERM`, accesos al demonio denegados; `/proc/<daemon>/{environ,maps}` legibles por root por política del kernel; la verificación de `bpftrace` tras salir el juego fue inconclusa | `vm_test_environment.md:818-841`; fila 8 |
| El build *release* se niega a proteger dentro de una VM | DOCUMENTED | Sin reverificar | `features.md:55-68`; fila 9 |
| Detección por polling en ≤ 50 ms con `kill -9` | DOCUMENTED | Sin captura con marca de tiempo; ya no es modo autónomo | fila 5; [[Test-Status]] Update |

**Procedencia del build de validación.** Las capturas del 2026-08-29 corresponden probablemente al commit `2624ae4` o a un árbol que lo contiene; `environment.txt` no registró `git_commit`, por lo que la correspondencia es UNVERIFIED ([[Test-Status]] Update).

### **III.3. Qué no se midió ni existe**

- **No se midió:** overhead de CPU y RAM (ledger fila 10; requisito del MVP, H5); tasas de detección y falsos positivos (fila 11, meta TDP ≥ 75 %); detección de una DLL o `LD_PRELOAD` inyectada (fila 14; `EXEC_MPROTECT` es solo un indicador); protección real en producción, es decir, el build *release* en hardware físico (fila 15); intentos de evasión; latencia de detección del Modo A; revisión de código probada.
- **No existe en el código:** SDK del lado servidor; prueba cliente↔servidor de punta a punta; política del motor sobre `bpf_lsm_active` (`features.md:252-262`); caso `SIGSTOP` sobre el demonio sin resolver (UNVERIFIED, [[Known-Limitations]] Update).
- **Límites declarados del diseño:** máximo de 16 procesos protegidos (`kernel/quark_kernel.c:47`); `maxactive = 64` con *fail-open* bajo carga sin medir (L510); PID resueltos con `task_tgid_vnr()`, sin soporte entre *namespaces* de PID; `/proc/<pid>/maps` legible por root; BPF-LSM *best-effort* según `lsm=`; mientras hay un proceso protegido fallan `bpftrace` y herramientas con BPF de tracing (`features.md:44-53, 125-130`).
- **Defectos del harness:** `results.csv` malformado y `summary.txt` solo con la condición B; `quark_cli` informa éxito sin confirmación del kernel; objetivo no PIE ([[Test-Status]]; [[Capture-findings-2026-08-29]] §7).

### **III.4. Repositorios y rutas**

**Tabla III.4. Repositorios**

| Repositorio | Ubicación | Estado | Fuente |
|---|---|---|---|
| `Quark-Anticheat` | `https://github.com/stefanomerinoderui/Quark-Anticheat` (remoto `origin`) | Código en rama `Dev`; documentación en `dev/docs`; `main` atrasada | `git remote -v` |
| `RecoilEngine` | Submódulo en `RecoilEngine/`; URL `https://github.com/Billones142/RecoilEngine.git`, rama `quark-anticheat-integration`; commit fijado `29e5b0b44a7604011eca4aaf1281c9c7e86ba5fd` | La integración con el SDK está en esa rama; el submódulo no está inicializado en los worktrees de lectura | `.gitmodules`; `git submodule status` |
| `proton-anticheats` | Repositorio local `uni-dev/proton-anticheats2026-11-13/proton-anticheats` (último commit `cc5078e`, 2026-11-13, según [[Proton-Anticheat-Research]]); URL remota: UNVERIFIED (pendiente de aportar) | La copia local analizada no contiene el directorio `.git`; el commit citado proviene de la nota del vault. Contiene `EAC.md`, `BattlEye.md`, `EAC_BPF_LSM_Service.md`, `Validation_Log.md` y otros | listado del directorio; [[Proton-Anticheat-Research]] |

Rutas del repositorio principal: código en `kernel/`, `quark_daemon/`, `sdk/`, `game_target/`, `cheat/`; documentación técnica en `docs/` de `Dev` (`features.md`, `vm_test_environment.md`, `log_messages.md`, `funcionamiento_codigo.md`, `contexto_proyecto.md`); vault en `docs/obsidian-vault/quark-vault/`; informe en `01-Project/Informe-PIF-Avance.md`; generación del documento en `tooling/build_informe.sh`.

### **III.5. Manual de despliegue y reproducción**

> Procedimiento extraído de `Makefile`, `kernel/Makefile`, `run_test_kernel.sh`, `tooling/keys/generate-testing-key.sh`, `docs/vm_test_environment.md` §15 y `tooling/install.sh` (rama `feature/gameStartProtection`). **No se ejecutó** para redactarlo. Debe ejecutarse **solo en una máquina virtual descartable**: carga un módulo de kernel y requiere privilegios de root.

1. **Entorno.** VM QEMU/KVM con Nobara 43 (kernel 7.0.9, entorno vigente; `vm_test_environment.md:10-12`); CachyOS (kernel 7.3.1; `vm/README.md:5-9`) queda como propuesta a futuro, con *headers* del kernel en ejecución, `gcc`, `clang`, `bpftool`, `cargo`, `openssl` (`libcrypto`), `make`, `sudo`.
2. **BPF-LSM.** Verificar que `cat /sys/kernel/security/lsm` contiene `bpf`; si falta, agregarlo al parámetro `lsm=` y reiniciar (`vm_test_environment.md:769-780`, ejemplo con `grubby`). Sin `bpf`, el demonio funciona solo con el `kretprobe` (`features.md:129-130`).
3. **Código.** Clonar `https://github.com/stefanomerinoderui/Quark-Anticheat` y obtener el commit `35c6031` (rama `Dev`); inicializar el submódulo solo si se prueba RecoilEngine (commit `29e5b0b`).
4. **Clave de pruebas.** `tooling/keys/generate-testing-key.sh` genera el par ECDSA P-256 y regenera `kernel/quark_pubkey.h`; la clave privada queda fuera de git y debe estar en `/opt/quark-anticheat/keys/quark_signing_key.pem` (0600, root) donde corra `quark_cli` (cabecera del script). Que la clave pública versionada coincida con alguna clave privada disponible: UNVERIFIED; la regeneración es el camino seguro.
5. **Compilar.** `make` (demonio, `quark_cli`, juego simulado, atacante; `Makefile` objetivo `all`); `make kernel-testing` (módulo con la omisión de VM; regenera `kernel/quark_cli_hash.h`) o `make kernel` (módulo *release*, se niega a proteger en una VM). `make daemon` genera `vmlinux.h` con `bpftool` desde `/sys/kernel/btf/vmlinux`.
6. **Prueba integrada del Ring 0.** `./run_test_kernel.sh` compila, carga el módulo, inicia el demonio y el juego simulado, ejecuta el atacante y verifica el bloqueo. `./run_test_kernel_release.sh` verifica que el build *release* rechaza proteger en una VM. `./run_test_no_quark.sh` es el control sin defensa (en `feature/gameStartProtection` el juego no arranca sin demonio: ver III.1).
7. **BPF-LSM.** Carga y verificador: `sudo -E cargo test --manifest-path quark_daemon/Cargo.toml -- --ignored` (`vm_test_environment.md:787-794`); comprobaciones de extremo a extremo: tabla de `vm_test_environment.md:796-816`.
8. **Instalación como servicio** (solo en `feature/gameStartProtection`): `sudo tooling/install.sh [--key RUTA]` instala en `/opt/quark-anticheat` y habilita las unidades systemd (cabecera del script).
9. **Motor real.** Compilación del motor y de los plugins de IA, y escenario de escaramuza: `vm_test_environment.md` §2.2-§6.6; compilación cruzada en contenedor Docker con `tooling/recoil-fedora-build/`.
10. **Documento.** `sh tooling/build_informe.sh` (pandoc y tectonic) genera `build/Informe-PIF-AAAA-MM-DD.pdf` y `.tex` a partir de `Informe-PIF-Avance.md`.

**Registro obligatorio al reproducir** ([[Test-Status]]): guardar `git_commit` y `git_branch` en `environment.txt` antes de capturar, para cerrar el riesgo R8.


### **III.6. Registro de los desarrollos posteriores al avance de mayo (2026-11-13)**

Este registro reúne lo ocurrido entre mayo y noviembre de 2026 tal como se relevó el 2026-11-13; su contenido se integró a los Capítulos I a XIII el 2026-11-25 y se conserva aquí como respaldo de las citas del informe.



**Alcance de la evidencia.** Este bloque incorpora al informe lo ocurrido entre mayo y noviembre de 2026. Las afirmaciones sobre el código se apoyan en la rama `origin/Dev` (commit `35c6031`, 2026-11-05) y en su documentación; se **leyeron, no se volvieron a ejecutar** para esta actualización. Cada afirmación indica su alcance (máquina virtual, build de *testing*, juego simulado o motor real) y su fuente, conforme al [[Claims-Ledger]]. Lo no medido se declara como tal.

#### A. Estado del prototipo (reemplaza el estado "a desarrollar" de los Capítulos V y IX)

- **ADDED** — Existe un prototipo funcional compuesto por tres piezas, tal como el informe lo planteó: un módulo de kernel (`kernel/quark_kernel.c`, v0.4.0), un demonio en espacio de usuario (`quark_daemon/`) y un SDK en C (`sdk/`). Respecto de `main`, la rama `Dev` suma 43 archivos y 5.883 líneas nuevas. Fuente: `git diff --stat main...origin/Dev`; [[Features]].
- **ADDED** — **Protección en Ring 0.** Un `kretprobe` sobre `ptrace_may_access` deniega, para un proceso protegido, los intentos de acceso de nivel *attach* de cualquier otro proceso: `ptrace`, lectura y escritura de `/proc/<pid>/mem` y `process_vm_readv/writev`. Las lecturas de solo lectura (por ejemplo `ps` o `htop`) no se bloquean. Fuente: [[Features]] §1.1.
- **ADDED** — **BPF-LSM y telemetría eBPF.** El demonio carga programas eBPF sobre ganchos LSM que (a) impiden a terceros cargar programas BPF de *tracing* mientras haya un proceso protegido, ya que un `kprobe` podría leer la memoria del juego sin pasar por `ptrace_may_access`, y (b) protegen los objetos del propio Quark (mapas, programas, enlaces y el proceso del demonio). Además registra eventos no bloqueantes (`PTRACE_ATTEMPT`, `PROCESS_VM_ACCESS`, `EXEC_MPROTECT`, `TASK_KILL`, `MODULE_LOAD`, `EXEC`). Fuente: [[Features]] §1.5–1.6; commit `e497dbf`.
- **ADDED** — **Canal de control autenticado.** Los comandos de proteger, desproteger y registrar el monitor de confianza viajan por Netlink y se verifican en el kernel con cuatro controles encadenados: uid del emisor verificado por el kernel, hash SHA-256 del ejecutable `quark_cli`, firma ECDSA P-256 sobre `{comando, pid, nonce}` y nonce creciente contra repetición. Esto respondió a dos fallas de escalada local encontradas durante el desarrollo. Fuente: [[Features]] §2; commit `48cc3f6`.
- **ADDED** — **Política de fallo cerrado.** `quark_sdk_init()` devuelve error si el kernel no confirma la protección, y un *watchdog* del SDK termina el juego si el demonio deja de responder. El build de *release* se niega a proteger dentro de una máquina virtual (bit *hypervisor* de CPUID); el build de *testing* lo permite pero se declara a sí mismo como tal (`is_testing_build=1`). Fuente: [[Features]] §1.2, §1.4, §3; commits `2624ae4`, `333bbe2`.
- **ADDED** — **Integración con un juego real.** El SDK se integró en RecoilEngine (motor de *Beyond All Reason*), que impide iniciar una partida protegida si Quark no confirma la protección. Fuente: [[VM-test-environment]] §6.5, §7; PR #1.

#### B. Decisiones técnicas que modifican el informe original

- **REPLACES** — «utiliza Rust como lenguaje principal» (Resumen) y «Codificación en Rust del módulo de kernel» (§5.1) → el módulo de kernel está escrito en **C**; el demonio está en **Rust** y los programas eBPF en C, cargados con `libbpf-rs`. Es la contingencia del riesgo R2 (bindings de Rust for Linux insuficientes), prevista en §5.7 y ejecutada. Fuente: `kernel/quark_kernel.c`; [[Risk-Register]] Update 2026-11-11; [[Claims-Ledger]] fila 12.
- **REPLACES** — «el framework de Linux Security Modules (LSM)» como base del módulo (§1.6, §9) → un LSM clásico no puede registrarse desde un módulo fuera del árbol del kernel, porque `security_add_hooks()` solo existe durante la inicialización y no se exporta. El módulo usa un `kretprobe`, y los ganchos LSM se obtienen a través de **BPF-LSM** desde el demonio. Fuente: [[Features]] §1.5; [[Claims-Ledger]] fila 13.
- **REPLACES** — la verificación en espacio de usuario como defensa autónoma (Modo A) → la verificación periódica de variables del juego (50 ms, con `kill -9`) se conserva, pero ya no es un modo autónomo sino una capa suplementaria: el SDK no arranca sin protección de kernel confirmada. Fuente: [[Test-Status]] Update 2026-11-11.
- **ADDED** — Límites declarados del diseño: una DLL o `LD_PRELOAD` inyectada que escribe sin llamadas al sistema no es observable (`EXEC_MPROTECT` es solo un indicador); `/proc/<pid>/maps` queda legible por root por política del kernel ≥ 6.x, lo que expone el diseño de memoria (ASLR) y no puede anularse desde un módulo; el máximo es de 16 procesos protegidos; y BPF-LSM es *best-effort*: si el usuario arranca sin `bpf` en `lsm=`, queda solo el `kretprobe`. Fuente: [[Features]] §1.1, §1.5; [[Known-Limitations]].

#### C. Validación realizada y alcance de lo medido (Objetivos específicos 4 y 5)

- **ADDED** — Con el módulo cargado, el ataque por `/proc/<pid>/mem` es denegado (`EACCES` en `open()`) en 10 de 10 repeticiones y el valor del juego permanece intacto; sin defensa el mismo ataque funciona en 5 de 5; descargando el módulo, el ataque vuelve a funcionar sobre el mismo PID, lo que atribuye el bloqueo a Quark y no a Yama (control negativo). **Alcance:** máquina virtual, build de *testing*, juego simulado; hay además una validación sobre el motor real. Fuente: [[Capture-findings-2026-08-29]] §2; [[Test-Status]].
- **ADDED** — Según la documentación de `Dev`, `process_vm_*` devuelve `EPERM` y la telemetría registra `PROCESS_VM_ACCESS` y `PTRACE_ATTEMPT`. Estado: DOCUMENTED, sin reverificar. Fuente: [[VM-test-environment]] §15.4.
- **ADDED** — **Pendiente de medición (H5).** No se midió el *overhead* de CPU y RAM (Objetivo 5); no se calcularon tasas de detección ni falsos positivos (Objetivo 4, KPI TDP ≥ 75 %); no se probaron intentos de evasión ni el build de *release* en hardware físico. El informe final no debe afirmar «bajo impacto de rendimiento» hasta contar con la medición. Plan: tres configuraciones (sin Quark, módulo, módulo + BPF-LSM), al menos 10 repeticiones cada una, registrando media, desviación y comando exacto ([[Working-Guidelines]] §3). Fuente: [[Claims-Ledger]] filas 10, 11, 15.

#### D. Relevamiento de mercado ampliado (Capítulo II)

Se realizó una investigación propia sobre cómo funcionan los anticheats comerciales bajo Proton. Está en un repositorio aparte (`proton-anticheats`, último commit `cc5078e`, 2026-11-13); ver [[Proton-Anticheat-Research]]. Hallazgos principales:

- **ADDED** — **Easy Anti-Cheat bajo Proton no contiene lógica anticheat.** El *runtime* de Proton es una capa de traducción entre la DLL de Windows que espera el juego y el cliente nativo de Linux (`easyanticheat_x64.so`), que debe incluir el desarrollador del juego. Por eso su disponibilidad es optativa por título y funciona como biblioteca en espacio de usuario dentro del proceso del juego. Fuente: `EAC.md`, `EAC_bridge_and_quark_takeaways.md` §1 (análisis estático de los binarios).
- **ADDED** — **BattlEye** adopta el diseño opuesto: el *runtime* distribuye el cliente real (`BEClient_x64.so`), pero está empaquetado y virtualizado. Un volcado en la VM dejó legible solo parte del código. Fuente: `BattlEye.md`, `BattlEye_Unpacked.md`.
- **ADDED** — **Easy Anti-Cheat para Linux v2** (anunciado por Epic el 2026-10-14, según fuentes públicas secundarias) reemplaza el camino anterior por un servicio de systemd más programas **BPF-LSM** que restringen el acceso de otros procesos a la memoria del juego, sin módulo de kernel. Es el mismo mecanismo que Quark usa en su capa BPF-LSM, y exige ocho requisitos (BPF-LSM activo, *lockdown* ≥ `integrity`, kexec deshabilitado, Secure Boot, TPM 2.0, IOMMU, kernel y módulos firmados, arranque medido). **Alcance:** información pública y cadenas observadas en un módulo capturado; ningún juego con EAC v2 estaba disponible, por lo que su comportamiento **no fue observado**. Fuente: `EAC_BPF_LSM_Service.md` §0–§3.
- **ADDED** — **Análisis dinámico de EAC (versión anterior).** En Rocket League, el lanzador hace 554 llamadas a `ptrace` en 0,6 s para crear y supervisar el proceso y luego se desacopla; el módulo del juego lee su propia memoria con `process_vm_readv` solo durante el arranque. **Alcance:** un juego, sin juego en línea. Fuente: `EAC_Linux_Module_Behaviour.md` §0.
- **REPLACES** — «Esto evidencia un nicho sin una solución nativa equivalente» (Cap. II) → vigente respecto del nivel de kernel local, pero el relevamiento muestra que la industria se mueve hacia el mismo enfoque (BPF-LSM sin módulo de kernel). El diferencial de Quark pasa de ser «nativo de kernel» a ser **abierto, académico y documentado**, y debe presentarse así en la defensa.
- **UNVERIFIED** — Las 45 afirmaciones inferidas del análisis estático están registradas en `Validation_Log.md`: 6 confirmadas por observación y el resto abiertas o bloqueadas (juego en línea, juego con EAC v2, BattlEye en VM). Hasta cerrarlas, son hipótesis.

#### E. Brechas identificadas frente a la industria (Capítulos IX y XI)

- **ADDED** — Qué incorporar según la comparación, en orden de valor: (1) **atestación verificada por servidor**: hoy `quark_sdk_is_active()` y similares devuelven valores calculados por el cliente, que un tramposo puede falsificar con un `LD_PRELOAD`; la firma debería originarse en el kernel y existe un problema abierto de raíz de confianza (clave por máquina; alternativas: confianza en el primer uso, clave del proveedor, cita TPM 2.0); (2) un canal de mensajes del anticheat a través de la red del propio juego; (3) reporte tipado de violaciones; (4) un gancho `lsm/mmap_file` para mapeos ejecutables de archivos ajenos, que `EXEC_MPROTECT` no cubre. Fuente: `EAC_bridge_and_quark_takeaways.md` §3; `EAC_BPF_LSM_Service.md` §6–7.
- **ADDED** — Ventaja de Quark sobre el cliente Linux de EAC en la comparación: bloqueo local en Ring 0 de `ptrace`, `/proc/<pid>/mem` y `process_vm_*`, bloqueo de BPF de *tracing* y autoprotección del servicio. Es una comparación contra información pública, no contra el comportamiento medido de EAC. Fuente: `EAC_bridge_and_quark_takeaways.md` §4.
- **ADDED** — No implementado hoy: SDK del lado servidor, prueba de punta a punta cliente↔servidor y política del motor sobre `bpf_lsm_active`. Fuente: [[Features]] §5.

#### F. Proceso, riesgos y configuración (Capítulos V y VI)

- **ADDED** — **Desviación metodológica.** El historial de git muestra prototipos sucesivos cada vez más realistas, integrados por *pull request* en `Dev`, en ráfagas de trabajo (junio, fines de agosto, octubre y noviembre) y sin registro contemporáneo de análisis de riesgo por ciclo ni de *sprints*. La propuesta de [[Process-Recommendation]] (estado: **propuesta**, pendiente de aceptación del equipo) es presentar el proceso como «modelo en espiral declarado; ejecución real: prototipado evolutivo guiado por riesgo». Los ciclos C1–C6 de [[Cycle-Log]] son una **reconstrucción desde git**, no un registro de la época. Hay un intervalo sin commits entre 2026-06-26 y 2026-08-27 cuya causa no consta (UNVERIFIED).
- **ADDED** — **Hitos.** H3 (módulo funcional en VM) y H4 (sistema integrado y probado) se cumplen en lo esencial según el historial; H5 (validación, documentación y defensa) sigue abierto. Fuente: [[Roadmap-and-Milestones]] Update 2026-11-11.
- **REPLACES** — «R6 — Limitaciones técnicas del videojuego open source que dificulten la integración» (riesgo vigente) → mitigado: la integración con RecoilEngine/BAR se logró.
- **ADDED** — Riesgos nuevos: R11 (la validación solo puede hacerse con build de *testing* porque el de *release* se niega a proteger en una VM), R12 (documentación que contradice al código), R13 (divergencia de ramas) y R14 (*overhead* sin medir con poco tiempo restante). Fuente: [[Risk-Register]] Update 2026-11-11.
- **ADDED** — **Gestión de la configuración (estado al 2026-11-13).** `main` quedó en el commit del 2026-06-11 más un cambio de `.gitignore`; la integración real ocurre en `Dev`. Las ramas `dev/linter` y `feat/bpf-lsm-telemetry` ya están integradas en `Dev` (PR #3 y #2). Quedan sin integrar dos ramas: `feature/gameStartProtection` (4 commits: instalador `tooling/install.sh` y un juego de prueba que se niega a arrancar sin el demonio ni BPF-LSM, lo que invalida el control negativo «sin Quark» tal como está) y `dev/docs` (2 commits: el vault, el estándar de escritura y el README corregido). Decisión pendiente: integrar ambas en `Dev`, actualizar `main` con una versión congelada y etiquetar un candidato a versión (`rc-1`). Fuente: `git rev-list --count` entre ramas.

#### G. Conclusión parcial

El proyecto demostró que es viable, dentro de una VM y con un build de *testing*, impedir en Linux el acceso externo a la memoria de un proceso mediante un módulo de kernel reforzado con BPF-LSM, y que ese mecanismo se integra en un motor de juego real. Queda por demostrar, antes de la defensa, el costo en rendimiento, la tasa de detección y la tasa de falsos positivos. La investigación sobre Easy Anti-Cheat y BattlEye muestra que la industria converge hacia BPF-LSM, lo que respalda la dirección técnica elegida y desplaza el aporte diferencial hacia la apertura y la documentación.
