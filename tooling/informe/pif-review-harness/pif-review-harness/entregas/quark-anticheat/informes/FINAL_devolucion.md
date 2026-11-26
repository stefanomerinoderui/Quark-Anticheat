# Devolución del Proyecto Integrador Final — Quark Anticheat (autorrevisión)

En su estado actual, el PIF no está en condiciones de ser elevado al tribunal: hay 2 observaciones bloqueantes (OBS-02 y OBS-12) y 12 corregibles. Esta devolución sale de una autorrevisión con el harness; no la emite la cátedra.

| | |
| --- | --- |
| Asignatura | Proyecto Final de Grado — Ingeniería en Sistemas de Información |
| Proyecto | Quark Anticheat |
| Estudiantes | Martínez Alarcón, Gabriel Sebastián; Merino De Rui, Stefano Nahuel |
| Versión evaluada | `Informe-PIF-2026-11-25.pdf` · `Dev@35c6031` · `dev/docs@ea676de` |
| Marco normativo | RR 97/23; cláusula de cátedra de uso de IA |
| Modalidad | 23.2 Diseño y Desarrollo |

## 1. Valoración general
Las Conclusiones (p. 158) separan lo medido de lo no medido y limitan la defensa al alcance probado. El Cap. II declara que la encuesta no se publicó y no inventa datos. No se detectaron secretos ni texto dirigido a evaluadores.

## 2. Observaciones obligatorias (RR 97/23)

| N.º | Artículo | Observación | Qué se espera | Evidencia a presentar |
| --- | --- | --- | --- | --- |
| OBS-02 | 10.1.2, 18.1.8; CAT-IA | No hay apartado final de declaración de uso de IA; el PDF contiene firmas `agent:claude-sonnet-5-5` (p. 4, 185). | Apartado final: para qué, cómo se verificó, prompts y enlace a la conversación. | Apartado con las cinco partes. |
| OBS-12 | 3, 24.3.13 | En `Dev@35c6031` no hay manual de despliegue ni plan de construcción inferible, ni CI. | Un tercero construye y arranca el sistema solo con el manual. | Sección de README con pasos y tag de la versión. |
| OBS-03 | 20 | La versión se generó con "cambios sin commitear"; el PDF cita URL de repositorio distintas. | Una URL oficial, coincidente con el Cap. XIII, y PDF de un commit etiquetado. | Commit o tag y Cap. XIII. |
| OBS-04 | 22.1 | Carátula sin universidad, facultad, carrera ni "Proyecto Integrador Final". | Carátula completa. | Página 1 corregida. |
| OBS-06 | 22.2 | Resumen de 696 palabras según el script. | Hasta 600 palabras. | Páginas 5–6 con conteo. |
| OBS-05 | 22.3, 22.4 | Atributos `{#…}` impresos en 16 páginas (carátulas, índice, notas). | Títulos limpios. | Págs. 2–4, 7, 132, 149, 184. |
| OBS-09 | 20, 22.7 | Anexos sin numeración "página X de Y". | Numeración independiente. | Páginas de anexos. |
| OBS-10 | 20 | Fuente TeX Gyre Termes en lugar de Times New Roman; márgenes ~2,9 cm. | Times New Roman 12, márgenes 3 / 2,5 cm. | Salida de `pdffonts`. |
| OBS-11 | 21 | Bloques "Update" con firma de agente y notas de edición del vault. | Un solo cuerpo, impersonal; el historial queda en git. | Índice y páginas sin los bloques. |
| OBS-14 | 20, 24.3.13 | LICENSE (GPLv3) solo en `dev/docs`; no está en el código entregado. | LICENSE en la versión entregada. | Archivo y tag. |
| OBS-07 | 24.3.2 | Encuesta diseñada y no publicada: sin n ni datos primarios. | Datos con n y análisis, o alcance documental acordado. | Resultados o acta. |
| OBS-08 | 24.3.8 | INPI: faltan "anticheat", variantes fonéticas y capturas con fecha; sin logotipo. | Búsqueda completa con constancia. | Capturas fechadas. |

## 3. Inconsistencias internas (Art. 18.1.6)
1. **OBS-01 — Control negativo.** El Anexo III (p. 170) declara que `feature/gameStartProtection` invalida el control "sin Quark". Evidencia: re-ejecución o acotación explícita a `Dev@35c6031`, con captura y commit.

## 4. Formato, bibliografía y estándar de cátedra
1. **OBS-13 — Fuentes con verificación pendiente.** P. 161–162: "URL: pendiente de aportar" y "contenido tomado de resumen de búsqueda". Evidencia: URL o datos completos de cada fuente y consulta directa.

