---
title: "Funcionamiento del código y guía de pruebas"
tags: [tecnico]
status: canonical
---

# Funcionamiento del Código y Guía de Pruebas

Este documento describe los componentes del prototipo de **Quark Anticheat**, sus dos modos de
protección, el protocolo de comunicación entre ellos y los pasos para compilar, ejecutar y
validar el sistema.

---

## 1. Componentes

| Componente | Lenguaje | Ubicación | Rol |
|---|---|---|---|
| Módulo de kernel | C | `kernel/quark_kernel.c` | Deniega en Ring 0 el acceso externo a la memoria de los procesos protegidos. |
| Demonio | Rust | `quark_daemon/src/main.rs` | Registra el juego, ordena la protección al kernel y (en modo userspace) verifica la coherencia de las variables. |
| Cliente netlink | C | `quark_daemon/quark_cli.c` | Binario auxiliar que traduce órdenes del demonio a mensajes netlink. |
| SDK | C | `sdk/quark_sdk.{c,h}` | Biblioteca que el videojuego enlaza para registrar variables y notificar cambios legítimos. |
| Videojuego *mock* | C | `game_target/game.c` | Objetivo de prueba. Registra `health` y `score`. |
| Cheat | C | `cheat/cheat.c` | Atacante. Abre `/proc/<PID>/mem` y sobrescribe una dirección. |

---

## 2. Los dos modos de protección

El prototipo implementa **dos mecanismos de defensa independientes**. Es importante
distinguirlos porque **no operan simultáneamente**: cuando el módulo de kernel está cargado,
inhabilita al propio demonio.

### 2.1. Modo A — Verificación en espacio de usuario (detección reactiva)

Sin el módulo de kernel cargado. El SDK informa al demonio cada cambio legítimo de una
variable registrada. En paralelo, un hilo del demonio abre `/proc/<PID>/mem` del juego y
relee las direcciones registradas cada 50 ms (`main.rs:269`), comparando el valor real
contra el último valor legítimo conocido.

* **Detecta** cualquier escritura externa a una variable registrada, venga de donde venga.
* **No la impide:** la escritura del cheat tiene éxito. La mitigación es *a posteriori*
  (`kill -9` sobre el juego, `main.rs:296`).
* Es un mecanismo de **muestreo**: una modificación que se revierta dentro de la ventana de
  50 ms puede pasar inadvertida.

### 2.2. Modo B — Mediación en el kernel (prevención)

Con `kernel/quark_kernel.ko` cargado. El módulo instala un **kretprobe** sobre
`ptrace_may_access()` (`quark_kernel.c:191`). Cuando el cheat llama a
`open("/proc/<PID>/mem")`, el kernel evalúa esa función; el manejador de retorno del kretprobe
comprueba si el PID objetivo está en la lista de protegidos y si el llamador es un proceso
distinto. Si ambas condiciones se cumplen, sobrescribe el valor de retorno con `false`
(`regs->ax = 0`, `quark_kernel.c:129`), y el kernel traduce ese rechazo en un fallo del
`open()` con `EACCES` ("Permission denied").

* **Impide** la escritura: nunca llega a producirse.
* Es **preventivo y no muestreado**: no depende de detectar el cambio después.
* Solo cubre accesos que **cruzan la frontera del kernel** (véase la sección 6).

> **Nota importante sobre la exclusión mutua.** El módulo no distingue al demonio de un
> atacante: el hilo de verificación del demonio también es un proceso externo intentando abrir
> `/proc/<PID>/mem`, de modo que el kernel también le deniega el acceso. En modo B el mensaje
> `[QUARK-MONITOR] Warning: Could not open /proc/<PID>/mem` es **el comportamiento esperado y
> correcto** (véase `log_messages.md`), y el Modo A queda inactivo. La protección la ejerce
> íntegramente el kernel.

### 2.3. Watchdog del SDK (fail-closed)

`quark_sdk_init()` lanza un hilo que comprueba una vez por segundo que la conexión con el
demonio sigue viva (`quark_sdk.c:52-98`). Si el demonio se cierra o muere, el juego se
autotermina con `_exit(137)` (`quark_sdk.c:95`), en lugar de continuar sin supervisión.

---

## 3. Protocolo de comunicación (IPC)

### 3.1. SDK y demonio: Unix Domain Socket (`/tmp/quark.sock`)

Cada mensaje consta de un encabezado de 8 bytes seguido de un payload variable:

1. `command` (4 bytes, `u32`, orden de bytes nativo)
2. `payload_len` (4 bytes, `u32`, orden de bytes nativo)
3. `payload` (`payload_len` bytes)

