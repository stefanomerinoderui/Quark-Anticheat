---
title: Kanban — cómo se usa
tags: [kanban, meta]
---

# Kanban

- Tablero: [[Board]] (requiere el plugin **Kanban** de mgmeyers). Columnas: Backlog → To Do → Doing → Review → Done.
- Las tarjetas **semilla** del tablero se derivaron de los documentos del repo ([[Test-Status]], [[Known-Limitations]]). Al importar Trello ([[Trello-Migration-Guide]]) se reemplaza el tablero.
- Una nota por tarjeta en `cards/` (plantilla: `Templates/Card`) para descripción, checklist y decisiones; evita conflictos de merge en `Board.md`.
- Reglas: WIP máx. 2 tarjetas por persona en *Doing*; toda tarjeta con dueño y criterio de aceptación; mover a *Done* solo con evidencia (log, captura, commit).
