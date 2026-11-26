#!/bin/bash
# Signs built packages and assembles a static pacman repository (for GitHub Pages).
#
# Usage: GPG_KEY_ID=<fingerprint> [REPO_URL=<public url>] \
#            packaging/arch/publish-repo.sh <package-dir> <site-dir>
#   The signing key must already be in the caller's GPG keyring. REPO_URL is the
#   URL <site-dir> will be served at, only used for the generated index.html.
#
# Output layout (<site-dir> is served as the Pages root):
#   x86_64/quark-anticheat.{db,files}[.sig] + *.pkg.tar.zst[.sig]
#   quark-anticheat.asc   public key for `pacman-key --add`
#   index.html            install instructions
#
# The repo is rebuilt from scratch on every release and only holds that
# release's packages; older versions stay downloadable from GitHub Releases.

set -euo pipefail

REPO_NAME=quark-anticheat
ARCH=x86_64

die() {
    echo "publish-repo: $*" >&2
    exit 1
}

[ $# -eq 2 ] || die "usage: GPG_KEY_ID=<fingerprint> $0 <package-dir> <site-dir>"
pkg_src="$1"
site="$2"
: "${GPG_KEY_ID:?GPG_KEY_ID must be set to the signing key fingerprint}"
REPO_URL="${REPO_URL:-https://OWNER.github.io/REPO}"

gpg --batch --list-secret-keys "$GPG_KEY_ID" >/dev/null 2>&1 ||
    die "secret key $GPG_KEY_ID is not in the GPG keyring"

shopt -s nullglob
packages=("$pkg_src"/*.pkg.tar.zst)
[ ${#packages[@]} -gt 0 ] || die "no *.pkg.tar.zst found in $pkg_src"

if [ -e "$site" ] && [ -n "$(ls -A "$site")" ]; then
    die "$site already exists and is not empty"
fi
repo_dir="$site/$ARCH"
mkdir -p "$repo_dir"
cp -- "${packages[@]}" "$repo_dir/"

echo "=== Signing packages ==="
for pkg in "$repo_dir"/*.pkg.tar.zst; do
    gpg --batch --yes --detach-sign --no-armor --local-user "$GPG_KEY_ID" "$pkg"
done

echo "=== Building signed repository database ==="
repo-add --sign --key "$GPG_KEY_ID" "$repo_dir/$REPO_NAME.db.tar.zst" "$repo_dir"/*.pkg.tar.zst

# repo-add leaves <name>.db/.files (+ .sig) as symlinks; GitHub Pages doesn't
# serve symlinks, so replace them with real copies.
for link in "$repo_dir"/*; do
    if [ -L "$link" ]; then
        target="$(readlink -f "$link")"
        rm -- "$link"
        cp -- "$target" "$link"
    fi
done

gpg --batch --armor --export "$GPG_KEY_ID" >"$site/$REPO_NAME.asc"

cat >"$site/index.html" <<EOF
<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>Quark Anticheat - repositorio pacman</title></head>
<body>
<h1>Quark Anticheat - repositorio pacman</h1>
<p>Clave de firma: <a href="$REPO_NAME.asc">$REPO_NAME.asc</a> (<code>$GPG_KEY_ID</code>)</p>
<pre>
sudo pacman-key --add $REPO_NAME.asc
sudo pacman-key --lsign-key $GPG_KEY_ID

# /etc/pacman.conf
[$REPO_NAME]
SigLevel = Required DatabaseRequired
Server = $REPO_URL/\$arch
</pre>
<p>Instrucciones completas en el README del repositorio.</p>
</body>
</html>
EOF

echo "=== Repository ready in $site ==="
ls -l "$repo_dir"
