# Devolución — Quark Anticheat (segunda pasada de autorrevisión, 2026-11-26)

No hay observaciones bloqueantes. Quedan 14 corregibles, que se resuelven con datos y decisiones de los autores o con cambios en `Dev`.

| N.º | Artículo | Observación | Qué se espera | Evidencia a presentar |
| --- | --- | --- | --- | --- |
| OBS-02/15 | CAT-IA; 10.1.2 | La declaración de IA existe (p. 162–163) pero falta el enlace y los prompts de las sesiones de redacción y autorrevisión, y confirmar otras herramientas. | Enlace y prompts de cada sesión, o declarar que no existen. | Apartado completado. |
| OBS-12/20 | 3; 24.3.13 | El Anexo III.5 es el manual de despliegue pero no se ejecutó; `Dev` no tiene manual propio ni CI. | Manual ejecutado en una VM limpia. | Log de la corrida y commit. |
| OBS-14/21 | 20; 24.3.13 | `Dev` no tiene LICENSE ni etiqueta de versión. | LICENSE y tag en la versión entregada. | Archivo, tag y colaboradores con acceso de la cátedra. |
| OBS-03/16 | 20 | Faltan el tablero de gestión entre los entregables y el tag. | Cap. XIII completo. | Cap. XIII corregido. |
| OBS-17 | 22.1 | La carátula no tiene el logo de la UCP. | Logo en la carátula. | Página 1. |
| OBS-18 | 4; 24.3.5 | El Cap. V 5.3 asigna roles pero no reparte actividades por integrante. | Tabla de actividades y responsabilidades. | Tabla en 5.3. |
| OBS-19 | 24.3.10 | El Cap. X no tiene cifras financieras; el Cap. XI no tiene supuestos ni hipótesis. | Costos con cifras y supuestos. | Tabla de costos con tarifa declarada. |
| OBS-07 | 24.3.2 | Encuesta diseñada y no publicada: sin n. | Datos con n o alcance documental acordado. | Resultados o acta. |
| OBS-08 | 24.3.8 | INPI: faltan "anticheat", variantes y capturas fechadas. | Búsqueda completa. | Capturas con fecha. |
| OBS-10 | 20 | La fuente es TeX Gyre Termes (clon métrico de Times). | Times New Roman 12 o aceptación docente. | `pdffonts` o constancia. |
| OBS-13 | 10.1.2; 18.1.7 | Entradas con "URL pendiente de aportar" y 5 referencias sin localizar. | URL o DOI completos. | Fuente por entrada. |
| OBS-01 | 18.1.6 | Control negativo invalidado por `feature/gameStartProtection`. | Re-ejecutar o acotar a `Dev@35c6031`. | Captura con commit. |

Resueltas respecto de la pasada anterior: carátula, `{#…}`, numeración de anexos, bloque firmado por agente y URL oficial del repositorio. El Resumen cumple el límite (446 palabras).

## Matriz de respuesta
Una fila por OBS vigente. La columna "Uso de IA" es obligatoria.

| N.º | Observación | Cambio realizado | Ubicación (pág./archivo) | Evidencia presentada | Responsable | Uso de IA |
| --- | --- | --- | --- | --- | --- | --- |
| OBS-01 | El Anexo III declara que feature/gameStartProtection invalida el control negativo; el informe lo avisa, pero la conclusión depende de un control que no es reproducible fuera de Dev@35c6031. |  |  |  |  |  |
| OBS-07 | El Cap. II declara que la encuesta fue diseñada y no publicada: no hay datos primarios ni n. El capítulo usa investigación documental e hipótesis provisionales, y lo dice. Quedan sin cubrir instrument |  |  |  |  |  |
| OBS-08 | La búsqueda INPI cubre 'quark' y 'quark anticheat'; no consta la búsqueda de 'anticheat' ni de variantes fonéticas (confirmar leyendo el Cap. VIII). |  |  |  |  |  |
| OBS-10 | El PDF usa TeX Gyre Termes (clon métrico de Times), no Times New Roman (fonts: FALLA). Margen derecho fuera de tolerancia solo en la p.19; 3 de 53 páginas (2-4) con interlineado menor a 1,9×. |  |  |  |  |  |
| OBS-13 | Hay entradas que declaran fuente no consultada o incompleta ('URL: pendiente de aportar', 'contenido tomado de resumen de búsqueda'). Indicador de Capa 1 (a revisar a mano): 5 referencias quedaron 'No |  |  |  |  |  |
| OBS-15 | Hay apartado de declaración con para qué, verificación, prompts por referencia y un enlace real (sesión de desarrollo). Faltan el enlace de las sesiones de redacción y autorrevisión, la transcripción  |  |  |  |  |  |
| OBS-16 | La URL oficial y el commit constan en el Cap. XIII y el PDF se generó desde un commit limpio. Faltan el tablero de gestión entre los entregables digitales y la etiqueta de la versión. El aviso de 5 UR |  |  |  |  |  |
| OBS-17 | La carátula incluye universidad, facultad, carrera, denominación, título, autores y fecha, pero no logo de la UCP (Art. 22.1 lo exige; sin archivo en el repositorio). |  |  |  |  |  |
| OBS-18 | El Cap. V 5.3 asigna roles pero no reparte actividades por integrante con evidencia (Art. 4). Faltan 'pérdida de un integrante' (riesgo, Cap. V) y 'definición de terminado' y 'retrospectiva' (Cap. VI) |  |  |  |  |  |
| OBS-19 | El Cap. X 10.3 no da cifras: declara financiamiento nulo y horas no registradas. El Cap. XI no tiene supuestos, hipótesis, métrica accionable ni umbral de decisión según el .tex (estándar de cátedra). |  |  |  |  |  |
| OBS-20 | El Anexo III.5 pasa a ser el manual de despliegue, pero declara que no se ejecutó, y Dev@35c6031 sigue sin manual propio ni CI. Mejora respecto de la pasada anterior (ROJO); sin ejecución no hay evide |  |  |  |  |  |
| OBS-21 | El Cap. XIII identifica repositorio y commit 35c6031, pero Dev no tiene LICENSE ni etiqueta de la versión entregada. |  |  |  |  |  |
