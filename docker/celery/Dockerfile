# MGLSD Village Social Security System — Celery image (workers + beat).
#
# Thin extension of the registry-platform celery base image. Adds the VSSS
# domain model and overlays run_celery.py with VSSS-specific worker patches.
# CELERY_* ENV defaults are inherited from the base. A single image runs as
# worker or beat, selected at runtime via CELERY_APP.
#
# Build context = repo root (so openg2p-registry-vsss-extension/ is reachable).
ARG RP_VERSION=1.2.2-rc.557
FROM openg2p/openg2p-registry-celery:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_vsss_extension

COPY openg2p-registry-vsss-extension/ /app/vsss-extension/
# Install the domain package. See docker/install-extension.sh for why this is
# not a bare `pip install`: the base image has no compiler, so the extension is
# installed with --no-deps and the script then asserts the base actually
# satisfies it, falling back to a full install with temporary build tooling.
COPY docker/install-extension.sh /usr/local/bin/install-extension.sh
RUN /usr/local/bin/install-extension.sh /app/vsss-extension \
 && rm /usr/local/bin/install-extension.sh

COPY docker/celery/run_celery.py /app/run_celery.py

CMD ["python3", "/app/run_celery.py"]
