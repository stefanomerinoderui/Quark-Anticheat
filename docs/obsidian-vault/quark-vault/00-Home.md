---
title: Quark Anticheat — Home
tags: [home, moc]
---

# Quark Anticheat — Segundo cerebro + Kanban

Anticheat nativo de nivel kernel (Ring 0) para GNU/Linux. PIF de Ingeniería en Sistemas de Información, UCP. Autores: Martínez Alarcón y Merino De Rui.

## Empezar aquí
- Estado actual del trabajo → [[04-Kanban/Board|Tablero Kanban]]
- Qué es y por qué existe → [[Contexto-del-proyecto]] · [[Architecture-Overview]]
- Qué falta y cuándo → [[Roadmap-and-Milestones]] · [[Risk-Register]]
- Qué sabemos que NO funciona o no está probado → [[Known-Limitations]] · [[Test-Status]]
- Cómo usar este vault → [[Vault-Guide]] · [[Trello-Migration-Guide]] · [[Best-Practices-Sources]]

## Mapa del vault
| Carpeta | Contenido |
|---|---|
| `01-Project` | Contexto, README, informe PIF, equipo, roadmap, riesgos, KPIs |
| `02-Technical` | Arquitectura, funcionamiento del código, catálogo de logs, limitaciones |
| `03-Testing` | VM de pruebas, capturas de validación, estado de las pruebas |
| `04-Kanban` | `Board.md` (plugin Kanban) y `cards/` (una nota por tarjeta) |
| `05-Meta` | Guías del vault, migración desde Trello, fuentes de buenas prácticas |
| `Templates` | Plantillas de tarjeta, reunión, decisión (ADR) |

## Documentos técnicos y de proyecto
[[README-del-repo]] · [[Contexto-del-proyecto]] · [[Informe-PIF-Avance]] · [[Funcionamiento-del-codigo]] · [[Log-messages]] · [[VM-test-environment]] · [[Capture-findings-2026-08-29]]

> **Este vault es la fuente de verdad.** `docs/*.md` son stubs que apuntan aquí. Excepciones (`status: snapshot`): README y informe PIF de la raíz. Ver [[Vault-Guide]].


## Update 2026-11-11 — agent:claude — alinear con origin/Dev@35c6031
- Nuevas notas: [[Features]] (qué hace Quark hoy) · [[Append-Only-Standard]] · [[Working-Guidelines]] · [[Process-Recommendation]] · [[Cycle-Log]]
- Las notas técnicas y de pruebas tienen `## Update 2026-11-11` al final: **leerlas hasta el final**.
