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
