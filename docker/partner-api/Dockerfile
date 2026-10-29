# MGLSD Village Social Security System — Partner API image.
#
# Thin extension of the registry-platform base image (see docker/staff-portal-api/
# Dockerfile for the full rationale). Adds only the VSSS domain model.
#
# Build context = repo root (so openg2p-registry-vsss-extension/ is reachable).
ARG RP_VERSION=1.2.2-rc.557
FROM openg2p/openg2p-registry-partner-api:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_vsss_extension

COPY openg2p-registry-vsss-extension/ /app/vsss-extension/
# Install the domain package. See docker/install-extension.sh for why this is
# not a bare `pip install`: the base image has no compiler, so the extension is
# installed with --no-deps and the script then asserts the base actually
# satisfies it, falling back to a full install with temporary build tooling.
COPY docker/install-extension.sh /usr/local/bin/install-extension.sh
RUN /usr/local/bin/install-extension.sh /app/vsss-extension \
 && rm /usr/local/bin/install-extension.sh
