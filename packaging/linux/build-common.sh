#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="${1:-0.1.0}"
OUT_DIR="${ROOT_DIR}/dist/packages"
APP_DIR="${ROOT_DIR}/dist/file-utility-suite"
BUILD_VENV="${ROOT_DIR}/dist/build-venv"

as_root() {
  if [[ "${EUID}" -eq 0 ]]; then
    "$@"
  else
    command -v sudo >/dev/null 2>&1 || {
      echo "This build requires root privileges or sudo to install dependencies." >&2
      exit 1
    }
    sudo "$@"
  fi
}

install_packages() {
  local packages=("$@")
  if command -v apt-get >/dev/null 2>&1; then
    as_root apt-get update
    as_root apt-get install -y "${packages[@]}"
  elif command -v dnf >/dev/null 2>&1; then
    as_root dnf install -y "${packages[@]}"
  elif command -v pacman >/dev/null 2>&1; then
    as_root pacman -Sy --needed --noconfirm "${packages[@]}"
  else
    echo "Unsupported Linux distribution: install the required tools manually." >&2
    exit 1
  fi
}

ensure_command() {
  local command_name="$1"
  shift
  command -v "${command_name}" >/dev/null 2>&1 || install_packages "$@"
}

ensure_python_build_environment() {
  if ! command -v python3 >/dev/null 2>&1; then
    install_packages python3
  fi
  if ! python3 -m venv --help >/dev/null 2>&1; then
    if command -v apt-get >/dev/null 2>&1; then
      install_packages python3-venv
    elif command -v dnf >/dev/null 2>&1; then
      install_packages python3
    else
      install_packages python
    fi
  fi

  mkdir -p "${OUT_DIR}"
  if [[ ! -x "${BUILD_VENV}/bin/python" ]]; then
    rm -rf "${BUILD_VENV}"
    python3 -m venv "${BUILD_VENV}"
  fi
  "${BUILD_VENV}/bin/python" -m pip install --upgrade pip
  "${BUILD_VENV}/bin/python" -m pip install -r "${ROOT_DIR}/requirements.txt" pyinstaller
}

build_binary() {
  ensure_python_build_environment
  rm -rf "${APP_DIR}"
  "${BUILD_VENV}/bin/python" -m PyInstaller --clean --noconfirm \
    "${ROOT_DIR}/file_utility_suite.spec"
}

stage_desktop_files() {
  local stage_dir="$1"
  mkdir -p "${stage_dir}/usr/bin" \
    "${stage_dir}/usr/share/applications" \
    "${stage_dir}/usr/share/icons/hicolor/scalable/apps"
  cp "${APP_DIR}" "${stage_dir}/usr/bin/file-utility-suite"
  chmod 0755 "${stage_dir}/usr/bin/file-utility-suite"
  cp "${ROOT_DIR}/packaging/linux/file-utility-suite.desktop" \
    "${stage_dir}/usr/share/applications/"
  cp "${ROOT_DIR}/packaging/linux/file-utility-suite.svg" \
    "${stage_dir}/usr/share/icons/hicolor/scalable/apps/"
}

require_x86_64() {
  [[ "$(uname -m)" == "x86_64" ]] || {
    echo "This packaging script currently supports x86_64 only." >&2
    exit 1
  }
}
