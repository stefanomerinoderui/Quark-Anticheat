---
title: "Borrador Cap. IV y Cap. XI"
tags: [proyecto, informe, borrador]
status: draft
---

# Borrador Cap. IV y Cap. XI — agent:claude-sonnet-5-5 — 2026-11-25

Convenciones: lo no medido ni citado se marca **UNVERIFIED**; lo que debe aportar una persona se marca **pendiente de aportar**. Fecha de consulta de todas las URL web: 2026-11-25. Fuentes internas: `Informe-PIF-Avance.md` (Update 2026-11-13, §D y §E), `Proton-Anticheat-Research.md`, `Features.md`.

---

# **CAPÍTULO IV — MODELO DE NEGOCIOS DEL PROYECTO**

## 4.1. Definición de negocios

**Actividades.** El proyecto diseña, desarrolla y documenta un sistema anticheat para GNU/Linux compuesto por un módulo de kernel (C, `kernel/quark_kernel.c`), un demonio en espacio de usuario (Rust, `quark_daemon/`) con programas eBPF, y un SDK en C (`sdk/`) que un juego integra para exigir la protección (Informe, Update 2026-11-13, §A). Las actividades de valor son: (a) el desarrollo y mantenimiento del código abierto; (b) la documentación técnica y de las decisiones de diseño; (c) la investigación comparada de los anticheats comerciales bajo Proton (Informe, Update 2026-11-13, §D); (d) la integración con motores de juego de código abierto (RecoilEngine, motor de *Beyond All Reason*).

**Mercado general.** El mercado es el de los videojuegos multijugador en línea que exigen un anticheat de nivel de kernel como condición de ejecución, y dentro de él el segmento de jugadores que usan GNU/Linux. Los anticheats comerciales se desarrollan principalmente para Windows (Wikipedia, 2026a), y en Linux su disponibilidad es optativa por título (ver 4.4), aparte de que la oferta actual es exclusivamente para anticheats en espacio de usuario. El tamaño del segmento Linux y su participación en cada título no se midieron en este proyecto: **UNVERIFIED** (la encuesta del Cap. II está **pendiente de aportar**).

**Tecnología.** Protección en Ring 0 mediante un `kretprobe` sobre `ptrace_may_access`, BPF-LSM y telemetría eBPF cargados desde el demonio, canal Netlink autenticado (uid, SHA-256 del ejecutable, firma ECDSA P-256 y nonce) y política de fallo cerrado en el SDK (Features §1–§3). El alcance validado es una máquina virtual con build de *testing* y un juego simulado, más una validación sobre el motor real (Informe, Update 2026-11-13, §C).

**Modelo de negocio en clave de adopción.** El proyecto no se comercializa (Cap. III, 3.3). No hay ingresos, precios ni clientes pagantes, y no se plantean. El "negocio" se define como la generación y sostenimiento de valor público: un componente abierto, auditable y reutilizable. El modelo se expresa en el CANVAS del Cap. XI.

## 4.2. Definiciones estratégicas

**Misión y visión.** Se adoptan las del Cap. I, 1.2.

**Propuesta de valor estratégica.** A partir del relevamiento de mercado, el diferencial pasa de "nativo a nivel de kernel" a **abierto, académico y documentado** (Informe, Update 2026-11-13, §D): la industria converge hacia BPF-LSM sin módulo de kernel, de modo que la ventaja sostenible reside en la apertura del código, la trazabilidad de las afirmaciones (Claims-Ledger) y la documentación del diseño, no en un mecanismo exclusivo.

