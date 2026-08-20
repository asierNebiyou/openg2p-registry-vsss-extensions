#!/usr/bin/env bash
# Publish VSSS images to a personal Docker Hub namespace when OpenG2P
# does not have openg2p/openg2p-vsss-* repositories.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

export DOCKER_IMAGE_NAMESPACE="${DOCKER_IMAGE_NAMESPACE:-asierneb}"
export BUILD_PLATFORM="${BUILD_PLATFORM:-linux/amd64}"
export PUSH="${PUSH:-1}"
export DOCKER_EXTRA_TAGS="${DOCKER_EXTRA_TAGS:-1.1.3}"

bash docker/scripts/build.sh \
  staff-portal-api/1.1.3.txt \
  partner-api/1.1.3.txt \
  celery/1.1.3.txt

SEED="${DOCKER_IMAGE_NAMESPACE}/openg2p-vsss-db-seed:1.1.3"
docker build --platform "${BUILD_PLATFORM}" \
  -f docker/db-seed/Dockerfile \
  -t "${SEED}" \
  "$ROOT"
if [[ "${PUSH}" == "1" ]]; then
  docker push "${SEED}"
fi