| Comando | Código | Payload |
|---|---|---|
| `CMD_REGISTER_GAME` | 1 | `pid` (4 B, `i32`) |
| `CMD_REGISTER_VAR` | 2 | `address` (8 B, `u64`), `size` (4 B, `u32`), `name` (32 B, string rellenada con ceros) |
| `CMD_UPDATE_VAR` | 3 | `address` (8 B, `u64`), `new_value` (8 B, `u64`) |

Como `address` se transmite como puntero en tiempo de ejecución obtenido por el propio juego,
el diseño es **indiferente a ASLR**: no hay direcciones fijadas de antemano.

### 3.2. Demonio y módulo de kernel: Netlink (protocolo 31)

Al recibir `CMD_REGISTER_GAME`, el demonio invoca `quark_cli` (`main.rs:117`), que envía un
mensaje netlink donde el `nlmsg_type` codifica la orden (1 = proteger PID) y el payload lleva
el PID. El módulo añade ese PID a su lista de procesos protegidos.

---

## 4. Compilación

```bash
make            # demonio (cargo), quark_cli, juego + SDK, cheat
make -C kernel  # módulo de kernel (requiere kernel-devel)
make clean
```

`make` produce:

1. `quark_daemon/target/release/quark_daemon`
2. `quark_daemon/quark_cli`
3. `game_target/game`
4. `cheat/cheat`

`make -C kernel` produce `kernel/quark_kernel.ko`.

---

## 5. Pruebas automatizadas

Los tres escenarios están automatizados como scripts en la raíz del repositorio. Son la vía
recomendada; la sección 7 describe el procedimiento manual equivalente.

### 5.1. `./run_test_no_quark.sh` — control negativo (el ataque funciona)

Arranca el juego sin demonio ni módulo, extrae la dirección de `health`, ejecuta el cheat y
comprueba que el juego **sigue vivo** con `health = 9999`. Establece que el vector de ataque
es real.

### 5.2. `./run_test.sh` — Modo A (detección en espacio de usuario)

Arranca demonio y juego, ejecuta el cheat y comprueba que el juego fue terminado con `SIGKILL`.
La escritura del cheat **tiene éxito**; lo que se demuestra es la detección y la mitigación
posterior.

### 5.3. `./run_test_kernel.sh` — Modo B (prevención en Ring 0)

Requiere `sudo` y cabeceras del kernel. Secuencia:

1. Compila espacio de usuario y módulo.
2. `sudo insmod kernel/quark_kernel.ko`.
3. Arranca el demonio.
4. Arranca el juego; al registrarse, el demonio ordena al kernel proteger su PID vía `quark_cli`.
5. Ejecuta el cheat contra la dirección de `health`.
6. **El kretprobe deniega el `open()`**; el cheat falla con `Permission denied`.
7. Verifica que el juego sigue ejecutándose y que `health` permanece en `100`.
8. `sudo rmmod quark_kernel` y vuelca las alertas de `dmesg`.

Ejecutar los tres en orden (5.1, luego 5.2, luego 5.3) constituye la validación completa: ataque exitoso
sin protección, detectado en Modo A, impedido en Modo B. El paso `rmmod` del final de 5.3 sirve
además como control negativo del propio módulo.

> Estos scripts modifican el estado del sistema (cargan módulos de kernel, envían `SIGKILL`).
> Ejecútalos en la máquina virtual de pruebas, no en un equipo de trabajo.

---

## 6. Alcance y limitaciones conocidas

Se documentan explícitamente porque delimitan qué demuestra el prototipo y qué no.

* **Solo se media el acceso que cruza al kernel.** El kretprobe intercepta `ptrace_may_access()`,
  que se evalúa en `open("/proc/<PID>/mem")`, `ptrace` y `process_vm_writev`. Una biblioteca
  compartida inyectada en el espacio de direcciones del juego (vía `LD_PRELOAD`, `ptrace`
  previo a la protección, o un mod cargado por el propio motor) puede escribir la variable con
  una instrucción de almacenamiento ordinaria, **sin syscall alguna**. Ese vector no es
  observable por este mecanismo, y en Modo B tampoco por el demonio, cuyo hilo de verificación
  está bloqueado por el propio módulo.
* **El watchdog no cubre `SIGSTOP`.** Detecta la desaparición del demonio (cierre del socket),
  pero un demonio detenido con `SIGSTOP` mantiene el socket abierto: `poll()` no devuelve
  `POLLHUP` ni datos, ninguna de las dos ramas de desconexión se dispara y el juego continúa
  sin supervisión efectiva.
