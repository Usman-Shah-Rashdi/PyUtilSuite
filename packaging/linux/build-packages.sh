#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="${1:-0.1.0}"
for script in build-deb.sh build-rpm.sh build-appimage.sh; do
  "${ROOT_DIR}/packaging/linux/${script}" "${VERSION}"
done
