# MGLSD Village Social Security System — Celery image (workers + beat).
#
# Thin extension of the registry-platform celery base image. Adds the VSSS
# domain model and overlays run_celery.py with VSSS-specific worker patches
# (partner auto-approve, AWE bearer-from-Keycloak, service registration).
# CELERY_* ENV defaults are inherited from the base. A single image runs as
# worker or beat, selected at runtime via CELERY_APP.
#
# Build context = repo root (so openg2p-registry-vsss-extension/ is reachable).
ARG RP_VERSION=1.2.2-rc.509
FROM openg2p/openg2p-registry-celery:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_vsss_extension

COPY openg2p-registry-vsss-extension/ /app/openg2p-registry-vsss-extension/
RUN pip install --no-cache-dir /app/openg2p-registry-vsss-extension

COPY docker/celery/run_celery.py /app/run_celery.py

CMD ["python3", "/app/run_celery.py"]
