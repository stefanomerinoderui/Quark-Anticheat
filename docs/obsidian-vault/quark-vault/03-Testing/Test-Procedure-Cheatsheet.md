---
title: Cheatsheet de pruebas
tags: [testing, cheatsheet]
source: Funcionamiento-del-codigo §4–5
---

# Cheatsheet de pruebas

```bash
make && make -C kernel          # compilar todo
./run_test_no_quark.sh          # control negativo: el ataque funciona
./run_test.sh                   # Modo A: detección + SIGKILL
sudo ./run_test_kernel.sh       # Modo B: prevención en Ring 0 (solo en la VM)
./capture.sh                    # captura resultados de modos A y B (commit af7e17f)
dmesg | grep QUARK-KERNEL       # ver alertas del kernel
journalctl -u quark.service -f  # log del daemon bajo systemd
```

⚠️ Cargan módulos de kernel y envían SIGKILL: ejecutar solo en la VM ([[VM-test-environment]]). Interpretar la salida con [[Log-messages]].


## Update 2026-11-11 — agent:claude — alinear con origin/Dev@35c6031
```bash
make lint                          # clang-tidy estricto (obligatorio en C)
make kernel-testing                # build con bypass de VM (is_testing_build=1)
make kernel                        # build de release (se niega a proteger en una VM)
tooling/keys/generate-testing-key.sh   # clave ECDSA de pruebas (la privada NO se commitea)
./run_test_kernel_release.sh       # prueba del build de release
journalctl -u quark.service -u quark-kernel.service -f
dmesg | grep QUARK-KERNEL ; # telemetría del daemon: líneas [QUARK-BPF] en su journal
```
- **UNVERIFIED** — `run_test.sh` y `run_test_no_quark.sh` pueden no representar ya el producto (ver [[Test-Status]] Update). `tooling/install.sh` existe solo en `feature/gameStartProtection`.
