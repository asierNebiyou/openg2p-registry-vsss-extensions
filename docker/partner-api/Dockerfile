# MGLSD Village Social Security System — Partner API image.
#
# Thin extension of the registry-platform base image (see docker/staff-portal-api/
# Dockerfile for the full rationale). Adds only the VSSS domain model.
#
# Build context = repo root. Install from the prebuilt wheel in
# docker/.build-wheels/ so this RUN step never needs PyPI for hatchling.
ARG RP_VERSION=1.2.2-rc.557
FROM --platform=linux/amd64 openg2p/openg2p-registry-partner-api:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_vsss_extension

COPY docker/.build-wheels/openg2p_registry_vsss_extension-*.whl /app/vsss-extension/
COPY docker/install-extension.sh /usr/local/bin/install-extension.sh
RUN /usr/local/bin/install-extension.sh /app/vsss-extension \
 && rm -rf /app/vsss-extension /usr/local/bin/install-extension.sh