**Objetivos estratégicos de adopción** (derivados de los objetivos del Cap. I; ninguna meta numérica de adopción se fija, **pendiente de definir por el equipo**):
1. Publicar el repositorio con licencia de software libre compatible con el kernel (Cap. VIII, pendiente).
2. Mantener la integración con al menos un motor de juego de código abierto (hoy: RecoilEngine, PR #1).
3. Completar la medición pendiente (overhead, detección, falsos positivos) antes de cualquier afirmación de rendimiento (Informe, Update 2026-11-13, §C).

## 4.3. Análisis de rivalidad amplificada

Se aplica el esquema de cinco fuerzas ampliado (competidores actuales, entrantes potenciales, sustitutos, proveedores, clientes) adaptado a un proyecto no comercial. Las valoraciones son cualitativas y se apoyan en las fuentes citadas; no se midió cuota de mercado alguna (**UNVERIFIED**).

| Fuerza | Análisis | Fuente |
|---|---|---|
| Competencia actual | Easy Anti-Cheat (Epic), BattlEye, VAC (Valve) y Vanguard (Riot) dominan el segmento. En Linux, EAC y BattlEye funcionan bajo Proton solo si el desarrollador los habilita; VAC corre igual en Linux; Vanguard no se ofrece en Linux. | 4.4 |
| Competidores potenciales | Epic anunció (2026-10-14, según fuentes públicas secundarias) Easy Anti-Cheat para Linux v2 con servicio systemd y programas BPF-LSM, sin módulo de kernel. Es el mismo mecanismo que usa la capa BPF-LSM de Quark. Su comportamiento no fue observado porUe no se publicó aún. | Informe, Update 2026-11-13, §D; `EAC_BPF_LSM_Service.md` |
| Sustitutos | (a) Detección del lado del servidor, que no depende del cliente; (b) no ofrecer el título en Linux; (c) juegos sin anticheat de kernel (ej. VAC en espacio de usuario). | Informe, Cap. XI previsto; GamingOnLinux (2026) |
| Proveedores | Kernel de Linux (interfaces LSM, eBPF, Netlink, kprobes), toolchain Rust/libbpf, distribuciones. Dependencia alta de la estabilidad de interfaces internas del kernel (riesgo R7) y de la configuración del usuario (BPF-LSM requiere `bpf` en `lsm=`; Features §1.5). | Informe, Cap. V 5.7; Known-Limitations |
| Clientes / adoptantes | Desarrolladores de juegos (integran el SDK; hoy un motor de código abierto) y jugadores Linux (instalan módulo y demonio). Los estudios comerciales dependen de proveedores con servicio, soporte y respaldo de servidor, que Quark no ofrece. | Informe, Update 2026-11-13, §A, §E |
| Barreras de entrada | Altas en lo técnico (kernel, detección, atestación) y para obtener confianza (ver Riot: Linux no permite atestar el estado de arranque ni los módulos de kernel). | GamingOnLinux (2024) |

**Lectura de rivalidad.** Quark no compite hoy por clientes comerciales: carece de SDK del lado servidor, de prueba de punta a punta cliente-servidor y de atestación verificada por servidor (Features §5; Informe, Update 2026-11-13, §E). Su espacio es el de la alternativa abierta, estudiable y reproducible.

## 4.4. Mapeo de competencia

**Tabla IV-1. Mapeo de competencia (información pública, consultada el 2026-11-25).** La columna "Linux" describe el soporte según las fuentes citadas; no se midió el comportamiento de estos productos salvo donde se indica.

| Solución (proveedor) | Naturaleza técnica según fuentes | Soporte en Linux | Modelo de licenciamiento / distribución | Fuente |
|---|---|---|---|---|
| Easy Anti-Cheat (Epic Games) | Anticheat comercial, disponible gratis a través de Epic Online Services en todas las plataformas de PC (según Epic). Bajo Proton el *runtime* es un puente y el cliente nativo (`easyanticheat_x64.so`) lo aporta el juego (análisis estático propio). | Funciona vía Wine/Proton si el desarrollador lo activa en el portal de Epic (Epic, 2021). Análisis dinámico propio: un juego, sin partida en línea. | Propietario, cerrado | Epic Online Services (2021); GamingOnLinux (2021a); `EAC.md` |
| BattlEye (BattlEye Innovations) | Anticheat comercial. El *runtime* de Proton distribuye el cliente real (`BEClient_x64.so`), empaquetado y virtualizado; solo legible en parte en el volcado propio. | Opt-in: el desarrollador debe solicitarlo a BattlEye (GamingOnLinux, 2021a, 2021b). Un juego puede incluir BattlEye sin habilitar Proton (GamingOnLinux, 2024b). | Propietario, cerrado | GamingOnLinux (2021a, 2021b, 2024b); `BattlEye.md` |
| VAC (Valve) | Sistema de Valve que detecta cheats en la PC del usuario con una base de cheats conocidos, similar a un antivirus; reportado como de espacio de usuario, no de kernel (descripción de terceros; Valve no publica el detalle interno). Los bans se aplican vía API de Steamworks. | La versión de Linux es idéntica a la de Windows (Valve Developer Community, s. f.). | Propietario, ligado a Steam/Steamworks | Valve (s. f.-a, s. f.-b) |
| Vanguard (Riot Games) | Anticheat con driver; Riot afirma que necesita verificar el entorno y atestar estado de arranque y módulos de kernel. | No soportado; Riot declara que Linux no permite atestar el estado de arranque ni los módulos de kernel, y que rechaza emulación y VM. | Propietario, cerrado, ligado a títulos de Riot | GamingOnLinux (2024a) |
| Easy Anti-Cheat para Linux v2 (Epic) | Servicio systemd + programas BPF-LSM, sin módulo de kernel; ocho requisitos de plataforma (BPF-LSM, *lockdown*, Secure Boot, TPM 2.0, IOMMU, entre otros). **UNVERIFIED**: información pública secundaria y cadenas observadas en un módulo capturado; ningún juego con EAC v2 estuvo disponible. | Nativo Linux con requisitos estrictos | Propietario | `EAC_BPF_LSM_Service.md` §0–§3 |
| **Quark Anticheat** | Módulo de kernel (C) + BPF-LSM/eBPF + demonio (Rust) + SDK (C). Bloquea localmente `ptrace`, `/proc/<pid>/mem` y `process_vm_*` en Ring 0; bloquea BPF de *tracing*; autoprotege al demonio (Features §1). | Nativo Linux. Validado en VM, build de *testing*, juego simulado y motor real. | **Abierto**, académico, documentado (licencia: Cap. VIII, pendiente) | Features; Informe, Update 2026-11-13, §A, §C |

**Tabla IV-2. Comparación cualitativa de capacidades.** "Sí/No/UNVERIFIED" según información pública; la comparación con EAC es contra información pública, no contra su comportamiento medido (Informe, Update 2026-11-13, §E).

| Capacidad | EAC (Proton) | BattlEye (Proton) | VAC | Vanguard | Quark |
|---|---|---|---|---|---|
| Código auditable por terceros | No | No | No | No | Sí (repositorio; licencia pendiente) |
| Funciona en Linux | Si el juego lo activa | Si el juego lo activa | Sí | No | Sí (prototipo) |
| Bloqueo local de acceso a memoria en Ring 0 en Linux | UNVERIFIED (EAC v2 usa BPF-LSM) | UNVERIFIED | No (reportado espacio de usuario) | No aplica | Sí, validado solo en VM/testing |
| Atestación verificada por servidor | UNVERIFIED | UNVERIFIED | UNVERIFIED | Sí declarado necesario (Riot) | No (brecha identificada) |
| Servicio y soporte comercial | Sí | Sí | Sí | Sí | No |
| Overhead medido | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | No medido (pendiente, H5) |

**Otros competidores.** Otros productos (por ejemplo FACEIT Anti-Cheat, Ricochet, XIGNCODE) no se relevaron por falta de fuente consultada: **UNVERIFIED / pendiente de relevar** si el equipo los considera necesarios. No se identificó, en este relevamiento, un anticheat de nivel de kernel abierto para Linux equivalente; la búsqueda no fue exhaustiva (**UNVERIFIED**).

**Conclusión del mapeo.** Los competidores existentes son cerrados y, salvo VAC, requieren el consentimiento del estudio para operar en Linux; la industria avanza hacia BPF-LSM. Quark ocupa el nicho de alternativa abierta y documentada, con brechas explícitas frente a la industria (atestación por servidor, SDK de servidor, canal de mensajes, reporte tipado).

---

# **CAPÍTULO XI — OPORTUNIDADES DEL PROYECTO**

## 11.1. CANVAS del proyecto

Se adapta el Business Model Canvas (Osterwalder & Pigneur, 2010) a un proyecto de código abierto sin comercialización: la columna de ingresos se reemplaza por sostenibilidad y no se declara ninguna cifra.

**Tabla XI-1. CANVAS de Quark Anticheat**

| Bloque | Contenido |
|---|---|
| **Segmentos de clientes / usuarios** | Desarrolladores de juegos de código abierto o independientes que quieran integrar un anticheat en Linux; jugadores de GNU/Linux; comunidad de seguridad e investigadores; cátedra y estudiantes (uso académico). Tamaño de cada segmento: UNVERIFIED (encuesta pendiente de aportar). |
| **Propuesta de valor** | Anticheat abierto, auditable y documentado para Linux; protección local en Ring 0 (bloqueo de `ptrace`, `/proc/<pid>/mem`, `process_vm_*`) reforzada con BPF-LSM; SDK con política de fallo cerrado; trazabilidad de cada afirmación (Claims-Ledger). |
| **Canales** | Repositorio público y documentación; divulgación en comunidades de gaming en Linux (Cap. VII); integración vía pull request en motores de código abierto (PR #1 en RecoilEngine); defensa y bibliografía académica. |
| **Relación con clientes** | Soporte comunitario por issues y pull requests; documentación técnica; ayuda de integración a proyectos adoptantes (alcance pendiente de definir por el equipo). |
| **Fuentes de ingresos / sostenibilidad** | No hay ingresos ni comercialización (Cap. III). Sostenibilidad: tiempo voluntario de los autores, contribuciones de la comunidad, uso académico. Financiamiento externo (becas, fondos para software libre): pendiente de explorar, sin datos. |
| **Recursos clave** | Equipo de dos integrantes (~696 h por integrante estimadas, Cap. V 5.6); código (kernel, demonio, SDK); vault de documentación; equipos personales y VM QEMU/KVM; investigación `proton-anticheats`. |
| **Actividades clave** | Desarrollo y pruebas del módulo, demonio y SDK; medición de overhead y tasas de detección (pendiente); investigación comparada; documentación; integración con motores. |
| **Socios clave** | Proyectos de juegos de código abierto (Beyond All Reason / RecoilEngine); comunidad del kernel de Linux (interfaces LSM, eBPF, Rust for Linux); la universidad (cátedra). Compromisos formales de socios: pendiente de aportar. |
| **Estructura de costos** | Sin financiamiento externo (Cap. III, 3.4); costo principal: horas de trabajo de los integrantes; infraestructura sin costo (software libre, equipos personales). Cualquier costo monetario: no registrado. |

## 11.2. Oportunidades de escalabilidad e innovación

Cada oportunidad indica su fuente y su estado. Ninguna está implementada hoy salvo indicación contraria (Features §5).

1. **Atestación verificada por servidor.** Hoy `quark_sdk_is_active()` y similares devuelven valores calculados por el cliente, falsificables con `LD_PRELOAD`. La firma debería originarse en el kernel. Queda abierto el problema de la raíz de confianza (clave por máquina, confianza en el primer uso, clave del proveedor o cita TPM 2.0). Es la brecha de mayor valor y la que Riot menciona como motivo de su negativa (GamingOnLinux, 2024a). Fuente: `EAC_bridge_and_quark_takeaways.md` §3.
2. **SDK del lado servidor y prueba cliente-servidor de punta a punta.** No implementados (Features §5). Habilitan que un estudio decida con base en la atestación.
3. **Canal de mensajes del anticheat por la red del propio juego** y **reporte tipado de violaciones.** Fuente: `EAC_bridge_and_quark_takeaways.md` §3.
4. **Gancho `lsm/mmap_file`** para mapeos ejecutables de archivos ajenos, que `EXEC_MPROTECT` no cubre. Fuente: `EAC_BPF_LSM_Service.md` §7.
5. **Ampliación de la cobertura de detección** a nuevos vectores (Cap. I, objetivo 2) y límites hoy declarados: DLL o `LD_PRELOAD` que escribe sin llamadas al sistema no es observable; `/proc/<pid>/maps` legible por root (Informe, Update 2026-11-13, §B).
6. **Soporte multi-distribución y de versiones de kernel** más allá de la distribución de referencia (Nobara) y del entorno de VM; hoy solo hay validación en VM y el build de *release* no se probó en hardware físico (Informe, Update 2026-11-13, §C).
7. **Migración progresiva de C a Rust** a medida que maduran los bindings del kernel; el soporte de Rust dejó de considerarse experimental en 2025 (Ojeda, 2025). El módulo actual está escrito en C por la contingencia del riesgo R2.
8. **Detección basada en comportamiento del lado del servidor** como complemento de la observación a nivel de kernel (Cap. XI previsto en el avance de mayo).
9. **Integración con más motores de código abierto** y distribución como paquete de distribución (instalador `tooling/install.sh`, rama `feature/gameStartProtection` sin integrar al 2026-11-13).
10. **Alineación con la tendencia de la industria.** EAC v2 adopta BPF-LSM (información pública secundaria); la convergencia valida la dirección técnica y abre la posibilidad de contraste reproducible cuando exista un juego con EAC v2 disponible (captura bloqueada hoy).
11. **Línea académica.** El material (vault, Claims-Ledger, investigación de anticheats bajo Proton) es reutilizable como caso de estudio de seguridad en Linux. Publicación académica o uso en cátedra: no acordado, pendiente de aportar.

**Riesgos de las oportunidades.** La dependencia de interfaces internas del kernel (R7), la ausencia de medición de rendimiento (R14) y la configuración exigida al usuario (BPF-LSM, Secure Boot, TPM) limitan la escalabilidad real. Ninguna oportunidad se presenta como viable sin validación propia.

---

Firmado: agent:claude-sonnet-5-5 — 2026-11-25

## Referencias APA nuevas (consulta: 2026-11-25)

Epic Online Services. (2021, septiembre). *Epic Online Services launches anti-cheat support for Linux, Mac and Steam Deck*. https://onlineservices.epicgames.com/en-US/news/epic-online-services-launches-anti-cheat-support-for-linux-mac-and-steam-deck *(Contenido tomado de resúmenes de búsqueda; la página exigió autenticación al intentar leerla. Fecha exacta de publicación: September 23, 2021, revisado en 2026-11-25)*

GamingOnLinux. (2021a, septiembre). *BattlEye confirms Linux support for Steam Deck will be opt-in like Easy Anti-Cheat*. https://www.gamingonlinux.com/2021/09/battleye-confirms-linux-support-for-steam-deck-will-be-opt-in-like-easy-anti-cheat *(Fecha exacta del día: 24 Sep 2021, verificado en 2026-11-25.)*

GamingOnLinux. (2021b, noviembre). *Supporting Linux, Proton and the Steam Deck with BattlEye is just an email away*. https://gamingonlinux.com/2021/11/supporting-linux-proton-and-the-steam-deck-with-battleye-is-just-an-email-away/ *(Fecha exacta del día: 6 Nov 2021, verificada en 2026-11-25.)*

GamingOnLinux. (2024a, 11 de abril). *Riot Games talk Vanguard anti-cheat for League of Legends and why it's a no for Linux*. https://www.gamingonlinux.com/2024/04/riot-games-talk-vanguard-anti-cheat-for-league-of-legends-and-why-its-a-no-for-linux

GamingOnLinux. (2024b, septiembre). *Grand Theft Auto V gets BattlEye anti-cheat, breaks online play on Steam Deck / Linux*. https://www.gamingonlinux.com/2024/09/grand-theft-auto-v-gets-battleye-anti-cheat-breaks-online-play-on-steam-deck-linux/ *(Solo se vio el título y la URL en la búsqueda; la descripción del artículo proviene del resumen de búsqueda. Verificar.)*

Osterwalder, A., & Pigneur, Y. (2010). *Business model generation*. Wiley. *(Obra de referencia general del Business Model Canvas; no consultada en esta sesión, verificar edición y páginas.)*

Valve Corporation. (s. f.-a). *Anti-cheat and game bans*. Steamworks Documentation. https://partner.steamgames.com/doc/features/anticheat/vac_integration *(La página describe bans por API y servidores; no define VAC. La descripción "similar a un antivirus" se toma de Valve (s. f.-b).)*

Valve Developer Community. (s. f.-b). *Valve Anti-Cheat*. https://developer.valvesoftware.com/wiki/Valve_Anti-Cheat *(Contenido tomado de resumen de búsqueda; no leído completo. Verificar antes de citar.)*

Nota: Valve (s. f.-a) y (s. f.-b) se distinguen en el texto de la Tabla IV-1; en la columna "Soporte en Linux" se citó "Valve Developer Community (s. f.)", que corresponde a (s. f.-b). Reutilizadas del informe: GamingOnLinux (2026), Ojeda (2025), Wikipedia (2026a).
