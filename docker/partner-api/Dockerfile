# MGLSD Village Social Security System — Partner API image.
#
# Thin extension of the registry-platform base image (see docker/staff-portal-api/
# Dockerfile for the full rationale). Adds only the VSSS domain model.
#
# Build context = repo root (so openg2p-registry-vsss-extension/ is reachable).
ARG RP_VERSION=1.2.2-rc.509
FROM openg2p/openg2p-registry-partner-api:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_vsss_extension

COPY openg2p-registry-vsss-extension/ /app/openg2p-registry-vsss-extension/
RUN pip install --no-cache-dir /app/openg2p-registry-vsss-extension
