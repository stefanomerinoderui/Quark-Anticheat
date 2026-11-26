---
title: Guía del vault
tags: [meta]
---

# Guía del vault

## Dónde vive y cómo se comparte
El vault está en `docs/obsidian-vault/quark-vault` dentro del repo → se comparte con **git**. Los plugins vienen **dentro del repo** (`.obsidian/plugins/`), con versiones fijadas, así que todos usan lo mismo sin instalar nada. `.gitignore` del vault excluye `workspace.json` y los `data.json` de plugins (estado personal).

| Plugin | Versión fijada |
|---|---|
| Kanban (mgmeyers) | 2.0.51 |
| Obsidian Git (Vinzent03) | 2.43.0 |
| Dataview (blacksmithgu) | 0.5.70 (su `manifest.json` aún dice 0.5.68) |

**Primera vez de cada persona (no se puede versionar):** abrir el vault → Ajustes → Community plugins → *Turn on community plugins*. El interruptor de "Restricted mode" es estado local de cada instalación. Los tres plugins ya figuran en `community-plugins.json`. Configurar Obsidian Git a mano (ver abajo), porque su `data.json` es personal.

**Actualizar un plugin:** una sola persona descarga la release nueva en `.obsidian/plugins/<id>/` (`main.js`, `manifest.json`, `styles.css`), actualiza la tabla de arriba y hace commit. Los plugins ejecutan código con acceso a tus notas: no actualizar desde fuentes que no sean el release oficial de cada repo.

**Obsidian Git:** el vault es un subdirectorio del repo; si el plugin no detecta la raíz git, revisar Ajustes → Obsidian Git → *Custom base path*. Sugerido: auto commit-and-sync cada 10 min, *pull on startup*.

## Fuente de verdad
**El vault es canónico.** Los `docs/*.md` son stubs que apuntan al vault: editar siempre allí. Excepciones, ambas de cara al exterior: `README.md` de la raíz (portada de GitHub) y el informe PIF de la raíz (entregable); sus copias en el vault tienen `status: snapshot`.

## Convenciones
- Nombres de archivo sin espacios, `Kebab-Case`; una idea por nota; enlaces `[[wikilink]]`.
- Frontmatter mínimo: `title`, `tags`, `source` (si es derivada). Tarjetas: ver `Templates/Card`.
- Labels de tarjeta: `owner/…`, `H1`–`H5`, `bug`, `docs`, `testing`, `kernel`, `daemon`, `sdk`.
- Decisiones importantes → ADR con `Templates/Decision-ADR`; reuniones → `Templates/Meeting`.
- Todo hecho técnico cita su fuente (archivo:línea o captura). Lo no medido se dice como no medido ([[Test-Status]]).

## Plugins recomendados
Kanban (mgmeyers), Obsidian Git, Dataview (consultas sobre frontmatter: tareas por dueño, velocidad), Templater o plantillas core, Tasks (opcional).

Ejemplo Dataview, tarjetas abiertas por dueño:
````
```dataview
TABLE status, due, story-points FROM "04-Kanban/cards"
WHERE status != "Done" SORT due ASC
```
````


## Update 2026-11-11 — agent:claude — estándar append-only y ciclos
- **ADDED** — Regla de escritura del vault: [[Append-Only-Standard]]. Hook: `git config core.hooksPath .githooks`; chequeo manual: `python3 tooling/check_append_only.py`. Instrucciones para agentes: `AGENTS.md` y `CLAUDE.md` en la raíz.
- **ADDED** — Carpeta `06-Cycles/` ([[Cycle-Log]]), plantilla `Templates/Cycle`, y notas [[Working-Guidelines]], [[Process-Recommendation]], [[Claims-Ledger]].
- **REPLACES** — «Dos copias editadas a mano divergen.» sigue siendo cierto; ahora además: lo importado de Dev entra siempre como `## Update`, nunca reescribiendo notas.
