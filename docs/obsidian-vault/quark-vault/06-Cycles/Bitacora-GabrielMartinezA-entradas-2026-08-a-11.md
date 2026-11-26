---
title: Bitácora de Gabriel Martínez Alarcón — entradas agosto a noviembre 2026
tags: [bitacora, entrega]
source: commits de gmartineza en el repositorio (git log --author gmartineza); formato de Bitacora_GabrielMartinezA.md
---

# Entradas de bitácora (para pegar en el documento de Drive)

Las fechas son las del trabajo (commit), no las de carga. Complementan las entradas 20260908 y 202601001 ya cargadas. Fuente de cada entrada: commits de la cuenta `gmartineza`.

## 20260828

- Se escribió el script `capture.sh` para capturar de forma reproducible los resultados de las pruebas del Modo A (demonio) y el Modo B (demonio y módulo de kernel), con un control sin protección. Commit `af7e17f`.
  - Corre el juego simulado en tres condiciones (sin protección, A y B), con un plan por defecto de 5, 15 y 10 repeticiones.
  - Guarda en disco todo el resultado crudo (`environment.txt`, `results.csv`, salidas del demonio, del juego y del atacante, `dmesg`) y un resumen por modo con la latencia del Modo A.
  - Se descartó reutilizar `run_test*.sh` porque imprimen solo aprobado o desaprobado y descartan los registros, y para el informe se necesita citar el comportamiento observado.
- Se dejó asentado en el encabezado del script que la latencia medida es de extremo a extremo y no separa detección de mitigación sin cambiar el código de `cheat.c` y del demonio.
- Verificación posterior: las capturas del 2026-08-29 (`Capture-findings-2026-08-29`) revelaron defectos del propio script (`results.csv` mal formado y `summary.txt` solo con una condición). Quedaron registrados como trabajo a corregir antes de la medición definitiva.

## 20261111

- Se decidió que el vault de Obsidian sea la fuente de verdad de la documentación y que `docs/*.md` pasen a ser stubs que apuntan a él. Commit `a0f5460`.
  - Se importaron los documentos del proyecto al vault y se alinearon con `Dev@35c6031` mediante bloques de actualización.
  - Se adoptó una regla de escritura append-only para no perder la evidencia de qué se sabía y cuándo, con `tooling/check_append_only.py` y un hook de pre-commit.
  - Se redactaron la guía de trabajo hasta la defensa, el registro de afirmaciones (`Claims-Ledger`) y el registro de ciclos reconstruido desde el historial de git.
- Se registró la ADR-001 sobre el proceso: se comparó el modelo en espiral declarado contra el prototipado evolutivo guiado por riesgo que muestra el historial, y se propuso el segundo por ser el que describe lo ocurrido. Queda pendiente la línea de aceptación.
- Se reescribió el `README.md` para que describa lo que implementa `Dev` (módulo en C con `kretprobe`, demonio en Rust con BPF-LSM, canal firmado) y no lo planeado al inicio. Commit `c68a6da`.
- Herramienta auxiliar: Claude Code (consta como coautor en los commits). Verificación posterior: cada afirmación sobre el código se contrastó contra `Dev@35c6031` y lo no comprobado se marcó `UNVERIFIED`.

## 20261113

- Se incorporó al informe la actualización con los desarrollos posteriores al avance de mayo y se agregó la nota de investigación de anticheats bajo Proton. Commit `648696d`.
  - La investigación vive en un repositorio aparte (`proton-anticheats`). Cubre el comportamiento de Easy Anti-Cheat y BattlEye bajo Proton, con etiquetas de observado, inferido y no verificado.
  - Evidencia: el runtime de Proton para Easy Anti-Cheat es solo un puente y el cliente real lo trae cada juego. BattlEye viene empaquetado y virtualizado. De las 45 afirmaciones inferidas del registro de validación, 6 están confirmadas y el resto abiertas o bloqueadas.
  - Decisión: mantener el enfoque de kernel de Quark como diferencial, porque la industria converge hacia mecanismos del mismo tipo (BPF-LSM) y el valor está en ser abierto y documentado.
