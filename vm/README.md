# VM de pruebas de Quark Anticheat

Configuración de la VM CachyOS usada para probar el módulo de kernel, el demonio y el juego.

Acceso: `ssh quark` (usuario `quark`) y `ssh quark-root` (root).

## Sistema

- CachyOS, kernel `7.3.1-1-cachyos` (el módulo debe compilarse contra estos headers: `linux-cachyos-headers 7.3.1-1`).
- 4 CPU, 7.7 GiB RAM, disco `/` de 26 GiB (quedan ~6 GiB libres tras instalar RecoilEngine; vigilar).
- Kernel compilado con clang: `CONFIG_CC_IS_CLANG=y`. `kprobes` habilitado. Firma de módulos opcional (no forzada).

## Herramientas instaladas

| Paquete | Uso |
|---|---|
| `gcc` 16, `clang` 23, `lld` 23, `llvm` 23, `base-devel` | Compilación de C/C++ y del módulo |
| `rust` 1.99 | Demonio Rust (`quark_daemon`) |
| `cmake` 4.4, `ninja` | Build de RecoilEngine |
| `boost`, `devil`, `7zip`, `sdl2-compat`, `openal`, `glew`, `glm` | Dependencias de RecoilEngine |
| `libvorbis`, `libogg`, `freetype2`, `libjpeg-turbo`, `libpng`, `libunwind`, `minizip`, `jsoncpp`, `curl`, `libx11`, `libxcursor`, `python` | Dependencias de RecoilEngine |

`zlib` no se instaló a propósito: entra en conflicto con `zlib-ng-compat`, que ya provee la misma API.

## Quark Anticheat

Instalado en `/opt/quark-anticheat` con `tooling/install.sh` (compilar antes con `make daemon && make kernel-testing`). El script avisa si BPF-LSM no está activo; en esta VM sí lo está (`bpf` figura en `/sys/kernel/security/lsm`). La clave de firma de pruebas existe solo en la VM; no copiar de vuelta `kernel/quark_pubkey.h` al repo.

- Ruta: `~/Projects/Quark-Anticheat` (copia sincronizada desde el host con `rsync`, sin `target/`, `*.ko` ni `*.o`).
- Userspace: `make` compila el demonio, el cliente, el juego de prueba y el cheat.
- Módulo de kernel: `make -C kernel` (el Makefile añade `LLVM=1` si el kernel fue compilado con clang). Se compila en la VM, nunca se copia un `.ko` del host, porque el kernel del host es distinto.
- Pruebas:
  - `./run_test_kernel.sh` como root (`ssh quark-root`): **pasa**. El módulo bloquea la escritura y la vida se mantiene en 100.
  - `./run_test.sh` (solo userspace): **se cuelga**, sin causa encontrada todavía.

## RecoilEngine (contenido antiguo, de la VM anterior)

- Ruta: `~/RecoilEngine`. Contiene la compilación anterior con el SDK de Quark enlazado (`build/spring`, `build/spring-headless`).
- Versión: `spring-headless` reporta `2026.07.01-38-g9b4be36 master`.
- Contenido: `build/maps` (Techno Lands), `build/packages`, `build/rapid`. El juego BAR completo no se ha verificado todavía; la prueba real es lanzar la partida.
- Archivo de partida: `build/skirmish_2ai.txt` (2 IA BARb, mapa Techno Lands).

Compilación nueva que hicimos en la VM (independiente de la anterior):

- Ruta: `~/Projects/RecoilEngine` (build en `build/`), instalación en `~/recoil-install`.
- Binarios: `~/recoil-install/spring` y `~/recoil-install/spring-headless`, versión `105.0.1`.
- Sin contenido de juego.
- Workarounds necesarios:
  1. Repo sin tags de git: se creó la etiqueta `105.0.1` en la copia de la VM para que el script de versión funcione.
  2. GNU ld rechaza `-Wl,--icf=all`: se configuró `-DCMAKE_EXE_LINKER_FLAGS=-fuse-ld=lld` (y shared/module).
  3. Config: `cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=RELEASE -DBUILD_spring-headless=ON -DBUILD_spring-dedicated=OFF -DAI_TYPES=NONE`.

## Launchers de escritorio

Archivos fuente en `vm/`. Copias en `/home/quark/Desktop/`:

- `BeyondAllReason-Quark.desktop`: abre el motor con `~/RecoilEngine/build`.
- `BAR-2xAI-Skirmish-Quark.desktop`: partida 2xIA con `skirmish_2ai.txt`.
- `recoil.desktop`: abre `~/recoil-install/spring` (sin contenido de juego). Creado en la VM, no está en el repo.

Los `Exec` usan `SPRING_DATADIR=/home/quark/RecoilEngine/build:/home/quark/RecoilEngine/cont`.

Nota: los launchers `*-Quark` dicen que el binario está "patched with the Quark Anticheat SDK". El binario de `~/RecoilEngine` sí enlaza el SDK (imprime `[QUARK-SDK] connection to daemon failed` sin demonio). La versión del SDK en `RecoilEngine` (commit `29e5b0b`, "version-attestation") no coincide con `sdk/` del repo host; comparar antes de usar.

## Pendiente

- Lanzar la partida BAR desde el launcher y confirmar que carga el juego completo.
- Investigar el cuelgue de `run_test.sh`.
- Comparar el SDK de la VM con el del host.
