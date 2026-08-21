#!/usr/bin/env bash
# Package the VSSS Helm chart WITH dependencies (required for Rancher / helm install).
#
# Bad packages (no charts/) fail with:
#   found in Chart.yaml, but missing in charts/ directory: common, postgres-init, ...
#
# Usage:
#   ./helm/scripts/package.sh              # writes ./vsss-<version>.tgz
#   ./helm/scripts/package.sh /tmp/out     # writes /tmp/out/vsss-<version>.tgz
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CHART="${ROOT}/helm/vsss"
OUT="${1:-${ROOT}}"

mkdir -p "${OUT}"
cd "${CHART}"

echo "==> helm dependency build (${CHART})"
helm dependency build

VERSION="$(awk '/^version:/{print $2; exit}' Chart.yaml)"
echo "==> helm package version=${VERSION} -> ${OUT}"
helm package . -d "${OUT}"

PKG="${OUT}/vsss-${VERSION}.tgz"
echo "==> verifying charts/ inside package"
missing=0
for dep in common postgres-init redis openg2p-id-generator keycloak-init openg2p-awe; do
  if ! tar -tzf "${PKG}" | grep -q "/charts/${dep}"; then
    echo "ERROR: ${dep} missing from ${PKG}" >&2
    missing=1
  fi
done
if [[ "${missing}" -ne 0 ]]; then
  exit 1
fi

echo "OK: ${PKG}"
ls -lh "${PKG}"
