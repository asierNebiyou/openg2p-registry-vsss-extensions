#!/bin/sh
# Install the VSSS extension into a published registry-platform base image.
#
# Shared by docker/staff-portal-api, docker/partner-api and docker/celery so the
# three cannot drift.
#
# Why this is not a bare `pip install` of the source tree:
#
#   The base image is the runtime. It already carries the stack the platform
#   itself runs on -- openg2p-fastapi-common, openg2p-g2pconnect-common-lib,
#   sqlalchemy, pydantic, the DB driver -- and it has NO compiler. The platform
#   Dockerfile installs gcc/libc-dev/linux-headers as a virtual .build-deps
#   package and runs `apk del` before publishing. The fat build this image
#   replaced did its pip install while those were still present, so a transitive
#   dependency with no musllinux wheel could compile; here it cannot, and the
#   build dies with
#       error: command 'gcc' failed: No such file or directory
#       note: This error originates from a subprocess, and is likely not a
#             problem with pip.
#
#   Installing from a source tree also triggers a PEP 517 build (hatchling).
#   That needs PyPI at image-build time. Many Docker Desktop / CI runners can
#   pull Hub images but cannot reach pypi.org (Network unreachable). So the
#   preferred path is a prebuilt .whl copied into the build context — pip
#   installs the wheel with --no-deps and never talks to the network.
#
# So: install the extension alone (--no-deps), then PROVE the base really does
# satisfy it. If the assertion fails, fall back to a full install with build
# tooling added temporarily and removed again, so the image stays thin when the
# fast path works and still builds when it does not.
set -eu

EXT_DIR="${1:-/app/vsss-extension}"
DIST=openg2p-registry-vsss-extension
MODULE=openg2p_registry_vsss_extension

# Modules the extension expects from the base image.
REQUIRED="openg2p_fastapi_common openg2p_registry_core sqlalchemy pydantic"

install_extension() {
    # Prefer a prebuilt wheel (no hatchling / PyPI needed). Fall back to the
    # source tree when no wheel is present (environments that can reach PyPI).
    WHEEL="$(find "$EXT_DIR" -maxdepth 1 -name 'openg2p_registry_vsss_extension-*.whl' 2>/dev/null | head -n 1 || true)"
    if [ -n "$WHEEL" ] && [ -f "$WHEEL" ]; then
        echo "[install-extension] installing ${DIST} from wheel $(basename "$WHEEL") (--no-deps)"
        pip install --no-cache-dir --no-deps "$WHEEL"
    else
        echo "[install-extension] installing ${DIST} from ${EXT_DIR} (--no-deps)"
        pip install --no-cache-dir --no-deps "$EXT_DIR"
    fi
}

install_extension

assert_runtime() {
    for m in $REQUIRED; do
        python3 -c "import $m" >/dev/null 2>&1 || { echo "  missing from base image: $m"; return 1; }
    done
    python3 -c "import importlib.metadata as m; m.version('${DIST}')" >/dev/null 2>&1 \
        || { echo "  ${DIST} did not install"; return 1; }
    python3 -c "import importlib.util,sys; sys.exit(0 if importlib.util.find_spec('${MODULE}') else 1)" \
        || { echo "  ${MODULE} is not importable -- check the wheel-sources remap in pyproject.toml"; return 1; }
    return 0
}

if assert_runtime; then
    echo "[install-extension] base image satisfies the extension; staying thin"
    exit 0
fi

echo "[install-extension] base image is missing something; retrying with build tooling"
# Full resolve: reinstall from the same target we used above (wheel or source).
RETRY_TARGET="${WHEEL:-$EXT_DIR}"
if command -v apk >/dev/null 2>&1; then
    apk add --no-cache --virtual .ext-build gcc libc-dev linux-headers make
    pip install --no-cache-dir "$RETRY_TARGET"
    apk del --no-network .ext-build
elif command -v apt-get >/dev/null 2>&1; then
    apt-get update
    apt-get install -y --no-install-recommends gcc libc6-dev make
    pip install --no-cache-dir "$RETRY_TARGET"
    apt-get purge -y gcc libc6-dev make
    apt-get autoremove -y
    rm -rf /var/lib/apt/lists/*
else
    echo "[install-extension] no apk or apt-get available; cannot install build tooling" >&2
    exit 1
fi

assert_runtime || { echo "[install-extension] still unsatisfied after full install" >&2; exit 1; }
echo "[install-extension] installed with build tooling, which was then removed"
