# Quark Anticheat: sistema anticheat nativo para GNU/Linux

Prototipo funcional de un sistema anticheat nativo de nivel de kernel (Ring 0) diseñado específicamente para distribuciones GNU/Linux. El proyecto analiza y demuestra la viabilidad técnica de interceptar y prevenir vectores de ataque comunes en videojuegos multijugador competitivos sin comprometer la estabilidad del sistema ni la experiencia del usuario.

> Estado: prototipo académico (PIF). Toda la validación se hizo en una máquina virtual con un build de **pruebas** del módulo; el build de **release** se niega a proteger dentro de una VM. Ver [Limitaciones](#limitaciones-conocidas).

## Componentes del sistema

* **Módulo de kernel** (C, v0.4.0): instala un **kretprobe** sobre `ptrace_may_access()` y, para los procesos protegidos, deniega los accesos de nivel *attach* (`ptrace`, `/proc/<PID>/mem`, `process_vm_*`) sobrescribiendo el valor de retorno. Mantiene la lista de PIDs protegidos (máx. 16). Sólo acepta órdenes de control firmadas (ECDSA P-256, con nonce anti-replay), enviadas por el `quark_cli` auténtico.
* **Servicio en espacio de usuario** (Rust): demonio que recibe el registro del juego por un socket de dominio Unix, ordena la protección al kernel mediante `quark_cli` (cliente netlink en C), verifica en un hilo las variables registradas y carga programas **BPF-LSM** y de **telemetría eBPF** (libbpf-rs) que bloquean la carga de programas BPF de tracing y protegen al propio demonio.
* **SDK** (C): biblioteca que el videojuego enlaza. `quark_sdk_init()` sólo tiene éxito si el kernel confirma la protección, lanza un *watchdog* que termina el juego si el demonio desaparece y expone el estado de protección (`quark_sdk_is_active()`, `quark_sdk_is_testing_build()`, `quark_sdk_is_bpf_lsm_active()`, `quark_sdk_get_version()`).

Qué hace cada pieza, con detalle y referencias de código: nota **Features** del vault (`docs/obsidian-vault/quark-vault/02-Technical/Features.md`).

## Tecnologías y herramientas clave

* **Lenguajes**: C (módulo de kernel, SDK, `quark_cli`, juego y *cheat* de prueba) y Rust, edición 2024 (demonio).
* **Mediación en el kernel**: kretprobe sobre `ptrace_may_access()` (bloqueo) y BPF-LSM (`bpf_prog_load`, acceso a objetos BPF y al demonio) más telemetría eBPF por ring buffer. Un LSM clásico no es viable desde un módulo fuera del árbol, por eso se usa BPF-LSM.
* **Comunicación interna**: netlink (protocolo 31) entre `quark_cli` y el módulo, con comandos firmados; socket Unix (`/tmp/quark.sock`) entre SDK y demonio, con el PID del cliente verificado por `SO_PEERCRED`.
* **Servicios**: unidades systemd `quark.socket`, `quark.service` y `quark-kernel.service` (`quark_daemon/systemd/`).
* **Entorno**: el proyecto declara Nobara Linux como distribución de referencia; la VM de pruebas actual es CachyOS (ver `vm/README.md`). Pruebas con QEMU/KVM.
* **Motor real de validación**: RecoilEngine (submódulo) con el SDK integrado, ejecutando Beyond All Reason.

## Estructura del repositorio

* `/kernel`: módulo de kernel en C (`quark_kernel.c`) y la clave pública de verificación (`quark_pubkey.h`).
* `/quark_daemon`: demonio en Rust (`src/main.rs`), programas BPF (`src/bpf/`), unidades systemd y `quark_cli.c`.
* `/sdk`: biblioteca de integración (`quark_sdk.h` / `quark_sdk.c`).
* `/game_target`: videojuego *mock* en C usado como objetivo de prueba.
* `/cheat`: herramienta de ataque en C que escribe sobre `/proc/<PID>/mem`.
* `/tooling`: generador de claves de prueba (`keys/`), compilación en contenedor de RecoilEngine (`recoil-fedora-build/`) y utilidades de documentación.
* `/vm`: documentación y accesos directos de la VM de pruebas.
* `/RecoilEngine`: submódulo del motor con el SDK integrado.
* `/docs`: punteros al vault de Obsidian.
* `/docs/obsidian-vault/quark-vault`: **fuente de verdad de la documentación** (arquitectura, pruebas, riesgos, Kanban, guías). Abrirlo con Obsidian; empezar por `00-Home.md`.
* Scripts en la raíz: `run_test.sh`, `run_test_no_quark.sh`, `run_test_kernel.sh` (build de pruebas), `run_test_kernel_release.sh` (verifica que el build de release se niega a proteger en una VM) y `capture.sh` (captura de resultados). Cargan módulos de kernel y envían señales: ejecutarlos sólo en la VM de pruebas.

## Requisitos previos

* Linux con cabeceras del kernel en ejecución y `CONFIG_KPROBES`. Si el kernel se compiló con clang (p. ej. CachyOS), el módulo se compila con LLVM (`clang`, `lld`, `llvm`).
* `make`, `gcc`.
* Rust estable reciente (`cargo`; edición 2024) y `clang` para compilar los programas BPF.
* `bpftool` y un kernel con BTF (`/sys/kernel/btf/vmlinux`) para generar `vmlinux.h`.
* OpenSSL con cabeceras (`libcrypto`) para `quark_cli` y la generación de claves.
* Para la protección BPF-LSM: `CONFIG_BPF_LSM=y` y `bpf` en el parámetro de arranque `lsm=`. Sin eso el demonio sigue funcionando sólo con la protección del kretprobe y lo avisa.
* `root` para cargar el módulo (`insmod`), preferentemente dentro de una VM QEMU/KVM.

## Compilación

```bash
tooling/keys/generate-testing-key.sh   # una vez: crea el par ECDSA de PRUEBAS y actualiza kernel/quark_pubkey.h
# instalar la clave privada en /opt/quark-anticheat/keys/quark_signing_key.pem (0600, root) donde corra quark_cli
make                                   # demonio (Rust + BPF), quark_cli, juego + SDK y cheat
make kernel-testing                    # módulo con el chequeo de VM desactivado (para la VM de pruebas)
make kernel                            # módulo de release: se niega a proteger dentro de una VM
make lint                              # clang-tidy estricto sobre todo el código C (obligatorio al modificar C)
make clean
```

La clave privada no está en el repositorio. En un clon nuevo hay que generar un par y **recompilar el módulo** para que embeba la clave pública correspondiente.

## Documentación y contribución

* Todo se documenta en el vault, que sigue una regla **append-only** (sólo se agrega texto, nunca se edita lo escrito): `05-Meta/Append-Only-Standard.md`. Activar el chequeo una vez por clon: `git config core.hooksPath .githooks`.
* Reglas para agentes y personas: `AGENTS.md` y `.agents/AGENTS.md` (reglas de C y linter).
* Los archivos de `docs/*.md` son sólo punteros al vault.

## Limitaciones conocidas

Resumen (detalle en `02-Technical/Known-Limitations.md` del vault):
* Validado en VM con build de **pruebas**; el de release no puede probarse en una VM.
* Un código inyectado en el propio juego (p. ej. `LD_PRELOAD`) escribe memoria sin cruzar el kernel y no es bloqueado; sólo hay telemetría de indicios.
* La protección BPF-LSM depende de que el usuario arranque con `bpf` en `lsm=`; el motor aún sólo comprueba `quark_sdk_is_active()`.
* Lecturas de `/proc/<PID>/maps` y `environ` siguen siendo posibles para root (política del kernel).
* No hay medición de overhead de CPU/RAM ni SDK del lado servidor.

## Autores

Proyecto desarrollado como Proyecto Integrador Final (PIF) en la carrera de Ingeniería en Sistemas de Información de la Universidad de la Cuenca del Plata:
* Martínez Alarcón, Gabriel Sebastián
* Merino De Rui, Stefano Nahuel
