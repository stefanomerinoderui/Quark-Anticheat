#!/bin/sh
# Genera build/Informe-PIF-AAAA-MM-DD.{pdf,tex} desde el vault. Requiere pandoc y tectonic.
set -e
cd "$(dirname "$0")/.."
SRC=docs/obsidian-vault/quark-vault/01-Project/Informe-PIF-Avance.md
D=${1:-$(date +%F)}
REV="$(git rev-parse --short HEAD)$(git diff --quiet HEAD -- "$SRC" || echo ' +cambios sin commitear')"
mkdir -p build
for ext in pdf tex; do
  pandoc -d tooling/informe/defaults.yaml -M "date=$D (commit $REV)" "$SRC" -o "build/Informe-PIF-$D.$ext"
done
echo "OK build/Informe-PIF-$D.pdf"
