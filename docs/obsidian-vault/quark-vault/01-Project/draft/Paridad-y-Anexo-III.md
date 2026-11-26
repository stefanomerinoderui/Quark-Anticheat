---
title: "Borrador — Auditoría de paridad informe↔Dev y Anexo III"
tags: [borrador, informe, paridad, anexo]
status: draft
---

# Borrador: paridad informe↔Dev y Anexo III

agent:claude-sonnet-5-5 · 2026-11-25 · borrador; **no** modifica `Informe-PIF-Avance.md`.

**Base de comparación.** `origin/Dev@35c6031` (2026-11-05 19:33 -03:00), leído en `../quark-wt/Dev`; `feature/gameStartProtection@2b088ab` (2026-11-06) como trabajo sin integrar. Se **leyó**; no se ejecutó nada (ni `make`, ni scripts, ni pruebas). Los conteos de líneas son `wc -l` (líneas físicas, no SLOC).

**Convenciones.** «L123» = línea de `Informe-PIF-Avance.md` (estado al 2026-11-25). Rutas de código = relativas a la raíz de `Dev@35c6031`. `[[Nota]]` = nota del vault. UNVERIFIED = inferido o sin evidencia hallada. Las propuestas de redacción están en impersonal y presente afirmativo (Art. 21); las que dependen de una decisión del equipo lo indican.

**Nota previa.** El Update 2026-11-13 (L611-664) ya corrige varios de estos puntos, pero **al final** del documento; el cuerpo (Resumen, Cap. I-XIII) sigue diciendo lo contrario. La fusión consiste en reescribir el cuerpo y dejar el Update como historial.

---

## Parte 1 — Auditoría de paridad

### 1.1 Portada y Resumen

**P01 · L30 · «Mayo de 2026»**
- Hecho: el contenido incorpora hechos hasta 2026-11-25 (último commit de Dev 2026-11-05; Update L611).
- Propuesta: fecha de edición «Noviembre de 2026» (decisión humana: puede conservarse «avance de mayo» como subtítulo del snapshot original).

**P02 · L38 · «utiliza Rust como lenguaje principal, dado que ofrece garantías de seguridad de memoria que reducen el riesgo de errores críticos en el contexto de módulos de kernel»**
- Hecho: el módulo de kernel es C (`kernel/quark_kernel.c`, `MODULE_VERSION("0.4.0")` en L42; 648 líneas). Rust solo en el demonio (`quark_daemon/src/main.rs`, `bpf.rs`; `Cargo.toml` edition 2024, `libbpf-rs 0.27`). Los programas eBPF están en C (`quark_daemon/src/bpf/quark.bpf.c`). Es la contingencia de R2 ejecutada ([[Risk-Register]] Update 2026-11-11; [[Claims-Ledger]] fila 12 = CONTRADICTED).
- Propuesta: «El desarrollo utiliza C para el módulo de kernel, el SDK y los programas eBPF, y Rust para el servicio en espacio de usuario. La decisión responde a la madurez insuficiente de los bindings de Rust for Linux para las interfaces requeridas, riesgo previsto y mitigado en el plan del proyecto.»

**P03 · L38 · «un módulo de kernel encargado de la supervisión de procesos, el acceso a memoria y la detección de patrones asociados a trampas»**
- Hecho: el módulo **previene** (no detecta patrones): un `kretprobe` sobre `ptrace_may_access` deniega a otros procesos el acceso de nivel *attach* (ptrace, `/proc/<pid>/mem`, `process_vm_readv/writev`) a un PID protegido (`docs/features.md:11-34`). La detección por comparación de variables es del demonio (`features.md:70-83`) y la telemetría, de eBPF (`features.md:132-145`). Lo no cubierto: DLL/`LD_PRELOAD` sin syscall ([[Known-Limitations]]; [[Claims-Ledger]] fila 14 = NOT MEASURED).
- Propuesta: «un módulo de kernel que deniega a cualquier otro proceso el acceso a la memoria de un proceso protegido mediante ptrace, `/proc/<pid>/mem` y `process_vm_readv/writev`».

**P04 · L38 · «un servicio en espacio de usuario responsable de la comunicación con el videojuego y la gestión de políticas de seguridad»**
- Hecho: el demonio registra el proceso del juego (socket Unix, `SO_PEERCRED`), ordena la protección al kernel con `quark_cli` por Netlink firmado, se registra como monitor de confianza, vigila variables cada 50 ms con `kill -9` ante discrepancia, y carga 12 programas BPF-LSM/telemetría (`features.md:70-83, 93-153, 155-209`; `docs/vm_test_environment.md:818-830`).
- Propuesta: «un servicio en espacio de usuario que registra los procesos protegidos, ordena su protección al módulo por un canal autenticado, carga los programas BPF-LSM y de telemetría y vigila las variables que el juego declara».

**P05 · L38 · «El desarrollo adopta un modelo en espiral con prácticas de SCRUM»**
- Hecho: el historial muestra prototipos sucesivos integrados por PR, en ráfagas, sin sprints ni análisis de riesgo por ciclo ([[Cycle-Log]] 2026-11-11: reconstrucción desde git; [[Process-Recommendation]] = **propuesta, pendiente de aceptación del equipo**).
- Propuesta (**condicionada a la decisión del equipo**): «El desarrollo se declara en espiral; la ejecución real es de prototipado evolutivo guiado por riesgo, en seis ciclos reconstruidos desde el historial de git.» Si el equipo no acepta, dejar L38 y agregar la desviación en Cap. VI (ver P38).