## 5. Verificación de referencias
Método: Crossref y OpenAlex automáticos (2026-11-25), sin búsqueda manual. De 17 entradas detectadas: 1 verificada, 2 con discrepancias, 5 no localizadas, 9 accesibles sin cotejo del contenido. Varios casos provienen de la extracción del PDF y no se confirman. No hay ninguna marcada "Fabricada". Acción: aportar DOI o URL completa de las 5 no localizadas (It's FOSS 2026, Ojeda 2025, The kernel development community 2024a y 2024b, Valve Developer Community s. f.) y revisar a mano el cruce citas↔bibliografía.

## 6. Matriz de respuesta a observaciones
Una fila por OBS; indicar página o archivo exacto. La columna "Uso de IA" es obligatoria.

| N.º | Observación | Cambio realizado | Ubicación (pág./archivo) | Evidencia presentada | Responsable | Uso de IA |
| --- | --- | --- | --- | --- | --- | --- |
| OBS-01 | El Anexo III declara que feature/gameStartProtection invalida el control negativo; el informe lo avisa, pero la conclusión depende de un control que no es reproducible fuera de Dev@35c6031. |  |  |  |  |  |
| OBS-02 | No hay apartado final de declaración de uso de IA y el PDF mismo contiene firmas 'agent:claude-sonnet-5-5'; el repo tiene archivo de contexto de agentes. |  |  |  |  |  |
| OBS-03 | La versión entregada no corresponde a un commit publicado ('+cambios sin commitear'). El PDF cita URL de repositorio distintas (una con posible errata 'quark-anticheaty' y otra a recoilengine); confir |  |  |  |  |  |
| OBS-04 | La carátula no muestra universidad, facultad, carrera ni la denominación 'Proyecto Integrador Final'; la fecha lleva '+cambios sin commitear'. |  |  |  |  |  |
| OBS-05 | Atributos de Pandoc ({#…}) aparecen impresos en carátulas de capítulo, índice y notas, en 16 páginas. Por esos residuos el detector no reconoció ninguna de las 13 carátulas de capítulo. |  |  |  |  |  |
| OBS-06 | El Resumen cuenta 696 palabras según el script (límite 600). Falta confirmar el conteo a mano. |  |  |  |  |  |
| OBS-07 | El Cap. II declara que la encuesta fue diseñada y no publicada: no hay datos primarios ni n. El capítulo usa investigación documental e hipótesis provisionales, y lo dice. Quedan sin cubrir instrument |  |  |  |  |  |
| OBS-08 | La búsqueda INPI cubre 'quark' y 'quark anticheat'; no consta la búsqueda de 'anticheat' ni de variantes fonéticas (confirmar leyendo el Cap. VIII). |  |  |  |  |  |
| OBS-09 | Los anexos no tienen numeración 'página X de Y' (0 de 110 páginas); el propio texto dice que se completa al maquetar. |  |  |  |  |  |
| OBS-10 | El PDF usa TeX Gyre Termes (clon métrico de Times), no Times New Roman (fonts: FALLA). Margen derecho fuera de tolerancia solo en la p.19; 3 de 53 páginas (2-4) con interlineado menor a 1,9×. |  |  |  |  |  |
| OBS-11 | El documento conserva bloques 'Update' con firma de agente y notas de edición propias del vault ('se conserva sin cambios como historial'). Rompe el registro impersonal uniforme del Art. 21 y el docum |  |  |  |  |  |
| OBS-12 | No se localizó manual de despliegue ni plan de construcción inferible en Dev@35c6031, y no hay CI; la construcción no se ejecutó. Sin manual no hay evidencia de que un tercero pueda construirlo y arra |  |  |  |  |  |
| OBS-13 | Hay entradas que declaran fuente no consultada o incompleta ('URL: pendiente de aportar', 'contenido tomado de resumen de búsqueda'). Indicador de Capa 1 (a revisar a mano): 5 referencias quedaron 'No |  |  |  |  |  |
| OBS-14 | LICENSE (GPLv3) existe solo en dev/docs; el código entregado (Dev@35c6031) no la tiene. La referencia evaluada es un commit, no una etiqueta. |  |  |  |  |  |

## 7. Próximos pasos
- [ ] Resolver OBS-01 a OBS-14, empezando por OBS-02 y OBS-12.
- [ ] Completar la matriz, con la columna de uso de IA.
- [ ] Dar acceso al repositorio a lapertosasergio_cen@ucp.edu.ar y etiquetar la versión.
- [ ] Revisar los capítulos que esta pasada no leyó (I, III–VII, IX–XIII).
