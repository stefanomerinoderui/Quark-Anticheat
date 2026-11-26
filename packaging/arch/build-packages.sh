#!/bin/bash
# Builds the Arch packages from the committed state of this checkout (HEAD).
#
# Usage: packaging/arch/build-packages.sh [extra makepkg args...]
#   Packages end up in packaging/arch/out/. Must run as a regular user
#   (makepkg refuses root); build dependencies must already be installed.
#
# Fails early if the version is inconsistent: PKGBUILD's pkgver must equal
# quark_daemon/Cargo.toml's version, and on a tag build (GITHUB_REF_TYPE=tag)
# also the tag name without its leading "v".

set -euo pipefail

die() {
    echo "build-packages: $*" >&2
    exit 1
}

PKG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(git -C "$PKG_DIR" rev-parse --show-toplevel)" ||
    die "not inside a git checkout"

pkgver="$(sed -n 's/^pkgver=//p' "$PKG_DIR/PKGBUILD")"
cargo_ver="$(sed -n 's/^version = "\(.*\)"/\1/p' "$REPO_ROOT/quark_daemon/Cargo.toml")"
[ -n "$pkgver" ] || die "could not read pkgver from PKGBUILD"
[ "$pkgver" = "$cargo_ver" ] ||
    die "PKGBUILD pkgver ($pkgver) != quark_daemon/Cargo.toml version ($cargo_ver)"

if [ "${GITHUB_REF_TYPE:-}" = "tag" ]; then
    tag_ver="${GITHUB_REF_NAME#v}"
    [ "$tag_ver" = "$pkgver" ] ||
        die "tag ${GITHUB_REF_NAME} does not match pkgver $pkgver"
fi

if [ -n "$(git -C "$REPO_ROOT" status --porcelain --untracked-files=no)" ]; then
    echo "build-packages: WARNING: uncommitted changes are NOT included (building HEAD)" >&2
fi

tarball="$PKG_DIR/quark-anticheat-$pkgver.tar.gz"
echo "=== Creating source tarball from HEAD ==="
git -C "$REPO_ROOT" archive --format=tar.gz --prefix="quark-anticheat-$pkgver/" \
    -o "$tarball" HEAD

mkdir -p "$PKG_DIR/out"
echo "=== Running makepkg ==="
cd "$PKG_DIR"
PKGDEST="$PKG_DIR/out" makepkg --cleanbuild --force "$@"
