---
title: Handoff para el harness de revisión de PIF
tags: [handoff, entrega, harness]
source: sesión 2026-11-25 (Plan-Inmediato-2026-11-25) y commits de dev/docs
---

# Handoff — entrega PIF Quark Anticheat para el harness de revisión

Autor: agent:claude-sonnet-5-5 · 2026-11-25. Para quien ejecute el harness (agente o persona) sin haber visto la sesión.

## Introducción (FYI de la cátedra)

El harness lo presentó el Ing. Sergio Lapertosa el 2026-11-19 ("Harness de Revisión de PIF — Guía de funcionamiento y uso"). Según su introducción: es un entorno local que revisa cada entrega del PIF contra la normativa vigente y deja cada hallazgo con evidencia verificable; combina scripts que miden lo objetivo con un agente de código (Claude Code) que evalúa ítem por ítem; produce un **informe para la cátedra** y una **devolución para los estudiantes**; cada observación cita la página del PDF o la línea del repositorio. Esta nota **no describe cómo se ejecuta** porque el resto de la guía no se recibió: completar la sección "Ejecución" con ella.

## Qué se entrega

| Pieza | Dónde | Estado |
|---|---|---|
| Informe (fuente única) | `docs/obsidian-vault/quark-vault/01-Project/Informe-PIF-Avance.md` | Todos los capítulos con contenido; ver "Huecos declarados" |
| PDF/LaTeX del informe | `build/Informe-PIF-2026-11-25.pdf` (+ `.tex`), generado con `sh tooling/build_informe.sh` | `build/` no está versionado: regenerar. 189 páginas en la última medición del agente de integración; no se re-contó tras el último cambio (Cap. VIII 8.3) |
| Código del MVP | rama `origin/Dev`, commit **`35c6031`** (2026-11-05) | Congelado, sin desarrollo nuevo |
| Trabajo no integrado | `origin/feature/gameStartProtection` `2b088ab` (2026-11-06) | Sin PR; invalida el control negativo "sin Quark" tal cual |
| Docs / vault / licencia | rama `dev/docs`, remoto `https://github.com/stefanomerinoderui/Quark-Anticheat.git` | Último push `b3096e7` |
| Investigación de anticheats | `proton-anticheats/` (copia sin `.git`; último commit citado `cc5078e` según el vault) | URL remota sin verificar |
| Motor de prueba | submódulo `RecoilEngine` (`Billones142/RecoilEngine`, pin `29e5b0b` según `.gitmodules`) | Vacío en los worktrees; no revisado |
| Reglamento | `docs/RR-97-23-Reglamento-de-Proyecto-Integrador-Final.md` | Transcripción limpiada a mano por el autor |

Commits de esta entrega en `dev/docs` (más reciente primero): `b3096e7` INPI "quark anticheat"; `82f0e4d` LICENSE GPLv3 + INPI "quark"; `c9f80c2` limpieza del Reglamento; `b3fe99a` integración de capítulos.

Equipo: Gabriel Sebastián Martinez Alarcón (autor; **único que presenta y defiende**) y Stefano Nahuel Merino De Rui (colaborador con atribución; no defiende). Cátedra: Ing. Sergio Lapertosa, Ing. Augusto Portillo, Ing. Martin Jones. La defensa es en febrero; el Reglamento no fija año y el informe dice solo "febrero".

## Cómo reproducir y verificar (lo que ya se corrió)

Desde la raíz del repo, rama `dev/docs`:
- `sh tooling/build_informe.sh` → `OK build/Informe-PIF-2026-11-25.pdf` (pandoc + tectonic; avisos de TeX por cajas anchas/angostas y `Object @page.1 already defined`, sin errores).
- `python tooling/check_append_only.py --worktree` → `append-only check: ok`.
- `grep -n "A completar\|Pendiente" docs/obsidian-vault/quark-vault/01-Project/Informe-PIF-Avance.md` → una coincidencia legítima (línea ~1596, dentro del Update 2026-11-13 que se conservó).
- Tamaño de código: `python tooling/sloc.py <ruta al worktree de Dev>` → 2.762 SLOC con pruebas, 1.977 solo producto (Cap. V 5.6, Anexo II).
- Gráficos: `tooling/grafico_steam_so.py`, `tooling/grafico_steam_idiomas.py` sobre `docs/steam-historic-hardware-survey-os.tsv` y `...-survey.tsv` (idiomas); salida en `docs/figuras/`.

**No se ejecutó nunca en esta sesión:** el módulo, el demonio, el SDK, las pruebas de la VM ni ninguna medición. Todo lo dicho del código se leyó de `Dev@35c6031` (`../quark-wt/Dev`, worktree de lectura) y de la documentación del repo. Para citar líneas hay que usar ese commit, no la rama local `dev/docs` (no contiene el código del MVP).

## Decisiones del autor que el informe aplica

