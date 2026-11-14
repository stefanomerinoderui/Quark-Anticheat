# Instrucciones para agentes (y personas)

Antes de escribir en el repo, leer:

1. **`docs/obsidian-vault/quark-vault/05-Meta/Append-Only-Standard.md`** (ver su Update 2026-11-14) — solo la **zona de evidencia** es append-only (capturas, Claims-Ledger, Test-Status, Cycle-Log, ADR, el estándar y la guía de trabajo; lista en `EVIDENCE` de `tooling/check_append_only.py`). El resto del vault y el informe entregable se **editan en el lugar**; el historial es git (sin `--force` ni `amend` sobre lo publicado, mensajes de commit que digan qué y por qué). Verificar con `python tooling/check_append_only.py --worktree` (hook opcional: `git config core.hooksPath .githooks`).
2. **`.../05-Meta/Working-Guidelines.md`** — cómo trabajamos de aquí a la defensa (ciclos, evidencia, qué no afirmar).
3. **`.agents/AGENTS.md`** (rama `Dev`) — reglas de código C y `make lint`.

Reglas rápidas:
- El vault es la fuente de verdad; `docs/*.md` son stubs.
- No afirmar nada que no esté medido o citado (commit, `archivo:línea`, captura). Marcar `UNVERIFIED` lo inferido.
- Leer el estado de `origin/Dev` (`git fetch`) antes de describir qué hace el código; la rama local puede estar atrasada.
- Firmar entradas como `agent:<modelo>`; fechas reales, nunca retroactivas.

## Requisito de entrega: TODOS los capítulos deben estar desarrollados
Fuente: `docs/RR-97-23-Reglamento-de-Proyecto-Integrador-Final.md` (Art. 22 y Art. 24) y exigencia explícita de la cátedra (2026-11-14): sin **todos** los capítulos completados no se habilita la defensa.

- Deben tener contenido real: Resumen, Índice, **Cap. I a XIII**, **Conclusiones**, **Bibliografía** (APA) y **Anexos I–III**. Un "[A completar]", "Pendiente" o una lista de secciones previstas **no cuenta** como capítulo desarrollado.
- Cada capítulo debe cubrir los puntos que el Art. 24.3 enumera para él (p. ej. Cap. II: fuentes, instrumentos, datos, gráficos, análisis, conclusiones; Cap. VIII: marca, clases internacionales, búsqueda INPI; Cap. XI: CANVAS y oportunidades; Cap. XII: aspectos positivos y a mejorar).
- Honestidad antes que relleno: si un dato no existe (p. ej. una encuesta no hecha), el capítulo se desarrolla con lo que sí hay (relevamiento documental, método, alcance, limitaciones) y lo dice; no se inventan datos, fechas ni citas. Las búsquedas INPI y datos de encuestas las debe aportar una persona.
- Forma de redacción (Art. 21): **impersonal**, verbos en **presente y afirmativo**, formato uniforme, sin desarrollos teóricos ni discusiones ajenas al proyecto.
- Forma del documento (Art. 20): A4; márgenes sup/inf 2,5 cm, izq/der 3 cm; interlineado doble; Times New Roman 12 (notas 10); cada capítulo en hoja aparte con carátula de capítulo; bibliografía APA; anexos con numeración propia "página X de Y"; unidades SI/SIMELA.
- Entrega: copia del PIF por correo a la Dirección de Carrera **5 días hábiles antes** de la defensa (Art. 14); defensa pública de hasta **45 min** (Art. 16); nota mínima 6.
- Generar el documento para revisión con `sh tooling/build_informe.sh` (pandoc + tectonic); fuente única: el informe del vault.
- Estado al 2026-11-14 de lo que sigue en placeholder en `Informe-PIF-Avance.md`: Cap. II (encuesta), IV (mapeo de competencia), VII, VIII, IX (modelo de datos, infraestructura), XI (CANVAS), XII, Conclusiones, Anexo I. Verificar con `grep -n "A completar\|Pendiente"` antes de dar el informe por listo. Los agregados van como `## Update` (append-only) o en una nota consolidada `Informe-PIF-v2` acordada por ambos.
