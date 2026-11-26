# BORRADOR — Capítulo II y Anexo I (para integrar en `Informe-PIF-Avance.md` o `Informe-PIF-v2`)

> Estado: borrador del 2026-11-25. Rige el Art. 24.3 (fuentes, instrumentos, datos, gráficos, análisis, conclusiones) y el Art. 21 (impersonal, presente afirmativo). Marcas: **UNVERIFIED** = inferido o no contrastado; **pendiente de aportar** = depende de una persona del equipo. No contiene resultados de encuesta porque la encuesta no se publicó.

---

# CAPÍTULO II — RELEVAMIENTO E INVESTIGACIÓN DE MERCADO

## 2.1. Objetivo y alcance del relevamiento

El relevamiento responde dos preguntas del proyecto: (a) cuál es el tamaño y la evolución del público potencial de un anticheat nativo para GNU/Linux y (b) cuál es el estado de la oferta existente. El alcance es la investigación documental de fuentes públicas (2.2) y el diseño de una encuesta anónima a *stakeholders* (2.3). La encuesta se diseña y no se publica; el capítulo no presenta resultados de ella.

## 2.2. Fuentes de datos

| Fuente | Tipo | Dato que aporta | Fecha de consulta |
|---|---|---|---|
| Steam Hardware & Software Survey (Valve) | Secundaria, estadística pública | Participación de sistemas operativos entre usuarios de Steam | 2026-11-25 |
| AreWeAntiCheatYet | Secundaria, base colaborativa | Estado de compatibilidad de juegos con anticheat en Linux | 2026-11-25 |
| Phoronix; GamingOnLinux; It's FOSS (prensa especializada) | Secundaria | Anuncio de Easy Anti-Cheat (EAC) para Linux v2 | 2026-11-25 |
| Repositorio propio `proton-anticheats` y nota `Proton-Anticheat-Research` | Primaria, análisis técnico propio | Funcionamiento de EAC y BattlEye bajo Proton | Commit `cc5078e`, 2026-11-13 |
| Encuesta a *stakeholders* (Reddit) | Primaria, instrumento diseñado | Interés, adopción y objeciones | No aplicada |

Limitaciones de las fuentes secundarias: la Steam Hardware Survey mide usuarios de Steam que aceptan participar y no a todos los jugadores de PC (alcance: usuarios de Steam; el sesgo de muestra no se cuantifica aquí, UNVERIFIED). AreWeAntiCheatYet es colaborativa y la fecha de actualización varía por fila; las filas consultadas muestran actualizaciones entre 2022 y 2024. Las notas de prensa sobre EAC v2 reproducen un anuncio de Epic Games; el comportamiento real de EAC v2 no se observó (ver Cap. II del Update 2026-11-13, sección D).

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

## 2.4. Presentación de datos: investigación documental de mercado

### 2.4.1. Participación de Linux entre usuarios de Steam

La Steam Hardware & Software Survey de octubre de 2026 informa los siguientes valores de sistema operativo (Valve, 2026):

| Sistema operativo | Participación | Variación mensual |
|---|---|---|
| Windows | 93,70 % | −1,33 pp |
| Linux | 3,95 % | +0,90 pp |
| macOS | 2,35 % | +0,43 pp |

Lectura: Linux supera el 3,9 % de los usuarios de Steam en ese mes y es el sistema con mayor aumento absoluto (+0,90 pp). Se trata de una sola observación mensual; la serie histórica y la tendencia no se relevaron aquí (pendiente de aportar: serie de los últimos meses desde la misma fuente, para graficar). El volumen absoluto de usuarios no se calcula porque la fuente consultada no se acompañó de un total verificable (UNVERIFIED). Los valores se extrajeron de la página con una herramienta automática de lectura; se recomienda contrastarlos visualmente con la fuente antes de la entrega.

**Gráfico previsto (Figura 2.1):** barras horizontales de los tres valores anteriores, fuente Valve (2026). Pendiente de aportar la versión gráfica.

### 2.4.2. Estado de compatibilidad de anticheats en Linux

