# 04 — IA generativa, integridad, datos personales e instancia oral

Ítems que cargan este módulo: `DIA-01`, `ETH-01`, `ORA-01`, `PRC-01`.

**Alcance:** la cláusula de cátedra CAT-IA rige en todas las entregas (AE y versión final). Portafolio y bitácora se verifican solo en las entregas parciales de AE (§portafolio). Las reglas de IA de la Guía Docente II, 27 y las mecánicas de IOVF no se verifican (`00_fuentes.md`, "Alcance").

## §clausula — Cláusula de cátedra CAT-IA (`DIA-01`)

> Si utilizó herramientas de IA generativa, debe declararlo en un apartado final indicando para qué se usó y cómo se verificó la información obtenida. Se deben indicar los prompts utilizados y compartir el enlace a la conversación con la herramienta de IA Generativa seleccionada. El uso no declarado, o la incorporación de datos no verificables, se registra con las observaciones correspondientes a los reglamentos. Tenga presente que en todas las producciones entregadas se le podrá pedir que dé cuenta oralmente.

**Qué verifica el harness** (`coherence.json#ai_declaration`):

| Elemento | Control | Si falta |
| --- | --- | --- |
| Apartado final de declaración | Encabezado "Declaración de uso de inteligencia artificial" (o similar) y su ubicación en el documento | Ver tabla de casos |
| Para qué se usó | Tareas y partes del trabajo asistidas, nombradas en concreto ("revisión ortográfica del Cap. II", no "como apoyo") | AMARILLO |
| Cómo se verificó la información | Procedimiento de verificación (fuente consultada, prueba ejecutada, cotejo) | AMARILLO |
| Prompts utilizados | Prompts transcriptos o listados | AMARILLO |
| Enlace a la conversación | Enlace compartido de la herramienta (ChatGPT, Claude, Gemini, Copilot, Perplexity, etc.) | AMARILLO; si el enlace no abre o no corresponde, pedir uno válido |

**Casos:**

| Situación | Semáforo | Fundamento |
| --- | --- | --- |
| Hay declaración completa | VERDE (con las preguntas de coloquio que surjan) | CAT-IA |
| Hay declaración incompleta | AMARILLO, con los elementos faltantes | CAT-IA |
| No hay declaración y hay **evidencia de uso** (mención de herramientas de IA en el texto, archivos de contexto de agentes en el repositorio, commits que lo indican, declaración genérica en otra parte) | ROJO | CAT-IA + RR97 10.1.2 (segundo inciso) y 18.1.8 |
| No hay declaración ni evidencia de uso | GRIS "no declarado; no hay evidencia de uso" y una pregunta de coloquio | — |
| Declaración genérica ("se usaron herramientas de IA como apoyo") | AMARILLO: no cumple CAT-IA | CAT-IA |

**Nunca** se concluye que un texto fue generado por IA a partir del estilo: no hay detector confiable. La evidencia de uso es documental (menciones, archivos, enlaces, commits).

**Datos no verificables.** CAT-IA los equipara al uso no declarado. Se registran en `REF-02` y `DAT-01` con fundamento en el Art. 10.1.2 (segundo inciso), el 18.1.7 y el 18.1.8 de la RR 97/23.

**Enlaces de conversación.** El docente puede abrirlos (requieren navegador; algunos piden iniciar sesión). El harness los lista; no los descarga.

## §indicadores — Indicadores verificables de integridad (`ETH-01`)

Se registran con ubicación y se convierten en preguntas para que el estudiante dé cuenta oralmente:
- Referencias "Fabricada" o "No localizada"; datos atribuidos a una fuente que no los contiene (`REF-02`).
- Búsqueda INPI, contactos o validaciones sin constancia.
- Cifras centrales sin fuente.
- Cambios bruscos de registro, persona gramatical o terminología entre capítulos.
- Secciones del Cap. XII casi idénticas entre integrantes.
- Texto dirigido a un evaluador o a un modelo en el PDF o el repositorio (`sdd_harness.json#injection`): hallazgo en sí mismo.
- Menciones de herramientas de IA fuera del apartado de declaración.

## §oral — Dar cuenta oralmente (`ORA-01`, solo informe docente)

Fundamento: la cláusula CAT-IA ("en todas las producciones entregadas se le podrá pedir que dé cuenta oralmente"), el Art. 8.2.4 (evaluar el proceso y la participación de cada estudiante) y el Art. 11 (aprobación docente previa a la defensa). En reentregas se concreta en el **coloquio previo** de la devolución.

El harness arma un banco de preguntas por integrante, en tres planos:
- **Dar cuenta:** qué hizo, cómo lo hizo, qué aportó, qué cambió a partir de la devolución.
- **Fundamentar:** por qué tomó cada decisión, con qué conceptos o autores, qué alternativa descartó.
- **Profundizar:** consecuencias, límites, qué haría distinto; fragmentos asistidos por IA (qué pidió, qué aceptó, qué corrigió y cómo lo verificó).

