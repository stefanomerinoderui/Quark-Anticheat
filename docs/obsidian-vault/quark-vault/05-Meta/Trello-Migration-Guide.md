---
title: Migrar Trello → Obsidian Kanban
tags: [meta, kanban, trello]
---

# Migrar Trello → Obsidian Kanban

Importante: no hay sincronización bidireccional fiable. Es una **migración única**; después Trello se archiva y el Kanban vive en el vault. Si el equipo necesita seguir con Trello en paralelo, repetir la importación sobrescribe `Board.md`.

## 1. Preparar Obsidian (cada integrante)
1. Abrir `docs/obsidian-vault/quark-vault` como vault.
2. Ajustes → Community plugins → *Turn on community plugins*. Kanban, Obsidian Git y Dataview ya vienen en el repo ([[Vault-Guide]]); no hay que instalar nada.
3. Clonar el repo (git) para compartir.

## 2. Exportar de Trello
En el tablero: menú **⋯ → Print, export, and share → Export as JSON**. Guardar como `board.json` **fuera del repo** (contiene datos de miembros; no commitearlo).

## 3. Convertir
```bash
python3 tooling/trello_to_obsidian.py ~/board.json docs/obsidian-vault/quark-vault/04-Kanban
```
Genera `Board.md` (columnas = listas de Trello, vencimientos como `@{AAAA-MM-DD}`, labels como `#tags`, completadas con `[x]`) y `cards/<título>.md` con descripción, checklists, comentarios, dueños y enlace `source: trello:<url>`. Listas/tarjetas archivadas se omiten (`--include-archived` para incluirlas). Solo usa la librería estándar.

Qué NO se migra: adjuntos, imágenes de portada, votos, automatizaciones Butler. Los adjuntos se descargan a mano a `04-Kanban/attachments/`.

## 4. Verificar
Abrir `Board.md`, comparar conteo de tarjetas por columna con Trello, revisar 3 tarjetas al azar. El script fue probado con un export sintético; **un export real de Trello puede traer campos distintos**: si algo falla, pegar el error y se ajusta.

## 5. Adoptar
- Hacer commit y push; el resto hace pull.
- Archivar el tablero de Trello (no borrarlo hasta confirmar).
- Para evitar conflictos: una persona mueve tarjetas a la vez, o commits pequeños y frecuentes (Obsidian Git cada 5–10 min con pull antes de push). Los conflictos en `Board.md` se resuelven a mano (es texto plano).

## Alternativa para tiempo real
Si necesitan edición simultánea sin git: Obsidian Sync (de pago) o un vault en carpeta compartida (Syncthing). Ambos tienen sus propios riesgos de conflicto con el Kanban.