* **El socket de control no está autenticado.** El demonio acepta el PID que le envía el cliente
  (`main.rs:112`) sin verificarlo contra `SO_PEERCRED`, y la unidad systemd expone el socket con
  `SocketMode=0666`. Cualquier proceso local puede registrar un PID arbitrario.
* **Techo de 16 procesos protegidos** (`MAX_PROTECTED_PROCESSES`, `quark_kernel.c:26`).
* **Espacios de nombres de PID.** El módulo resuelve PIDs con `task_pid_vnr()`, relativo al
  espacio de nombres del llamante; la protección no es correcta si el juego y el atacante viven
  en espacios de nombres distintos.
* **`maxactive = 64`** (`quark_kernel.c:140`): si se agotan las instancias de kretprobe bajo
  carga, las llamadas no interceptadas pasan sin mediación (*fail-open*). El contador `nmissed`
  del probe permite cuantificarlo.
* **El juego *mock* invoca `prctl(PR_SET_PTRACER, PR_SET_PTRACER_ANY)`** (`game.c:31`) para que
  el ataque sea reproducible sin `root` bajo Yama `ptrace_scope = 1`. Esto **amplía
  deliberadamente** la superficie de ataque del objetivo de prueba y no formaría parte de un
  despliegue real. El motor RecoilEngine integrado no hace esta llamada.

---

## 7. Procedimiento manual (tres terminales)

Equivalente a la sección 5.2, útil para observar el flujo interactivamente.

**Terminal 1 — demonio:**
```bash
./quark_daemon/target/release/quark_daemon
```

**Terminal 2 — juego:**
```bash
./game_target/game
```
Imprime su PID y las direcciones virtuales de `health` y `score`. Las teclas `h` (recibir daño),
`s` (sumar score) y `p` (imprimir estado) generan cambios legítimos, que el SDK notifica y el
demonio acepta sin alertar.

**Terminal 3 — ataque:**
```bash
./cheat/cheat <PID> <HEALTH_ADDRESS> <NEW_VALUE>
# ej.: ./cheat/cheat 12345 0x55555555c010 9999
```

Resultado esperado en Modo A: el cheat informa `SUCCESS! Wrote 4 bytes.`, y en menos de ~50 ms
el demonio emite la alerta y termina el juego:

```text
==================================================
⚡⚡ [QUARK ALERT] TAMPERING DETECTED! ⚡⚡
Variable Name:   health
Memory Address:  0x55555555C010
Expected Value:  80
Actual Value:    9999
==================================================
[QUARK ACTION] Terminating target process 12345 immediately...
```

La Terminal 2 muestra `Killed`.

Para el Modo B, cargar el módulo antes de arrancar el demonio; el cheat fallará con
`Permission denied` y el juego no será terminado.

---

## 8. Validación sobre un motor real

La integración con **RecoilEngine / Beyond All Reason** y su ejecución en la máquina virtual de
pruebas están documentadas por separado en [[VM-test-environment]],
que recoge versiones exactas, recursos de la VM, el parche aplicado al motor y el registro de
las pruebas de bloqueo y del watchdog.

El catálogo de mensajes de log de todos los componentes está en
[[Log-messages]].


## Update 2026-11-11 — agent:claude — alinear con origin/Dev@35c6031

Este documento describe el estado de `BAR-example-test`. Para el código vigente leer [[Features]]. Cambios que invalidan texto de arriba:

- **REPLACES** — «cuando el módulo de kernel está cargado, inhabilita al propio demonio» (§2) y la «Nota importante sobre la exclusión mutua» (§2.2) → el daemon es `trusted_monitor_pid`; el mensaje `[QUARK-MONITOR] Warning: Could not open /proc/<PID>/mem` ya **no** es el comportamiento esperado en Modo B (fue el bug de [[VM-test-environment]] §14).
- **REPLACES** — «El socket de control no está autenticado.» (§6) → ver [[Known-Limitations]] Update 2026-11-11.
- **REPLACES** — «`ptrace` ... `EACCES`» en 2.2 → se deniegan solo accesos *attach*; lectura de `maps/environ` pasa.
- **REPLACES** — «`quark_cli` ... `nlmsg_type` codifica la orden (1 = proteger PID)» (§3.2) → los comandos 1/2/3 llevan `nonce` y firma ECDSA; ver [[Features]] §2.3.
- **ADDED** — Ejecutar con `make lint` (clang-tidy estricto, reglas en `.agents/AGENTS.md` de Dev) y `run_test_kernel_release.sh` para el build de release.
