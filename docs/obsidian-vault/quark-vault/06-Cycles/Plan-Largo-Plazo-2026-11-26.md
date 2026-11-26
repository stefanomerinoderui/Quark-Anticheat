---
title: Plan de acción a largo plazo — de la entrega de noviembre a la defensa de febrero
tags: [plan, defensa, cronograma]
status: borrador v1 (supuestos abiertos en §9)
source: Handoff-Plan-Largo-Plazo-2026-11-26; Plan-Inmediato-2026-11-25; devolución del harness 2026-11-26; Working-Guidelines §3 y §5; Risk-Register
---

# Plan de acción a largo plazo (2026-11-30 → defensa de febrero de 2027)

Autor: agent:claude-sonnet-5-5 · 2026-11-26 · **borrador v1**: las fechas de la cátedra y la disponibilidad horaria no constan y se tratan como **supuestos** (§9). Los porcentajes son estimaciones por juicio (UNVERIFIED) para dimensionar el trabajo restante; no van en el informe.

Responsable de todo lo que figura aquí: **Gabriel Sebastián Martinez Alarcón** (único que defiende). **Stefano Nahuel Merino De Rui** colabora donde se indica (permisos sobre `Dev`, reparto de actividades) y no presenta en esta ventana. Lo posterior a la defensa queda fuera de alcance.

## 1. Resumen

- **Dónde estamos.** El informe tiene contenido real en todos los capítulos (Resumen, I–XIII, Conclusiones, Bibliografía, Anexos I–III) y el MVP está congelado en `Dev@35c6031`. La segunda pasada del harness de la cátedra (2026-11-26) no encontró observaciones bloqueantes y dejó **14 corregibles**.
- **Qué falta, en una línea.** Lo que más pesa no es redacción sino **evidencia**: medir overhead y tasa de detección/falsos positivos, probar evasión y el build de *release*, reunir datos primarios de stakeholders y cerrar la propiedad intelectual (INPI, licencia en `Dev`).
- **Cómo se ordena.** 12 semanas. Primero lo barato que cierra observaciones del harness (semanas 1–3), después las mediciones técnicas (3–7), la encuesta y los contactos corren en paralelo (1–9), el informe se congela el **2027-01-29** y las últimas semanas son defensa.
- **Qué puede ver el profesor y cuándo:** un entregable verificable por semana (columna "Se puede ver" de §4).

## 2. Trabajo restante aproximado

### 2.1 Módulos del MVP (código en `origin/Dev@35c6031`; sin cambios desde el plan inmediato)

