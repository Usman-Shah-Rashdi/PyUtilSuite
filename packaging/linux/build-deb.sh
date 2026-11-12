#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build-common.sh
source "${SCRIPT_DIR}/build-common.sh" "${1:-0.1.0}"

require_x86_64
ensure_command dpkg-deb dpkg-dev
build_binary

STAGE_DIR="${ROOT_DIR}/dist/deb-root"
rm -rf "${STAGE_DIR}"
stage_desktop_files "${STAGE_DIR}"
mkdir -p "${STAGE_DIR}/DEBIAN"
cat > "${STAGE_DIR}/DEBIAN/control" <<EOF
Package: file-utility-suite
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: amd64
Maintainer: PyUtilSuite contributors
Description: Desktop file conversion and organization utility
EOF

dpkg-deb --build --root-owner-group "${STAGE_DIR}" \
  "${OUT_DIR}/file-utility-suite_${VERSION}_amd64.deb"
echo "Debian package written to ${OUT_DIR}/file-utility-suite_${VERSION}_amd64.deb"
