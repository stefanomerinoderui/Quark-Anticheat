---

kanban-plugin: board

---

## Backlog

- [ ] Medir overhead de CPU/RAM con y sin módulo (requerido por MVP/H5) #testing #H5
- [ ] Corregir harness de captura: `results.csv` malformado y `summary.txt` solo con condición B #testing #bug
- [ ] Registrar `git_commit`/`git_branch` en `environment.txt` y re-capturar sobre el build del repo #testing #bug
- [ ] Reconciliar mensajes "Refusing to confirm protection…" (existen en capturas, no en el repo) #daemon #bug
- [ ] Capturar el watchdog del SDK (sonda previa inconclusa) #testing
- [ ] Decidir y documentar SDK fail-closed vs. target vivo (§7.3 de capturas) #sdk
- [ ] Autenticar el socket de control (`SO_PEERCRED`, `SocketMode`) #seguridad #stretch
- [ ] Medir `nmissed` del kretprobe bajo carga (`maxactive=64`) #kernel #stretch

## To Do

- [ ] Redactar informe final con alcance real (qué se prueba y qué no) #docs #H5 @{2026-11-14}
- [ ] Preparar defensa del PIF #docs #H5 @{2026-11-15}

## Doing

## Review

## Done

- [x] Prevención Ring 0 validada 10/10 (kretprobe + EACCES) #kernel
- [x] Integración con RecoilEngine / Beyond All Reason y watchdog del SDK #sdk
- [x] Activación por socket systemd del daemon #daemon
- [x] Importar documentación al vault de Obsidian #docs



%% kanban:settings
```
{"kanban-plugin":"board"}
```
%%
