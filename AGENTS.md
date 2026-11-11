# Instrucciones para agentes (y personas)

Antes de escribir en el repo, leer:

1. **`docs/obsidian-vault/quark-vault/05-Meta/Append-Only-Standard.md`** — en el vault solo se *agrega* texto al final; nunca se edita ni borra lo existente. Verificar con `python3 tooling/check_append_only.py` (activar hook: `git config core.hooksPath .githooks`).
2. **`.../05-Meta/Working-Guidelines.md`** — cómo trabajamos de aquí a la defensa (ciclos, evidencia, qué no afirmar).
3. **`.agents/AGENTS.md`** (rama `Dev`) — reglas de código C y `make lint`.

Reglas rápidas:
- El vault es la fuente de verdad; `docs/*.md` son stubs.
- No afirmar nada que no esté medido o citado (commit, `archivo:línea`, captura). Marcar `UNVERIFIED` lo inferido.
- Leer el estado de `origin/Dev` (`git fetch`) antes de describir qué hace el código; la rama local puede estar atrasada.
- Firmar entradas como `agent:<modelo>`; fechas reales, nunca retroactivas.
