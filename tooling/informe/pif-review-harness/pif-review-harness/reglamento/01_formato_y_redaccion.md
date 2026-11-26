# 01 — Formato, redacción y ortografía

Ítems que cargan este módulo: `FMT-01`, `FMT-02`, `FMT-03`, `EST-01` (sección Carátula).

## §formato — Aspectos formales (RR97 Art. 20)

Se verifican sobre el documento completo (RR97 Art. 20).

| Control | Regla | Artifact | Cómo se mide | Tolerancia |
| --- | --- | --- | --- | --- |
| Hoja | A4 (595 × 842 pt) | `pdf_format.json#page_size` | Tamaño de página | ± 3 pt |
| Margen izquierdo / derecho | 3 cm (≈ 85 pt) | `#margins` | Extremo del texto del cuerpo, mediana sobre páginas de cuerpo | − 6 pt |
| Margen superior | 2,5 cm (≈ 71 pt) | `#margins` | Primer renglón del cuerpo, excluyendo encabezado | − 6 pt |
| Margen inferior | 2,5 cm | — | **No medir**: el pie de página contamina la medición. No usar como evidencia. | — |
| Interlineado | Doble | `#line_spacing` | Distancia mediana entre líneas base / tamaño de fuente | ≥ 1,9 (Word "doble" ≈ 2,3) |
| Tipografía | Times New Roman 12 en cuerpo; 10 en notas y citas al pie | `#fonts` | Proporción de caracteres en fuentes "Times" y tamaño predominante | ≥ 85 % |
| Numeración | Correlativa en el cuerpo; anexos con numeración propia "página X de Y" | `#page_numbers`, `#annex_numbering` | Número impreso detectado en encabezado/pie | — |
| Unidades | SIMELA / SI | `coherence.json#units` | Unidades no SI detectadas (pulgadas, millas, libras, °F) | revisar caso |
| Entrega digital | Documentación del PIF + código fuente, tablero de gestión y demás datos digitales | `repos.json` | | — |
| Títulos, encabezado y pie | Libre elección (Art. 20) | — | No se observan | — |
| Láminas | Dentro del capítulo, numeradas como una página; plegado según IRAM | — | Revisión visual | — |

**Interpretación:** un desvío en pocas páginas aisladas (tablas, figuras) es AMARILLO con la lista de páginas. Desvío sistemático también es AMARILLO, salvo que el perfil lo marque bloqueante. Si `pdf_format.json` no se pudo generar (PDF escaneado, sin texto), GRIS y pedir verificación visual con `pdftoppm -r 50`.

## §redaccion — Redacción (RR97 Art. 21)

- Impersonal: sin primera persona ("hicimos", "nuestro sistema", "consideramos"). `pdf_format.json#first_person` lista candidatos por página.
- Verbos en presente y en afirmativo.
- Criterio uniforme de formato (títulos, numeración de figuras y tablas, estilo de citas).
- Literal: "No deberán exponerse desarrollos teóricos, ni plantearse discusiones o alternativas ajenas al desarrollo específico del tema del proyecto" (definiciones de manual extensas, marcos teóricos genéricos, discusiones que no deciden nada del proyecto).

**La deliberación no va en el cuerpo (estándar de cátedra, derivado del Art. 21):** el cuerpo consigna la decisión, su fundamento y la alternativa descartada de manera sintética; el razonamiento completo va en la bitácora y en los anexos.

**Excepción de cátedra:** en el **Capítulo XII (Lecciones Aprendidas)** la cátedra admite secciones individuales, firmadas, en primera persona sobre el aporte propio. La primera persona allí no se observa. La primera persona en Cap. XII no es observación; su ausencia, o un Cap. XII redactado en plural impersonal para todo el equipo, sí lo es (ver `02_estructura_capitulos.md §cap12`).

**Registro uniforme (estándar de cátedra; Art. 21 "criterio uniforme"):** el documento consolidado no puede leerse como una yuxtaposición de entregas previas (cambios de persona gramatical, de terminología o de formato entre capítulos). Registrar ejemplos con página.

## §ortografia — Ortografía y redacción (`FMT-03`)

Fundamento: presentación escrita "clara, con secuencia lógica, coherencia, información completa y fehaciente" (RR97 18.1.8) y las sugerencias "para una redacción clara y precisa, con lenguaje técnico apropiado" (8.2.2). No se calculan descuentos: son propios de las AE y no se verifican en el PIF.

- `languagetool.json` (si está disponible) aporta **candidatos**. El harness informa cantidades y ejemplos; el docente confirma cuáles son errores en `artifacts/ortografia_confirmada.json`.
- Observación en la devolución: AMARILLO con la lista de páginas y ejemplos confirmados, y la evidencia de corrección.
- **Reiteración:** si una observación formal de una devolución anterior reaparece, `SEG-01` la marca como reincidente por su clave.

## §caratula — Carátula (RR97 22.1) y tapa (RR97 20)

- Logo y nombre de la UCP.
- Facultad: la RR97 (2023) dice "Facultad de Ingeniería y Tecnología"; la denominación vigente en 2026 es **Facultad de Ingeniería, Tecnología y Arquitectura** (AE26). Se aceptan ambas; se sugiere la vigente.
- Carrera exacta: **Ingeniería en Sistemas de Información**.
- Denominación **Proyecto Integrador Final**.
- Título, autores, año de presentación.
- Sin numerar.
- **Tapa** (Art. 20, para el ejemplar impreso): dura, con Universidad, Facultad, Carrera, "Proyecto Integrador Final", título, nombre del alumno, mes y año en curso. En la entrega digital se controla la carátula del Art. 22.1.

`coherence.json#caratula` informa qué textos se encontraron en la primera página.
