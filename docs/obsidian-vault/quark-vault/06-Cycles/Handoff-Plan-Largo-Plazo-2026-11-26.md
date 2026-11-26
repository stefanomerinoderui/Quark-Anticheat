---
title: Handoff — redactar el plan de acción a largo plazo (hasta la defensa de febrero)
tags: [handoff, plan, defensa]
source: sesión 2026-11-25/26; Plan-Inmediato-2026-11-25; Handoff-Harness-2026-11-25; autorrevisión del harness (2026-11-26)
---

# Handoff — plan de acción a largo plazo

Autor: agent:claude-sonnet-5-5 · 2026-11-26. Para quien redacte el plan sin haber visto la sesión. Esta nota **no es el plan**: reúne el pedido, los insumos, las restricciones y las decisiones abiertas.

## 1. El pedido (palabras del autor, resumidas)

- La instancia de defensa se habilita a mediados o fines de febrero (año 2027; el Reglamento no fija fecha ni año: **UNVERIFIED** la fecha exacta). Hoy es 2026-11-26: quedan unas 11–12 semanas.
- Este es el **plan 2**, "a largo plazo", complementario del [[Plan-Inmediato-2026-11-25]] (ya ejecutado: MVP congelado e informe con todos los capítulos iniciados).
- Se **entrega al profesor/evaluador** para que oriente, guíe y "audite" (pregunte avances con frecuencia, de forma desestructurada). El autor pidió **no gastar esfuerzo en pautar cómo debe revisar el profesor ni cómo mostrárselo**; el esfuerzo va en **qué tiene que poder ver el profesor** (producto del trabajo) y **cómo llegar a ello** (pasos que ejecuta el autor).
- Debe incluir una referencia del **trabajo restante aproximado** (porcentajes de [[Plan-Inmediato-2026-11-25]], recalculados tras el plan inmediato) para que el profesor dimensione lo que falta. Esos porcentajes son estimación por juicio (UNVERIFIED) y **no van en el informe**, solo en el plan.
- Contenido pedido para cada plan: planeado vs hecho, siguientes pasos, bloqueantes y mitigaciones, riesgos y mitigaciones; módulos del MVP y capítulos del informe por separado.
- Tareas que el autor ya dijo que pertenecen a este plan (no al inmediato): refinar y **publicar la encuesta** (Reddit, cuenta de X aún inexistente), **correos a Steam y otras empresas** que puedan aportar know-how o validación, y el resto del relevamiento con stakeholders. El Plan inmediato quedó con investigación documental y hipótesis provisionales (Cap. II H-D1 a H-D3).

## 2. Restricciones (decididas por el autor)

- **Nunca inventar datos**; todo con fuente o `UNVERIFIED` (AGENTS.md).
- Defiende **solo Gabriel Sebastián Martinez Alarcón**. Stefano Nahuel Merino De Rui es colaborador con atribución y **no** presenta en esta ventana (adeuda materias). Todo lo posterior a la defensa de Gabriel (continuación por Stefano, "afterlife") está **fuera de alcance**.
- Entorno de pruebas: Nobara 43 (CachyOS solo propuesta futura). Licencia: GNU GPLv3.
- Proceso: prototipado evolutivo guiado por riesgo (ADR-001, aún "proposed"). Ante conflicto entre lo planeado y lo reciente, prevalece lo reciente.
- Los `UNVERIFIED` menores restantes se consideran fuera de alcance y no bloqueantes.
- No medir el overhead de competidores (son de espacio de usuario; fuera de alcance justificado en Cap. IV).
- Contactos externos: en el plan inmediato no se tomaron "por falta de tiempo para esperar respuestas"; con 11–12 semanas **sí caben** y el autor los asignó a este plan.
- Fecha de entrega a la Dirección: 5 días hábiles antes de la defensa (Art. 14); defensa pública de hasta 45 min (Art. 16); nota mínima 6.

## 3. Estado de partida (hechos con fuente)

Ramas y commits: informe y docs en `dev/docs` (`ea676de` publicado); el trabajo del harness vive en la rama `review/harness-autorevision-2026-11-25` (HEAD `854533b`, publicada), que está **por delante** de `dev/docs` y contiene `tooling/informe/pif-review-harness/`. MVP congelado en `origin/Dev` `35c6031`; `origin/feature/gameStartProtection` `2b088ab` sin integrar; `main` atrasada. **Decisión abierta:** en qué rama consolidar y si se integra `review/...` en `dev/docs`.

Resultado de la segunda pasada del harness (informe `tooling/informe/pif-review-harness/pif-review-harness/entregas/quark-anticheat/informes/REENTREGA-1_devolucion.md`, 2026-11-26): **sin observaciones bloqueantes; 14 corregibles** (OBS-01, 02/15, 03/16, 07, 08, 10, 12/20, 13, 14/21, 17, 18, 19). Son el backlog natural de este plan:

