---
title: "ADR-001 Proceso a seguir: espiral vs prototipado evolutivo"
tags: [meta, adr, proceso, defensa]
status: proposed
date: 2026-11-11
author: agent:claude
---

# ADR-001 — Espiral vs prototipado evolutivo

Entrada de decisión (ledger, append-only). **Estado: propuesta** hasta que Gabriel y Stefano agreguen abajo una línea `## AAAA-MM-DD — <nombre> — ACEPTADA / RECHAZADA`.

## Contexto
- El informe (§6.1) declara **modelo en espiral + prácticas SCRUM**. La evidencia en git ([[Cycle-Log]]) muestra prototipos sucesivos cada vez más realistas, integrados por PR en `Dev`, trabajo en ráfagas (jun, fin de ago, oct, nov), sin sprints, backlog en git ni registro de riesgos actualizado.
- Hoy es 2026-11-11 y H5 (validación + documentación + defensa) está estimado para **mediados de noviembre**. No hay tiempo para otro ciclo de desarrollo completo; lo que queda es estabilizar, medir y documentar.

## Opciones evaluadas
| Criterio | Espiral (Boehm) | Prototipado evolutivo |
|---|---|---|
| Qué exige | Por ciclo: objetivos → análisis y resolución de riesgos → desarrollo/verificación → revisión y plan del siguiente | Construir un prototipo, ponerlo a prueba, refinarlo hasta que *es* el producto |
| Coincide con lo que **realmente se hizo** | Parcial: hubo riesgo-primero (R2, R6) pero sin análisis ni revisión escritos | **Alto**: cada hito reutilizó y endureció el prototipo anterior |
| Evidencia disponible hoy | Escasa (no hay registros de ciclo contemporáneos) | Abundante (commits, PRs, VM doc §3–§15, capturas) |
| Costo de adoptarlo ahora | Alto: habría que inventar ciclos o abrir uno nuevo sin tiempo | Bajo: se formaliza lo que ya ocurre |
| Riesgo en la defensa | Alto si se afirma "espiral estricto": un tribunal puede pedir los análisis de riesgo por ciclo | Medio: hay que explicar la desviación del informe |
| Qué aporta que falta hoy | **Revisión explícita de riesgos y decisión go/no-go** | Convergencia hacia un entregable congelado |
| Encaje con 2 personas y una fecha fija | Pesado | Liviano |

## Decisión recomendada
**Seguir como prototipado evolutivo, con una "puerta de riesgo" tomada de la espiral al cierre de cada iteración.** En concreto:
1. **Modelo operativo = prototipado evolutivo**: un solo prototipo vivo (`Dev`), iteraciones cortas, cada una cierra con evidencia.
2. **De la espiral se conserva únicamente la revisión de riesgos** (3 riesgos principales, cómo se probó cada uno, decisión go/no-go) en una entrada de [[Cycle-Log]] por iteración. Es barata y es lo que el informe prometió.
3. **No afirmar SCRUM** a menos que el tablero de Trello (a migrar, ver [[Trello-Migration-Guide]]) muestre sprints reales. Si no los muestra, decir "tablero Kanban".
4. **Honestidad sobre la desviación:** en la defensa y en el informe final presentar el proceso como *"modelo en espiral declarado; ejecución real: prototipado evolutivo guiado por riesgo"*, con las desviaciones y su razón escritas (R2: bindings de Rust inmaduros → C + BPF-LSM; ver [[Risk-Register]]).
5. **Prohibido rellenar el pasado:** los ciclos C1–C6 de [[Cycle-Log]] son una *reconstrucción desde git* y están rotulados así. No se redactan registros "como si" fueran contemporáneos.

## Por qué no "espiral estricto"
Porque lo único que lo distingue de lo que hacemos son los artefactos por ciclo (análisis de riesgo, plan siguiente) y esos **no existen** de forma contemporánea. Crearlos ahora con fechas viejas sería falsificar evidencia; crearlos con fecha de hoy los vuelve evidencia de *disciplina futura*, no de proceso pasado. Es defendible lo primero y no lo segundo.

## Consecuencias
- Se agrega una iteración de cierre **C7 "estabilizar y medir"** y una **C8 "paquete de defensa"** (ver [[Working-Guidelines]]).
- El informe necesitará una nota de desviación metodológica (agregar como `## Update` en [[Informe-PIF-Avance]]).
- Si el tribunal insiste en espiral: la respuesta honesta es que las iteraciones fueron guiadas por riesgo (con ejemplos fechados) pero no hubo revisión formal por ciclo hasta C7.

## Limitaciones de esta evaluación
Se basa solo en git/GitHub. Trello, reuniones semanales y los registros semanales de avance que menciona el informe (§6.2) pueden contener evidencia de proceso que no vi. **Revisarlos antes de aceptar esta ADR.**
