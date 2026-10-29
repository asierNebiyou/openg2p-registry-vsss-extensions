# MGLSD Village Social Security System — DB-seed image.
#
# Thin extension of the registry-platform db-seed base image. Clears the
# reference (farmer) seed content and replaces it with VSSS's meta_data,
# awe_meta_data, templates and sample seed JSON.
# Overrides the farmer-shaped loaders with the VSSS ones. No master_data is
# shipped: VSSS has no inbound connectors, so there are no sender partners
# to register.
#
# The base image already provides psql, the Python seed runtime,
# load_attributes_from_mds.py and sync_geo_widgets.py, so this image no longer
# builds from postgres:16-alpine and no longer clones openg2p-data at build
# time — sample data comes from the base image's data dir (OPENG2P_DATA_DIR).
#
# Build context = repo root (so openg2p-registry-vsss-extension/ and
# docker/db-seed/ are both reachable).
ARG RP_VERSION=1.2.2-rc.557
# Base images are published for linux/amd64 only; a variable keeps buildkit
# from warning about a constant --platform (FromPlatformFlagConstDisallowed).
ARG BASE_PLATFORM=linux/amd64
FROM --platform=${BASE_PLATFORM} openg2p/openg2p-registry-db-seed:${RP_VERSION}

ENV EXTENSION_FOLDER=openg2p-registry-vsss-extension

RUN rm -rf /seed/meta_data/* /seed/awe_meta_data/* /seed/templates/* /seed/seed-data/* /seed/master_data/* \
 && mkdir -p /seed/awe_meta_data

COPY openg2p-registry-vsss-extension/src/openg2p_registry_vsss_extension/meta_data/      /seed/meta_data/
COPY openg2p-registry-vsss-extension/src/openg2p_registry_vsss_extension/awe_meta_data/  /seed/awe_meta_data/
COPY openg2p-registry-vsss-extension/src/openg2p_registry_vsss_extension/templates/      /seed/templates/
COPY docker/db-seed/seed-data/                                                           /seed/seed-data/

# Seed deps (minio, for the MinIO uploads). Installed explicitly rather than
# relying on the base image, so the VSSS upload scripts cannot break if a base
# image drops them.
# Only install if the base image does not already provide it. The base has no
# compiler (the platform Dockerfile apk-dels its build deps before publishing),
# so an unnecessary resolve can fail on a transitive dep with no musllinux wheel.
COPY docker/db-seed/requirements.txt /tmp/requirements.txt
RUN python3 -c "import minio" >/dev/null 2>&1 \
 || pip install --no-cache-dir --break-system-packages -r /tmp/requirements.txt \
 ; rm /tmp/requirements.txt

# VSSS domain-specific loaders + entrypoint (AWE seed step).
COPY docker/db-seed/load_sample_data.py  /seed/load_sample_data.py
COPY docker/db-seed/load_geo_data.py     /seed/load_geo_data.py
COPY docker/db-seed/upload_images.py     /seed/upload_images.py
COPY docker/db-seed/upload_templates.py  /seed/upload_templates.py
COPY docker/db-seed/entrypoint.sh        /seed/entrypoint.sh

RUN chmod +x /seed/load_sample_data.py /seed/load_geo_data.py \
             /seed/upload_images.py /seed/upload_templates.py /seed/entrypoint.sh
