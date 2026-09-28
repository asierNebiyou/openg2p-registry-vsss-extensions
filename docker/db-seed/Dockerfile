# MGLSD Village Social Security System — DB-seed image.
#
# Thin extension of the registry-platform db-seed base image. Clears the
# reference seed content and replaces it with VSSS meta_data, AWE meta_data,
# templates, master_data partner rows, and sample seed JSON. Overrides the
# reference load_sample_data.py / upload_images.py with VSSS loaders.
# Also layers a small entrypoint extension that seeds /seed/master_data into the
# shared Master Data DB (connector sender partners).
#
# Build context = repo root (so openg2p-registry-vsss-extension/ and
# docker/db-seed/ are both reachable).
ARG RP_VERSION=1.2.2-rc.509
FROM openg2p/openg2p-registry-db-seed:${RP_VERSION}

RUN rm -rf /seed/meta_data/* /seed/awe_meta_data/* /seed/templates/* /seed/seed-data/* \
 && mkdir -p /seed/master_data

COPY openg2p-registry-vsss-extension/src/openg2p_registry_vsss_extension/meta_data/      /seed/meta_data/
COPY openg2p-registry-vsss-extension/src/openg2p_registry_vsss_extension/awe_meta_data/  /seed/awe_meta_data/
COPY openg2p-registry-vsss-extension/src/openg2p_registry_vsss_extension/templates/      /seed/templates/
COPY openg2p-registry-vsss-extension/src/openg2p_registry_vsss_extension/master_data/    /seed/master_data/
COPY docker/db-seed/seed-data/                                                          /seed/seed-data/

# VSSS domain-specific loaders + entrypoint (master_data seed step).
COPY docker/db-seed/load_sample_data.py /seed/load_sample_data.py
COPY docker/db-seed/upload_images.py    /seed/upload_images.py
COPY docker/db-seed/entrypoint.sh       /seed/entrypoint.sh

RUN chmod +x /seed/load_sample_data.py /seed/upload_images.py /seed/entrypoint.sh
