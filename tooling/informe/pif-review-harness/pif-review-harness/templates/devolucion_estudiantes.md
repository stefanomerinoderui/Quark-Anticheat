<!--
PLANTILLA — Devolución formal a los estudiantes (avances, informe final y reentregas del PIF). Marco: RR 97/23 + cláusula de cátedra CAT-IA.
Tono: español rioplatense ("ustedes"), profesional y directo. Sin datos de commits por persona, sin rúbrica, sin sospechas.
Fuente: findings_final_<INST>.json con destino "devolucion" o "ambos"; OBS-xx tal como quedaron en review_state.json.
Reglas: cada OBS con "Qué se espera" y "Evidencia a presentar". En la versión final ninguna OBS pide bitácora ni portafolio: la evidencia vive en el informe y en la matriz. En las entregas de AE se incluye la sección 8 bis. Nunca nota, cierre ni regularidad.
Convertir a Word si hace falta: pandoc <archivo>.md -o <archivo>.docx
-->

# Devolución del Proyecto Integrador Final — {{titulo}}

{{Frase inicial con el veredicto: "En su estado actual, el PIF no está en condiciones de ser elevado al tribunal. Para eso es necesario resolver las observaciones obligatorias de esta devolución y validar el coloquio previo."}}

| | |
| --- | --- |
| Asignatura | Proyecto Final de Grado — Ingeniería en Sistemas de Información |
| Proyecto | {{titulo}} |
| Estudiantes | {{integrantes}} |
| Versión evaluada | {{pdf_archivo}} · repositorio {{repo_url}} @ {{ref}} |
| Marco normativo | Resolución Rectoral UCP N.º 97/23 (Reglamento General del PIF); cláusula de cátedra sobre declaración de uso de IA |
| Modalidad que corresponde | {{23.x — nombre}} |

## 1. Encuadre normativo

La aprobación del PIF está a cargo de los docentes de la asignatura y es la que habilita la defensa oral ante el tribunal (Art. 11). El tribunal califica entre 6 y 10, "dado que el estudiante aprobó la primera instancia" (Art. 18.2): por eso el control de calidad es previo y está a cargo de la cátedra. El equipo docente devuelve el material con retroalimentaciones e indica las modificaciones necesarias (Art. 8.2.2), evalúa el proceso de producción y la participación de cada estudiante en los trabajos grupales (Art. 8.2.4) y evalúa el informe final en un plazo no mayor a veinte días (Art. 8.2.6). Los estudiantes responden por cualquier falseamiento o adulteración voluntaria de la información (Art. 10.1.2, segundo inciso). Esta devolución y el coloquio previo son los instrumentos de los Art. 8.2.2, 8.2.4 y 8.2.6, y su resultado es la aprobación del Art. 11.

## 2. Valoración general

{{Fortalezas reales y avances respecto de la versión anterior, con ejemplos concretos y páginas.}}

{{Las observaciones que surgen del estándar de contenido de cátedra (no del reglamento) se presentan en la sección 5 como mejoras, no como obligatorias.}}

## 3. Observaciones obligatorias (RR 97/23)

| N.º | Artículo | Observación | Qué se espera | Evidencia a presentar |
| --- | --- | --- | --- | --- |
| OBS-01 | {{Art.}} | {{…}} | {{…}} | {{…}} |

## 4. Inconsistencias internas (Art. 18.1.6)

{{N}}. **OBS-xx — {{título}}.** {{Descripción con páginas.}}
   Evidencia: {{qué tiene que quedar en la nueva versión}}.

## 5. Formato, redacción, bibliografía y estándar de contenido de cátedra

{{N}}. **OBS-xx — {{título}}.** {{…}}
   Evidencia: {{…}}.

## 6. Verificación de referencias

Fecha y método: {{fecha}}; consulta a Crossref y OpenAlex por DOI y por título{{, búsquedas web registradas}}.

| N.º | Referencia (autor, año) | Estado | Discrepancia o búsqueda realizada | Acción requerida |
| --- | --- | --- | --- | --- |
| {{n}} | {{…}} | {{Fabricada / No localizada / Con discrepancias}} | {{…}} | {{aportar la fuente real o eliminar y reescribir el párrafo}} |

Referencias verificadas sin observaciones: {{lista en una línea}}. Las no revisadas individualmente se rigen por la observación de formato APA.

**Afirmaciones con datos verificadas contra su fuente:**

| Afirmación | Página del PIF | Fuente citada | ¿La respalda? |
| --- | --- | --- | --- |
| {{…}} | {{…}} | {{…}} | {{Sí / Sí, con reservas / Parcialmente / No / No verificable}} |

**Cruce citas ↔ Bibliografía:** {{citas sin entrada, entradas no citadas, duplicados}}.

