#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build-common.sh
source "${SCRIPT_DIR}/build-common.sh" "${1:-0.1.0}"

require_x86_64
ensure_python_build_environment

APPIMAGETOOL="${ROOT_DIR}/dist/appimagetool"
if [[ ! -x "${APPIMAGETOOL}" ]]; then
  if ! command -v curl >/dev/null 2>&1; then
    install_packages curl
  fi
  curl -fL --retry 3 \
    "https://github.com/AppImage/appimagetool/releases/latest/download/appimagetool-x86_64.AppImage" \
    -o "${APPIMAGETOOL}"
  chmod 0755 "${APPIMAGETOOL}"
fi

APP_DIR="${ROOT_DIR}/dist/AppDir"
rm -rf "${APP_DIR}"
mkdir -p "${APP_DIR}/usr"
stage_desktop_files "${APP_DIR}"
cp "${ROOT_DIR}/packaging/linux/file-utility-suite.desktop" \
  "${APP_DIR}/file-utility-suite.desktop"
cp "${ROOT_DIR}/packaging/linux/file-utility-suite.svg" \
  "${APP_DIR}/file-utility-suite.svg"
cat > "${APP_DIR}/AppRun" <<'EOF'
#!/usr/bin/env bash
exec "$(dirname "$0")/usr/bin/file-utility-suite" "$@"
EOF
chmod 0755 "${APP_DIR}/AppRun"

"${APPIMAGETOOL}" "${APP_DIR}" \
  "${OUT_DIR}/File-Utility-Suite-${VERSION}-x86_64.AppImage"
echo "AppImage written to ${OUT_DIR}/File-Utility-Suite-${VERSION}-x86_64.AppImage"
