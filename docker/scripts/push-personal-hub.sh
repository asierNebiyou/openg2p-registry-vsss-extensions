#!/usr/bin/env bash
# Publish VSSS images to a personal Docker Hub namespace when OpenG2P
# does not have openg2p/openg2p-vsss-* repositories.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

export DOCKER_IMAGE_NAMESPACE="${DOCKER_IMAGE_NAMESPACE:-asierneb}"
export BUILD_PLATFORM="${BUILD_PLATFORM:-linux/amd64}"
export PUSH="${PUSH:-1}"
export DOCKER_EXTRA_TAGS="${DOCKER_EXTRA_TAGS:-1.1.2}"

bash docker/scripts/build.sh \
  staff-portal-api/develop.txt \
  partner-api/develop.txt \
  celery/develop.txt

SEED="${DOCKER_IMAGE_NAMESPACE}/openg2p-vsss-db-seed:develop"
docker build --platform "${BUILD_PLATFORM}" \
  -f docker/db-seed/Dockerfile \
  -t "${SEED}" \
  -t "${DOCKER_IMAGE_NAMESPACE}/openg2p-vsss-db-seed:1.1.2" \
  "$ROOT"
if [[ "${PUSH}" == "1" ]]; then
  docker push "${SEED}"
  docker push "${DOCKER_IMAGE_NAMESPACE}/openg2p-vsss-db-seed:1.1.2"
fi