| OBS | Qué falta | Quién lo puede cerrar |
|---|---|---|
| 02/15 | Enlaces/prompts de sesiones de redacción y autorrevisión; confirmar otras herramientas de IA | autor (declarar si no existen) + `AI-Prompt-Log.md` |
| 12/20 | Ejecutar el manual de despliegue (Anexo III.5) en una VM limpia; `Dev` sin manual propio ni CI | autor, VM Nobara 43 |
| 14/21 | `LICENSE` y tag en `Dev`; dar acceso a la cátedra a los repos | autor/Stefano (escritura en `Dev`) |
| 03/16 | Tablero de gestión en los entregables (Cap. XIII) y tag | autor |
| 17 | Logo de la UCP en la carátula (no hay archivo en el repo) | autor aporta el archivo |
| 18 | Cap. V 5.3: reparto de actividades por integrante; riesgo "pérdida de un integrante"; "definición de terminado" y retrospectiva (Cap. VI) | autor con Stefano |
| 19 | Cap. X cifras de costos con tarifa declarada; Cap. XI supuestos, hipótesis, métrica y umbral de decisión | autor define tarifa y supuestos |
| 07 | Encuesta: publicar y analizar con n, o acordar alcance documental con la cátedra | autor |
| 08 | INPI: "anticheat", variantes fonéticas, capturas fechadas | autor (acceso al sitio) |
| 10 | Fuente TeX Gyre Termes en vez de Times New Roman 12 (y margen/interlineado en pocas páginas) | autor decide con la cátedra o cambia el build |
| 13 | Entradas con "URL pendiente" y 5 referencias sin localizar | autor/agente con fuentes |
| 01 | Control negativo invalidado por `gameStartProtection`: re-ejecutar o acotar a `Dev@35c6031` | autor, VM |

Además, huecos de validación declarados en las Conclusiones y que el plan debe ubicar en el tiempo: overhead de CPU/RAM (3 configuraciones × ≥10 repeticiones, ver `05-Meta/Working-Guidelines.md` §3), tasa de detección y falsos positivos (KPI TDP ≥ 75 %), intentos de evasión, build de *release* en hardware físico, latencia del Modo A y watchdog, defectos del harness de captura (`results.csv`, `git_commit` sin registrar), prueba cliente↔servidor (opcional). Otros pendientes humanos: Figura 1 (grafo PERT), línea de aceptación del ADR-001 (zona append-only), titulares del copyright y cabeceras SPDX, revisión de compatibilidad GPLv3 vs `MODULE_LICENSE("GPL")`, logo propio, discrepancias documentales del repo (R12).

Fecha a tener presente: `plan_entregas.json` del harness fija `fecha_limite` **2026-12-15** para las instancias FINAL y REENTREGA-1. No consta en esta sesión si es una fecha oficial de la cátedra o una configuración del harness: **confirmar con el autor** antes de ponerla en el plan.

## 4. Insumos a leer primero

`AGENTS.md`; [[Plan-Inmediato-2026-11-25]] (porcentajes y estado de módulos/capítulos); [[Handoff-Harness-2026-11-25]]; `05-Meta/Working-Guidelines.md` (§3 plan de cierre, §5 preguntas difíciles del tribunal); [[Risk-Register]] (R1–R14); [[Test-Status]] y [[Claims-Ledger]]; `01-Project/Informe-PIF-Avance.md` (Conclusiones, Cap. II, VIII, XIII); `docs/Quark_Encuesta_Diapositivas.txt` (instrumento y recorte a ~25 ítems, piloto de 5–10 personas, versión corta para desarrolladores, consulta a moderadores en inglés y español); la devolución del harness arriba citada; `06-Cycles/Bitacora-GabrielMartinezA-entradas-2026-08-a-11.md` (tono y nivel de detalle de las bitácoras del autor). Código solo de `origin/Dev` (`git fetch` primero).

## 5. Qué debe producir quien tome esto

1. Un plan (nota nueva en `06-Cycles/`, p. ej. `Plan-Largo-Plazo-<fecha>.md`) con: referencia de trabajo restante por módulo y por capítulo (separados); línea de tiempo semanal hasta la ventana de defensa con hitos; por cada hito, **qué se puede mostrar al profesor** y **los pasos para llegar**; bloqueantes y mitigaciones; riesgos y mitigaciones (partir de R11–R14 y de los ítems de §3); preparación de la defensa (presentación de ≤ 45 min, preguntas difíciles) y fecha de entrega a la Dirección calculada hacia atrás.
2. Evitar una sección que pauta cómo el profesor revisa (decisión del autor).
3. Marcar `UNVERIFIED` lo no respaldado y no inventar fechas de la cátedra.

## 6. Preguntas que el autor debe responder (o el plan debe dejar como supuesto explícito)

- Fecha o rango real de defensa y significado del 2026-12-15 del harness.
- Horas semanales disponibles de Gabriel (y de Stefano como colaborador) hasta febrero; hay exámenes u otras materias que fijen semanas muertas (UNVERIFIED: no consta).
- Acceso a hardware físico para el build de *release* y a una VM limpia Nobara 43.
- Quién tiene permisos de escritura en `Dev` y en el repositorio de la cátedra.
- Si se acepta ADR-001 y si `gameStartProtection` se integra, se descarta o se deja como rama documentada.
- Tarifa horaria a declarar para el costeo (Cap. X).

## 7. Cierre de tarea (reglas del repo)

Verificar con `python tooling/check_append_only.py --worktree` y `sh tooling/build_informe.sh` si se toca el informe; mensajes de commit que digan qué y por qué (sin `--force` ni `amend` sobre lo publicado); agregar entrada resumida a [[AI-Prompt-Log]] al terminar; firmar `agent:<modelo>`.
