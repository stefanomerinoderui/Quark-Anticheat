---
title: Bitácora de ciclos
tags: [ciclos, proceso, ledger]
status: canonical
---

# Bitácora de ciclos (ledger, append-only)

Una entrada por iteración, con `Templates/Cycle`. Estándar: [[Append-Only-Standard]]. Proceso elegido: [[Process-Recommendation]].

## 2026-11-11 — agent:claude — RECONSTRUCCIÓN desde git (no es registro contemporáneo)

> Esta entrada reconstruye C1–C6 mirando `git log --all` y los PR de GitHub el 2026-11-11. Las fechas son de los commits. Los objetivos y riesgos son **interpretación** mía a partir de los mensajes y los documentos; el equipo debe confirmarlos con un `## Update`. Ninguna parte debe presentarse como análisis hecho en su momento.

| Ciclo | Fechas | Prototipo resultante | Riesgo que parece atacar | Evidencia |
|---|---|---|---|---|
| C1 | 2026-06-11 | Juego mock + SDK + demonio con verificación en userspace (polling 50 ms + `kill -9`) y primer módulo de kernel (198 líneas); informe PIF | Viabilidad de detectar escrituras externas | `9b9aa22` |
| C2 | 2026-06-25 | Prevención en Ring 0: kretprobe sobre `ptrace_may_access` + Netlink + `quark_cli`; `run_test_kernel.sh` | R1, R2 (se usa C, no Rust) | `174e467` |
| C2b (paralelo) | 2026-06-25/26 | Linter y banderas de compilación | calidad de código en kernel | `a5e636a`, `4c99f00`, `8116604` |
| — | 2026-06-26 → 08-27 | **Sin commits.** Motivo desconocido | — | UNVERIFIED: revisar Trello / registros semanales |
| C3 | 2026-08-27/28 (PR #1 mergeado 08-31) | Integración con RecoilEngine / Beyond All Reason real, watchdog, activación por socket systemd, submódulo fijado, `capture.sh` | R6 (juego real) | `6b05ad7`, `be83f67`, `74e7af1`, `d15a37c`, `af7e17f` |
| C4 | 2026-08-29 → 08-31 | Endurecimiento: no reportar éxito sin confirmación del kernel, detección de VM + build *testing* + atestación, canal autenticado (firma ECDSA), monitor de confianza | R1, riesgo de bypass local | `2624ae4`, `333bbe2`, `48cc3f6`, `2216684`, `462d536`; bug de origen en [[VM-test-environment]] §11 |
| C5 | 2026-09-30, 2026-10-05 (PR #2) | BPF-LSM + telemetría eBPF; documentación de features | R2 (LSM/eBPF vía alternativa viable) | `40a788a`, `e497dbf`, [[Features]] |
| C6 | 2026-11-05/06 (PR #3 + rama sin PR) | clang-tidy estricto; instalador; el juego mock exige daemon y BPF-LSM | calidad y reproducibilidad | `e364434`..`35c6031`; rama `feature/gameStartProtection` |

**Lazo de retroalimentación observable:** el hallazgo en la VM de que Cheat Engine leía memoria sin error tras un reinicio sin módulo cargado ([[VM-test-environment]] §11) produjo `2624ae4` (fail-closed) y luego §12–§14. Ojo: `2624ae4` es **anterior** (03:14 UTC) a las capturas formales del 2026-08-29 (03:33 UTC), así que esas capturas **no** causaron ese arreglo.

**Corrección a un análisis previo (agent:claude, 2026-11-11):** en la conversación del mismo día se dijo que el documento de capturas llevó al arreglo `2624ae4`; la cronología anterior muestra que no.

**Lo que NO muestra el historial:** análisis de riesgo escrito por ciclo, planificación del ciclo siguiente, sprints, velocidad. Ver [[Process-Recommendation]].
