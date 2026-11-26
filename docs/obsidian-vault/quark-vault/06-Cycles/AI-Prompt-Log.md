---
title: Registro resumido de prompts a agentes de IA
tags: [meta, ia, ledger, agentes]
status: canonical
---

# Registro resumido de prompts a agentes de IA

Ledger **append-only**: una entrada nueva al final por sesión o por pedido relevante. Sirve de base para la declaración de uso de IA del informe (cláusula CAT-IA), porque las sesiones de terminal no tienen enlace compartible.

**Reglas de autodocumentación (agentes y personas)**
- Resumir, no transcribir. Una línea por pedido: qué se pidió y qué resultó.
- Si el prompt es una referencia ("ejecutá el archivo X", "seguí esta nota"), registrar un resumen de las **instrucciones** de X, no solo el nombre, con su ruta y versión (commit).
- Indicar herramienta y modelo, fecha real, sesión (enlace si existe; si no, "sesión de terminal local") y qué archivos produjo.
- Los agentes agregan su entrada al terminar cada tarea; firmar `agent:<modelo>`. Nunca fabricar prompts de sesiones que no se vieron: marcar `UNVERIFIED`.

## 2026-08-27 a 2026-08-31 — Claude Code (web) — desarrollo del prototipo
- Sesión: `https://claude.ai/code/session_01JeTq4KYFDuzr41fQnUoCfQ` (trailer `Claude-Session` en 11 commits de `Dev`, cuenta `Billones142`).
- Pedidos: UNVERIFIED (no se tiene la transcripción). Resultado visible en los commits: autenticación del canal Netlink, rechazo de la protección en VM con omisión de pruebas, watchdog y validación contra el motor real, servicio systemd del módulo, submódulo RecoilEngine.

## 2026-11-25 a 2026-11-26 — Claude Code (terminal) — `agent:claude-sonnet-5-5` — autorrevisión del PIF
Sesión de terminal local, sin enlace compartible.
1. **Ejecutar el handoff del harness.** Se pasó `06-Cycles/Handoff-Harness-2026-11-25.md` y las carpetas del harness y del skill. Instrucciones resumidas del handoff: entregar el informe del vault (todos los capítulos con contenido), reproducir con `sh tooling/build_informe.sh` y `python tooling/check_append_only.py --worktree`, leer el código solo de `Dev@35c6031`, no afirmar lo no medido, declarar los huecos conocidos (INPI, logo, encuesta, ADR-001, licencia) y completar la sección "Ejecución" cuando se tuviera la guía de la cátedra. Resultado: lectura del README y `AGENTS.md` del harness y del skill `corregir-pif-ucp`.
2. **"Autorrevisión completa" en una rama nueva.** Resultado: rama `review/harness-autorevision-2026-11-25`, plan `entregas/quark-anticheat/plan_entregas.json`, Capa 1, 26 hallazgos con Checker y los informes de cumplimiento y devolución.
3. **Commit y push del estado, y mejoras en las fuentes `.md`/`.tex` según el flujo de redacción, incluida la declaración de IA; luego otra pasada del harness leyendo el `.tex`.** Resultado: commits `535885f` y `cbfb87b` (carátula, ids de títulos, anexos "X de Y", Anexo III.5/III.6, Cap. XIII, declaración de IA) y segunda pasada sin ROJO.
4. **Publicar todo, conservar las matrices en git y agregar autodocumentación de prompts.** Resultado: este registro, la regla en `AGENTS.md` y el ajuste de `.gitignore` de `entregas/`.