| Módulo | Planeado (informe de mayo) | Hecho (fuente) | Aprox. hecho | Falta |
|---|---|---|---|---|
| Módulo de kernel | Rust + LSM | C con `kretprobe` Ring 0, canal Netlink firmado, fallo cerrado (Features §1–2) | ~85 % | namespaces de PID, `maxactive`, build de *release* en hardware físico |
| Demonio + eBPF/BPF-LSM | servicio de políticas | Rust + 12 programas eBPF, telemetría, autoprotección | ~85 % | caso `SIGSTOP`, política del motor sobre `bpf_lsm_active` |
| SDK | API de integración | `init` con fallo cerrado y watchdog | ~80 % | SDK de servidor, prueba cliente↔servidor (opcional) |
| Integración RecoilEngine/BAR | juego open source | integrado (PR #1) | ~75 % | cobertura de pruebas sobre el motor real |
| Validación y pruebas | tasas de detección, overhead | 10/10 en VM, control negativo, 5/5 sin defensa | ~40 % | **overhead, TDP/falsos positivos, evasión, release en hardware**, harness de captura |
| Gestión del repo | — | `dev/docs` publicada; `main` (2026-11-26) ya incluye `Dev@35c6031`, `LICENSE`, empaquetado Arch (`packaging/arch`), CI y el socket en `/run/quark` (`e9f8c00`), que `Dev` no tiene; tag solo `v0.1.0` | ~60 % | tag `rc-1` y manual en `Dev` (`LICENSE` ya está en `main`), decidir `gameStartProtection` |

**Global módulos ≈ 70 %.** El trabajo restante se concentra en validación (≈ 60 % de lo que queda) y en gestión del repo.

### 2.2 Capítulos del informe (estado tras el plan inmediato)

Todos tienen contenido; el % es cuánto del alcance exigido por el Art. 24.3 se estima cubierto, y qué lo limita. Juicio propio basado en la devolución del harness (OBS-xx).

| Capítulo | ≈ % | Qué falta |
|---|---|---|
| Resumen, I, III | 85–90 | solo ajustes de paridad al cierre |
| II Relevamiento | 55 | datos primarios con n (encuesta) o alcance documental acordado (OBS-07) |
| IV Modelo de negocios | 80 | revisión final de fuentes (OBS-13) |
| V Planificación | 80 | actividades por integrante, riesgo "pérdida de un integrante", Figura 1 PERT (OBS-18) |
| VI Metodologías | 80 | definición de terminado, retrospectiva (OBS-18) |
| VII Marketing | 75 | acciones ejecutadas y resultados de difusión |
| VIII Propiedad intelectual | 70 | INPI completo con capturas, logo, titulares (OBS-08) |
| IX Diseño | 85 | verificar citas de línea; manual de despliegue (OBS-12/20) |
| X Recursos | 60 | cifras de costos con tarifa declarada (OBS-19) |
| XI Oportunidades | 70 | supuestos, hipótesis, métrica y umbral (OBS-19) |
| XII Lecciones | 75 | actualizar con lo medido en febrero |
| XIII Entregables | 80 | tablero de gestión, tag (OBS-03/16, 14/21) |
| Conclusiones | 60 | dependen de las mediciones (overhead, TDP, evasión) |
| Bibliografía / Anexos | 75–85 | URLs pendientes y 5 referencias sin localizar (OBS-13); anexos con resultados nuevos |

**Global capítulos ≈ 75–80 %.** Las observaciones de forma (OBS-10 fuente, OBS-17 logo) son pequeñas pero visibles.

## 3. Reglas del plan

- Nada se afirma sin medición o cita; lo inferido va `UNVERIFIED` ([[Working-Guidelines]] §4, §6).
- Ciclos con puerta de riesgo: un ciclo abierto a la vez, apertura ≤ 15 min (objetivo, alcance, top-3 riesgos, criterio de salida), cierre GO/NO-GO/PIVOT en [[Cycle-Log]].
- Toda medición se hace en VM Nobara 43 con build *testing* y se declara; ninguna sale de la VM de pruebas con módulos de kernel.
- Cambios al código de `Dev` solo con permiso de escritura y decisión del autor; el plan **no incluye desarrollo de funciones nuevas**, solo medición, correcciones documentales y metadatos (LICENSE, tag, SPDX).
- Cierre de cada tarea: `python tooling/check_append_only.py --worktree`, `sh tooling/build_informe.sh` si se toca el informe, entrada en [[AI-Prompt-Log]].

## 4. Línea de tiempo semanal

Semanas desde el lunes. Esfuerzo relativo: S ≤ medio día, M ≈ 1–2 días, L > 2 días (estimación, UNVERIFIED; las horas reales dependen de §9).

| Sem. | Desde | Foco | Pasos para llegar | Se puede ver |
|---|---|---|---|---|
| 1 | 11-30 | Congelar RC y cerrar lo barato | (a) abrir ciclo C7; (b) decidir `gameStartProtection` (integrar, descartar o documentar) y registrar ADR-001; (c) tag `rc-1` y `LICENSE` en `Dev` (M); (d) registrar `git_commit`/`git_branch` en `environment.txt`; (e) recorte de la encuesta a ~25 ítems + versión corta para desarrolladores + EN/ES (M); (f) INPI: "anticheat" y variantes con capturas fechadas (S) | tag `rc-1` en `Dev`; ADR-001 resuelto; INPI con capturas (Cap. VIII); encuesta v2 |
| 2 | 12-07 | Informe: 14 observaciones, primera mitad | OBS-17 logo UCP; OBS-18 actividades por integrante y riesgo; OBS-19 costos con tarifa declarada y supuestos de Cap. XI; OBS-13 URLs y referencias; OBS-02/15 declaración de IA; OBS-10 decidir fuente con la cátedra (M cada grupo); piloto de la encuesta con 5–10 personas; crear cuenta de X; borrador de correos; consulta a moderadores | informe REENTREGA sin las observaciones de forma; PDF regenerado |
| 3 | 12-14 | Medición I y publicación | arreglar harness de captura (`results.csv`, `summary.txt`) y re-capturar sobre `rc-1` (M); manual de despliegue ejecutado en VM limpia con log (M, OBS-12/20); **publicar la encuesta** (si moderadores aprueban) y enviar los correos; **si la fecha 2026-12-15 es real: reentrega al harness el 12-15** | log de despliegue; harness con captura reproducible; encuesta en línea; correos enviados (sin esperar respuesta) |
| 4 | 12-21 | Medición II: overhead | 3 configuraciones (sin Quark / módulo / módulo + BPF-LSM) × ≥ 10 repeticiones, misma carga, media, desviación y comando exacto (L); cierra R14 | tabla de overhead con comandos; entrada en [[Claims-Ledger]] |
| 5 | 12-28 | Semana de holgura (fiestas) | solo recolección pasiva de encuesta y seguimiento; redactar Cap. V/VI pendientes | — (semana sin hito comprometido) |
| 6 | 01-04 | Medición III: detección y falsos positivos | lista cerrada de casos con resultado esperado **antes** de ejecutar: `/proc/pid/mem`, `ptrace`, `process_vm_*`, carga de BPF, `LD_PRELOAD`, lecturas legítimas (`ps`, `htop`) (L); calcular TDP (KPI ≥ 75 %) y falsos positivos | matriz de casos con esperado vs obtenido y TDP |
| 7 | 01-11 | Evasión y *release* | intentos de evasión acotados a los límites declarados (rmmod como root, sin `bpf` en `lsm=`) — responder la pregunta del tribunal "¿y si el tramposo es root?" (M); build de *release* en hardware físico **si hay acceso** (§9), si no, declarar el alcance (R11); seguimiento de correos (S) | nota de evasión con límites; resultado de *release* o declaración de alcance |
| 8 | 01-18 | Datos de stakeholders y revisión de licencia | cerrar encuesta y analizar con n (o acta de alcance documental); Cap. II con datos; revisar compatibilidad GPLv3 vs `MODULE_LICENSE("GPL")` y SPDX en `Dev` si se acepta (M) | Cap. II con resultados; decisión de licencia registrada |
| 9 | 01-25 | **Congelar informe** | integrar mediciones en Cap. IX/XII/Conclusiones/Anexos; recalcular y marcar `UNVERIFIED` lo que quede; corregir la documentación del repo contra el código (R12); generar PDF; pasada del harness; **congelado el 2027-01-29** | PDF final candidato; informe del harness sin rojos |
| 10 | 02-01 | Paquete de defensa | guion de demo reproducible (comandos, estado inicial, qué se espera, plan B si falla la VM); banco de preguntas difíciles con respuesta y evidencia ([[Working-Guidelines]] §5); presentación ≤ 45 min | guion de demo; banco de preguntas; presentación v1 |
| 11 | 02-08 | Ensayo y entrega | ensayo completo de la demo en VM limpia con cronómetro; **entrega a la Dirección** ≥ 5 días hábiles antes de la defensa (§6); copia congelada y tag final | PDF entregado; tag final; video o log del ensayo |
| 12 | 02-15 | Defensa | ajustes finales, ensayo, defensa en la fecha fijada | — |

Los ítems de varias semanas (encuesta, correos) se abren y cierran con fecha en el [[Cycle-Log]]; la ausencia de respuestas externas **no bloquea** nada.

## 5. Siguientes pasos inmediatos (próximos 7 días)

1. Responder las preguntas de §9 (fecha de defensa, horas semanales, hardware, permisos en `Dev`, tarifa).
2. Abrir el ciclo C7 en [[Cycle-Log]] con objetivo, alcance, top-3 riesgos y criterio de salida.
3. Decidir `gameStartProtection` y aceptar o no ADR-001 (línea de aceptación en la zona append-only).
4. Taggear `rc-1` y agregar `LICENSE` en `Dev` (requiere permiso de escritura).
5. Búsquedas INPI pendientes con capturas fechadas.
6. Recortar y traducir la encuesta; pedir permiso a moderadores de los subreddits elegidos.
7. Cerrar OBS-17, 18, 19, 13 y 02/15 del informe (las que no dependen de mediciones).

## 6. Fecha de entrega hacia atrás (supuesto)

Supuesto de trabajo: la instancia se habilita a mediados o fines de febrero de 2027 y el caso más exigente es una defensa el **lunes 2027-02-15**. El Art. 14 pide entregar 5 días hábiles antes: **2027-02-08**. El 8 y 9 de febrero de 2027 podrían ser feriados de Carnaval (UNVERIFIED: no consultado el calendario oficial), por lo que el plan apunta a entregar el **viernes 2027-02-05** y congelar el informe el 2027-01-29. Si la defensa es más tarde, la semana de holgura se usa para ensayar. **Reemplazar por las fechas reales cuando se confirmen.**

## 7. Bloqueantes y mitigaciones

| Bloqueante | Efecto | Mitigación |
|---|---|---|
| Sin permiso de escritura en `Dev` | no se pueden crear tag, LICENSE ni SPDX (OBS-14/21) | pedirlo a Stefano o a quien administre el repo en la semana 1; plan B: tag y LICENSE en un repositorio espejo documentado |
| Sin hardware físico | no hay prueba de *release* (R11) | declarar el alcance en Conclusiones (ya declarado) y repetir la pregunta del tribunal con la respuesta honesta |
| Moderadores no autorizan la encuesta | n bajo o nulo (OBS-07) | difundir por canales propios; si el n es insuficiente, acordar con la cátedra el alcance documental y declararlo en Cap. II |
| Sin respuesta de Steam/empresas | sin validación externa | no se depende de ellas: se registran los envíos y las respuestas que lleguen; el plan no se retrasa |
| Fuente Times New Roman (OBS-10) | observación visible de forma | decidir con la cátedra en la semana 2 si el clon métrico TeX Gyre Termes es aceptable; si no, cambiar la fuente en el build |
| Fecha de defensa desconocida | cronograma hacia atrás incierto | trabajar al caso más exigente (§6) y reajustar al confirmarse |
| VM inestable durante mediciones (R1) | mediciones inválidas | snapshot limpio antes de cada corrida; registrar comando y versión; repetir ≥ 10 veces |

## 8. Riesgos y mitigaciones

Parten de [[Risk-Register]] R11–R14 y se agregan los nuevos de este plan.

| Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|
| R11 — validación solo con build *testing* | Alta | Alto | hardware físico si se consigue; si no, alcance declarado |
| R12 — docs contradicen al código | Alta | Medio | pasada de paridad contra `origin/Dev` en la semana 9 y [[Claims-Ledger]] |
| R13 — divergencia de ramas | Alta | Medio | semana 1: decidir qué rama es el MVP congelado (`Dev@35c6031` vs `main`, que difiere en el socket `/run/quark`) y documentarlo |
| R14 — overhead sin medir | Alta | Alto | semana 4 reservada; si falla, declarar "no medido" y no afirmar bajo impacto |
| Un único defensor (Gabriel) y poca disponibilidad | Media | Alto | semanas holgadas (5) y estimaciones S/M/L revisables; recortar encuesta y correos antes que las mediciones |
| Hallazgos técnicos que contradigan lo declarado (p. ej. TDP < 75 %) | Media | Alto | es un resultado válido: se informa tal cual y se acota el alcance en Conclusiones; no se ajusta el KPI |
| Estimación de esfuerzo errónea | Media | Medio | revisión al cerrar cada semana; mover tareas a la semana 5 o 11 |
| Evasión que revele un hueco no documentado | Media | Medio | registrar como límite en [[Known-Limitations]]; no corregir código en esta ventana |
| Incompatibilidad GPLv3 / kernel GPLv2 | Baja | Medio | semana 8 con la cátedra o asesor; mientras tanto declarado como tema a revisar |
| Cambios de reglas o fechas de la cátedra | Media | Medio | confirmar la fecha y el harness con el equipo de cátedra en la semana 1 |

## 9. Supuestos y preguntas abiertas

Hasta que se respondan, el plan usa estos supuestos (cambiarlos reajusta §4 y §6):

- **Fecha de defensa:** mediados/fines de febrero 2027; caso exigente lunes 15 (UNVERIFIED). El 2026-12-15 del harness (`plan_entregas.json`, instancias FINAL y REENTREGA-1): no consta si es oficial; se trata como **posible reentrega** (semana 3).
- **Horas semanales de Gabriel y Stefano:** no constan; las estimaciones son S/M/L, no horas. Semanas muertas por exámenes u otras materias: desconocidas (se asumió solo la semana 5).
- **Hardware físico y VM limpia Nobara 43:** no consta si hay acceso.
- **Permisos de escritura en `Dev` y en el repositorio de la cátedra:** no constan.
- **Tarifa horaria para costos (Cap. X):** sin definir; hasta entonces el Cap. X dice "no registrada".
- **ADR-001 y `gameStartProtection`:** sin decisión.
- **Logo de la UCP:** el archivo debe aportarlo una persona (OBS-17).

## 10. Referencias

[[Handoff-Plan-Largo-Plazo-2026-11-26]] · [[Plan-Inmediato-2026-11-25]] · [[Handoff-Harness-2026-11-25]] · [[Working-Guidelines]] · [[Risk-Register]] · [[Claims-Ledger]] · [[Known-Limitations]] · [[Cycle-Log]] · devolución del harness: `tooling/informe/pif-review-harness/pif-review-harness/entregas/quark-anticheat/informes/REENTREGA-1_devolucion.md`.
