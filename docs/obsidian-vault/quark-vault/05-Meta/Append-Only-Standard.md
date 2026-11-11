---
title: Estándar de escritura append-only
tags: [meta, estandar, agentes]
status: canonical
effective: 2026-11-11
---

# Estándar de escritura append-only

**Regla única:** en este vault **solo se agrega texto; nunca se edita ni se borra lo ya escrito.** Si algo dejó de ser cierto, se agrega una entrada que lo dice. Aplica por igual a personas y a agentes (Claude, Copilot, etc.). Inspirado en OpenSpec (cambios como *deltas* ADDED/MODIFIED/REMOVED, historial archivado), pero más estricto: aquí ni siquiera la "especificación vigente" se reescribe.

**Por qué:** (1) el informe y la defensa necesitan poder demostrar *qué sabíamos y cuándo*; (2) dos personas y varios agentes editando en paralelo se pisan; (3) un agente que "limpia" una nota puede borrar evidencia sin que nadie lo note. Vigente desde 2026-11-11; el contenido previo es la línea base congelada.

## 1. Tipos de nota y cómo se escriben

| Tipo | Ejemplos | Cómo se escribe |
|---|---|---|
| **Ledger** (bitácora) | decisiones/ADR, reuniones, ciclos (`06-Cycles/`), log de cada tarjeta | Una entrada nueva al final: `## AAAA-MM-DD HH:MM — autor — título`. |
| **Referencia viva** | arquitectura, limitaciones, estado de pruebas, riesgos, roadmap | Se agrega al final un bloque `## Update AAAA-MM-DD — autor` con *deltas* (ver §2). El texto viejo queda intacto. |
| **Evidencia** | capturas, hallazgos, resultados de prueba | Congelada al crearse. Correcciones y reinterpretaciones = nueva nota o `## Update`. |
| **Estado** (exentos) | `04-Kanban/Board.md`, `.obsidian/**`, `Templates/` | Se editan normalmente; el historial lo da git. Las **notas de tarjeta** sí son append-only (sección `## Log`). |

## 2. Deltas (formato del `## Update`)

Cada delta nombra exactamente qué reemplaza, con una cita corta del texto afectado:

```markdown
## Update 2026-11-11 — agent:claude — alinear con Dev@35c6031
- **ADDED** — <hecho nuevo>. Fuente: `ruta:línea` / commit / captura.
- **REPLACES** — «<cita corta del texto viejo>» (§X) → <enunciado vigente>. Fuente: …
- **WITHDRAWN** — «<cita>» ya no aplica porque …
- **UNVERIFIED** — <cosa que sospechamos que cambió pero no comprobamos>.
```

Regla de lectura: **la última entrada sobre un tema gana.** Para saber el estado vigente se lee la nota completa y se aplican los Update en orden.

## 3. Reglas

1. **Nunca** reescribir, reordenar, "limpiar", reformatear ni borrar texto existente. Tampoco corregir typos (si cambia el sentido, delta `REPLACES`).
2. **Solo** son editables en el lugar estas claves del frontmatter: `status`, `superseded-by`, `updated`.
3. Las inserciones van **solo al final** del archivo, nunca en el medio.
4. Cada entrada lleva **fecha** (la real, de escritura — jamás retroactiva), **autor** (`gabriel`, `stefano`, `agent:<modelo>`) y **fuente** verificable. Lo no verificado se marca `UNVERIFIED`.
5. **Consolidar:** cuando una nota acumula muchos Update, se crea una nota **nueva** (`Nombre-v2`) con `supersedes: [[Nombre]]`; la vieja recibe `superseded-by: [[Nombre-v2]]` y queda congelada. Nunca se pisa la original.
6. **Renombrar/mover** un archivo está permitido solo sin cambiar su contenido (`git mv`, similitud 100 %).
7. **Excepción única:** secretos o datos personales subidos por error. Solo una persona, con acuerdo del equipo, puede reescribir la historia; se deja un ledger-entry (sin el secreto) explicando qué y por qué.
8. Los archivos fuera del vault (código, `README.md`, `docs/*.md` stub) siguen sus propias reglas.

## 4. Cómo escribir sin violar la regla

**Personas:** en Obsidian, ir al final de la nota y escribir debajo. No tocar nada por encima.

**Agentes:** *no* usar `Write` sobre un archivo existente del vault. Usar `cat >> archivo <<'EOF' … EOF`, o `Edit` anclando en las últimas líneas con `new_string = old_string + adición`. Antes de terminar: `python3 tooling/check_append_only.py` debe pasar. Ver `AGENTS.md` en la raíz del repo.

## 5. Cumplimiento automático
- `tooling/check_append_only.py` compara contra `HEAD` (o `--base REF`) y falla si hay líneas eliminadas/modificadas o inserciones que no sean al final, fuera de lo permitido en §3.
- Activar el hook una vez por clon: `git config core.hooksPath .githooks`.
- Limitación: el chequeo no puede juzgar si un `REPLACES` es verdadero; eso lo revisa la otra persona.

Ver también: [[Working-Guidelines]], [[Vault-Guide]].
