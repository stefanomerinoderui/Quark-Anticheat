---
title: "Borrador Cap. XII y Conclusiones"
tags: [proyecto, informe, borrador]
status: draft
author: agent:claude-sonnet-5-5
date: 2026-11-25
---

> Borrador para fusionar en `Informe-PIF-Avance` (o `Informe-PIF-v2`). Estado descrito: `origin/Dev@35c6031` (2026-11-05), leído y no re-ejecutado. Las abreviaturas de fuente son notas del vault o documentos de `Dev` (`docs/*.md` de ese commit). Lo inferido va marcado UNVERIFIED. Redacción impersonal en presente (Art. 21).

# CAPÍTULO XII — LECCIONES APRENDIDAS DEL PROYECTO

## 12.1. Alcance y fuentes

Este capítulo recoge lo que el historial del repositorio y las notas del vault permiten afirmar sobre la ejecución del proyecto. No existen revisiones por hito escritas en su momento (ver 12.3.1), por lo que las lecciones se derivan de una reconstrucción desde git ([[Cycle-Log]], entrada 2026-11-11, rotulada como no contemporánea) y de los registros de riesgos, pruebas y afirmaciones. Trello, las reuniones semanales y los registros semanales de avance que menciona la sección 6.2 no se revisaron para este borrador (UNVERIFIED; [[Process-Recommendation]], "Limitaciones de esta evaluación").

## 12.2. Aspectos positivos

**12.2.1. La contingencia del riesgo R2 se ejecuta y resulta viable.** El plan contingente de R2 (componentes sin bindings estables en C) estaba escrito antes del desarrollo (§5.7). El módulo de kernel resulta en C (`kernel/quark_kernel.c`), el demonio en Rust y los programas eBPF en C cargados con `libbpf-rs` (Update 2026-11-13, B; [[Risk-Register]] Update 2026-11-11; [[Claims-Ledger]] fila 12). La decisión por componente, que la sección 5.7 exigía documentar, queda sustentada por una restricción técnica concreta: un LSM clásico no se registra desde un módulo fuera del árbol porque `security_add_hooks()` solo existe durante la inicialización y no se exporta; la capa LSM se obtiene mediante BPF-LSM desde el demonio ([[Features]] §1.5; [[Claims-Ledger]] fila 13).

**12.2.2. Los hallazgos de seguridad propios se corrigen en el desarrollo.** Durante el diseño del canal de control se encuentran dos fallas de escalada local: (1) cualquier proceso local podía abrir un socket Netlink (protocolo 31) y ordenar desproteger el PID de otro; (2) el socket Unix del demonio (`/tmp/quark.sock`, `SocketMode=0666`) confiaba en el `pid` declarado por el cliente, de modo que el propio demonio, con privilegios de root, desprotegía a la víctima (`docs/vm_test_environment.md:610-624`, `docs/features.md:157-163`). La corrección se hace en capas (pid real por `SO_PEERCRED`, emisor root verificado por el kernel, hash SHA-256 de `quark_cli`, firma ECDSA P-256 con nonce creciente; commit `48cc3f6`; [[Features]] §2). El documento de la VM deja asentado que corregir solo la primera falla habría sido insuficiente porque la segunda produce el mismo efecto (`docs/vm_test_environment.md:623-624`). Estado de la verificación: DOCUMENTED, sin reverificar ([[Claims-Ledger]] fila 7). Queda un residual declarado: `SocketMode=0666` ([[Risk-Register]] Update 2026-11-11, R10).

**12.2.3. Las pruebas realimentan el diseño.** El hallazgo en la VM de que Cheat Engine leía memoria sin error tras un reinicio sin módulo cargado ([[VM-test-environment]] §11) produce el comportamiento de fallo cerrado (`2624ae4`: el SDK no informa éxito sin confirmación del kernel) y luego la detección de VM con build *testing* y atestación (`333bbe2`) ([[Cycle-Log]], "Lazo de retroalimentación observable"). La cronología también corrige una lectura previa: `2624ae4` (03:14 UTC) es anterior a las capturas formales del 2026-08-29 (03:33 UTC), por lo que estas no motivaron ese arreglo.

**12.2.4. La validación distingue causa de correlación.** El resultado principal está acotado por un control negativo: con el módulo cargado, el ataque por `/proc/<pid>/mem` falla con `EACCES` en 10 de 10 repeticiones; sin defensa funciona en 5 de 5; al descargar el módulo vuelve a funcionar sobre el mismo PID, lo que atribuye el bloqueo a Quark y no a Yama ([[Capture-findings-2026-08-29]] §2; [[Test-Status]]). Alcance: VM, build de *testing*, juego simulado; además hay una validación sobre el motor real ([[VM-test-environment]] §7).

