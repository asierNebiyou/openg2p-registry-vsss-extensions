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
# Build context = repo root (so openg2p-registry-vsss-extension/ is reachable).
ARG RP_VERSION=1.2.2-rc.557
FROM openg2p/openg2p-registry-staff-api:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_vsss_extension

COPY openg2p-registry-vsss-extension/ /app/vsss-extension/
# Install the domain package. See docker/install-extension.sh for why this is
# not a bare `pip install`: the base image has no compiler, so the extension is
# installed with --no-deps and the script then asserts the base actually
# satisfies it, falling back to a full install with temporary build tooling.
COPY docker/install-extension.sh /usr/local/bin/install-extension.sh
RUN /usr/local/bin/install-extension.sh /app/vsss-extension \
 && rm /usr/local/bin/install-extension.sh
