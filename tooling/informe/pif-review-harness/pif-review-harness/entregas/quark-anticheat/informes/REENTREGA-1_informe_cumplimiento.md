# Informe de Cumplimiento — REENTREGA-1 (segunda pasada de autorrevisión)

| | |
| --- | --- |
| Proyecto | Quark Anticheat (`quark-anticheat`) |
| Equipo | G. S. Martinez Alarcón (autor, defiende); S. N. Merino De Rui (colaborador) |
| Modalidad | 23.2 Diseño y Desarrollo |
| Versión evaluada | `Informe-PIF-2026-11-26.pdf` (197 págs.), generado desde el commit `cbfb87b`; lectura del `.tex` equivalente. Código `Dev@35c6031`. |
| Versión anterior | `Informe-PIF-2026-11-25.pdf` (193 págs.) |
| Fecha | 2026-11-26 · `agent:claude-sonnet-5-5` |

Autorrevisión del equipo; no es una evaluación de la cátedra.

## 1. Resumen ejecutivo
**Veredicto propuesto:** sin ROJO. Quedan 14 hallazgos AMARILLO que requieren datos, decisiones de personas o cambios en `Dev`. La habilitación es decisión docente (Art. 11).

| Semáforo | Cantidad | Ítems |
| --- | --- | --- |
| ROJO | 0 | — (bajaron DIA-01 y GATE-01) |
| AMARILLO | 14 | GATE-01, REPO-01, ENT-01, FMT-01, EST-01 (logo), EST-02, EST-03, EST-04, EST-05, COH-01, REF-02, DIA-01, ENG-01, SEG-01 |
| VERDE | 5 | FMT-02, EST-01 (resumen), EST-06 (anexos y conclusiones), ETH-01 |
| GRIS | 6 | FMT-03, DAT-01, REF-01, REQ-01, ORA-01, ACA-01 |

**Más graves:** (1) la declaración de IA tiene sin aportar los enlaces y prompts de las sesiones de redacción y autorrevisión; (2) el manual de despliegue (Anexo III.5) nunca se ejecutó; (3) el reparto de responsabilidades por integrante no tiene evidencia y los commits de `Dev` se concentran en un integrante.

**Seguimiento de la pasada anterior (SEG-01):** subsanadas OBS-03, 04, 05, 09 y 11 (falso positivo OBS-06). Parciales OBS-02 y OBS-12. Reinciden OBS-01, 07, 08, 10, 13 y 14. El state del harness lista OBS-15 a 21 como nuevas por cambios de clave: son las mismas OBS-02, 03, 04, 12 y 14 en su estado actual.

**Referencias:** sin cambios: 1 verificada, 2 con discrepancias, 5 no localizadas, 0 fabricadas (sin búsqueda manual).

## 2. Cambios aplicados (fuente `Informe-PIF-Avance.md`)
Declaración de IA (p. 162–163); carátula completa; títulos sin `{#…}`; anexos "página X de 29"; bloque firmado por agente movido al Anexo III.6; URL y commit oficial en el Cap. XIII; Anexo III.5 rotulado como manual de despliegue; ADR-001 reformulada.

## 3. Pendientes
- Aportan personas: enlaces y prompts de IA, resultados de la encuesta, capturas INPI, logo de la UCP, cifras de costos, referencias con URL.
- Cambios en `Dev` (congelado): LICENSE, tag, manual propio, CI.
- Herramientas: Times New Roman (tectonic no carga la fuente del sistema).

## 4. Solo informe docente
- Commits en `Dev`: 24 de un integrante y 1 del otro; coloquio sobre el Art. 4 y verificar emails de autoría.
- DAT-01: revisar a mano las páginas con teléfonos detectados (Ley 25.326).
- Capas no cubiertas: REQ-01, ORA-01, ACA-01 y ortografía. Capítulos sin lectura completa.
- Preguntas de coloquio: ¿qué partes se redactaron con IA y cómo las verificaron? ¿Cómo construyen el módulo en una VM limpia? ¿Qué evidencia sostiene H-D1 a H-D3?
- El Checker pidió mover a este informe las `pregunta_coloquio` de DIA-01, EST-02 y GATE-01 (ya están acá).