**12.2.5. La integración con un juego real se logra.** El SDK se incorpora a RecoilEngine (*Beyond All Reason*), que impide iniciar una partida protegida si Quark no confirma la protección (PR #1; [[VM-test-environment]] §6.5, §7). El riesgo R6 pasa a estado mitigado ([[Risk-Register]]).

**12.2.6. La práctica de afirmar solo con evidencia se instala.** El [[Claims-Ledger]] clasifica cada afirmación como SUPPORTED, DOCUMENTED, NOT MEASURED o CONTRADICTED, y [[Working-Guidelines]] §6 define cuándo una afirmación está lista para el informe. Esta práctica permite declarar con precisión lo no medido (filas 10, 11, 14, 15) en lugar de repetir la formulación aspiracional del README.

**12.2.7. El análisis de la competencia aporta una validación de rumbo.** El relevamiento sobre Easy Anti-Cheat y BattlEye bajo Proton, y la información pública sobre EAC para Linux v2 basada en BPF-LSM, indican que la industria converge hacia el mecanismo que Quark usa en su capa BPF-LSM (Update 2026-11-13, D). Alcance: información pública y análisis estático; el comportamiento de EAC v2 no se observó.

## 12.3. Aspectos a mejorar

**12.3.1. Falta de registro contemporáneo del proceso.** El informe declara modelo en espiral con prácticas SCRUM (§6.1), pero el historial muestra prototipos sucesivos integrados por *pull request* sin análisis de riesgo escrito por ciclo, planificación del ciclo siguiente, *sprints* ni velocidad ([[Cycle-Log]], "Lo que NO muestra el historial"; [[Process-Recommendation]], contexto). Los indicadores de la sección 6.5 (ICC, velocidad en SP, desvío de esfuerzo) no se calcularon con datos de la época (UNVERIFIED: ningún documento revisado los contiene). Los ciclos C1–C6 son interpretación posterior. Lección: la puerta de riesgo por iteración de [[Working-Guidelines]] §2 (objetivo, alcance, tres riesgos, criterio de salida, decisión GO/NO-GO/PIVOT) se aplica desde el inicio de cada ciclo y no al final. La desviación se declara así: modelo en espiral declarado; ejecución real, prototipado evolutivo guiado por riesgo ([[Process-Recommendation]]; estado: propuesta pendiente de aceptación del equipo).

**12.3.2. Trabajo en ráfagas.** Los commits se concentran en junio, fines de agosto, octubre y noviembre; entre 2026-06-26 y 2026-08-27 no hay commits y la causa no consta (UNVERIFIED) ([[Cycle-Log]]; Update 2026-11-13, F). Frente a una estimación de ≈ 22 h/semana por integrante (§5.6), el historial no permite contrastar horas reales, porque no hay registro de horas en las fuentes revisadas (UNVERIFIED). Lección: registrar horas y tareas semanalmente, como ya preveía la sección 6.2, para que el riesgo R5 (disponibilidad) y R3 (esfuerzo) tengan datos.

**12.3.3. Documentación que contradice al código.** El README de `Dev` y el informe original afirman un módulo "en Rust" y el uso del "framework LSM"; el módulo es C y la capa LSM es BPF-LSM ([[Claims-Ledger]] filas 12 y 13, CONTRADICTED). El README de `Dev` es aspiracional respecto del overhead (`contexto_proyecto.md`, según [[Test-Status]] Update 2026-11-11). El Resumen y el Cap. X siguen diciendo "Rust como lenguaje principal" ([[Plan-Inmediato-2026-11-25]], "Estado de capítulos"). Esto se registra como R12 ([[Risk-Register]]). Lección: actualizar la documentación en el mismo *pull request* que cambia la decisión técnica, y no dejar la corrección en un bloque `Update` al final del informe.

**12.3.4. Divergencia de ramas.** `main` queda en el commit del 2026-06-11 más un cambio de `.gitignore`; la integración real ocurre en `Dev`. `feature/gameStartProtection` (4 commits, sin PR) hace que el juego simulado exija demonio y BPF-LSM para arrancar, con lo que el control negativo "sin Quark" deja de funcionar tal cual; `dev/docs` tampoco está integrada ([[Risk-Register]] R13; Update 2026-11-13, F; [[Plan-Inmediato-2026-11-25]], "Congelamiento del MVP"). Lección: un solo prototipo vivo, `main` actualizada solo con versiones congeladas y etiquetadas (`rc-1`, pendiente), y revisión del impacto sobre los scripts de prueba antes de cada *merge*.

**12.3.5. Procedencia de las capturas y defectos del harness.** Las capturas del 2026-08-29 se hicieron sin registrar `git_commit` ni `git_branch` en `environment.txt`, por lo que el commit probado no se puede demostrar y la correspondencia con `2624ae4` es probable pero UNVERIFIED ([[Test-Status]] Update 2026-11-11; [[Risk-Register]] R8). El harness presenta `results.csv` malformado y `summary.txt` que solo reporta la condición B; `quark_cli` informa éxito sin confirmación del kernel en el binario capturado ([[Capture-findings-2026-08-29]] §7.1, §7.6). Se asume sin corregir `capture.sh` (UNVERIFIED). Lección: fijar y registrar la revisión antes de capturar y tratar el harness como código sujeto a pruebas.

**12.3.6. Validación postergada hacia el final.** El overhead de CPU/RAM, las tasas de detección y falsos positivos, los intentos de evasión y el build de *release* en hardware físico no se midieron ([[Claims-Ledger]] filas 10, 11, 14, 15; [[Risk-Register]] R11 y R14). Medir esos aspectos corresponde a la etapa 4 del cronograma, pero la dependencia (el build de *release* se niega a proteger en una VM) era previsible desde el desarrollo de la detección de VM y no se anticipó en el registro de riesgos hasta noviembre. Lección: elegir tempranamente el entorno de medición y planificar la medición como parte de cada ciclo, no como actividad final.

**12.3.7. Estimación sin recalibración.** La estimación COCOMO usa constantes del modelo intermedio y un factor de reducción de 0,15 aplicado por criterio (§5.6, nota metodológica). El código real no se contrastó con las 8.000 SLOC estimadas ni con los 99 SP en las fuentes revisadas (UNVERIFIED). Lección: comparar estimado y real al cierre de cada iteración, como establece el plan preventivo de R3.

**12.3.8. Encuesta y datos de mercado.** El instrumento de encuesta del Cap. II está diseñado y sin resultados ([[Plan-Inmediato-2026-11-25]], Fase 2). Lección: publicar el instrumento al inicio del cronograma, ya que depende de respuestas de terceros.

---

# CONCLUSIONES DEL PROYECTO

> Carácter **parcial**: el proyecto no cierra todas las mediciones comprometidas en el Capítulo I. Cada conclusión indica alcance y fuente.

## C.1. Frente al objetivo general

El objetivo general comprometía analizar, diseñar y desarrollar un anticheat de nivel de kernel para GNU/Linux y evaluar su viabilidad técnica, su impacto en el rendimiento y los riesgos de seguridad asociados a los privilegios de kernel. Se logra un prototipo funcional de tres piezas (módulo de kernel v0.4.0, demonio, SDK en C) y se muestra, dentro de una VM, con build de *testing* y juego simulado, que un módulo de kernel reforzado con BPF-LSM impide el acceso externo a la memoria de un proceso protegido y que el mecanismo se integra en un motor real (Update 2026-11-13, A y G; [[Test-Status]]). **No se evalúa el impacto en el rendimiento**, por lo que la parte del objetivo y de la misión referida a "sin degradar la experiencia del usuario" **no tiene respaldo medido**. No se afirma bajo impacto de rendimiento ([[Claims-Ledger]] fila 10, NOT MEASURED). Los riesgos de seguridad de los privilegios de kernel se abordan en parte: se encuentran y corrigen dos fallas propias de escalada local (12.2.2), y quedan límites declarados en [[Known-Limitations]].

## C.2. Frente a los objetivos específicos

| N° | Objetivo (Cap. I, 1.2) | Estado | Evidencia |
|---|---|---|---|
| 1 | Definir la arquitectura (kernel, servicio, interfaz) en un documento de diseño | Parcial. La arquitectura existe en código y en la documentación de `Dev` ([[Features]]); el Cap. IX se redacta a partir de ella. Entregable E1.4/E2.3 como documento formal: UNVERIFIED | Update 2026-11-13, A–B |
| 2 | Identificar y documentar al menos cinco vectores de ataque | Parcial. El diseño cubre ptrace, `/proc/<pid>/mem`, `process_vm_readv/writev` y carga de BPF de *tracing*; con `EXEC_MPROTECT` como indicador. Eso suma cuatro vectores bloqueados o cubiertos más un indicador. La clasificación formal de cinco vectores no consta en las fuentes revisadas (UNVERIFIED) | [[Features]] §1.1, §1.5; Update 2026-11-13, A–B |
| 3 | Implementar la API/SDK y verificarla en un juego de código abierto | Logrado en lo esencial: SDK en C integrado en RecoilEngine/BAR; el motor no inicia una partida protegida sin confirmación. Faltan SDK de servidor y prueba cliente↔servidor | PR #1; [[VM-test-environment]] §6.5, §7; [[Features]] §5 |
| 4 | Validar con casos de prueba por vector, registrando tasas de detección y falsos positivos | Parcial. Un vector (`/proc/<pid>/mem`) con 10/10 de bloqueo y control negativo; `process_vm_*` y `ptrace` documentados sin reverificar. **No se calculan tasas de detección ni falsos positivos** | [[Test-Status]]; [[Claims-Ledger]] filas 1–3, 8, 11 |
| 5 | Medir el overhead de CPU y RAM | **No cumplido.** No existe medición | [[Claims-Ledger]] fila 10; [[Test-Status]] |

## C.3. Lo que no se midió ni se probó

- Overhead de CPU y RAM (Objetivo 5); plan: tres configuraciones, al menos 10 repeticiones, media y desviación ([[Working-Guidelines]] §3).
- Tasa de detección y falsos positivos; el KPI TDP ≥ 75 % (§6.5) no se calcula.
- Intentos de evasión o *bypass*: no hay pruebas. La inyección por DLL o `LD_PRELOAD` sin llamadas al sistema no es observable y `EXEC_MPROTECT` es solo un indicador ([[Claims-Ledger]] fila 14).
- Build de *release* en hardware físico: toda la validación usa build de *testing* en VM porque el de *release* se niega a proteger dentro de una VM ([[Claims-Ledger]] fila 15; R11).
- Latencia de detección de la verificación en espacio de usuario y comportamiento del *watchdog* con captura (sonda inconclusa) ([[Test-Status]]).
- Resultados de la encuesta del Cap. II (instrumento sin aplicar).

## C.4. Limitaciones del resultado

La conclusión es válida para: VM, build de *testing*, kernel de la distribución de referencia en la versión capturada (kernel y distribución de generaciones Fedora distintas, [[Capture-findings-2026-08-29]] §7.5), un juego simulado y un motor real. El diseño no cubre `/proc/<pid>/maps` legible por root, un máximo de 16 procesos protegidos y BPF-LSM *best-effort*: sin `bpf` en `lsm=` queda solo el `kretprobe` ([[Features]] §1.1, §1.5; [[Known-Limitations]]). No hay atestación verificada por servidor: `quark_sdk_is_active()` y similares devuelven valores calculados por el cliente (Update 2026-11-13, E).

## C.5. Sobre el diferencial

El relevamiento muestra que Easy Anti-Cheat para Linux v2 adopta BPF-LSM sin módulo de kernel (información pública secundaria; no observado). El diferencial de Quark pasa de "nativo de kernel" a "abierto, académico y documentado", con la ventaja de bloquear localmente en Ring 0 `ptrace`, `/proc/<pid>/mem` y `process_vm_*`. Esa ventaja se compara contra información pública, no contra el comportamiento medido de EAC (Update 2026-11-13, D–E).

## C.6. Trabajo pendiente

1. Congelar un candidato a versión (`rc-1`) y registrar `git_commit` y `git_branch` en cada captura; decidir las ramas `feature/gameStartProtection` y `dev/docs`.
2. Corregir el harness y re-capturar.
3. Medir el overhead y calcular detección y falsos positivos sobre una lista cerrada de casos (ataque por `/proc/pid/mem`, `ptrace`, `process_vm_*`, carga de BPF, `LD_PRELOAD`, lecturas legítimas como `ps` y `htop`).
4. Probar evasión y el build de *release* en hardware físico.
5. Implementar el SDK de servidor y la prueba cliente↔servidor ([[Features]] §5).
6. Cerrar las 45 afirmaciones abiertas del análisis de EAC/BattlEye (`Validation_Log.md`).

Según la lectura de este borrador, la defensa puede sostener que el prototipo demuestra viabilidad técnica *en el alcance indicado*; no puede sostener bajo overhead, tasas de detección ni resistencia a evasión hasta contar con esas mediciones.

— agent:claude-sonnet-5-5, 2026-11-25
