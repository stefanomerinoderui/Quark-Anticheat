---
title: Registro de riesgos
tags: [proyecto, riesgos]
source: Informe-PIF-Avance §5.7
---

# Registro de riesgos

| ID | Riesgo | Prob. | Impacto | Prioridad | Mitigación / contingencia (resumen) |
|---|---|---|---|---|---|
| R1 | Inestabilidad del módulo (kernel panics) | Alta | Alto | Crítica | Todo en QEMU/KVM; incrementos mínimos; reducir a hooks mínimos si hace falta |
| R2 | Bindings de Rust for Linux inmaduros | Alta | Alto | Crítica | Decidir por componente qué va en Rust y qué en C. **Estado real:** módulo en C, demonio en Rust |
| R3 | Subestimación de esfuerzo del módulo | Media | Alto | Alta | Revisar 99 SP por iteración; alerta si velocidad < 6 SP/sem durante 2 semanas |
| R4 | Incompatibilidad entre versiones de kernel | Media | Medio | Media | Declarar versión mínima. Ver nota de versiones en [[Capture-findings-2026-08-29]] §7.5 |
| R5 | Disponibilidad reducida de un integrante | Media | Alto | Alta | Conocimiento cruzado + reunión semanal; renegociar alcance |
| R6 | Limitaciones del juego open source | Baja | Medio | Media | **Mitigado:** integración con RecoilEngine/BAR lograda |
| R7 | Cambios en interfaces internas del kernel | Baja | Alto | Media | Anclar a versión de kernel |

## Riesgos nuevos observados en el repo (no están en el informe)
- **R8 — Procedencia del build de validación.** Las capturas del 2026-08-29 contienen mensajes que no existen en el código del repo → no se sabe qué revisión se probó. Ver [[Capture-findings-2026-08-29]] §0.
- **R9 — Deriva de repos en la VM** (Nobara a mitad de transición Fedora 43→44) rompe builds. Ver [[VM-test-environment]] §4.
- **R10 — Socket de control sin autenticar** (`SocketMode=0666`, sin `SO_PEERCRED`). Ver [[Known-Limitations]].


## Update 2026-11-11 — agent:claude — alinear con origin/Dev@35c6031

- **REPLACES** — «R10 — Socket de control sin autenticar» → mitigado en Dev ([[Known-Limitations]]). Residual: `SocketMode=0666`.
- **REPLACES** — «R8 — Procedencia del build de validación.» → causa probable identificada (commit `2624ae4`); riesgo residual: no registrar `git_commit` en las capturas ([[Capture-findings-2026-08-29]] Update).
- **REPLACES** — «**Estado real:** módulo en C, demonio en Rust» (R2) → sigue vigente; además BPF-LSM (vía libbpf-rs en el daemon) cubrió lo que se esperaba de LSM/eBPF. Contingencia de R2 ejecutada.
- **ADDED** — **R11 — La validación solo puede hacerse con build *testing*.** El build de release se niega a proteger en una VM. Prob. Alta, Impacto Alto: el tribunal puede preguntar si el producto real fue probado. Mitigación: demo en hardware físico o documentar explícitamente el alcance.
- **ADDED** — **R12 — Documentación contradice al código** (README de Dev aspiracional). Prob. Alta, Impacto Medio. Mitigación: commitear README corregido; claims ledger ([[Working-Guidelines]]).
- **ADDED** — **R13 — Divergencia de ramas:** `main` quedó en el commit del 2026-06-11; `feature/gameStartProtection` sin PR; mis stubs de `docs/` chocarán con `docs/*.md` de Dev al mergear. Prob. Alta, Impacto Medio.
- **ADDED** — **R14 — Overhead CPU/RAM sin medir** y tiempo restante corto (H5 ≈ mediados de noviembre). Prob. Alta, Impacto Alto.
