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
# --no-deps is deliberate. The base image already carries the whole runtime the
# platform itself runs on (openg2p-fastapi-common, openg2p-g2pconnect-common-lib,
# sqlalchemy, pydantic, the DB driver), and it has no compiler: the platform
# Dockerfile installs gcc/libc-dev as a virtual .build-deps package and runs
# `apk del` before the image is published. The fat build this image replaced did
# its pip install WHILE those build deps were present, so a transitive dependency
# with no musllinux wheel could still compile. Here it cannot, and pip fails with
# "command 'gcc' failed: No such file or directory ... likely not a problem with
# pip". Installing only this package avoids resolving transitive deps that the
# base image already satisfies.
RUN pip install --no-cache-dir --no-deps /app/vsss-extension

COPY docker/celery/run_celery.py /app/run_celery.py

CMD ["python3", "/app/run_celery.py"]
