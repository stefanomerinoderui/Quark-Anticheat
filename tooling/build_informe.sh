#!/bin/sh
# Genera build/Informe-PIF-AAAA-MM-DD.{pdf,tex} desde el vault. Requiere pandoc y tectonic.
# Fuente: TeX Gyre Termes (clon metrico de Times); tectonic no carga Times New Roman del sistema.
set -e
cd "$(dirname "$0")/.."
SRC=docs/obsidian-vault/quark-vault/01-Project/Informe-PIF-Avance.md
D=${1:-$(date +%F)}
REV="$(git rev-parse --short HEAD)$(git diff --quiet HEAD -- "$SRC" tooling/informe || echo ' +cambios sin commitear')"
case "$(echo "$D" | cut -d- -f2)" in
  01) M=Enero;; 02) M=Febrero;; 03) M=Marzo;; 04) M=Abril;; 05) M=Mayo;; 06) M=Junio;;
  07) M=Julio;; 08) M=Agosto;; 09) M=Septiembre;; 10) M=Octubre;; 11) M=Noviembre;; 12) M=Diciembre;;
esac
mkdir -p build
for ext in pdf tex; do
  pandoc -d tooling/informe/defaults.yaml -M "date=$M de $(echo "$D" | cut -d- -f1)" -M "subject=Versión del documento: $D, commit $REV" "$SRC" -o "build/Informe-PIF-$D.$ext"
done
echo "OK build/Informe-PIF-$D.pdf (commit $REV)"
