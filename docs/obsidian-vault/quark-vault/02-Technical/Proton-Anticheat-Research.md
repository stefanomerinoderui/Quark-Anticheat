---
title: Investigación de anticheats bajo Proton
tags: [investigacion, mercado, eac, battleye]
status: canonical
created: 2026-11-13
---

# Investigación de anticheats bajo Proton

Nota-puente (ledger, append-only, [[Append-Only-Standard]]). El trabajo vive **fuera de este repo**, en `proton-anticheats` (repositorio git propio, último commit `cc5078e`, 2026-11-13, 10 commits desde 2026-11-06). Usada en el informe: [[Informe-PIF-Avance]] Update 2026-11-13, §D–E.

## Qué es
Ingeniería inversa y trazas de los *runtimes* de Easy Anti-Cheat y BattlEye bajo Proton, para decidir qué copiar y qué no en Quark. Etiquetas del material: **[O]** observado, **[I]** inferido, **[B]** información pública no verificada.

| Documento | Estado |
|---|---|
| `EAC.md`, `EAC_bridge_and_quark_takeaways.md` | Hecho. El *runtime* de Proton es solo un puente; el cliente real lo trae cada juego |
| `EAC_Linux_Module_Runtime.md`, `EAC_Linux_Module_Behaviour.md` | Hecho (un juego, sin juego en línea) |
| `EAC_BPF_LSM_Service.md` | **Investigación documental [B]/[I]**; captura bloqueada hasta que exista un juego con EAC v2 |
| `BattlEye.md`, `BattlEye_Unpacked.md` | Hecho; cliente empaquetado y virtualizado, solo legible en parte |
| `BattlEye_PostInit.md`, `EAC_Legacy_GameModule.md` | En curso / esperando acción del usuario |
| `Validation_Log.md` | 45 afirmaciones [I]: 6 confirmadas, el resto abiertas o bloqueadas |
| `analysis-plan/10_synthesis_quark.md` | **Pendiente:** matriz de funcionalidades de síntesis (`Quark_Feature_Matrix.md` no existe) |

## Decisión de integración (propuesta, 2026-11-13)
1. **No copiar al repo de Quark.** Tiene historia propia, contiene capturas derivadas de binarios propietarios (los binarios mismos no se versionan) y duplicaría 3.300 líneas. En el vault solo vive esta nota, con el commit de referencia.
2. **La copia sin versionar `Quark-Anticheat/proton-anticheats/` está desactualizada** (le faltan `EAC_BPF_LSM_Service.md`, `EAC_Config_Formats.md`, `EAC_Legacy_GameModule.md`, `EAC_Linux_Module_Behaviour.md`, `BattlEye_PostInit.md` y varios scripts). Borrarla o agregarla a `.gitignore` cuando el equipo lo decida; no se tocó.
3. **Qué entra al informe:** solo los hallazgos con su etiqueta de alcance (Update del informe, §D–E). EAC v2 se presenta como **información pública**, no como observación propia.
4. **Qué entra al backlog de Quark** (de `EAC_bridge_and_quark_takeaways.md` §3 y `EAC_BPF_LSM_Service.md` §7), todo posterior a la defensa salvo decisión contraria: atestación verificada por servidor (raíz de confianza abierta), gancho `lsm/mmap_file`, reporte tipado de violaciones, canal por la red del juego, cita TPM 2.0.
5. **Antes de citar como evidencia:** cerrar o marcar `UNVERIFIED` cada fila abierta de `Validation_Log.md` que se use.

## Contradicciones con el vault
- `Features` §1.5 y `Known-Limitations` Update dicen que BPF-LSM es el camino viable; la investigación muestra que EAC v2 hace lo mismo. **No contradice**, pero cambia el argumento diferencial del informe (Cap. II Update).