AreWeAntiCheatYet lista 1.167 juegos, con la siguiente clasificación (AreWeAntiCheatYet, 2026):

| Estado | Juegos | Participación |
|---|---|---|
| Supported | 196 | 17 % |
| Running | 280 | 24 % |
| Planned | 2 | 0 % |
| Broken | 636 | 54 % |
| Denied | 53 | 5 % |

Lectura: el 54 % de los títulos listados figura como *Broken* y el 5 % como *Denied*; entre los títulos *Denied* se cuentan Fortnite, Apex Legends y Valorant. El 41 % figura como *Supported* o *Running*. La definición de cada estado según el mismo sitio es """
- Supported: Games that run on Linux due to the developers going out of their way to enable the anti-cheat to run on Linux or games that have anti-cheat which works perfectly fine out of the box under Wine/Proton (e.g. Overwatch, Battlefield 4)
- Running: Games that will run on Linux without impact on online gameplay but may require you to perform certain tinkering steps (This does not include any means of explicitly bypassing the anti-cheat)
- Planned: Games where the developers have explicitly stated that they plan to enable their anti-cheat to work on Linux or that they plan to support the game natively
- Broken: Games that will not run online due to the deployed anti-cheat solution
- Denied: Games where the developers have explicitly stated that they will not enable the anti-cheat solution to work on Linux or have denied the possibility of Linux support
"""; la lista incluye juegos sin anticheat activo o con filas sin actualizar (las filas observadas se actualizaron entre 2022 y 2024), por lo que las proporciones indican el orden de magnitud y no un estado vigente. Los conteos provienen de la cabecera de la página, leída con una herramienta automática y verificadas manualmente.

### 2.4.3. Oferta existente: EAC y BattlEye bajo Proton

Los hallazgos de la investigación propia se resumen en la sección D del Update 2026-11-13 y en `Proton-Anticheat-Research`: EAC bajo Proton es un cliente nativo (`easyanticheat_x64.so`) que incluye el desarrollador del juego y funciona en espacio de usuario; BattlEye distribuye un cliente empaquetado y virtualizado. Ambos dependen de la decisión de cada desarrollador y ninguno actúa como anticheat de kernel en Linux.

### 2.4.4. Movimiento de la industria: EAC para Linux v2

