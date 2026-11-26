# Inicio rapido

Quark Anticheat se distribuye como paquetes de pacman firmados con PGP, publicados en un repositorio propio servido por GitHub Pages:

```
https://stefanomerinoderui.github.io/Quark-Anticheat/
```

La instalación consta de tres pasos: confiar en la clave de firma, agregar el repositorio a `/etc/pacman.conf` e instalar los paquetes.

Los comandos con `sudo` requieren privilegios de root porque modifican el llavero de pacman (`/etc/pacman.d/gnupg`), la configuración del sistema (`/etc/pacman.conf`) o instalan paquetes del sistema.

## 1. Instalar la clave PGP de firma

pacman sólo acepta paquetes de este repositorio si están firmados con una clave en la que el sistema confía. Esa clave no está en ningún servidor de claves: se publica junto al repositorio.

**Huella de la clave:**

```
4CC6 6B02 7678 7FEA 35E4  2CDA 930D 78FA BEFA A50F
```

Esta huella figura en el repositorio de código (este archivo), un canal distinto del sitio que sirve la clave. Si la huella de la clave descargada no coincide, **no se debe continuar**.

1. Descargar la clave pública:

   ```bash
   curl -fsSLO https://stefanomerinoderui.github.io/Quark-Anticheat/quark-anticheat.asc
   ```

2. Comprobar la huella antes de importarla:

   ```bash
   gpg --show-keys --with-fingerprint quark-anticheat.asc
   ```

   La línea debajo de `pub` debe coincidir con la huella indicada arriba.

3. Agregar la clave al llavero de pacman:

   ```bash
   sudo pacman-key --add quark-anticheat.asc
   ```

4. Firmarla localmente. Este paso marca la clave como confiable; sin él pacman la conoce pero rechaza las firmas hechas con ella:

   ```bash
   sudo pacman-key --lsign-key 4CC66B0276787FEA35E42CDA930D78FABEFAA50F
   ```

5. Verificar que quedó importada y firmada:

   ```bash
   pacman-key --list-keys 4CC66B0276787FEA35E42CDA930D78FABEFAA50F
   ```

   La salida debe indicar la confianza como `[  full  ]`.

## 2. Agregar el repositorio a `/etc/pacman.conf`

Editar `/etc/pacman.conf` con privilegios de root (por ejemplo `sudoedit /etc/pacman.conf`) y agregar al final del archivo:

```ini
[quark-anticheat]
SigLevel = Required DatabaseRequired
Server = https://stefanomerinoderui.github.io/Quark-Anticheat/$arch
```

- `[quark-anticheat]` es el nombre de la base de datos del repositorio y debe escribirse exactamente así.
- `SigLevel = Required DatabaseRequired` exige que tanto los paquetes como la base de datos estén firmados con una clave confiable. No debe relajarse a `Optional` ni `Never`.
- `$arch` se escribe literalmente: pacman lo reemplaza por la arquitectura del sistema (`x86_64`).
- La sección debe quedar **después** de `[options]`. El orden respecto de `[core]` y `[extra]` no importa porque los nombres de paquete no se superponen.

Sincronizar las bases de datos:

```bash
sudo pacman -Sy
```

La salida debe incluir una línea `quark-anticheat` sin errores de firma.

## 3. Instalar los paquetes

| Paquete                  | Para quién                | Contenido                                                          |
| ------------------------ | ------------------------- | ------------------------------------------------------------------ |
| `quark-anticheat-daemon` | jugadores                 | demonio y unidades systemd. Instala también `quark-anticheat-dkms` |
| `quark-anticheat-dkms`   | (dependencia)             | módulo de kernel (DKMS) y `quark_cli`                              |
| `quark-anticheat-sdk`    | desarrolladores de juegos | `libquark_sdk.so`, `quark_sdk.h` y `quark-sdk.pc`                  |

DKMS compila el módulo para cada kernel instalado y necesita sus cabeceras: `linux-headers` para el kernel `linux`, `linux-zen-headers` para `linux-zen`, `linux-lts-headers` para `linux-lts`, etc.

```bash
sudo pacman -Syu quark-anticheat-daemon linux-headers
sudo modprobe quark_kernel
sudo systemctl enable --now quark.socket
```

El módulo se carga automáticamente en los arranques siguientes. El demonio arranca solo cuando un juego se conecta a `/run/quark/quark.sock`.

En la primera compilación DKMS genera una clave de firma propia de la máquina en `/etc/quark-anticheat/quark_signing_key.pem` (sólo legible por root). Esa clave es distinta de la clave PGP de los paquetes: la usa el módulo para aceptar únicamente órdenes de `quark_cli`.

El módulo de los paquetes es la versión de release y se niega a proteger procesos dentro de una máquina virtual.

## Solución de problemas

**`error: quark-anticheat: signature from "Quark Anticheat Packaging" is unknown trust`**
La clave se agregó pero no se firmó localmente. Repetir el paso 1.4.

**`error: quark-anticheat: key "4CC66B0276787FEA35E42CDA930D78FABEFAA50F" is unknown`**
La clave no está en el llavero de pacman. pacman ofrece importarla (`Import PGP key ...? [Y/n]`), pero falla porque la clave no está en ningún servidor de claves. Repetir los pasos 1.1 a 1.4.

**`signature ... is invalid` o `invalid or corrupted package (PGP signature)`**
El paquete o la base de datos no coinciden con su firma. No se debe forzar la instalación. Volver a sincronizar con `sudo pacman -Syy`; si el error persiste, reportarlo en el repositorio.

**`signature ... has expired` o `key ... expired`**
La clave de firma se renovó o se reemplazó. Descargar la clave publicada, comprobar la huella actualizada en este archivo y repetir el paso 1.

**`failed to retrieve some files` / error 404 al sincronizar**
Revisar que la línea `Server` termine en `/$arch` y que el nombre de la sección sea `[quark-anticheat]`.

**DKMS no compila el módulo**
Comprobar que estén instaladas las cabeceras del kernel en uso (`uname -r`). El registro de la compilación queda en `/var/lib/dkms/quark-anticheat/<versión>/build/make.log`.

## Desinstalación

```bash
sudo systemctl disable --now quark.socket
sudo pacman -Rns quark-anticheat-daemon quark-anticheat-dkms quark-anticheat-sdk
```

Para quitar también el repositorio y la confianza en su clave: borrar la sección `[quark-anticheat]` de `/etc/pacman.conf` y ejecutar:

```bash
sudo pacman-key --delete 4CC66B0276787FEA35E42CDA930D78FABEFAA50F
```

La clave de firma de la máquina queda en `/etc/quark-anticheat/`; se puede borrar ese directorio si no se va a reinstalar.