Si hay indicadores con evidencia concreta (§indicadores), el informe docente **propone** pedir que el o los integrantes den cuenta oralmente de esos puntos, citando los IDs. Es decisión docente; en la devolución a los estudiantes no se mencionan sospechas, solo observaciones con evidencia.

## §datos — Datos personales

Datos reales de personas identificables: anonimizados o con consentimiento documentado; los datos sensibles no van al repositorio ni a los anexos (Ley 25.326). Expuestos: ROJO con pedido de remoción y, si son credenciales, rotación.

## §trazabilidad — Evidencias de proceso

La trazabilidad del PIF se apoya en el historial de commits (con los límites de `05 §trazabilidad`), el tablero de gestión (Art. 20, entrega digital), las versiones entregadas registradas en `review_state.json`, la declaración CAT-IA, el coloquio y, en las entregas de AE, el Portafolio y las Bitácoras.

## §portafolio — Portafolio Digital y Bitácora Individual (`PRC-01`, solo entregas parciales de AE)

Aplica cuando `exige_portafolio_bitacora = true` (AE1, AE2, AE4). En la versión final del PIF no se verifica.

**Reglas de la Guía de Evaluación Multimodal (GD2):**
- Cada componente se registra **COMPLETO** ("presentado y reúne los mínimos requeridos; no significa excelencia") o **INCOMPLETO** ("falta, es insuficiente y requiere reelaboración") (GD2 7). Portafolio y bitácora son componentes de cierre: si falta uno, la AE no puede cerrarse aunque el producto sea suficiente.
- **Portafolio** = espacio de las Actividades de Proceso: borradores y versiones, registros de campo, entrevistas o evidencias, decisiones y justificaciones, devoluciones y ajustes, productos parciales, pruebas y reflexiones (GD2 8.1).
- **Bitácora:** "Toda AE grupal debe tener una evidencia individual correlativa". Siempre individual; "no debe reducirse a una crónica del tipo 'nos reunimos y repartimos tareas'": recupera decisiones reales, dificultades, alternativas, relación con las evidencias del Portafolio y fundamentos (GD2 8.2).

**Contenido que pide cada consigna** (`audit_proceso.py` lo busca por nombre y contenido de archivo):

| AE1 | AE2 | AE4 |
| --- | --- | --- |
| a) Instrumentos 1 a 22 (ficha de intereses, acta de constitución firmada, precalificación, PESTEL, cinco fuerzas, cadena de valor, FODA, registro de fuentes); b) evidencia de contacto (correos, actas, guías de entrevista, respuestas); c) versiones sucesivas; d) enlaces a repo y tablero; e) devolución y versión mejorada | a) Instrumentos de la Unidad Dos (delimitación, lienzo, rivalidad amplificada, recursos); b) **matriz de trazabilidad** hallazgo → requisito → componente; c) acta de validación de requisitos con el referente; d) versiones del documento y del catálogo; e) registro de corridas de CI; f) devolución de AE1 y constancia de correcciones | a) Instrumentos de la Unidad Cuatro (hoja de ruta, factibilidad ponderada, búsqueda marcaria, supuestos y experimentos de escalabilidad); b) actas de revisión y retrospectiva de los sprints; c) plan de implantación y acta de cierre; d) corridas de CI y verificación del manual en máquina limpia; e) versiones sucesivas del informe; f) devoluciones y constancia de correcciones; g) guion de la demostración y protocolo de contingencia |

**Bitácora — seis elementos por entrada fechada** (consignas AE1, AE2, AE4): 1) qué se decidió; 2) qué alternativas se evaluaron y con qué criterio se descartaron; 3) qué evidencia sostiene la decisión; 4) qué aportó personalmente el autor, con remisión al commit, tarjeta o apartado; 5) qué desacuerdo hubo y cómo se resolvió según el acta de constitución; 6) qué herramienta auxiliar se usó y con qué alcance. En AE4 cubre las semanas 13 a 15.

**Cómo informar:** una fila por componente (portafolio; bitácora de cada integrante) con la propuesta COMPLETO / INCOMPLETO, los elementos faltantes y la evidencia a presentar. Señales para el docente (no conclusiones): bitácoras casi idénticas entre integrantes, bitácora sin decisiones (crónica), menos de dos entradas fechadas. El registro definitivo es del docente.

**Relación con la declaración de IA:** el punto 6 de la bitácora registra la herramienta y su alcance en el proceso; la cláusula CAT-IA exige además el apartado final de declaración en la producción entregada. Se verifican ambos.
