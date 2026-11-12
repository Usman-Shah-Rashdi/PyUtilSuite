#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=build-common.sh
source "${SCRIPT_DIR}/build-common.sh" "${1:-0.1.0}"

require_x86_64
ensure_command rpmbuild rpm-build
build_binary

STAGE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/file-utility-suite-stage.XXXXXX")"
RPM_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/file-utility-suite-rpm.XXXXXX")"
cleanup() {
  rm -rf "${STAGE_DIR}" "${RPM_ROOT}"
}
trap cleanup EXIT
stage_desktop_files "${STAGE_DIR}"
mkdir -p "${RPM_ROOT}"/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
CHANGELOG_DATE="$(LC_ALL=C date -u '+%a %b %d %Y')"
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
mkdir -p "%{buildroot}/usr/bin" "%{buildroot}/usr/share/applications" "%{buildroot}/usr/share/icons/hicolor/scalable/apps"
install -m 755 ${STAGE_DIR}/usr/bin/file-utility-suite "%{buildroot}/usr/bin/file-utility-suite"
install -m 644 ${STAGE_DIR}/usr/share/applications/file-utility-suite.desktop "%{buildroot}/usr/share/applications/file-utility-suite.desktop"
install -m 644 ${STAGE_DIR}/usr/share/icons/hicolor/scalable/apps/file-utility-suite.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/file-utility-suite.svg"

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
echo "RPM package written to ${OUT_DIR}"