Entorno de pruebas vigente: Nobara 43 (CachyOS solo como propuesta futura) · licencia GNU GPLv3 para todo el proyecto (archivo `LICENSE` en `dev/docs`; no está en `Dev`) · proceso: prototipado evolutivo guiado por riesgo (ADR-001; **sigue "proposed"** en la zona de evidencia, falta su línea de aceptación) · ante conflicto entre lo planeado y lo reciente prevalece lo reciente · COCOMO recalculado con el tamaño medido (corrige un EAF de 3,76 a 3,34 de la versión anterior) · sin contactos externos ni medición de overhead de competidores (fuera de alcance, justificado en Cap. IV) · todo lo posterior a la defensa de Gabriel (continuación por Stefano) es fuera de alcance.

## Huecos declarados (el harness los va a encontrar; son conocidos)

Contenido que debe aportar una persona:
- Búsqueda INPI completa: hecha "quark" (14 registros vigentes, 2 en clases 9 y 42) y "quark anticheat" (sin registros); faltan "anticheat", variantes fonéticas y **capturas con fecha** (Cap. VIII Tablas 8.1–8.2).
- Logotipo (no existe).
- Resultados de la encuesta: instrumento diseñado (`docs/Quark_Encuesta_Diapositivas.txt`), no publicado; piloto y consulta a moderadores pendientes. Cap. II usa investigación documental e hipótesis de demanda H-D1 a H-D3 (provisionales).
- Figura 1 (grafo PERT): no incorporada; declarada como tarea editorial.
- ADR-001: línea de aceptación (append-only).
- Titulares del copyright y cabeceras SPDX en el código; `LICENSE` en `Dev`.
- Compatibilidad GPLv3 declarada vs `MODULE_LICENSE("GPL")` del kernel (GPLv2): tema a revisar, no bloqueante.

Validación técnica no realizada (declarado en Conclusiones, no se afirma lo contrario): overhead de CPU/RAM, tasa de detección y falsos positivos, intentos de evasión, build de release en hardware físico, latencia del Modo A y comportamiento del watchdog, prueba cliente↔servidor. Lo medido (ataque `/proc/<pid>/mem` denegado 10/10, control negativo, 5/5 sin defensa) es en **VM, build de testing, juego simulado** y una validación sobre el motor real.

Debilidades de fuentes (marcadas `UNVERIFIED` en el texto, consideradas por el autor fuera de alcance y no bloqueantes): cifras de usuarios de Steam tomadas de prensa; Dot Esports sin autor/fecha verificados; compilación de panke con datos de Reddit sin verificar y título/URL exactos sin aportar; clase 42 de Niza sin cotejar en español; BPF-LSM sin referencia primaria de kernel.org; algunas citas de línea de los `.service`/`Cargo.toml` pueden estar corridas 1–2 líneas; discrepancia `vm/README.md` (CachyOS) vs `docs/vm_test_environment.md` (Nobara 43, la vigente).

Documentación del repo desactualizada respecto del código (R12): `docs/funcionamiento_codigo.md` aún dice que el módulo usa ganchos LSM (usa `kretprobe`); comentario obsoleto en `quark_daemon/src/main.rs:447-450`.

## Estructura del informe para mapear ítems del harness

Resumen · Cap. I Definición · II Relevamiento (encuesta, datos Steam, hipótesis) · III Entorno y dominio · IV Modelo de negocios (competencia, 4.5 estimación de segmento) · V Planificación (ciclos reales C1–C6, riesgos R1–R14, 5.6 COCOMO) · VI Metodologías · VII Marketing · VIII PI (marca, Niza, INPI, GPLv3) · IX Diseño (arquitectura, flujos, datos, interfaces con `archivo:línea`) · X Recursos · XI Oportunidades (CANVAS) · XII Lecciones · XIII Entregables · Conclusiones (parciales) · Bibliografía (APA) · Anexos I (datos), II (SLOC y cronograma), III (MVP congelado, reproducción). Borradores originales por capítulo en `01-Project/draft/` (siguen versionados; la fuente vigente es el informe). Reglas de forma aplicables (Art. 20/21 del Reglamento): A4, márgenes 2,5/3 cm, interlineado doble, Times New Roman 12, capítulos en hoja aparte, redacción impersonal en presente afirmativo; el PDF generado es para revisión y no se verificó punto por punto contra el Art. 20.

## Reglas de trabajo para quien continúe

`AGENTS.md` y `05-Meta/Working-Guidelines.md`: no afirmar lo no medido ni citado; marcar `UNVERIFIED`; leer `origin/Dev` antes de describir el código; zona de evidencia append-only (sin `--force` ni `amend` sobre lo publicado); firmar como `agent:<modelo>`; fechas reales.

## Ejecución del harness

*Pendiente de completar con la guía de la cátedra (instalación, comandos, entradas esperadas, salidas).* Entradas probables a confirmar: el PDF de `build/`, este repo y `Dev@35c6031`.

## Plan siguiente

El plan a largo plazo hasta febrero (para informar a la cátedra qué se hará y qué se mostrará) todavía no se redactó; ver [[Plan-Inmediato-2026-11-25]] para el alcance de la entrega de hoy.
