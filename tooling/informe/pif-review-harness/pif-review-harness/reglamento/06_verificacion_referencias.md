# 06 — Bibliografía: APA 7, existencia de fuentes y respaldo de afirmaciones

Ítems que cargan este módulo: `REF-01`, `REF-02`.

Fundamento: el tribunal evalúa las fuentes consultadas (RR97 18.1.7), la bibliografía sigue APA (Art. 20, APA 7 por cátedra) y los estudiantes responden por falseamiento de información (Art. 10.1.2, segundo inciso). **Una referencia inexistente es una falta grave, no un detalle de formato.**

## §cruce — Citas ↔ lista (`apa_citations.json`)

Informar por separado: citas sin entrada; entradas nunca citadas; mismo autor con años distintos entre texto y lista; autor citado con un nombre que no figura en la lista ("Meta Open Source" vs. "Meta Platforms"); diferencias de grafía o de cantidad de autores; duplicados (misma obra en dos idiomas o ediciones).

## §apa — Formato APA 7

Fechas de recuperación mal formadas (en APA 7 solo para contenidos que cambian: "Recuperado el 23 de noviembre de 2025, de"); mezcla de s.f. y n.d.; "y" vs. "&"; URL acortadas (se pide la completa); DOI como `https://doi.org/...`; orden alfabético; iniciales de autores.

## §existencia — Verificación de existencia (`referencias_verificacion.json`)

El script consulta Crossref (por DOI y por búsqueda bibliográfica) y OpenAlex, y comprueba URLs. Antes de declarar un DOI "no registrado" hace un **control positivo** con un DOI conocido: si el control falla, todas las conclusiones negativas quedan GRIS.

Para las entradas que el script deja "No localizada (búsqueda automática)", el Maker hace **búsquedas web reales** y las registra (consulta, resultado, fecha) en el hallazgo. Por tipo:
- Artículos y ponencias: Crossref, OpenAlex, sitio de la revista o conferencia.
- Libros: editorial, WorldCat; la edición tiene que existir en el idioma citado.
- Web, documentación, prensa: que la página exista, que fecha y URL coincidan y que trate lo atribuido.
- Software: autor real del proyecto o autor corporativo, no el usuario de GitHub.
- Normativa: número y año en el boletín oficial o sitio del organismo.

**La memoria del modelo no es evidencia.**

## §señales — Señales de referencia fabricada

Autores que no coinciden con los de la obra real o mezclan áreas no relacionadas; nombres que no parecen personas (p. ej., "Enthusiast, A. C."); URL o título de una obra de otros autores; DOI no registrado (con control positivo) o que resuelve a otra obra; título real con autores, año o revista cambiados; volumen, páginas o edición inexistentes; URL plausible que devuelve 404 o algo sin relación.

## §estados — Clasificación

| Estado | Criterio |
| --- | --- |
| Verificada | Existe; autores, año, título y fuente coinciden. |
| Con discrepancias | Existe, pero difiere en autores, año, edición, título o URL. Indicar el dato correcto. |
| No localizada | No se encontró tras las búsquedas. Registrar las búsquedas y, si corresponde, que el DOI no está registrado. **No es una acusación.** |
| Fabricada / Autoría inventada | Evidencia concreta de datos falsos combinados (DOI o URL de otra obra, autores que la obra real no tiene). Se describe la evidencia, no la intención. |

## §respaldo — ¿La fuente dice lo que se le atribuye?

Para afirmaciones con datos duros (porcentajes, métricas de modelos, cifras de mercado, estadísticas del dominio): abrir la fuente y comprobar. Al menos 5 afirmaciones, o todas si son menos. Registrar: afirmación, página del PIF, fuente, respaldo (Sí / Sí, con reservas / Parcialmente / No / No verificable). Señalar cuando la "fuente" es una declaración comercial y no un dato estadístico.

## §volcado — Qué va a la devolución

- Una observación de formato APA (evidencia: cada referencia con DOI o URL completa y accesible).
- Si hay "Con discrepancias", "No localizada", "Fabricada" o afirmaciones no respaldadas: una observación **obligatoria** propia (Art. 10.1.2 segundo inciso, 18.1.7 y 20). Evidencia exigida: la fuente real de cada referencia observada, o su eliminación y la reescritura del párrafo que se apoyaba en ella.
- La sección "Verificación de referencias" de la devolución (tabla ordenada con fabricadas y no localizadas primero; tabla de afirmaciones; cruce citas ↔ lista).
- En el coloquio, los estudiantes muestran la fuente original de cada referencia observada.
