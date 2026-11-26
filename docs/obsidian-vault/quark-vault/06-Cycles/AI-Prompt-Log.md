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
5. **Entradas de bitácora de agosto a noviembre.** Se pidió generar entradas fechadas por trabajo realizado, a partir de los commits propios que no estaban en `Bitacora_GabrielMartinezA.md`, imitando el tono, estilo y extensión de ese archivo. Resultado: `06-Cycles/Bitacora-GabrielMartinezA-entradas-2026-08-a-11.md`.

## 2026-11-26 — Claude Code (terminal) — `agent:claude-sonnet-5-5` — handoff del plan a largo plazo
Sesión de terminal local, sin enlace compartible. Es la continuación de la sesión del 2026-11-25 (plan inmediato, integración de capítulos, handoff del harness); solo se resumen los pedidos que esa sesión vio.
1. **Plan inmediato y relevamiento (2026-11-25).** Se pidió medir el estado de módulos y capítulos y armar el plan de un día con agentes. Resultado: `06-Cycles/Plan-Inmediato-2026-11-25.md`, borradores en `01-Project/draft/` e integración en `Informe-PIF-Avance.md`.
2. **Integración con decisiones del autor, GPLv3 e INPI.** Resultado: capítulos integrados, `LICENSE`, Cap. VIII con las búsquedas "quark" y "quark anticheat", commits y push a `dev/docs`.
3. **Handoff del harness.** Se pegó la introducción de la guía de la cátedra. Resultado: `06-Cycles/Handoff-Harness-2026-11-25.md`.
4. **Handoff del plan a largo plazo.** Se pidió un handoff específico para redactar ese plan. Resultado: `06-Cycles/Handoff-Plan-Largo-Plazo-2026-11-26.md` (pedido, restricciones, 14 observaciones del harness como backlog, insumos y preguntas abiertas). No incluye el plan en sí.

## 2026-11-26 — Claude Code (terminal) — `agent:claude-opus-5-5` / `agent:claude-sonnet-5-5` — paquetes pacman y repositorio firmado
Sesión de terminal local, sin enlace compartible.
1. **Planificar desde `TODO.md` el GitHub Action que genera un paquete pacman instalable.** Sub-ítems del TODO: firma con una clave privada guardada como secreto del repositorio, repositorio pacman publicado con GitHub Pages y análisis de si conviene separar demonio, módulo (DKMS) y SDK. Resultado: plan aprobado (paquetes separados, publicación sólo en tags `v*`).
2. **Crear una rama nueva desde `main` actualizado antes de implementar.** Resultado: rama `feat/arch-packaging` desde `origin/main@18fdc01`. El plan se revisó contra el código nuevo: el módulo ahora compila (kretprobes) y la SDK exige confirmación de Ring 0, así que DKMS pasó a incluirse. El autor decidió usar una clave de firma por máquina generada por DKMS y rutas FHS configurables al compilar.
3. **Implementación.** Resultado: `packaging/arch/` (PKGBUILD dividido, `build-packages.sh`, `publish-repo.sh`, unidad systemd, `.install`), `packaging/dkms/` (`dkms.conf` y script PRE_BUILD que genera la clave y los headers), `.github/workflows/arch-packages.yml`, `make sdk` (`libquark_sdk.so`), rutas configurables en `quark_cli.c` (`QUARK_SIGNING_KEY_PATH`) y en el demonio (`QUARK_CLI_PATH`, sin `sudo` cuando ya corre como root), README y `TODO.md`. Verificado en un contenedor `archlinux:base-devel`: compilación de los paquetes, compilación DKMS contra `linux-headers` 7.3.6 (el `.ko` embebe el hash del `quark_cli` instalado y la clave pública de la máquina), instalación desde el repositorio firmado con `SigLevel = Required` y rechazo de un paquete alterado. No verificado todavía: la ejecución en GitHub Actions y la carga del módulo en un kernel real.
4. **Mover el socket y explicar la configuración de secretos y variables del repositorio.** Resultado: `/tmp/quark.sock` → `/run/quark/quark.sock` en la SDK, el demonio (crea el directorio y deja el socket en 0666 cuando no hay socket activation), `quark.socket`, el Makefile y los scripts de prueba (crean `/run/quark` con `sudo install -d`); documentación vigente actualizada y nota `## Update` en `VM-test-environment.md`. Verificado en contenedor: demonio como root en el nuevo camino y juego como `nobody` conectándose. Pendiente: re-sincronizar la copia de la SDK en RecoilEngine. Tutorial de secretos y variables entregado en la conversación.
