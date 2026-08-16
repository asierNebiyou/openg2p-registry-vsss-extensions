#!/bin/sh
set -e

# ──────────────────────────────────────────────────────────────
# OpenG2P MGLSD Registry DB Seed Entrypoint
#
# Meta-data SQL ships with the vsss-extension (register definitions, schemas,
# tabs, sections, lookups, configs). Sample registrant data, sub-table data
# and profile images come from openg2p-data (cloned into /openg2p-data at
# image build time). Jinja templates ship under the extension's templates/
# folder and are uploaded to MinIO with object key = filename
# (= g2p_registry_documents.document_store_id).
#
# Expected environment variables:
#   PGHOST, PGPORT (default 5432), PGDATABASE, PGUSER, PGPASSWORD
#   LOAD_SAMPLE_DATA — "true" to load demography + VSSS sub-tables (default: false)
#   LOAD_IMAGES      — "true" to upload profile images to MinIO (default: false)
#   LOAD_TEMPLATES   — "true" to upload Jinja templates to MinIO (default: false)
#   MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE
#   TEMPLATE_BUCKET_NAME, TEMPLATES_DIR — default bucket "templates" (DocumentBucket.TEMPLATES)
#   IMAGE_BUCKET_NAME, IMAGES_DIR — default bucket "documents" (DocumentBucket.DOCUMENTS)
#   OPENG2P_DATA_DIR (default "/openg2p-data")
#
# Master-data database (geo reference data; the master-data service is a generic
# commons service and ships no seed data, so geo — which is registry sample /
# reference data — is loaded here into the master_data DB over the network):
#   MD_PGHOST, MD_PGPORT, MD_PGDATABASE, MD_PGUSER, MD_PGPASSWORD
#   LOAD_GEO_DATA — "true" to load the geo hierarchy into master_data (default:
#                   "false"). Enable alongside LOAD_SAMPLE_DATA so the geo ids the
#                   registry rows derive already resolve in master_data.
# ──────────────────────────────────────────────────────────────

PGPORT="${PGPORT:-5432}"
LOAD_GEO_DATA="${LOAD_GEO_DATA:-false}"
LOAD_SAMPLE_DATA="${LOAD_SAMPLE_DATA:-false}"
LOAD_IMAGES="${LOAD_IMAGES:-false}"
LOAD_TEMPLATES="${LOAD_TEMPLATES:-false}"

SEED_DIR="/seed"
META_DATA_DIR="${SEED_DIR}/meta_data"

run_sql_files() {
  dir="$1"
  label="$2"

  if [ ! -d "$dir" ]; then
    echo "[db-seed] No ${label} directory found at ${dir}, skipping."
    return
  fi

  sql_files=$(find "$dir" -name '*.sql' -type f | sort)
  if [ -z "$sql_files" ]; then
    echo "[db-seed] No SQL files found in ${dir}, skipping."
    return
  fi

  echo "[db-seed] Running ${label} scripts from ${dir} ..."
  for f in $sql_files; do
    echo "[db-seed]   -> $(basename "$f")"
    psql -v ON_ERROR_STOP=0 -f "$f"
  done
  echo "[db-seed] ${label} scripts completed."
}

echo "============================================="
echo " OpenG2P MGLSD Registry DB Seed"
echo " Extension     : ${EXTENSION_FOLDER:-unknown}"
echo " Database      : ${PGDATABASE}@${PGHOST}:${PGPORT}"
echo " Master DB     : ${MD_PGDATABASE:-unset}@${MD_PGHOST:-unset}:${MD_PGPORT:-5432}"
echo " Geo data      : ${LOAD_GEO_DATA}"
echo " Sample data   : ${LOAD_SAMPLE_DATA}"
echo " Images        : ${LOAD_IMAGES}"
echo " Templates     : ${LOAD_TEMPLATES}"
echo "============================================="

# 1. Meta-data SQL (always)
run_sql_files "$META_DATA_DIR" "meta-data"

# 1b. Master-data SQL (incoming partner registrations for connector senders).
# Runs against the shared master-data DB when MD_PG* creds are provided.
# Uses per-invocation PG* overrides so the main PG* env stays untouched.
MASTER_DATA_SEED_ENABLED="${MASTER_DATA_SEED_ENABLED:-false}"
MASTER_DATA_DIR="${SEED_DIR}/master_data"
if [ "$MASTER_DATA_SEED_ENABLED" = "true" ] && [ -n "${MD_PGDATABASE:-}" ]; then
  echo "[db-seed] Running master-data scripts against ${MD_PGDATABASE}@${MD_PGHOST:-$PGHOST} ..."
  # Subshell so the PG* overrides don't leak into later steps.
  (
    export PGHOST="${MD_PGHOST:-$PGHOST}"
    export PGPORT="${MD_PGPORT:-$PGPORT}"
    export PGDATABASE="${MD_PGDATABASE}"
    export PGUSER="${MD_PGUSER:-$PGUSER}"
    export PGPASSWORD="${MD_PGPASSWORD:-$PGPASSWORD}"
    run_sql_files "$MASTER_DATA_DIR" "master-data"
  )
else
  echo "[db-seed] Skipping master-data seed (MASTER_DATA_SEED_ENABLED=${MASTER_DATA_SEED_ENABLED})."
fi

# 1c. Geo reference data into the master_data DB. Must run before sample data so
#     the geo ids derived by load_sample_data.py already resolve in master_data.
#     Opt-in: defaults OFF so existing environments are unchanged.
if [ "$LOAD_GEO_DATA" = "true" ]; then
  echo "[db-seed] Loading geo data into master_data ..."
  python3 /seed/load_geo_data.py
else
  echo "[db-seed] Skipping geo data (LOAD_GEO_DATA=${LOAD_GEO_DATA})."
fi

# 2. Sample data from openg2p-data JSON
if [ "$LOAD_SAMPLE_DATA" = "true" ]; then
  echo "[db-seed] Loading sample data from openg2p-data ..."
  python3 /seed/load_sample_data.py
else
  echo "[db-seed] Skipping sample data (LOAD_SAMPLE_DATA=${LOAD_SAMPLE_DATA})."
fi

# 3. Profile images to MinIO
if [ "$LOAD_IMAGES" = "true" ]; then
  echo "[db-seed] Uploading profile images to MinIO ..."
  python3 /seed/upload_images.py
else
  echo "[db-seed] Skipping image upload (LOAD_IMAGES=${LOAD_IMAGES})."
fi

# 4. Jinja templates to MinIO
if [ "$LOAD_TEMPLATES" = "true" ]; then
  echo "[db-seed] Uploading templates to MinIO ..."
  python3 /seed/upload_templates.py
else
  echo "[db-seed] Skipping template upload (LOAD_TEMPLATES=${LOAD_TEMPLATES})."
fi

echo "[db-seed] Done."
