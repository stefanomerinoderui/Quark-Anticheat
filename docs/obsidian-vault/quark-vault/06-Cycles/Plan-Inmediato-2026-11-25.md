---
title: Plan de acción inmediata — entrega 2026-11-25/26
tags: [plan, entrega, informe, mvp]
source: relevamiento de estado 2026-11-25 sobre origin/Dev@35c6031 y Informe-PIF-Avance
---

# Plan de acción inmediata (1 día)

Autor: agent:claude-sonnet-5-5 · 2026-11-25. Los porcentajes son **estimaciones por juicio, UNVERIFIED**; sirven de referencia de trabajo restante para el tutor y **no van en el informe**.

## Objetivo de la entrega
1. MVP congelado tal como está (sin desarrollo nuevo).
2. Informe en paridad con el código actual, con **todos** los capítulos iniciados (borrador/avance real, sin inventar datos).
3. Plan a largo plazo hasta febrero (turno posterior).

## Equipo
- Gabriel Sebastián Martinez Alarcón — defiende en febrero.
- Stefano Nahuel Merino De Rui — colaborador; presenta más adelante (adeuda materias).
- Cátedra: Ing. Sergio Lapertosa, Ing. Augusto Portillo, Ing. Martin Jones.
- Marca: Quark Anticheat. Logo: no existe aún. Contactos externos: no se toman por ahora (no hay tiempo para esperar respuestas).

## Estado de módulos (~70 % del MVP)
- Módulo de kernel ~85 %: `kretprobe` Ring 0, canal Netlink firmado, fallo cerrado. Falta: namespaces de PID, `maxactive`, build release en hardware físico. Está en C (Rust descartado por R2).
- Demonio + eBPF/BPF-LSM ~85 %: falta caso `SIGSTOP`, política del motor sobre `bpf_lsm_active`.
- SDK ~80 %: falta SDK de servidor y prueba cliente↔servidor.
- Integración RecoilEngine/BAR ~75 %.
- Validación ~40 %: 10/10 en VM (build testing); falta overhead, tasa de detección/falsos positivos, evasión; harness con defectos.
- Gestión del repo ~60 %: `main` atrasada al 2026-11-25 (el 2026-11-26 ya integra `Dev@35c6031`); `feature/gameStartProtection` sin integrar.

## Estado de capítulos (~60 %)
- Desarrollados: I, III, V, VI, X, XIII, Resumen, Bibliografía, Anexo II.
- Parciales: II, IV, IX. Placeholder: VII, VIII, XI, XII, Conclusiones, Anexo I, Anexo III.
- Desfasados respecto del código: Resumen y Cap. X ("Rust principal"); el Update 2026-11-13 está al final, no integrado.

## Congelamiento del MVP (solo lectura, sin desarrollar)
Últimos commits por rama remota (2026-11-25): `Dev` 35c6031 (2026-11-05); `feature/gameStartProtection` 2b088ab (2026-11-06, sin PR, invalida el control negativo "sin Quark"); `feat/bpf-lsm-telemetry` e497dbf e `dev/linter` 8116604 (ya integradas en `Dev`); `dev/docs` 7604129 (2026-11-14); `main` 989693f (atrasada). Estado a describir: **`Dev@35c6031`**, mencionando `gameStartProtection` como trabajo adicional sin integrar. Worktrees de lectura: `../quark-wt/Dev`, `../quark-wt/gameStartProtection`.

## Fase 1 — agentes en paralelo
Borradores en `01-Project/draft/<capítulo>.md`, sin tocar `Informe-PIF-Avance.md`. Cada uno: impersonal, presente afirmativo (Art. 21); cada afirmación con fuente (`archivo:línea`, commit o cita APA) o marcada UNVERIFIED; **nunca inventar datos**; lo que debe aportar una persona va como "pendiente de aportar".

1. Cap. II + Anexo I (mercado; la encuesta se documenta como instrumento diseñado, sin resultados).
2. Cap. IV + XI (competencia, CANVAS, oportunidades).
3. Cap. VII + VIII (marketing comunitario; marca, clases, licencia; búsqueda INPI pendiente de persona).
4. Cap. XII + Conclusiones.
5. Cap. IX (diseño real desde `Dev`).
6. Paridad: lista de contradicciones del Resumen, Cap. I, III, V, VI, X y XIII frente a `Dev`, con propuesta de redacción + Anexo III.

## Fase 2 — datos de personas
Ya aportados: equipo, cátedra, marca, instrumento de encuesta. Pendientes humanos: búsqueda INPI, logo, publicar la encuesta, tag del MVP.

## Fase 3 — integración y entrega
Fusionar borradores en el informe (o `Informe-PIF-v2`), `grep "A completar\|Pendiente"`, `sh tooling/build_informe.sh`, `python tooling/check_append_only.py --worktree`, revisar Art. 20 y 21.