- Se ajustó `.gitignore` para excluir la copia local de `proton-anticheats` (commit `989693f`).
- Herramienta auxiliar: Claude Code. Verificación con las fuentes citadas en la nota y marcas de certeza por afirmación.

## 20261114

- Se resolvió generar el PDF y el LaTeX del PIF desde el ensayo del vault con pandoc y tectonic, con el formato del Art. 20 (A4, márgenes, interlineado doble). Commit `7604129`.
  - Alternativa descartada: mantener un documento de texto aparte, porque duplicaba la fuente y rompía la paridad con el vault.
- Se incorporó la transcripción del Reglamento del Proyecto Integrador Final (RR 97/23) al repositorio para trabajar con el texto citable. Commit `0922708`.
- Se acotó la regla append-only a la zona de evidencia, para poder editar en el lugar el informe y el resto del vault, y se registró como requisito de entrega que todos los capítulos estén desarrollados. Commit `efce8f2`.
  - Evidencia: Art. 22 y 24 del Reglamento y la exigencia de la cátedra del mismo día.
- Herramienta auxiliar: Claude Code. Verificación con `check_append_only.py` y generación del PDF.

## 20261125

- Se integraron todos los capítulos del informe (II, IV, VII, VIII, IX, XI, XII, Conclusiones y Anexos I a III) con el estado real de `Dev@35c6031`, y se recalculó COCOMO con el tamaño medido (2.762 SLOC con pruebas y 1.977 solo producto). Commit `b3fe99a`.
  - Se corrigió el factor de ajuste de 3,76 a 3,34 al usar el tamaño real en lugar del estimado.
  - Se agregaron los gráficos de la Steam Survey y el instrumento de la encuesta.
  - Lo no medido ni citado se dejó declarado, sin inventar datos.
- Se eligió la licencia GNU GPLv3 para todo el proyecto y se agregó el archivo `LICENSE`. Se transcribió en el Cap. VIII la búsqueda de marcas en el INPI de "quark" (14 registros vigentes, 2 en las clases 9 y 42) y de "quark anticheat" (sin registros). Commits `82f0e4d` y `b3096e7`.
  - Aporte personal: realizar las búsquedas en el buscador del INPI. Quedan pendientes "anticheat" solo, variantes fonéticas y capturas con fecha.
- Se limpió a mano la transcripción del Reglamento (encabezado repetido por el OCR) y se recuperaron líneas perdidas. Commit `c9f80c2`.
- Se redactó la nota de traspaso para ejecutar el harness de revisión de la cátedra (qué se entrega, qué se ejecutó y qué no, huecos conocidos). Commit `ea676de`.
- Herramienta auxiliar: Claude Code. Verificación: `build_informe.sh` y `check_append_only.py` sin errores, y regla de no afirmar lo no medido.

## 20261126

- Se ejecutó el harness de revisión de la cátedra sobre el PIF propio como autorrevisión, en dos pasadas (el PDF y luego el `.tex`), con verificación de citas literales y un revisor independiente. Commits `4def3ef` y `1139591`.
  - Resultado: la primera pasada dio 2 observaciones bloqueantes (falta de declaración de IA y de manual de despliegue). Tras corregir, la segunda pasada no tiene bloqueantes y deja 14 corregibles.
  - Se descartaron como falsos positivos del script el largo del Resumen (446 palabras, no 696) y las URL de repositorio (cortes de línea del PDF).
- Se corrigió el informe fuente (commits `535885f` y `cbfb87b`): carátula completa, títulos sin atributos impresos, numeración "página X de Y" en anexos, apartado de declaración de uso de IA, repositorio oficial en el Cap. XIII, Anexo III.5 como manual de despliegue y bibliografía al final.
- Se decidió documentar los prompts de forma resumida en `AI-Prompt-Log.md`, porque las sesiones de terminal no tienen enlace compartible, y versionar las matrices de respuesta del harness. Commit `1139591`.
- Pendiente para el equipo: logo de la UCP, capturas fechadas del INPI, cifras de costos del Cap. X, resultados de la encuesta, y un `LICENSE` y una etiqueta en `Dev`.
- Herramienta auxiliar: Claude Code (`claude-sonnet-5-5`). Verificación: lectura de la salida de cada script, citas literales contrastadas con el PDF y revisión independiente de los hallazgos.
