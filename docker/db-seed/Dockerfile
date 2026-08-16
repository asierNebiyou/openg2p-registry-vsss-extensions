# MGLSD VSSS DB-seed image.
#
# Postgres-client image that ships:
#   - meta_data SQL from the openg2p-registry-vsss-extension
#   - flat Jinja templates from the openg2p-registry-vsss-extension
#   - openg2p-data repo (cloned at build time) containing demography JSON,
#     VSSS sub-table JSON and profile images
# At container-run time it:
#   - applies meta_data SQL against Postgres
#   - optionally loads sample data from openg2p-data JSON via load_sample_data.py
#   - optionally uploads profile images to MinIO via upload_images.py
#   - optionally uploads Jinja templates to MinIO via upload_templates.py
#
# Build context = repo root (so that openg2p-registry-vsss-extension/ and
# docker/db-seed/ are both reachable).

ARG EXTENSION_FOLDER=openg2p-registry-vsss-extension

FROM postgres:16-alpine

ARG EXTENSION_FOLDER
ARG GIT_COMMIT=dev
ARG BUILD_TIME=dev
ARG OPENG2P_DATA_REPO=https://github.com/openg2p/openg2p-data.git
ARG OPENG2P_DATA_BRANCH=2.0

ENV GIT_COMMIT=${GIT_COMMIT} \
    BUILD_TIME=${BUILD_TIME} \
    EXTENSION_FOLDER=${EXTENSION_FOLDER} \
    OPENG2P_DATA_DIR=/openg2p-data

RUN apk add --no-cache python3 py3-pip py3-psycopg2 git

COPY docker/db-seed/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir --break-system-packages -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Copy meta-data SQL and flat templates from the extension source tree.
# (sample_data/ no longer exists in the extension — data lives in openg2p-data.)
COPY ${EXTENSION_FOLDER}/src/ /tmp/ext-src/

RUN mkdir -p /seed/meta_data /seed/master_data /seed/templates && \
    find /tmp/ext-src -maxdepth 2 -type d -name meta_data | while read d; do \
      cp -r "$d"/* /seed/meta_data/ 2>/dev/null || true; \
    done && \
    find /tmp/ext-src -maxdepth 2 -type d -name master_data | while read d; do \
      cp -r "$d"/* /seed/master_data/ 2>/dev/null || true; \
    done && \
    find /tmp/ext-src -maxdepth 2 -type d -name templates | while read d; do \
      find "$d" -maxdepth 1 -type f -name '*.j2' -exec cp {} /seed/templates/ \; ; \
    done && \
    rm -rf /tmp/ext-src

# Clone openg2p-data (demography JSON, VSSS sub-table JSON, images).
RUN git clone --depth 1 -b ${OPENG2P_DATA_BRANCH} ${OPENG2P_DATA_REPO} /openg2p-data \
    && rm -rf /openg2p-data/.git

# Optional seed-data JSON assets (dormant until load_sample_data is wired to them).
COPY docker/db-seed/seed-data/ /seed/seed-data/

COPY docker/db-seed/entrypoint.sh /seed/entrypoint.sh
COPY docker/db-seed/upload_templates.py /seed/upload_templates.py
COPY docker/db-seed/upload_images.py /seed/upload_images.py
COPY docker/db-seed/load_sample_data.py /seed/load_sample_data.py
COPY docker/db-seed/load_geo_data.py /seed/load_geo_data.py
RUN chmod +x /seed/entrypoint.sh \
             /seed/upload_templates.py \
             /seed/upload_images.py \
             /seed/load_sample_data.py \
             /seed/load_geo_data.py

ENTRYPOINT ["/seed/entrypoint.sh"]
