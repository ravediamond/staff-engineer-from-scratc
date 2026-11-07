#!/usr/bin/env bash
# Copy your private material (STAR bank, case files, real numbers) into reference/your-work/.
# That folder is gitignored: it never reaches this public repo.
# Usage: bash scripts/sync_private.sh ~/src/staff-prep-private
set -euo pipefail
SRC="${1:?usage: sync_private.sh <path to your private repo>}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/reference/your-work"
if [ ! -d "$SRC" ]; then
  echo "not found: $SRC" >&2
  exit 1
fi
mkdir -p "$DEST"
rsync -a --delete --exclude '.git' "$SRC/" "$DEST/"
git -C "$(dirname "$0")/.." check-ignore -q "$DEST" || { echo "DANGER: $DEST is not gitignored" >&2; exit 2; }
echo "synced $(find "$DEST" -type f | wc -l | tr -d ' ') files into reference/your-work/ (gitignored)"
