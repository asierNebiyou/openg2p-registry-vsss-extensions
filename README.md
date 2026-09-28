# Village Social Security System

An installable **Village Social Security System (VSSS)** built as a thin extension of the
OpenG2P [registry platform](https://github.com/OpenG2P/registry-platform). Under the
inverted build model the platform publishes the runnable base images and the
`openg2p-registry` Helm chart; this repo adds **only** the VSSS domain
(and the connector stack) on top.

This is the **`1.2`** line: images extend **registry-platform `1.2`** via the
pinned `RP_VERSION` in each Dockerfile and the matching `openg2p-registry` chart
dependency in `helm/vsss/Chart.yaml`.

## What this repo owns

| Path | Purpose |
|------|---------|
| `openg2p-registry-vsss-extension/` | VSSS domain package — Individual / Household / Village registers, services, seed metadata, connector templates |
| `docker/` | Thin Dockerfiles (`FROM openg2p/openg2p-registry-*` + `pip install` the extension) |
| `helm/vsss/` | Thin wrapper chart: pins `openg2p-registry`, VSSS values overlay, **connector** templates |
| `translation/` | Domain translation strings |
| `test/test_rp_pin_lockstep.py` | Fails CI if Docker `RP_VERSION` and chart dependency drift |

The `openg2p-registry` base image tag (`RP_VERSION` in each Dockerfile) and the
chart dependency version in `helm/vsss/Chart.yaml` are **hardcoded and
pinned together**. Images and the wrapper chart are versioned in lockstep by CI.

```bash
./scripts/bump-rp-version.sh -n          # dry-run: which version would be picked
./scripts/bump-rp-version.sh             # bump Dockerfiles + Chart.yaml together
```

## Deploy

```bash
helm repo add openg2p https://openg2p.github.io/openg2p-helm
helm dependency build ./helm/vsss
helm install vsss ./helm/vsss \
  --set global.registryHostname=vsss.example.org
```

Connector credentials (when `connector.seed.enabled=true`) come from a Secret
named `<release>-connector-seed` — see `helm/vsss/README.md`.

See deployment docs at [docs.openg2p.org](https://docs.openg2p.org).

## License

[MPL-2.0](LICENSE)