## 7. Matriz de respuesta a observaciones

Pautas: completar una fila por observación; indicar página o archivo exacto de la nueva versión; la columna "Uso de IA" es obligatoria: "No se utilizó" o la remisión al apartado final de declaración (para qué, verificación, prompts y enlace). **Sin la matriz completa, la reentrega no se evalúa.**

{{Pegar la salida de: python3 scripts/state.py matriz --id <id>}}

## 8. Declaración de uso de inteligencia artificial

> Si utilizó herramientas de IA generativa, debe declararlo en un apartado final indicando para qué se usó y cómo se verificó la información obtenida. Se deben indicar los prompts utilizados y compartir el enlace a la conversación con la herramienta de IA Generativa seleccionada. El uso no declarado, o la incorporación de datos no verificables, se registra con las observaciones correspondientes a los reglamentos. Tenga presente que en todas las producciones entregadas se le podrá pedir que dé cuenta oralmente.

{{Resultado de DIA-01 en una o dos oraciones: declaración completa / qué elementos faltan / uso no declarado (con la OBS correspondiente).}}

Los estudiantes responden por cualquier falseamiento o adulteración voluntaria de la información (RR 97/23, Art. 10.1.2, segundo inciso); un dato que no puede verificarse, o una fuente que no dice lo que se le atribuye, se observa con ese fundamento y el de los Arts. 18.1.7 y 18.1.8.

## 8 bis. Portafolio Digital y Bitácora Individual (solo entregas parciales de AE)

Conforme a la Guía de Evaluación Multimodal, el Portafolio y la Bitácora Individual de cada integrante son componentes de la entrega. La Bitácora debe registrar, por entrada fechada, qué se decidió, qué alternativas se evaluaron, qué evidencia sostiene la decisión, qué aportó cada integrante, qué desacuerdos hubo y qué herramientas auxiliares se usaron.

| Componente | Propuesta | Elementos faltantes / señales | Evidencia a presentar |
| --- | --- | --- | --- |
| Portafolio Digital | {{COMPLETO / INCOMPLETO}} | {{…}} | {{…}} |
| Bitácora — {{integrante 1}} | {{COMPLETO / INCOMPLETO}} | {{…}} | {{…}} |
| Bitácora — {{integrante 2}} | | | |

*COMPLETO = presentado y con los mínimos requeridos; no significa excelencia (Guía de Evaluación Multimodal, 7). El registro definitivo es del docente.*

## 9. Acceso y visibilidad del repositorio de código

- Dar acceso a **lapertosasergio_cen@ucp.edu.ar** antes de la reentrega: repositorio público (verificar que abra sin iniciar sesión), colaborador en cuenta personal o rol Read en organización.
- Repositorio único y oficial, coincidente con el Cap. XIII; etiqueta de la versión entregada; historial completo sin force push ni squash de lo publicado; autoría identificable; README con estructura y ejecución; sin credenciales ni datos personales (`.env` en `.gitignore`; claves expuestas, rotadas).
- Evidencia: URL y etiqueta; captura de colaboradores o de la visibilidad pública; captura del historial con aportes de todos los integrantes.

## 10. Coloquio previo a la aceptación del PIF

Individual, unos 15 minutos por integrante, después de la reentrega con la matriz completa. Cada integrante: recorre la matriz y muestra la evidencia que el docente elija; fundamenta decisiones y alternativas descartadas; navega el código en el repositorio y muestra la aplicación funcionando; explica los fragmentos asistidos por IA; muestra la fuente original de las referencias observadas. Resultado por integrante: **Validado** (se acepta el PIF y se habilita la inscripción a la defensa, Art. 12 y 13) o **No validado** (la cátedra indica qué reforzar y fija nueva fecha). No reemplaza la defensa ante el tribunal.

## 11. Preguntas para preparar el coloquio y la defensa

1. {{5 a 8 preguntas específicas del proyecto: validación, escalabilidad, seguridad y datos personales (Ley 25.326), costos vs. ingresos, aporte de cada integrante}}

## 12. Próximos pasos

{{Fecha acordada para la próxima versión. Los cambios de código se subsanan con trazabilidad explícita en el repositorio (commits y etiqueta).}}

- [ ] Resolver OBS-01 a OBS-{{nn}}.
- [ ] Completar la matriz de respuesta (incluida la columna de uso de IA).
- [ ] Incluir el apartado final de declaración de uso de IA (para qué, verificación, prompts y enlace) o declarar que no se utilizó.
- [ ] Dar acceso al repositorio y etiquetar la versión de la reentrega.
- [ ] Acordar fecha del coloquio previo.
- [ ] Tras la aprobación: copia a Dirección de Carrera 5 días hábiles antes de la defensa (Art. 14); ejemplar digital y Formulario N.º 2 (Art. 19).
