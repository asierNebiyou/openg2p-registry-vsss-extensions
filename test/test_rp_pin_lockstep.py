"""Guard: the openg2p-registry pin must be identical in every place it appears.

A variant extends ONE registry-platform version, used two ways:
  * the Docker base images — `ARG RP_VERSION=<v>` in every docker/*/Dockerfile
  * the Helm chart — the `openg2p-registry` dependency `version:` in Chart.yaml

If these drift, an image is built FROM one base while the chart deploys another,
and the overlay lands on a harness it does not match. Before the inverted-build
migration this repo had no single pin at all: the docker/*/1.1.3.txt manifests
pinned registry-platform 1.1.2 while the chart pinned nothing, so a "1.1.3"
image was really 1.1.2 content. `scripts/bump-rp-version.sh` moves both
together; this test fails the build if anything ever splits them again.

No dependencies beyond the stdlib + pytest — runs anywhere the other tests do.
"""

import pathlib
import re

import pytest

REPO = pathlib.Path(__file__).resolve().parent.parent
CHART = REPO / "helm" / "vsss" / "Chart.yaml"


def _docker_pins():
    pins = {}
    for f in sorted((REPO / "docker").glob("*/Dockerfile")):
        m = re.search(r"^ARG RP_VERSION=(\S+)", f.read_text(), re.M)
        if m:
            pins[f.relative_to(REPO).as_posix()] = m.group(1)
    return pins


def _chart_pin():
    m = re.search(
        r"-\s*name:\s*openg2p-registry\b.*?version:\s*(\S+)",
        CHART.read_text(), re.S,
    )
    return m.group(1) if m else None


def test_every_dockerfile_declares_the_pin():
    """A Dockerfile without ARG RP_VERSION is building from an unpinned base."""
    dockerfiles = sorted((REPO / "docker").glob("*/Dockerfile"))
    assert dockerfiles, "no docker/*/Dockerfile found"
    unpinned = [
        f.relative_to(REPO).as_posix()
        for f in dockerfiles
        if not re.search(r"^ARG RP_VERSION=", f.read_text(), re.M)
    ]
    assert not unpinned, f"Dockerfile(s) with no ARG RP_VERSION: {unpinned}"


def test_rp_pin_is_in_lockstep():
    docker = _docker_pins()
    chart = _chart_pin()
    assert docker, "no ARG RP_VERSION found in any docker/*/Dockerfile"
    assert chart, "no openg2p-registry dependency version found in Chart.yaml"

    all_pins = set(docker.values()) | {chart}
    if len(all_pins) != 1:
        lines = [f"  helm/vsss/Chart.yaml openg2p-registry dependency: {chart}"]
        lines += [f"  {p}: {v}" for p, v in docker.items()]
        pytest.fail(
            "openg2p-registry pin has SPLIT — images and chart must be identical:\n"
            + "\n".join(lines)
            + "\n\nFix with: ./scripts/bump-rp-version.sh <version>"
        )
