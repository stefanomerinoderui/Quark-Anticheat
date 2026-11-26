#!/usr/bin/env python3
"""SLOC por componente: lineas no vacias y no solo-comentario. Uso: python tooling/sloc.py RAIZ_DEL_WORKTREE
shortcut: comentarios C/Rust (// y /* */) y shell (#) por heuristica de linea, sin parser; no cuenta Makefile ni Cargo.lock."""
import sys, pathlib
GROUPS = {
 'Modulo de kernel (C)': ['kernel/quark_kernel.c', 'kernel/quark_pubkey.h'],
 'Servicio en espacio de usuario (Rust)': ['quark_daemon/src/main.rs', 'quark_daemon/src/bpf.rs', 'quark_daemon/build.rs'],
 'Programas eBPF (C)': ['quark_daemon/src/bpf/quark.bpf.c', 'quark_daemon/src/bpf/quark_events.h'],
 'Cliente de control quark_cli (C)': ['quark_daemon/quark_cli.c'],
 'SDK (C)': ['sdk/quark_sdk.c', 'sdk/quark_sdk.h'],
 'Pruebas y harness (C, Bash)': ['game_target/game.c', 'cheat/cheat.c', 'run_test.sh', 'run_test_kernel.sh',
                                  'run_test_kernel_release.sh', 'run_test_no_quark.sh', 'capture.sh'],
}
def sloc(p):
    n, blk = 0, False
    for l in p.read_text(encoding='utf-8', errors='replace').splitlines():
        s = l.strip()
        if blk:
            if '*/' in s: blk = False; s = s.split('*/', 1)[1].strip()
            else: continue
        if s.startswith('/*'):
            if '*/' not in s: blk = True
            continue
        if not s or s.startswith('//') or (p.suffix == '.sh' and s.startswith('#')): continue
        n += 1
    return n
root = pathlib.Path(sys.argv[1]); tot = 0
for g, fs in GROUPS.items():
    c = {f: sloc(root / f) for f in fs}; t = sum(c.values()); tot += t
    print(f'{g}: {t}  ' + ', '.join(f'{f}={v}' for f, v in c.items()))
print('TOTAL', tot)
