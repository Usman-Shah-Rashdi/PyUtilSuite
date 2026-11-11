#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="${1:-0.1.0}"
OUT_DIR="${ROOT_DIR}/dist/packages"
BUILD_DIR="${ROOT_DIR}/dist/arch-build"

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