Epic Games anunció el 2026-10-14 la reconstrucción de EAC para Linux («EAC Linux v2»). Según la prensa especializada, no instala ni carga un módulo de kernel; usa un servicio de systemd que se ejecuta mientras corre un juego protegido y programas eBPF sobre BPF-LSM que restringen el acceso de otros procesos a la memoria del juego. Los requisitos informados incluyen kernel y módulos firmados, atestación de Secure Boot, arranque medido, IOMMU, *lockdown* en modo *integrity*, kexec deshabilitado y BPF-LSM activo. Fortnite es el piloto previsto, y luego se ofrecería a otros desarrolladores; no se informó fecha de lanzamiento (Phoronix, s. f.; It's FOSS, 2026). Alcance: información de prensa sobre un anuncio; el comportamiento real de EAC v2 no fue observado por el equipo porque aún no es accesible públicamente.

## 2.5. Análisis

1. **Demanda potencial.** Un 3,95 % de los usuarios de Steam usa Linux en octubre de 2026, con crecimiento mensual positivo (+0,90 pp). Es un segmento minoritario en términos relativos y creciente en la única observación disponible; no se afirma una tendencia sostenida sin serie histórica.
2. **Brecha de oferta.** La mayoría de los títulos con anticheat listados en AreWeAntiCheatYet no funciona en Linux (*Broken* 54 %, *Denied* 5 %). Esto indica que la disponibilidad de anticheat es una barrera de acceso, con la reserva sobre la vigencia de las filas (2.4.2).
3. **Dirección de la industria.** El anuncio de EAC v2 va hacia BPF-LSM sin módulo de kernel, el mismo mecanismo que la capa BPF-LSM de Quark. La línea técnica del proyecto se alinea con la industria; el diferencial pasa a ser la apertura del código y la documentación académica (ver Cap. II, Update 2026-11-13, D).
4. **Oportunidad.** La combinación de un segmento creciente, una oferta que depende de cada desarrollador y una solución de referencia (EAC v2) aún sin lanzamiento constituye una oportunidad para una alternativa abierta. Esta lectura es una inferencia del equipo y se contrasta con la encuesta una vez aplicada.
5. **Lo que el relevamiento no permite concluir:** tamaño de mercado en unidades o dinero, disposición a adoptar Quark, y confianza en el código abierto, que dependen de la encuesta (no aplicada).

## 2.6. Conclusiones del capítulo

- Linux alcanza el 3,95 % de los usuarios de Steam en octubre de 2026 (Valve, 2026).
- La compatibilidad de anticheats en Linux es parcial: 17 % *Supported* y 24 % *Running* sobre 1.167 juegos listados (AreWeAntiCheatYet, 2026), con filas de antigüedad variable.
- La industria incorpora BPF-LSM en EAC v2, lo que respalda la dirección técnica de Quark.
- La validación con usuarios reales (interés, diferencial de código abierto, adopción) permanece pendiente: la encuesta está diseñada y no publicada. Hasta su aplicación, las hipótesis de demanda son UNVERIFIED.

---

# ANEXO I — DATOS RELEVADOS

*Numeración propia: «página X de Y» (a completar al maquetar).*

## I.1. Cuestionario (versión de diseño)

Estructura de bloques y preguntas clave: ver 2.3. El texto completo de los ~25 ítems recortados es **pendiente de aportar**. Material de origen: `docs/Quark_Encuesta_Diapositivas.txt` (presentación de diseño; no es el cuestionario final).

## I.2. Datos de fuentes secundarias

| Dato | Valor | Fuente | Consulta |
|---|---|---|---|
| Linux, Steam Survey, oct. 2026 | 3,95 % (+0,90 pp) | Valve (2026) | 2026-11-25 |
| Windows, ídem | 93,70 % (−1,33 pp) | Valve (2026) | 2026-11-25 |
| macOS, ídem | 2,35 % (+0,43 pp) | Valve (2026) | 2026-11-25 |
| Juegos listados | 1.167 | AreWeAntiCheatYet (2026) | 2026-11-25 |
| Supported / Running / Planned / Broken / Denied | 196 / 280 / 2 / 636 / 53 | AreWeAntiCheatYet (2026) | 2026-11-25 |

## I.3. Respuestas de la encuesta

Sin datos. La encuesta no se publicó. Se completan aquí, sin editar los datos crudos, las respuestas exportadas, el tamaño de muestra, la tasa de finalización y el tiempo medio (pendiente de aportar).

## I.4. Registro de método

Los valores de Valve y AreWeAntiCheatYet se obtuvieron el 2026-11-25 mediante lectura automática de las páginas; no hay captura de pantalla archivada (pendiente de aportar: capturas con fecha, para la zona de evidencia).

---

## Referencias APA nuevas

AreWeAntiCheatYet. (2026). *Are We Anti-Cheat Yet?* Recuperado el 25 de noviembre de 2026, de https://areweanticheatyet.com/

It's FOSS. (2026). *Epic Games wants Linux gamers. It's rebuilding EAC for Fortnite.* Recuperado el 25 de noviembre de 2026, de https://itsfoss.com/news/epic-games-linux-anti-cheat-fortnite/

Phoronix. (s. f.). *Epic Games to improve Easy Anti-Cheat on Linux with anti-cheat systemd service & eBPF.* Recuperado el 25 de noviembre de 2026, de https://phoronix.com/news/Easy-Anti-Cheat-Better-Linux

Valve Corporation. (2026). *Steam Hardware & Software Survey: October 2026.* Recuperado el 25 de noviembre de 2026, de https://store.steampowered.com/hwsurvey/

Nota: los autores y fechas de las dos notas de prensa ya se verificaron.

— agent:claude-sonnet-5-5 (2026-11-25)
