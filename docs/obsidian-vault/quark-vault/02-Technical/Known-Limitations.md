---
title: Limitaciones conocidas
tags: [tecnico, limitaciones, riesgos]
source: Funcionamiento-del-codigo §6
---

# Limitaciones conocidas

Resumen; el detalle y las referencias de línea están en [[Funcionamiento-del-codigo]] §6.

- Solo se media lo que cruza al kernel: una DLL/`LD_PRELOAD` inyectada escribe sin syscall → invisible (y en Modo B el daemon tampoco lo ve).
- El watchdog no cubre `SIGSTOP` del daemon (el socket sigue abierto).
- Socket de control sin autenticar (sin `SO_PEERCRED`, `SocketMode=0666`).
- Máximo 16 procesos protegidos (`MAX_PROTECTED_PROCESSES`).
- PIDs resueltos con `task_pid_vnr()`: incorrecto entre namespaces de PID distintos.
- `maxactive = 64` en el kretprobe: bajo carga, fail-open (medir con `nmissed`).
- El juego mock usa `PR_SET_PTRACER_ANY` (amplía la superficie a propósito); el motor real no.
- Modo A y B son mutuamente excluyentes: el módulo bloquea también al daemon.
- LSM y eBPF: trabajo futuro; módulo en Rust (Rust for Linux): trabajo futuro.

Convertir cada ítem en tarjeta Kanban solo si se decide atacarlo antes de la defensa; si no, documentarlo como alcance fuera del MVP.


## Update 2026-11-11 — agent:claude — alinear con origin/Dev@35c6031

Fuentes: [[Features]] (docs/features.md de Dev, v0.4.0 del módulo), [[VM-test-environment]] §11–15, historial de `origin/Dev`. La nota original se escribió contra una copia local atrasada de la rama `BAR-example-test`.

- **REPLACES** — «Socket de control sin autenticar (sin `SO_PEERCRED`, `SocketMode=0666`).» → Dev autentica el canal: pid del cliente vía `SO_PEERCRED` (`main.rs`), Netlink con uid verificado por el kernel, hash SHA-256 del ejecutable de `quark_cli` y comandos firmados ECDSA P-256 con nonce anti-replay ([[Features]] §2; commit `48cc3f6`). `SocketMode=0666` **sigue** en `quark.socket`; la defensa ahora es no confiar en el pid declarado por el cliente.
- **REPLACES** — «Modo A y B son mutuamente excluyentes: el módulo bloquea también al daemon.» → el daemon se registra como `trusted_monitor_pid` (comando 3, firmado) y queda exento del bloqueo; su monitor de variables convive con el kretprobe ([[Features]] §1.1, §2.4; commit `2216684`). Matiz: el SDK ya no arranca sin protección de kernel confirmada, así que el Modo A **ya no existe como modo autónomo** (ver [[Test-Status]]).
- **REPLACES** — «LSM y eBPF: trabajo futuro; módulo en Rust (Rust for Linux): trabajo futuro.» → BPF-LSM y telemetría eBPF están implementados en el daemon (PR #2, `e497dbf`). Un LSM clásico es imposible desde un `.ko` fuera del árbol (`security_add_hooks()` es `__init`), por eso se usa BPF-LSM ([[Features]] §1.5). El módulo sigue en **C**; Rust for Linux sigue siendo trabajo futuro.
- **REPLACES** — «PIDs resueltos con `task_pid_vnr()`» → Dev usa `task_tgid_vnr()` (proceso, no hilo). El problema de namespaces de PID distintos **sigue** (`vnr` es relativo al namespace del llamante). Fuente: `kernel/quark_kernel.c:459-468` en Dev.
- **ADDED** — Las lecturas de solo-lectura (`PTRACE_MODE_READ`) ya no se bloquean: `/proc/<pid>/{maps,environ,auxv}` es legible por root (política del kernel ≥6.x, `may_access_mm()`), lo que expone el layout ASLR. No lo puede anular un módulo ni BPF-LSM ([[Features]] §1.1).
- **ADDED** — Build de **release** se niega a proteger dentro de una VM (CPUID hypervisor bit). Todo lo validado en la VM usa un build *testing* (`is_testing_build=1`); ningún resultado de VM es evidencia de la protección de un build de release ([[Features]] §1.2).
- **ADDED** — BPF-LSM es *best-effort*: si `bpf` no está en `lsm=` (el usuario controla su arranque) el daemon sigue solo con kretprobe; el motor aún solo chequea `quark_sdk_is_active()`, no `bpf_lsm_active` ([[Features]] §3, §5).
- **ADDED** — Mientras hay un proceso protegido fallan `bpftrace`, `perf trace` con BPF y unidades systemd con BPF-LSM ([[Features]] §1.5).
- **ADDED** — No implementado según [[Features]] §5: SDK del lado servidor, prueba cliente↔servidor de punta a punta, política del motor para `bpf_lsm_active`.
- **UNVERIFIED** — Watchdog vs `SIGSTOP` sobre el daemon: no encontré evidencia en Dev de que se haya resuelto. `maxactive = 64` y el techo de 16 PIDs siguen en `kernel/quark_kernel.c:47,510`.
