#!/usr/bin/env bash
set -euo pipefail

# shellcheck source=build-common.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/build-common.sh" "${1:-0.1.0}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="${1:-0.1.0}"
OUT_DIR="${ROOT_DIR}/dist/packages"
BUILD_DIR="${ROOT_DIR}/dist/arch-build"

require_x86_64
if ! command -v pacman >/dev/null 2>&1; then
  echo "The Arch package must be built on an Arch Linux system." >&2
  exit 1
fi
ensure_command makepkg base-devel
build_binary

rm -rf "${BUILD_DIR}"
mkdir -p "${BUILD_DIR}" "${OUT_DIR}"
cp "${ROOT_DIR}/packaging/linux/PKGBUILD" "${BUILD_DIR}/"
sed -i "s/^pkgver=.*/pkgver=${VERSION}/" "${BUILD_DIR}/PKGBUILD"
cp "${ROOT_DIR}/dist/file-utility-suite" "${BUILD_DIR}/"
cp "${ROOT_DIR}/packaging/linux/file-utility-suite.desktop" "${BUILD_DIR}/"
cp "${ROOT_DIR}/packaging/linux/file-utility-suite.svg" "${BUILD_DIR}/"
(
  cd "${BUILD_DIR}"
  makepkg --clean --noconfirm --syncdeps --needed
)
find "${BUILD_DIR}" -maxdepth 1 -name '*.pkg.tar.*' -exec cp {} "${OUT_DIR}/" \;
