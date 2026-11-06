#!/bin/bash
# Installs an already-built Quark Anticheat into /opt/quark-anticheat and enables its
# systemd units (kernel module loader + socket-activated daemon).
#
# Build first (as a regular user):
#   make daemon && make kernel            # release module (refuses to protect inside a VM)
#   make daemon && make kernel-testing    # testing module (VM check bypassed; test rigs only)
#
# Then install (root is needed: writes to /opt and /etc/systemd/system, loads a module):
#   sudo tooling/install.sh [--key PATH]
#
# --key PATH   ECDSA signing key that quark_cli uses to sign netlink commands. It must
#              be the private half of the public key compiled into the module
#              (kernel/quark_pubkey.h). Default: tooling/keys/quark_signing_key.pem
#              (made by tooling/keys/generate-testing-key.sh).
#
# Environment overrides:
#   QUARK_PREFIX    install location (default /opt/quark-anticheat)
#   QUARK_LSM_FILE  file listing the active LSMs (default /sys/kernel/security/lsm)
#
# BPF-LSM: the daemon's enforcement hooks need `bpf` in the active LSM list. If it is
# missing the install still succeeds, but this script warns loudly, because games that
# require full protection (quark_sdk_is_bpf_lsm_active()) will refuse to run.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

PREFIX="${QUARK_PREFIX:-/opt/quark-anticheat}"
LSM_FILE="${QUARK_LSM_FILE:-/sys/kernel/security/lsm}"
KEY_SRC="tooling/keys/quark_signing_key.pem"
UNIT_DIR="/etc/systemd/system"

die() {
    echo "ERROR: $*" >&2
    exit 1
}

warn() {
    echo "WARNING: $*" >&2
}

parse_args() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
        --key)
            [[ $# -ge 2 ]] || die "--key needs a path"
            KEY_SRC="$2"
            shift 2
            ;;
        -h | --help)
            sed -n '2,/^set -euo/p' "${BASH_SOURCE[0]}" | sed '$d; s/^# \{0,1\}//'
            exit 0
            ;;
        *) die "unknown argument: $1 (see --help)" ;;
        esac
    done
}

require_root() {
    [[ $EUID -eq 0 ]] || die "must run as root (try: sudo $0)"
}

require_built_artifacts() {
    local missing=0 file
    for file in kernel/quark_kernel.ko quark_daemon/quark_cli \
        quark_daemon/target/release/quark_daemon "$KEY_SRC"; do
        if [[ ! -f "$file" ]]; then
            echo "missing: $file" >&2
            missing=1
        fi
    done
    [[ $missing -eq 0 ]] || die "build first (make daemon && make kernel-testing) and generate the signing key (tooling/keys/generate-testing-key.sh)"
}

# Whether this kernel was built with BPF-LSM support at all.
kernel_has_bpf_lsm_support() {
    # Output is captured instead of piped into `grep -q`: with pipefail, grep -q
    # exiting early would SIGPIPE the producer and fail the whole pipeline.
    local config setting
    for config in /proc/config.gz "/boot/config-$(uname -r)"; do
        [[ -r "$config" ]] || continue
        if [[ "$config" == *.gz ]]; then
            setting="$(zcat "$config" | grep '^CONFIG_BPF_LSM=' || true)"
        else
            setting="$(grep '^CONFIG_BPF_LSM=' "$config" || true)"
        fi
        [[ "$setting" == "CONFIG_BPF_LSM=y" ]]
        return
    done
    return 2 # unknown
}

# Returns 0 if BPF-LSM is active, 1 otherwise (after printing why and how to fix it).
check_bpf_lsm() {
    local active
    if [[ ! -r "$LSM_FILE" ]]; then
        warn "cannot read $LSM_FILE: BPF-LSM could not be detected."
        return 1
    fi
    active="$(<"$LSM_FILE")"
    if [[ ",$active," == *",bpf,"* ]]; then
        echo "BPF-LSM: active (LSMs: $active)"
        return 0
    fi

    warn "BPF-LSM was NOT detected (active LSMs: ${active:-none})."
    warn "The daemon will run without its enforcement hooks and games that require"
    warn "BPF-LSM will refuse to start."
    local support=0
    kernel_has_bpf_lsm_support || support=$?
    case "$support" in
    0)
        warn "This kernel supports it. Add 'bpf' to the boot-time LSM list, e.g. append"
        warn "  lsm=${active},bpf"
        warn "to the kernel command line in your bootloader config, then reboot."
        ;;
    1) warn "This kernel was built without CONFIG_BPF_LSM=y; a different kernel is needed." ;;
    *) warn "Could not read the kernel config to tell whether CONFIG_BPF_LSM=y is set." ;;
    esac
    return 1
}

install_files() {
    echo "Installing to $PREFIX"
    install -d -m 755 "$PREFIX/kernel" "$PREFIX/quark_daemon/target/release"
    install -d -m 700 "$PREFIX/keys"
    install -m 644 kernel/quark_kernel.ko "$PREFIX/kernel/quark_kernel.ko"
    install -m 755 quark_daemon/quark_cli "$PREFIX/quark_daemon/quark_cli"
    install -m 755 quark_daemon/target/release/quark_daemon \
        "$PREFIX/quark_daemon/target/release/quark_daemon"
    install -m 600 -o root -g root "$KEY_SRC" "$PREFIX/keys/quark_signing_key.pem"
}

install_units() {
    local unit
    for unit in quark.socket quark.service quark-kernel.service; do
        # The shipped units hardcode /opt/quark-anticheat; follow QUARK_PREFIX.
        sed "s#/opt/quark-anticheat#$PREFIX#g" "quark_daemon/systemd/$unit" >"$UNIT_DIR/$unit"
        chmod 644 "$UNIT_DIR/$unit"
    done
    systemctl daemon-reload
}

# Reload the new module and start the socket-activated daemon fresh.
restart_services() {
    systemctl stop quark.service quark.socket 2>/dev/null || true
    systemctl enable quark-kernel.service quark.socket >/dev/null 2>&1
    systemctl restart quark-kernel.service
    systemctl start quark.socket
}

main() {
    parse_args "$@"
    require_root
    require_built_artifacts

    local bpf_lsm_ok=1
    check_bpf_lsm || bpf_lsm_ok=0

    install_files
    install_units
    restart_services

    local module_state="NOT loaded" loaded_modules
    loaded_modules="$(lsmod)"
    if [[ "$loaded_modules" == *$'\n'"quark_kernel "* ]]; then
        module_state="loaded"
    fi
    echo "Quark Anticheat installed: kernel module $module_state, quark.socket $(systemctl is-active quark.socket)."
    if [[ $bpf_lsm_ok -eq 0 ]]; then
        warn "Reminder: BPF-LSM is not active, so protection is incomplete (see above)."
    fi
}

main "$@"
