#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="${1:-0.1.0}"
OUT_DIR="${ROOT_DIR}/dist/packages"
APP_DIR="${ROOT_DIR}/dist/file-utility-suite"
STAGE_DIR="${ROOT_DIR}/dist/package-root"

rm -rf "${OUT_DIR}" "${APP_DIR}" "${STAGE_DIR}"
mkdir -p "${OUT_DIR}" "${STAGE_DIR}/usr/bin" \
  "${STAGE_DIR}/usr/share/applications" \
  "${STAGE_DIR}/usr/share/icons/hicolor/scalable/apps"

python -m pip install -r "${ROOT_DIR}/requirements.txt" pyinstaller
python -m PyInstaller --clean --noconfirm "${ROOT_DIR}/file_utility_suite.spec"
cp "${APP_DIR}" "${STAGE_DIR}/usr/bin/file-utility-suite"
chmod 0755 "${STAGE_DIR}/usr/bin/file-utility-suite"
cp "${ROOT_DIR}/packaging/linux/file-utility-suite.desktop" \
  "${STAGE_DIR}/usr/share/applications/"
cp "${ROOT_DIR}/packaging/linux/file-utility-suite.svg" \
  "${STAGE_DIR}/usr/share/icons/hicolor/scalable/apps/"

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

if command -v rpmbuild >/dev/null 2>&1; then
  RPM_ROOT="${ROOT_DIR}/dist/rpm"
  CHANGELOG_DATE="$(LC_ALL=C date -u '+%a %b %d %Y')"
  rm -rf "${RPM_ROOT}"
  mkdir -p "${RPM_ROOT}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
  cat > "${RPM_ROOT}/SPECS/file-utility-suite.spec" <<EOF
Name: file-utility-suite
Version: ${VERSION}
Release: 1
Summary: Desktop file conversion and organization utility
License: MIT
BuildArch: x86_64

%description
Desktop file conversion and organization utility.

%install
mkdir -p %{buildroot}/usr/bin %{buildroot}/usr/share/applications %{buildroot}/usr/share/icons/hicolor/scalable/apps
install -m 755 ${STAGE_DIR}/usr/bin/file-utility-suite %{buildroot}/usr/bin/file-utility-suite
install -m 644 ${STAGE_DIR}/usr/share/applications/file-utility-suite.desktop %{buildroot}/usr/share/applications/file-utility-suite.desktop
install -m 644 ${STAGE_DIR}/usr/share/icons/hicolor/scalable/apps/file-utility-suite.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/file-utility-suite.svg

%files
/usr/bin/file-utility-suite
/usr/share/applications/file-utility-suite.desktop
/usr/share/icons/hicolor/scalable/apps/file-utility-suite.svg

%changelog
* ${CHANGELOG_DATE} PyUtilSuite contributors <noreply@example.com> - ${VERSION}-1
- Automated release build
EOF
  rpmbuild --define "_topdir ${RPM_ROOT}" -bb \
    "${RPM_ROOT}/SPECS/file-utility-suite.spec"
  find "${RPM_ROOT}/RPMS" -name '*.rpm' -exec cp {} "${OUT_DIR}/" \;
fi

if command -v appimagetool >/dev/null 2>&1; then
  APP_DIR="${ROOT_DIR}/dist/AppDir"
  rm -rf "${APP_DIR}"
  mkdir -p "${APP_DIR}/usr/bin" "${APP_DIR}/usr/share/applications" \
    "${APP_DIR}/usr/share/icons/hicolor/scalable/apps"
  cp -a "${STAGE_DIR}/usr/." "${APP_DIR}/usr/"
  cp "${ROOT_DIR}/packaging/linux/file-utility-suite.svg" \
    "${APP_DIR}/file-utility-suite.svg"
  appimagetool "${APP_DIR}" \
    "${OUT_DIR}/File-Utility-Suite-${VERSION}-x86_64.AppImage"
fi

echo "Packages written to ${OUT_DIR}"