**P06 · L40 · «Los resultados esperados incluyen un prototipo funcional integrado con un videojuego de código abierto, la validación … y la medición de su impacto en el rendimiento»**
- Hecho: prototipo integrado con RecoilEngine/Beyond All Reason (`docs/vm_test_environment.md:353-372, 379-398`; [[Claims-Ledger]] fila 4 = SUPPORTED, en VM, build *testing*). Validación: 10/10 denegaciones sobre juego simulado, 5/5 ataques exitosos sin defensa, control negativo ([[Capture-findings-2026-08-29]] §2; [[Test-Status]]). Overhead CPU/RAM, tasas de detección y falsos positivos: NOT MEASURED (filas 10, 11).
- Propuesta: «El prototipo funciona integrado con RecoilEngine (motor de Beyond All Reason). La validación, realizada en máquina virtual con el build de pruebas, muestra la denegación del acceso externo a la memoria en 10 de 10 repeticiones sobre un juego simulado y una verificación sobre el motor real. El impacto en el rendimiento, la tasa de detección y la tasa de falsos positivos se declaran como trabajo pendiente.» (Reemplazar el pendiente por el valor medido si se mide antes de la entrega.)

**P07 · L36 · «en esta plataforma el anticheat, cuando existe, opera únicamente en espacio de usuario»**
- Hecho: vigente para EAC/BattlEye bajo Proton. EAC para Linux v2 (anunciado 2026-10-14, fuente pública secundaria, **no observado**) usa servicio systemd + BPF-LSM sin módulo de kernel (Update L643; `proton-anticheats/EAC_BPF_LSM_Service.md` §0-§3).
- Propuesta: añadir «y, según información pública reciente, mediante programas BPF-LSM sin módulo de kernel».

### 1.2 Capítulo I

**P08 · L152 · «sin degradar la experiencia del usuario»** (Misión) y L156 «evaluando … su impacto en el rendimiento»
- Hecho: sin medición ([[Claims-Ledger]] fila 10). Afirmarlo sin dato viola [[Working-Guidelines]] §3.
- Propuesta (Misión): «…que preserve la integridad del entorno de ejecución de videojuegos; el impacto en el rendimiento se mide y se informa en el Capítulo XII/Conclusiones.» Si no se mide: «…cuyo impacto en el rendimiento queda pendiente de medición».

