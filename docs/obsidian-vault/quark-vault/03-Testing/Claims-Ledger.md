---
title: Registro de afirmaciones (claims ledger)
tags: [testing, defensa, ledger]
status: canonical
---

# Claims ledger

Cada afirmación del informe, README o defensa debe tener una fila. Estados: **SUPPORTED** (evidencia citada y reproducible), **DOCUMENTED** (hay texto en el repo pero no lo reverifiqué), **NOT MEASURED**, **CONTRADICTED** (el código dice otra cosa). Agregar filas y estados nuevos **al final** con `## Update` (ver [[Append-Only-Standard]]); no editar estas filas.

## 2026-11-11 — agent:claude — siembra inicial
| # | Afirmación | Estado | Evidencia / acción |
|---|---|---|---|
| 1 | Ring 0 impide la escritura externa vía `/proc/<pid>/mem` | SUPPORTED | [[Capture-findings-2026-08-29]] §2.3 (10/10 en juego mock, build *testing*); [[VM-test-environment]] §7 en motor real |
| 2 | Sin defensa el ataque funciona | SUPPORTED | Capturas §2.1 (5/5) |
| 3 | El bloqueo se debe al módulo, no a Yama | SUPPORTED | Control negativo §2.4 |
| 4 | Funciona sobre un juego real (BAR) | SUPPORTED | [[VM-test-environment]] §6.5, §7 |
| 5 | Detección por polling en ≤50 ms + `kill -9` (Modo A) | DOCUMENTED | Sin captura con marca de tiempo; además ya no es modo autónomo ([[Test-Status]]) |
| 6 | Watchdog del SDK termina el juego si cae el daemon | DOCUMENTED | [[VM-test-environment]] §8; la sonda de captura fue inconclusa |
| 7 | Canal de control autenticado (firma ECDSA, hash de `quark_cli`) | DOCUMENTED | [[Features]] §2, [[VM-test-environment]] §13; reverificar |
| 8 | BPF-LSM bloquea cargas de BPF de tracing y protege al daemon | DOCUMENTED | [[Features]] §1.5, [[VM-test-environment]] §15; reverificar |
| 9 | El build de release se niega a proteger en una VM | DOCUMENTED | [[Features]] §1.2, §12 de la VM doc; reverificar |
| 10 | "Bajo impacto de rendimiento / muy bajo overhead" | NOT MEASURED | Medir CPU/RAM (ver [[Working-Guidelines]] §3) |
| 11 | Tasas de detección y falsos positivos (informe §6.4, KPI TDP ≥75 %) | NOT MEASURED | Definir casos de prueba y contarlos |
| 12 | "Módulo de kernel en Rust" (informe, README de Dev) | CONTRADICTED | El módulo es C (`kernel/quark_kernel.c`) |
| 13 | "Usa el framework LSM" (README de Dev) | CONTRADICTED | LSM clásico imposible fuera del árbol; se usa BPF-LSM + kretprobe ([[Features]] §1.5) |
| 14 | Una DLL/`LD_PRELOAD` inyectada es detectada | NOT MEASURED | Solo hay telemetría `EXEC_MPROTECT` (indicador); sin prueba ([[Known-Limitations]]) |
| 15 | Protección real en producción | NOT MEASURED | Toda la validación es con build *testing* en VM ([[Known-Limitations]] Update) |
