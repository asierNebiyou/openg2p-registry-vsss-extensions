# MGLSD Village Social Security System — Staff Portal API image.
#
# Under the inverted build model the registry-platform publishes the base image
# (platform code + fastapi-common/iam-core runtime + entrypoint/CMD/ENV). This
# image only adds the VSSS domain model on top: the vsss-extension is
# pip-installed under its own import name (openg2p_registry_vsss_extension) and
# selected at runtime by REGISTRY_EXTENSION_MODULE (Option C).
#
# RP_VERSION pins the openg2p-registry base image tag. Keep it in lockstep with
# the openg2p-registry chart dependency pinned in helm/vsss/Chart.yaml —
# test/test_rp_pin_lockstep.py fails the build if they drift.
#
# Build context = repo root. The extension is installed from a prebuilt wheel in
# docker/.build-wheels/ (produced by make docker-vsss-build / docker-vsss-build.sh)
# so this RUN step never needs PyPI for hatchling.
ARG RP_VERSION=1.2.2-rc.557
FROM --platform=linux/amd64 openg2p/openg2p-registry-staff-api:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_vsss_extension

COPY docker/.build-wheels/openg2p_registry_vsss_extension-*.whl /app/vsss-extension/
COPY docker/install-extension.sh /usr/local/bin/install-extension.sh
RUN /usr/local/bin/install-extension.sh /app/vsss-extension \
 && rm -rf /app/vsss-extension /usr/local/bin/install-extension.sh