**P09 · L161-164 · Objetivos específicos 2, 4 y 5**
- Hecho: Obj. 4 (tasas de detección y falsos positivos) y Obj. 5 (overhead): NOT MEASURED (filas 10, 11; [[Test-Status]]). Obj. 3 (SDK verificado en juego open source): cumplido en VM/*testing* (`sdk/quark_sdk.h`; `vm_test_environment.md:353-372`). Obj. 2 (≥5 vectores documentados): UNVERIFIED, no se halló un documento de vectores clasificado en `docs/` de Dev ni en el vault (revisión de los títulos y de `features.md`, sin búsqueda exhaustiva); los vectores efectivamente cubiertos son: ptrace attach, `/proc/<pid>/mem`, `process_vm_readv/writev`, carga de BPF de tracing, escritura de variables vigilada (`features.md:11-153`). Obj. 1: el diseño existe en `docs/contexto_proyecto.md` y [[Architecture-Overview]]; el «documento de diseño con diagramas» formal es UNVERIFIED.
- Propuesta: redactar cada objetivo con su estado: «Obj. 3: cumplido (SDK integrado en RecoilEngine). Obj. 4 y 5: la medición se declara pendiente.» Es una decisión de redacción: los objetivos pueden mantenerse como metas y reportar su cumplimiento en las Conclusiones.

**P10 · L168-170 · «sin que exista actualmente una solución técnica equivalente para dicha plataforma»**
- Hecho: el nicho «módulo de kernel local» sigue sin equivalente conocido, pero EAC v2 ofrece protección equivalente vía BPF-LSM (Update L643, L645; información pública, UNVERIFIED en observación propia).
- Propuesta: «No existe una solución de nivel de kernel abierta y documentada equivalente; los proveedores comerciales anuncian para Linux un servicio con programas BPF-LSM (información pública, sin verificación propia).»

**P11 · L176 · «propuesta de anticheat de nivel de kernel concebido de forma nativa … Su segundo diferencial es la adopción de Rust como lenguaje principal»**
- Hecho: Rust no es el lenguaje del módulo (P02). El diferencial «nativo de kernel» se debilita frente a EAC v2; el Update L645 lo traslada a «abierto, académico y documentado».
- Propuesta: «El primer diferencial es su carácter abierto y documentado. El segundo, la combinación de un módulo de kernel en C con un servicio en Rust y programas BPF-LSM que cubren lo que un LSM clásico no puede registrar fuera del árbol del kernel (`docs/features.md:95-100`). El tercero, su orientación académica frente al carácter cerrado de los anticheats comerciales.» Se elimina la cita de Ojeda (2025) de este párrafo (queda en Cap. III para el estado de Rust en el kernel).

**P12 · L184 · «El módulo de kernel supervisa los procesos activos del sistema, los accesos a memoria y los patrones de comportamiento … genera eventos que comunica al servicio en espacio de usuario»**
- Hecho: ver P03. El módulo no genera eventos hacia el demonio; registra en `dmesg` con `pr_warn_ratelimited` (`features.md:34`) y responde por Netlink a los comandos firmados (`features.md:155-209`, `kernel/quark_kernel.c:46,612`). Los eventos (`PTRACE_ATTEMPT`, `PROCESS_VM_ACCESS`, `EXEC_MPROTECT`, `TASK_KILL`, `MODULE_LOAD`, `EXEC`) los emiten los programas BPF por un *ring buffer* hacia el demonio (`features.md:132-145`).
- Propuesta: «El módulo de kernel deniega el acceso de nivel attach a la memoria de los procesos protegidos y registra cada intento en el log del kernel. Los eventos de telemetría los generan programas eBPF cargados por el servicio.»

**P13 · L184 · «el framework de Linux Security Modules (LSM) … (The kernel development community, 2024a)»**
- Hecho: un LSM clásico no se registra desde un módulo fuera del árbol: `security_add_hooks()` es `__init` y no se exporta (`features.md:95-100`; [[Claims-Ledger]] fila 13 = CONTRADICTED para el README de Dev). Se usa BPF-LSM (`lsm/bpf_prog_load`, `lsm/ptrace_access_check`, `lsm/file_mprotect`, `lsm/task_kill`; `features.md:107-145`) y un `kretprobe` para el bloqueo principal. Requiere `CONFIG_BPF_LSM=y` y `bpf` en `lsm=`; es *best-effort* (`features.md:97-99, 129-130`).
- Propuesta: «La capacidad de observación y mediación se apoya en un `kretprobe` sobre `ptrace_may_access` y en programas BPF-LSM, que exponen ganchos de seguridad del kernel desde eBPF sin requerir un módulo LSM compilado en el kernel (The kernel development community, 2024a).» (La cita 2024a describe LSM general; verificar que sostenga la frase sobre BPF-LSM o agregar la referencia de BPF-LSM, ver P53.)

**P14 · L186 · «recibe los eventos generados por el módulo de kernel, aplica las políticas … notificación al juego o el registro del incidente»**
- Hecho: el demonio no recibe eventos del módulo (P12). Acciones reales: `kill -9` ante discrepancia de variable (`features.md:78-80`); registro `[QUARK-BPF]`/`[QUARK-KERNEL ALERT]` ([[Log-messages]]); el SDK termina el juego si cae el demonio (`features.md:85-91`). «Notificación al juego»: UNVERIFIED (no se halló en `features.md`).
- Propuesta: «El servicio registra los procesos protegidos, ordena su protección, carga los programas BPF, registra la telemetría y termina el proceso del juego ante una discrepancia en las variables vigiladas.»

**P15 · L188 · API/SDK «sin requerir conocimiento de los detalles internos»**
- Hecho: vigente. Funciones reales: `quark_sdk_init`, `register_var`, `update_var`, `is_active`, `is_testing_build`, `is_bpf_lsm_active`, `get_version`, `close` (`features.md:239-250`; `sdk/quark_sdk.h`, 105 líneas). `init` devuelve -1 si el kernel no confirma la protección.
- Propuesta: agregar la política de fallo cerrado: «`quark_sdk_init()` falla si el kernel no confirma la protección, y un *watchdog* termina el juego si el servicio deja de responder».

### 1.3 Capítulo III

**P16 · L205 · «distribución de referencia Nobara Linux»**
- Hecho: dos entornos documentados: Nobara 43, kernel 7.0.9-200 (`vm_test_environment.md:10-12`) y CachyOS, kernel 7.3.1-1-cachyos, clang (`vm/README.md:5-9`, commit `38d49cd`, 2026-11-05). Cuál se usó para la versión final: UNVERIFIED. Resultados de §15.4: Nobara 7.0.9.
- Propuesta: «El desarrollo y las pruebas usan Nobara Linux 43 (kernel 7.0.9) y CachyOS (kernel 7.3.1) en máquinas virtuales QEMU/KVM.» Decisión humana: confirmar cuál es la de referencia.

**P17 · L211 · «LSM, eBPF, Netfilter»** y L245 «LSM, eBPF, Netfilter establecen límites»
- Hecho: Netfilter no se usa (sin coincidencias de `netfilter`/`nf_register` en `kernel/`, `quark_daemon/src`, `sdk/`). Tampoco `ioctl` (L519, L384 «netlink/ioctl»): el canal es Netlink protocolo 31 (`kernel/quark_kernel.c:46`) y socket Unix daemon↔juego (`sdk/quark_sdk.c:11`).
- Propuesta: «Interfaces del kernel utilizadas: `kretprobe`, Netlink, BPF-LSM y tracepoints eBPF.» Netfilter pasa a «no utilizado».

**P18 · L214 · «Cobertura de detección: … determinado por los patrones implementados en el módulo de kernel»**
- Hecho: la cobertura es: bloqueo de attach-level, bloqueo de BPF de tracing, autoprotección del demonio, vigilancia de variables, telemetría (`features.md:11-153`). Límites: DLL/`LD_PRELOAD` sin syscall; `/proc/<pid>/maps` legible por root (kernel ≥ 6.x, `features.md:44-53`); 16 procesos máx. (`kernel/quark_kernel.c:47`); `maxactive = 64` (L510); PIDs con `task_tgid_vnr()` sin soporte entre namespaces ([[Known-Limitations]]).
- Propuesta: enumerar la cobertura y los límites anteriores.

**P19 · L221 · variable exógena «Evolución del ecosistema de soporte de Rust para módulos de kernel»**
- Hecho: vigente como variable externa, pero el proyecto no usa Rust for Linux.
- Propuesta: «…condiciona la migración futura del módulo de C a Rust; el proyecto no depende de ella en su versión actual.»

**P20 · L229-233 · «El sistema incluye: … supervisa procesos, accesos a memoria y patrones … Un conjunto de casos de prueba ejecutados sobre un videojuego de código abierto»**
- Hecho: «casos de prueba» = scripts de VM (`run_test*.sh`, `capture.sh`) y 11 pruebas `#[test]` en el demonio (9 en `bpf.rs`, 2 en `main.rs`; una con `#[ignore]` que exige root, `bpf.rs:408-409`); la validación sobre el motor real fue manual ([[Test-Status]]). Lista de «no implementado»: SDK de servidor, prueba cliente↔servidor, política del motor para `bpf_lsm_active` (`features.md:252-265`).
- Propuesta: ajustar el primer ítem como en P03 y agregar a «Quedan fuera»: SDK del lado servidor, prueba cliente↔servidor y validación en hardware físico del build *release*.

**P21 · L245 · «Las pruebas con privilegios elevados requieren entornos virtualizados»**
- Hecho: correcto, con una consecuencia no consignada: el build *release* se niega a proteger dentro de una VM (CPUID, `features.md:55-68`), así que lo validado en VM es el build *testing* (`is_testing_build=1`) ([[Risk-Register]] R11; [[Claims-Ledger]] fila 15).
- Propuesta: agregar a Límites técnicos: «El build de producción rechaza ejecutarse en una VM; toda la validación disponible corresponde al build de pruebas.»

**P22 · L245 · «El soporte de Rust para módulos de kernel … presenta una madurez menor»**
- Hecho: vigente y ya aplicado (P02). Sin contradicción; agregar «razón por la cual el módulo está en C».

**P23 · L248 / L295-298 (Cap. V §5.3) · equipo de dos integrantes, ambos «en todas las fases»**
- Hecho: [[Plan-Inmediato-2026-11-25]] L17-18: Martínez Alarcón defiende en febrero; Merino De Rui colabora y presentará más adelante. Merino es dueño del repositorio (L484 del informe; remoto `stefanomerinoderui/Quark-Anticheat`).
- Propuesta: **no cambiar sin acuerdo de ambos**; si se acuerda: «Los dos integrantes desarrollan el proyecto; la defensa se programa en fechas distintas.» UNVERIFIED hasta confirmación.

### 1.4 Capítulo V

**P24 · L263-268 · Etapas «secuenciales»; Etapa 3 «Codificación en Rust del módulo de kernel»**
- Hecho: módulo en C (P02). Cronología real (ciclos reconstruidos, [[Cycle-Log]]): C1 2026-06-11 primer prototipo (`9b9aa22`); C2 2026-06-25 Ring 0 (`174e467`); sin commits 2026-06-26 → 2026-08-27 (causa UNVERIFIED); C3 2026-08-27/28 motor real (`6b05ad7`); C4 2026-08-29/31 endurecimiento (`2624ae4`, `333bbe2`, `48cc3f6`, `2216684`); C5 2026-09-30/10-05 BPF-LSM (`e497dbf`); C6 2026-11-05/06 linter e instalador.
- Propuesta: «Etapa 3 … codificación en C del módulo de kernel y en Rust del servicio en espacio de usuario.» Agregar un párrafo «Ejecución real» con la tabla de ciclos marcada «reconstruida desde git».

**P25 · L267 · «pruebas unitarias y de integración … verificando el comportamiento ante escenarios de carga, condiciones de carrera y entradas malformadas»**
- Hecho: no se halló evidencia en Dev ni en el vault de pruebas de carga, carrera ni entradas malformadas (UNVERIFIED). `maxactive = 64` fail-open bajo carga sin medir (`kernel/quark_kernel.c:510`; [[Known-Limitations]]).
- Propuesta: «Las pruebas de integración se ejecutan en QEMU/KVM con scripts y herramientas de ataque propias; las pruebas de carga, condiciones de carrera y entradas malformadas quedan pendientes.»

**P26 · L268 · Etapa 4 «evaluando la eficacia en la detección y el impacto sobre el rendimiento»**
- Hecho: sin medición (P08). Etapa 4 abierta (Update L657).
- Propuesta: marcar «en curso» y listar lo cumplido (integración con motor real) y lo pendiente.

**P27 · L274 y L543 · Entregable E1.4 «evaluación de bindings de Rust por API, vectores de ataque clasificados, videojuego de prueba seleccionado y justificado»**
- Hecho: no se halló ese documento. Lo existente: decisión R2 ([[Risk-Register]] L12, L29), `docs/contexto_proyecto.md:28` («Escrito en C con opción de portado a Rust»), juego elegido = RecoilEngine/BAR (`vm_test_environment.md:23-80`). UNVERIFIED que exista como documento fechado.
- Propuesta: no afirmar el entregable; citar las fuentes existentes o producirlo (persona).

**P28 · L276 · «Módulo de kernel compilado y estable»** y L291 H3 «0 kernel panics no controlados»
- Hecho: no hay registro de panics por sesión (UNVERIFIED; KPI 5 sin datos, [[KPIs]]).
- Propuesta: «módulo compilado (v0.4.0) y operativo en VM»; eliminar «estable» o declarar «sin kernel panics registrados» solo si una persona lo confirma.

**P29 · L283-291 · Hitos H1-H5 con fechas del plan**
- Hecho ([[Roadmap-and-Milestones]] Update 2026-11-11; Update L657): H3 módulo funcional en VM: 2026-06-25 (`174e467`), antes de lo planificado (fin ago). H4 integrado y probado «en lo esencial»: motor real 2026-08-28/31, BPF-LSM 2026-10-05 (PR #2), pero el criterio «≥ 75 % de casos aprobados» no se calculó ([[Claims-Ledger]] fila 11). H5 (mediados nov) abierto al 2026-11-25; defensa en febrero ([[Plan-Inmediato-2026-11-25]] L17). H1/H2: entregables E1.4/E2.3 UNVERIFIED (P27, P47).
- Propuesta: agregar columna «Estado al 2026-11-25» con esos valores y la fecha real de H3.

**P30 · L466-468 · «5.8. Hitos de Control» seguido de «Tabla VIII. Hitos de control» sin tabla**
- Hecho: defecto de forma. La tabla de hitos está en L283-289 dentro de 5.2; 5.8 solo tiene el rótulo.
- Propuesta: mover la tabla y los criterios (L291) bajo 5.8. Además, la numeración de tablas es I, II, IV, V, VI, VII, III, VIII (L306-L444): renumerar (Art. 20).

**P31 · L320 · E3.1 «Implementación del módulo de kernel (Rust)»** y L322 E3.3
- Hecho: C (P02).
- Propuesta: «(C)».

**P32 · L364-370 · Tabla IV: Módulo de kernel «(C + Rust) … 3.000-4.500 SLOC»; total 6.800-10.200; «Valor central 8.000 SLOC»**
- Hecho (wc -l en `Dev@35c6031`, líneas físicas con comentarios, no SLOC): módulo 659 (`quark_kernel.c` 648 + `quark_pubkey.h` 11); demonio 1.765 (`main.rs` 622, `bpf.rs` 455, `quark.bpf.c` 402, `quark_cli.c` 260, `build.rs` 26); SDK 390 (`quark_sdk.c` 285, `.h` 105); juego simulado y atacante 198 (`game.c` 115, `cheat.c` 83). Total ≈ 3.012 líneas físicas. El módulo no contiene Rust.
- Propuesta: agregar una **Tabla IV-bis «Tamaño real del prototipo (líneas físicas, `wc -l`, Dev@35c6031)»** con esos valores y la nota «la estimación original (8.000 SLOC) se mantiene como referencia de planificación; el tamaño real es menor». No recalcular COCOMO sin decisión del equipo.

**P33 · L384-386 · Tabla V (Story Points)**: «Canal … (netlink/ioctl)», «Integración con Rust for Linux 13 SP», «Supervisión de procesos con eBPF 21 SP»
- Hecho: sin `ioctl` (P17); Rust for Linux descartado (P02); eBPF implementado como telemetría + BPF-LSM (12 programas, 4 mapas, 12 enlaces, `vm_test_environment.md:818-830`).
- Propuesta: nota «El ítem de Rust for Linux no se ejecuta; el esfuerzo se reasigna a BPF-LSM y al canal autenticado». No inventar SP reales (no hay registro: [[Cycle-Log]] «Lo que NO muestra»).

**P34 · L442-464 · «Se identifican siete riesgos»** y Tabla III
- Hecho: [[Risk-Register]] tiene R1-R14. Añadidos: R8 procedencia del build (causa probable `2624ae4`), R9 deriva de repos en la VM, R10 socket sin autenticar (mitigado, residual `SocketMode=0666`), R11 validación solo con build *testing* (Alta/Alto), R12 documentación contradice al código (Alta/Medio), R13 divergencia de ramas (Alta/Medio), R14 overhead sin medir (Alta/Alto).
- Propuesta: «Se identifican catorce riesgos; los siete primeros se planificaron y los siete restantes se observaron durante el desarrollo», con tabla ampliada y columna «Estado»: R2 materializado, contingencia ejecutada; R6 mitigado.

**P35 · L449 / L459 · R2 y su plan «determinando qué se implementa en Rust y qué requiere C»**
- Hecho: se materializó y se ejecutó la contingencia: C en el módulo y Rust en el demonio ([[Risk-Register]] Update L29).
- Propuesta: agregar «Estado: materializado; contingencia aplicada: módulo en C, servicio en Rust, BPF-LSM mediante `libbpf-rs`».

**P36 · L458 · R1 contingente «se reduce el alcance al conjunto mínimo de hooks (LSM básico) y se posponen las funcionalidades eBPF»**
- Hecho: ocurrió lo inverso: LSM clásico es inviable fuera del árbol (P13); eBPF/BPF-LSM se implementó. R1 preventivo «todo en QEMU/KVM» vigente, con la salvedad R11.
- Propuesta: reemplazar «LSM básico» por «`kretprobe` sobre `ptrace_may_access`».

**P37 · L453, L463 · R6 «Baja … al menos dos candidatos … evalúan»**
- Hecho: mitigado: integración con RecoilEngine/BAR lograda (Update L658). La evaluación de dos candidatos: UNVERIFIED (solo hay documentación de RecoilEngine y del juego simulado).
- Propuesta: «Estado: mitigado (integración lograda con RecoilEngine/Beyond All Reason)»; omitir «al menos dos candidatos» salvo evidencia.

**P38 · L461, L464 · R4/R7 «declara la versión mínima», «ancla a una versión de kernel»**
- Hecho: no se halló una versión mínima declarada; los entornos documentados difieren (7.0.9 en Nobara, `vm_test_environment.md:10-12`; 7.3.1 en CachyOS, `vm/README.md:5-9`; el `.ko` se compila en cada VM, `vm/README.md` §Quark). `vmlinux.h` generado en host 7.2.7 y usado en VM 7.0.9 por CO-RE (`vm_test_environment.md:827`). `README.md` de Dev (L12-L40 del README) dice «kernel 6.1 o superior con soporte estable para Rust», contradicho por el código ([[Risk-Register]] R12). BPF-LSM exige `CONFIG_BPF_LSM` y `lsm=…,bpf` (`features.md:97-99`).
- Propuesta: «Los kernels de prueba son 7.0.9 (Nobara 43) y 7.3.1 (CachyOS). El módulo se compila contra los *headers* de cada equipo. El soporte de otras versiones no se verificó.»

**P39 · L472 · MVP «demuestra la detección de al menos los vectores de ataque identificados y reporta el overhead»**
- Hecho: el MVP real **previene** (deniega) los vectores de la lista de P09 y no reporta overhead (NOT MEASURED). End-to-end con RecoilEngine: sí, en VM y build *testing*. Estado por módulo (estimaciones por juicio, UNVERIFIED, no van en el informe): [[Plan-Inmediato-2026-11-25]] L22-28.
- Propuesta: «El MVP es un prototipo funcional compuesto por el módulo de kernel (C), el servicio (Rust) y el SDK (C), integrado con RecoilEngine. Impide el acceso externo a la memoria del proceso protegido por ptrace, `/proc/<pid>/mem` y `process_vm_*`, bloquea la carga de programas BPF de tracing y se autoprotege. Se valida en VM con build de pruebas. No incluye SDK de servidor ni medición de rendimiento.»

**P40 · L352 · Figura 1 «(Insertar el diagrama …)»**
- Hecho: placeholder; el grafo no está incorporado.
- Propuesta: insertar la figura o quitar el texto de instrucción (persona).

### 1.5 Capítulo VI

**P41 · L478-480 · «Se adopta el modelo en espiral … cada ciclo atraviesa las fases …»**
- Hecho: P05. No existen artefactos de riesgo por ciclo ([[Cycle-Log]]; [[Process-Recommendation]]).
- Propuesta (**condicionada**): «Se declara el modelo en espiral con prácticas de SCRUM (Boehm, 1988; Schwaber & Sutherland, 2020). La ejecución real es de prototipado evolutivo guiado por riesgo: seis prototipos sucesivos integrados por *pull request*, con revisión de riesgos reconstruida desde el historial. No se registran sprints.»

**P42 · L484 · «vinculando los commits con las actividades del Gantt … El registro semanal de avance de cada integrante contrasta horas y tareas»**
- Hecho: los mensajes de commit de `origin/Dev` no mencionan IDs de actividad (E1.1…E4.4) (búsqueda en `git log` sin resultados); no se halló registro semanal de horas ([[Cycle-Log]] «Lo que NO muestra»; Trello pendiente de migrar, [[Trello-Migration-Guide]]). UNVERIFIED si existe en Trello.
- Propuesta: «El historial de git (29 commits en `Dev`, 3 *pull requests* integrados) registra el avance. El tablero Kanban del proyecto complementa el seguimiento.» Omitir lo de horas hasta aportar el registro.

**P43 · L488 · «El desarrollo se ancla a una versión de kernel específica declarada en la documentación técnica»**
- Hecho: contradicho (P38).
- Propuesta: «La documentación técnica registra los kernels de prueba (7.0.9 y 7.3.1). No se fija una versión mínima soportada.»

**P44 · L492 · Testing**: «pruebas unitarias y de integración … tasas de detección y falsos positivos … eBPF facilita la instrumentación con bajo overhead»
- Hecho: pruebas = scripts (`run_test.sh`, `run_test_kernel.sh`, `run_test_kernel_release.sh`, `run_test_no_quark.sh`, `capture.sh`), 11 `#[test]` en el demonio, tabla de verificación de `vm_test_environment.md:796-816`. Tasas: NOT MEASURED. Defectos del harness: `results.csv` malformado, `summary.txt` solo condición B (§7.1) ([[Test-Status]]). La cita de New Relic (2025) sostiene una afirmación general sobre eBPF, no una medición de Quark.
- Propuesta: describir las pruebas reales con su alcance (VM, build *testing*, juego simulado/motor real) y quitar «bajo overhead» referido al proyecto.

**P45 · L496-504 · cinco indicadores y «resultados de cada revisión se documentan»**
- Hecho: ICC, velocidad, DE: sin registro; TDP: NOT MEASURED; estabilidad: sin registro de panics. UNVERIFIED que existan revisiones por hito documentadas.
- Propuesta: tabla «Indicador | Meta | Valor al 2026-11-25» con «sin registro» donde corresponda.

### 1.6 Capítulo X

**P46 · L524 · «≈ 696 horas por integrante … 8 meses (≈ 22 h/semana)»**
- Hecho: estimación de planificación; horas reales sin registro (UNVERIFIED). El historial muestra trabajo en ráfagas (jun, fin ago, oct, nov) y un intervalo sin commits 2026-06-26 → 2026-08-27 ([[Cycle-Log]]).
- Propuesta: «El esfuerzo planificado asciende a… Las horas reales no se registran.»

**P47 · L525 · Recursos físicos**
- Hecho: además de equipos personales: VM QEMU/KVM en `192.168.122.203`, disco de 23 GB (`vm_test_environment.md:7-21`); VM CachyOS de 4 CPU, 7,7 GiB RAM, 26 GiB de disco (`vm/README.md:7-12`); host Arch Linux con contenedores Docker (Fedora 44) para compilar plugins de IA de RecoilEngine (`vm_test_environment.md:16-19, 264-296`; `tooling/recoil-fedora-build/`).
- Propuesta: agregar esos recursos.

**P48 · L527 · «Lenguaje principal Rust, con C para los componentes sin bindings estables; interfaces del kernel LSM, eBPF y Netfilter; virtualización QEMU/KVM; distribución de referencia Nobara Linux; sistema de control de versiones»**
- Hecho (fuentes: `Makefile`, `quark_daemon/Cargo.toml`, `kernel/Makefile`, `docs/features.md`):
  - Lenguajes: C (módulo, SDK, `quark_cli`, programas BPF, juego simulado, atacante); Rust edition 2024 (demonio); C++ (RecoilEngine).
  - Bibliotecas: `libbpf-rs 0.27`, `libbpf-cargo 0.27` (build), `libc 0.2`; OpenSSL `libcrypto` (`quark_cli`, `Makefile`); API criptográfica del kernel (`crypto_alloc_sig("x962(ecdsa-nist-p256)")`, `features.md:193-197`).
  - Interfaces del kernel: `kretprobe`, Netlink protocolo 31, BPF-LSM, tracepoints; sin Netfilter.
  - Herramientas: GCC, clang/LLVM (módulo en kernels compilados con clang, `kernel/Makefile`), `bpftool` (genera `vmlinux.h`), `clang-tidy` (`make lint`), `cargo`, systemd (`quark.socket`, `quark.service`, `quark-kernel.service`), Docker, QEMU/KVM, git/GitHub.
  - Distribuciones: Nobara 43, CachyOS.
  - Todo es software libre: UNVERIFIED para herramientas auxiliares usadas en pruebas (p. ej. el cliente de memoria externo mencionado en [[Cycle-Log]]); sin verificar licencias.
- Propuesta: reescribir la viñeta con la lista anterior y eliminar Rust como «lenguaje principal» y Netfilter.

### 1.7 Capítulo XIII

**P49 · L539 · «Módulo de kernel (C + Rust)»**
- Hecho: C (P02).
- Propuesta: «Módulo de kernel (C), servicio en espacio de usuario (Rust), SDK (C), programas eBPF (C), herramientas de prueba (juego simulado, atacante, scripts de VM), unidad systemd y scripts de instalación (`tooling/install.sh`, solo en `feature/gameStartProtection`), alojados en `Quark-Anticheat`; submódulo `RecoilEngine` con la integración.»

**P50 · L543-548 · lista de documentación**
- Hecho por ítem:
  - E1.4 documento de diseño preliminar: UNVERIFIED (P27).
  - E2.3 diagramas: existe un diagrama `mermaid` en `docs/contexto_proyecto.md:19` y en [[Architecture-Overview]]; diagramas formales UNVERIFIED.
  - Prototipo end-to-end (MVP): existe, alcance VM/*testing*.
  - Informe de validación con tasas de detección y falsos positivos: **no existe**; existe el informe de capturas [[Capture-findings-2026-08-29]] (10/10, 5/5, control negativo).
  - Medición de overhead: **no existe**.
  - Documentación final y material de defensa: en curso.
  - Faltan en la lista, y existen: `docs/features.md`, `docs/vm_test_environment.md`, `docs/log_messages.md`, `docs/funcionamiento_codigo.md` (en Dev), el vault, la investigación `proton-anticheats` y el informe.
- Propuesta: lista con columna «Estado» (existe / parcial / pendiente) y las rutas.

### 1.8 Bibliografía y notas

**P51 · L564, L574, L578 · Kaspersky (2020), The kernel development community (2024b), Wikipedia (2026b)**
- Hecho: figuran en la bibliografía pero no se citan en el cuerpo (L1-L553). APA exige correspondencia.
- Propuesta: citarlas donde corresponda (Kaspersky en Cap. I/II sobre trampas; 2024b en Cap. III sobre Rust; Wikipedia 2026b en Cap. II sobre EAC) o retirarlas.

**P52 · Bibliografía vs Update 2026-11-13 (L637-646)**
- Hecho: el Update afirma hechos sobre EAC v2, BattlEye y el análisis dinámico sin entrada bibliográfica ni cita APA; son fuentes propias (`proton-anticheats`, commit `cc5078e`) y «fuentes públicas secundarias» no identificadas (anuncio de Epic del 2026-10-14: fuente exacta UNVERIFIED).
- Propuesta: agregar «Martínez Alarcón, G. S., & Merino De Rui, S. N. (2026). *proton-anticheats* \[Repositorio\]. URL: UNVERIFIED (pendiente de aportar)» y la referencia concreta del anuncio de EAC v2 cuando una persona la aporte. No inventar la cita.

**P53 · Bibliografía: falta referencia de BPF-LSM**
- Hecho: el informe sostiene que BPF-LSM es el camino (P13) y no hay referencia que lo respalde; `features.md:95-100` es documentación propia.
- Propuesta: agregar la documentación del kernel sobre BPF-LSM; la URL y la fecha de consulta se verifican por una persona antes de incluirla (no se verificó en esta auditoría).

**P54 · L592-609 · Notas al pie 7-9** (LSM, eBPF, Netfilter)
- Hecho: Netfilter ya no se usa (P17); la nota 9 y la mención en L211 sobran. La nota 7 (LSM) puede ampliarse con BPF-LSM.
- Propuesta: eliminar la nota 9 al quitar Netfilter; renumerar.

**P55 · Update L617, L660 (autocorrección)**
- Hecho: L660 dice `dev/docs` «2 commits»; al 2026-11-25 `origin/dev/docs` está 6 commits por delante de `Dev` (`git rev-list --count origin/Dev..origin/dev/docs`), `gameStartProtection` 4 (correcto) y `main` 1 commit por delante de `Dev` (`989693f`, `.gitignore`).
- Propuesta: actualizar a «seis commits» al integrar el Update al cuerpo.

### 1.9 Resumen de severidad

- **Contradicen al código (corregir sí o sí):** P02, P03, P11, P12, P13, P17, P24, P31, P35, P36, P48, P49.
- **Afirman lo no medido:** P06, P08, P09, P26, P39, P44, P50.
- **Desactualizados por el tiempo transcurrido:** P01, P29, P34, P37, P55.
- **Sin evidencia hallada (UNVERIFIED):** P14 (notificación al juego), P25, P27, P28, P38, P42, P45, P46.
- **Requieren decisión humana:** P05/P41 (proceso), P16 (distribución de referencia), P23 (defensa por integrante), P32 (recalcular o no COCOMO), P52/P53 (referencias).

---

## Parte 2 — Borrador de ANEXO III (otros anexos)

> Texto listo para incorporar al informe. Hojas de anexo con numeración propia «página X de Y» (Art. 20/24.6). Se redacta en impersonal y presente afirmativo.

### Anexo III. Otros anexos

#### III.1. Estado del producto mínimo viable congelado

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

#### III.2. Qué se probó y con qué alcance

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

#### III.3. Qué no se midió ni existe

- **No se midió:** overhead de CPU y RAM (ledger fila 10; requisito del MVP, H5); tasas de detección y falsos positivos (fila 11, meta TDP ≥ 75 %); detección de una DLL o `LD_PRELOAD` inyectada (fila 14; `EXEC_MPROTECT` es solo un indicador); protección real en producción, es decir, el build *release* en hardware físico (fila 15); intentos de evasión; latencia de detección del Modo A; revisión de código probada.
- **No existe en el código:** SDK del lado servidor; prueba cliente↔servidor de punta a punta; política del motor sobre `bpf_lsm_active` (`features.md:252-262`); caso `SIGSTOP` sobre el demonio sin resolver (UNVERIFIED, [[Known-Limitations]] Update).
- **Límites declarados del diseño:** máximo de 16 procesos protegidos (`kernel/quark_kernel.c:47`); `maxactive = 64` con *fail-open* bajo carga sin medir (L510); PID resueltos con `task_tgid_vnr()`, sin soporte entre *namespaces* de PID; `/proc/<pid>/maps` legible por root; BPF-LSM *best-effort* según `lsm=`; mientras hay un proceso protegido fallan `bpftrace` y herramientas con BPF de tracing (`features.md:44-53, 125-130`).
- **Defectos del harness:** `results.csv` malformado y `summary.txt` solo con la condición B; `quark_cli` informa éxito sin confirmación del kernel; objetivo no PIE ([[Test-Status]]; [[Capture-findings-2026-08-29]] §7).

#### III.4. Repositorios y rutas

**Tabla III.4. Repositorios**

| Repositorio | Ubicación | Estado | Fuente |
|---|---|---|---|
| `Quark-Anticheat` | `https://github.com/stefanomerinoderui/Quark-Anticheat` (remoto `origin`) | Código en rama `Dev`; documentación en `dev/docs`; `main` atrasada | `git remote -v` |
| `RecoilEngine` | Submódulo en `RecoilEngine/`; URL `https://github.com/Billones142/RecoilEngine.git`, rama `quark-anticheat-integration`; commit fijado `29e5b0b44a7604011eca4aaf1281c9c7e86ba5fd` | La integración con el SDK está en esa rama; el submódulo no está inicializado en los worktrees de lectura | `.gitmodules`; `git submodule status` |
| `proton-anticheats` | Repositorio local `uni-dev/proton-anticheats2026-11-13/proton-anticheats` (último commit `cc5078e`, 2026-11-13, según [[Proton-Anticheat-Research]]); URL remota: UNVERIFIED (pendiente de aportar) | La copia local analizada no contiene el directorio `.git`; el commit citado proviene de la nota del vault. Contiene `EAC.md`, `BattlEye.md`, `EAC_BPF_LSM_Service.md`, `Validation_Log.md` y otros | listado del directorio; [[Proton-Anticheat-Research]] |

Rutas del repositorio principal: código en `kernel/`, `quark_daemon/`, `sdk/`, `game_target/`, `cheat/`; documentación técnica en `docs/` de `Dev` (`features.md`, `vm_test_environment.md`, `log_messages.md`, `funcionamiento_codigo.md`, `contexto_proyecto.md`); vault en `docs/obsidian-vault/quark-vault/`; informe en `01-Project/Informe-PIF-Avance.md`; generación del documento en `tooling/build_informe.sh`.

#### III.5. Cómo reproducir

> Procedimiento extraído de `Makefile`, `kernel/Makefile`, `run_test_kernel.sh`, `tooling/keys/generate-testing-key.sh`, `docs/vm_test_environment.md` §15 y `tooling/install.sh` (rama `feature/gameStartProtection`). **No se ejecutó** para redactarlo. Debe ejecutarse **solo en una máquina virtual descartable**: carga un módulo de kernel y requiere privilegios de root.

1. **Entorno.** VM QEMU/KVM con Nobara 43 (kernel 7.0.9) o CachyOS (kernel 7.3.1) (`vm_test_environment.md:10-12`; `vm/README.md:5-9`), con *headers* del kernel en ejecución, `gcc`, `clang`, `bpftool`, `cargo`, `openssl` (`libcrypto`), `make`, `sudo`.
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

---

## Pendientes de aportar por una persona
- Confirmar la distribución de referencia (P16) y el reparto de la defensa (P23).
- Aceptar o rechazar ADR-001 (P05, P41).
- URL remota de `proton-anticheats` y referencia exacta del anuncio de EAC v2 (P52).
- Registro de horas, revisiones por hito y panics, si existen en Trello (P28, P42, P45, P46).
- Tag del MVP y decisión de integrar `feature/gameStartProtection` y `dev/docs` (Plan-Inmediato, Fase 2).

— agent:claude-sonnet-5-5, 2026-11-25
