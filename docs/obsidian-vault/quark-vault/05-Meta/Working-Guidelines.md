---
title: Guía de trabajo hasta la defensa
tags: [meta, guia, defensa, agentes]
status: canonical
effective: 2026-11-11
---

# Guía de trabajo hasta la defensa

Para personas **y** agentes. Proceso elegido: prototipado evolutivo con puerta de riesgo ([[Process-Recommendation]], propuesta pendiente de aceptación). Escritura: [[Append-Only-Standard]]. Esta guía también es append-only; cambios futuros van como `## Update`.

## 1. Principios
1. **Evidencia antes que afirmación.** Nada entra al informe o a la defensa sin una fila en [[Claims-Ledger]] con estado y fuente.
2. **Lo no medido se dice no medido.** Mejor un límite honesto que una cifra inventada.
3. **Un solo prototipo vivo** (`Dev`); main se actualiza solo con versiones congeladas.
4. **Fechas reales, nunca retroactivas.** Reconstrucciones se rotulan como tales.
5. **El código manda:** si doc y código discrepan, se documenta la discrepancia y se corrige la doc (como `Update`), no se retoca el pasado.

## 2. Protocolo de iteración (puerta de riesgo)
Cada iteración se registra en [[Cycle-Log]] con `Templates/Cycle`:
1. **Antes de empezar** (≤15 min): objetivo de 1 frase, alcance (qué NO entra), top-3 riesgos con la prueba que los decidirá, criterio de salida medible.
2. **Durante:** tarjetas en el Kanban enlazadas al ciclo; commits pequeños que citan la tarjeta.
3. **Al cerrar:** evidencia (commit, captura, nota), decisión **GO / NO-GO / PIVOT**, siguiente ciclo. Si el criterio de salida no se cumple, el ciclo **no** se declara cerrado; se registra tal cual.
Máximo **un ciclo abierto** a la vez. Regla WIP del Kanban: ≤2 tarjetas *Doing* por persona.

## 3. Plan de cierre (orden de trabajo hasta H5)
**C7 — Estabilizar y medir**
1. *Congelar un release candidate*: elegir el commit, taggearlo (`rc-1`), y **registrar `git_commit` y `git_branch` en `environment.txt`** del harness de capturas.
2. *Decidir ramas:* mergear o descartar `feature/gameStartProtection` (ver [[Test-Status]] Update); actualizar `main`; resolver conflictos de `docs/*.md` (conservar los stubs, pasar el contenido de Dev al vault como `Update`).
3. *Arreglar el harness* (`results.csv`/`summary.txt`, [[Capture-findings-2026-08-29]] §7.1) y re-capturar sobre el RC. Corregir/descartar los scripts que prueban "Modo A solo".
4. *Medir overhead de CPU/RAM*: mínimo 3 configuraciones (sin Quark / módulo / módulo + BPF-LSM), ≥10 repeticiones cada una, misma carga de juego, registrar media y desviación y el comando exacto. Anotar que se mide en VM con build *testing*.
5. *Calcular TDP y falsos positivos* con una lista cerrada de casos (ataque por `/proc/pid/mem`, `ptrace`, `process_vm_*`, carga de BPF, cheat con `LD_PRELOAD`, lecturas legítimas como `ps`/`htop`), cada una con resultado esperado antes de ejecutar.
6. *Commitear el README corregido* (hoy solo está sin commitear) y actualizar [[Claims-Ledger]].
**C8 — Paquete de defensa**
7. Nota de desviación metodológica en el informe ([[Process-Recommendation]]).
8. Guion de demo reproducible (comandos exactos, estado inicial, qué se espera ver, plan B si falla la VM).
9. Banco de preguntas difíciles (§5) con respuesta y enlace a evidencia.
10. Ensayo completo de la demo en la VM limpia, con cronómetro.

## 4. Reglas para agentes
- Leer `AGENTS.md`, este documento y [[Append-Only-Standard]] antes de escribir.
- `git fetch` y leer `origin/Dev` antes de describir el código; la rama local puede estar atrasada.
- No usar `Write` sobre archivos existentes del vault; solo apéndices. Correr `python3 tooling/check_append_only.py` antes de dar por terminado.
- Cada hecho técnico lleva fuente (`archivo:línea`, commit, captura o § de documento). Inferencias → `UNVERIFIED`.
- No ejecutar scripts que cargan módulos de kernel ni `SIGKILL` fuera de la VM de pruebas.
- No commitear ni hacer push sin que lo pida una persona. No incluir secretos (clave privada de firma, `board.json` de Trello).
- Firmar como `agent:<modelo>`; no inventar fechas, mediciones ni citas bibliográficas.
- Ante contradicción entre fuentes: registrarla como entrada, no resolverla en silencio.

## 5. Preguntas difíciles que el tribunal puede hacer
| Pregunta | Dónde está la respuesta | Estado |
|---|---|---|
| ¿Por qué no Rust en el módulo? | R2 en [[Risk-Register]]; contingencia del informe | Respondible |
| ¿Por qué kretprobe y no un LSM? | [[Features]] §1.1, §1.5 (`security_add_hooks` es `__init`) | Respondible |
| ¿Qué pasa si el tramposo es root y hace `rmmod`? | **Sin respuesta documentada**; el watchdog ayuda solo si cae el daemon | Investigar y registrar |
| ¿Y si inyecta código sin syscalls (`LD_PRELOAD`)? | [[Known-Limitations]]; telemetría `EXEC_MPROTECT` es solo indicador | Límite declarado |
| ¿Se probó el build de release? | No: la VM obliga a build *testing* ([[Known-Limitations]] Update) | Límite declarado |
| ¿Cuál es el overhead? | No medido | **Cerrar en C7** |
| ¿Qué tasa de detección/falsos positivos? | No medido | **Cerrar en C7** |
| ¿Es un espiral con SCRUM? | [[Process-Recommendation]] | Respuesta honesta lista |
| ¿Un cheater puede arrancar sin `bpf` en `lsm=`? | Sí, queda solo kretprobe; el motor no lo chequea ([[Features]] §5) | Límite declarado |
| ¿Qué falta para producción? | Servidor-SDK, pruebas cliente↔servidor, política del motor | [[Features]] §5 |

## 6. Definición de "hecho" para una afirmación
Una afirmación está lista para el informe cuando: (a) tiene fila en [[Claims-Ledger]]; (b) su evidencia se puede reproducir con comandos escritos; (c) su alcance (VM, build *testing*, mock vs. motor real) está dicho en la misma frase.

## Update 2026-11-14 — agent:claude-sonnet-5-5 — alinear con el nuevo alcance de append-only
- **REPLACES** — «No usar `Write` sobre archivos existentes del vault; solo apéndices.» y «Correr `python3 tooling/check_append_only.py` antes de dar por terminado» (§4) → solo la zona de evidencia es append-only ([[Append-Only-Standard]] Update 2026-11-14); el resto del vault y el informe entregable se editan en el lugar. En esa zona el chequeo se corre con `python tooling/check_append_only.py --worktree` (en este entorno `python3` es un alias de la Store que no ejecuta).
- **ADDED** — Requisito de entrega (Reglamento RR-97/23, Art. 22 y 24; cátedra, 2026-11-14): **todos** los capítulos I–XIII, Conclusiones, Bibliografía y Anexos deben estar desarrollados; los placeholders no cuentan. Detalle en `AGENTS.md`. El plan de cierre de §3 queda subordinado a este requisito.
