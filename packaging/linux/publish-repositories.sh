#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PACKAGE_DIR="${1:-${ROOT_DIR}/dist/packages}"
REPO_DIR="${2:-${ROOT_DIR}/dist/repository}"
GPG_KEY_ID="${GPG_KEY_ID:-}"

rm -rf "${REPO_DIR}"
mkdir -p "${REPO_DIR}/apt/pool/main" "${REPO_DIR}/apt/dists/stable/main/binary-amd64"
mkdir -p "${REPO_DIR}/rpm" "${REPO_DIR}/arch/x86_64"
cp "${PACKAGE_DIR}"/*.deb "${REPO_DIR}/apt/pool/main/" 2>/dev/null || true
cp "${PACKAGE_DIR}"/*.rpm "${REPO_DIR}/rpm/" 2>/dev/null || true
cp "${PACKAGE_DIR}"/*.pkg.tar.* "${REPO_DIR}/arch/x86_64/" 2>/dev/null || true

if compgen -G "${REPO_DIR}/apt/pool/main/*.deb" >/dev/null; then
  command -v dpkg-scanpackages >/dev/null
  command -v apt-ftparchive >/dev/null
  (cd "${REPO_DIR}/apt" && dpkg-scanpackages pool /dev/null \
    > dists/stable/main/binary-amd64/Packages)
  gzip -9kf "${REPO_DIR}/apt/dists/stable/main/binary-amd64/Packages"
  apt-ftparchive release "${REPO_DIR}/apt/dists/stable" \
    > "${REPO_DIR}/apt/dists/stable/Release"
fi

if compgen -G "${REPO_DIR}/rpm/*.rpm" >/dev/null; then
  command -v createrepo_c >/dev/null
  createrepo_c "${REPO_DIR}/rpm"
fi

if compgen -G "${REPO_DIR}/arch/x86_64/*.pkg.tar.*" >/dev/null; then
  command -v repo-add >/dev/null
  (cd "${REPO_DIR}/arch/x86_64" && repo-add --nocolor \
    file-utility-suite.db.tar.gz ./*.pkg.tar.*)
fi

if [[ -n "${GPG_KEY_ID}" ]]; then
  gpg --batch --yes --armor --export "${GPG_KEY_ID}" > "${REPO_DIR}/repository-key.asc"
  if [[ -f "${REPO_DIR}/apt/dists/stable/main/binary-amd64/Packages" ]]; then
    gpg --batch --yes --detach-sign --armor \
      "${REPO_DIR}/apt/dists/stable/main/binary-amd64/Packages"
    gpg --batch --yes --clearsign --output \
      "${REPO_DIR}/apt/dists/stable/InRelease" \
      "${REPO_DIR}/apt/dists/stable/Release"
    gpg --batch --yes --detach-sign --armor \
      "${REPO_DIR}/apt/dists/stable/Release"
  fi
  if [[ -f "${REPO_DIR}/rpm/repodata/repomd.xml" ]]; then
    gpg --batch --yes --detach-sign --armor \
      "${REPO_DIR}/rpm/repodata/repomd.xml"
  fi
  if [[ -f "${REPO_DIR}/arch/x86_64/file-utility-suite.db.tar.gz" ]]; then
    gpg --batch --yes --detach-sign --local-user "${GPG_KEY_ID}" \
      "${REPO_DIR}/arch/x86_64/file-utility-suite.db.tar.gz"
  fi
else
  echo "GPG_KEY_ID is not set; repository indexes were generated unsigned." >&2
fi
