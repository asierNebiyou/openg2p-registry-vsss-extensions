# MGLSD Village Social Security System — Celery image (workers + beat).
#
# Thin extension of the registry-platform celery base image. Adds the VSSS
# domain model and overlays run_celery.py with VSSS-specific worker patches.
# CELERY_* ENV defaults are inherited from the base. A single image runs as
# worker or beat, selected at runtime via CELERY_APP.
#
# Build context = repo root. Install from the prebuilt wheel in
# docker/.build-wheels/ so this RUN step never needs PyPI for hatchling.
ARG RP_VERSION=1.2.2-rc.557
FROM --platform=linux/amd64 openg2p/openg2p-registry-celery:${RP_VERSION}

ENV REGISTRY_EXTENSION_MODULE=openg2p_registry_vsss_extension

COPY docker/.build-wheels/openg2p_registry_vsss_extension-*.whl /app/vsss-extension/
COPY docker/install-extension.sh /usr/local/bin/install-extension.sh
RUN /usr/local/bin/install-extension.sh /app/vsss-extension \
 && rm -rf /app/vsss-extension /usr/local/bin/install-extension.sh

COPY docker/celery/run_celery.py /app/run_celery.py

CMD ["python3", "/app/run_celery.py"]
