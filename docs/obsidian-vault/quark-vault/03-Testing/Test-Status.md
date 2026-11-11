---
title: Estado de las pruebas
tags: [testing, estado]
source: Capture-findings-2026-08-29 §7, §9
---

# Estado de las pruebas

## Respaldado por capturas ([[Capture-findings-2026-08-29]] §9)
- Modo B previene el ataque: 10/10 repeticiones, `EACCES` en `open()`, valor del juego intacto (100), más 2 réplicas independientes.
- Control negativo: con el módulo descargado el mismo ataque sobre el mismo PID funciona → el bloqueo es de Quark, no de Yama.
- Sin defensa el ataque funciona: 5/5.
- Validación sobre RecoilEngine/BAR real: [[VM-test-environment]] §7.

## No respaldado (no afirmar en el informe sin nueva evidencia)
- Latencia de detección del Modo A (en las capturas nunca corrió).
- Comportamiento del watchdog (sonda inconclusa).
- Overhead de CPU/RAM (**requerido por el MVP y por H5**).
- Intentos de evasión/bypass.
- Revisión de código probada (el build no coincide con el repo).

## Defectos del harness / hallazgos a resolver ([[Capture-findings-2026-08-29]] §7)
- `results.csv` malformado y `summary.txt` solo reporta la condición B (§7.1).
- Condición A no existe como modo defendido en el binario capturado (§7.2).
- El SDK anuncia fail-closed pero el target sigue vivo (§7.3).
- Target no PIE (§7.4); kernel y distro de generaciones Fedora distintas (§7.5).
- `quark_cli` informa éxito sin confirmación del kernel (§7.6).
- Entorno sin `git_commit`/`git_branch` registrado (§0, §6) — **fijar antes de re-capturar**.

Estas líneas se reflejan como tarjetas en el [[04-Kanban/Board|tablero]].


## Update 2026-11-11 — agent:claude — alinear con origin/Dev@35c6031

Base: [[Features]], [[VM-test-environment]] §11–15 y commits de `origin/Dev`. Lo de Dev lo leí en documentación y commits; **no lo re-ejecuté**.

- **REPLACES** — «Condición A no existe como modo defendido en el binario capturado (§7.2).» → no es un defecto del binario sino diseño: desde `2624ae4` ("refuse to report success until kernel-level protection is confirmed") `quark_sdk_init()` devuelve -1 si el kernel no confirma. El Modo A pasó a ser capa suplementaria ([[Features]] §1.3, §4). Los scripts `run_test.sh`/`capture.sh` que prueban "Modo A solo" miden algo que el producto ya no ofrece.
- **REPLACES** — «Revisión de código probada (el build no coincide con el repo).» → el build **sí** corresponde al historial: las tres cadenas "Refusing to confirm protection…" / "Refusing to continue unprotected." están en el commit `2624ae4` (2026-08-29 00:14 -03:00 = 03:14 UTC) y las capturas corrieron a las 03:33 UTC. Lo más probable es que se capturara con ese commit o un árbol que lo contiene. Sigue **UNVERIFIED** porque `environment.txt` no guardó `git_commit`.
- **ADDED** — Dev documenta pruebas nuevas en [[VM-test-environment]] §11 (ack/nack y "protected match"), §12 (VM-detection, build testing), §13 (canal autenticado), §14 (monitor del daemon), §15 (BPF-LSM/telemetría, incluye `process_vm_*` → EPERM y señales `TASK_KILL`). Resultados por revisar uno a uno antes de citarlos en el informe.
- **ADDED** — Sigue sin medirse el overhead de CPU/RAM: `git grep overhead` en los docs de Dev solo encuentra la afirmación aspiracional («muy bajo overhead») en `contexto_proyecto.md`. Es requisito del MVP (informe §5.9).
- **ADDED** — Rama `feature/gameStartProtection` (sin PR): el juego mock exige BPF-LSM y daemon para arrancar (`69cdab6`, `2b088ab`), más `tooling/install.sh`. Cambia `run_test_no_quark.sh` y `game.c`; el control negativo "sin Quark" dejará de funcionar tal cual si se mergea sin revisar.
- **UNVERIFIED** — Si `results.csv`/`summary.txt` del harness (§7.1) se corrigieron: `capture.sh` no cambió entre mi base y Dev, así que se asume que **no**.
