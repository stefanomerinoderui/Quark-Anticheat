---
title: Roadmap e hitos
tags: [proyecto, planificacion]
source: Informe-PIF-Avance §5.1–5.2
---

# Roadmap e hitos

Metodología: modelo en espiral (Boehm) + prácticas SCRUM por iteración ([[Informe-PIF-Avance]] §6.1).

## Etapas
1. **Análisis técnico** (may–jun 2026): APIs del kernel, vectores de trampa, juego de prueba.
2. **Diseño arquitectónico** (jun–jul): hooks, comunicación kernel↔usuario, diagramas.
3. **Desarrollo** (jul–oct): módulo de kernel, demonio, SDK, pruebas en QEMU/KVM.
4. **Validación y soporte** (oct–nov): juego real, tasas de detección, overhead CPU/RAM, documentación y defensa.

## Hitos
| Hito | Descripción | Fecha estimada | Entregable |
|---|---|---|---|
| H1 | Análisis técnico completo | fin jun 2026 | Doc. de diseño preliminar (E1.4) |
| H2 | Arquitectura definida | fin jul 2026 | Diagramas (E2.3) |
| H3 | Módulo de kernel funcional en VM | fin ago 2026 | Módulo estable (E3.1) |
| H4 | Sistema integrado y probado | fin oct 2026 | Suite de pruebas (E3.4) |
| H5 | Validación sobre juego + documentación + defensa | mediados nov 2026 | Informe final y defensa (E4.4) |

Criterios de aprobación H3: carga sin errores en QEMU/KVM, ≥1 evento de supervisión, 0 kernel panics no controlados. H4: ≥75 % de casos aprobados. H5: integración funcionando, documentación completa, defensa en fecha.

## Dónde estamos (según el repo, al 2026-11-11)
- Prevención en Ring 0 (Modo B) validada contra la VM y contra un RecoilEngine/BAR real: [[VM-test-environment]], [[Capture-findings-2026-08-29]].
- Watchdog del SDK, activación por socket systemd e integración con RecoilEngine hechos (commit `6b05ad7`).
- Pendiente para H5: ver [[Test-Status]] (overhead no medido, watchdog sin captura, procedencia del build, defecto del harness) y el [[04-Kanban/Board|tablero]].

> Las fechas de arriba son las del informe; el cronograma real vive en el Kanban (fechas de vencimiento en las tarjetas).


## Update 2026-11-11 — agent:claude — alinear con origin/Dev@35c6031

Estado por hito según el historial de git (no según el cronograma del informe):
- **H3** módulo funcional en VM — cumplido (2026-06-25 kretprobe en Ring 0; validado en VM).
- **H4** sistema integrado y probado — cumplido en lo esencial: motor real (PR #1, 2026-08-28/31), endurecimiento (2026-08-29/31), BPF-LSM/telemetría (PR #2, 2026-10-05).
- **H5** — abierto. Falta: medir overhead, resolver contradicciones doc↔código, decidir sobre `feature/gameStartProtection`, prueba cliente↔servidor (opcional, [[Features]] §5), informe y defensa.
- **REPLACES** — «Pendiente para H5: ver [[Test-Status]] (overhead no medido, watchdog sin captura, procedencia del build, defecto del harness)» → procedencia del build: explicada; el resto sigue pendiente. Plan de cierre: [[Working-Guidelines]].
