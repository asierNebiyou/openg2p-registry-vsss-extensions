# MGLSD Village Social Security System (VSSS)

An installable **MGLSD Village Social Security System** built as a thin extension
of the OpenG2P [registry platform](https://github.com/OpenG2P/registry-platform).
Under the inverted build model the platform publishes the runnable base images
and the `openg2p-registry` Helm chart; this repo adds **only** the VSSS domain
on top.

This is the **`1.2`** line: images extend **registry-platform `1.2`** via the
pinned `RP_VERSION` in each Dockerfile and the matching `openg2p-registry` chart
dependency in `helm/vsss/Chart.yaml`.

## What this repo owns

| Path | Purpose |
|------|---------|
| `openg2p-registry-vsss-extension/` | VSSS domain package — Individual / Household / **Village** registers, services, seed metadata, AWE policies |
| `docker/` | Thin Dockerfiles (`FROM openg2p/openg2p-registry-*` + `pip install` the extension) |
| `helm/vsss/` | Thin wrapper chart: pins `openg2p-registry` and supplies the VSSS values overlay (no templates of its own) |
| `translation/` | Domain translation strings |
| `test/test_rp_pin_lockstep.py` | Fails CI if Docker `RP_VERSION` and the chart dependency drift |

The `openg2p-registry` base image tag (`RP_VERSION` in each Dockerfile) and the
chart dependency version in `helm/vsss/Chart.yaml` are **hardcoded and pinned
together**. Images and the wrapper chart are versioned in lockstep by CI.

```bash
./scripts/bump-rp-version.sh -n          # dry-run: which version would be picked
./scripts/bump-rp-version.sh             # bump Dockerfiles + Chart.yaml together
```

### Village register

VSSS adds a **Village** register (and Village intake form) above Household —
the main structural difference from the MoWSA NSR lineage this domain was ported
from. It has its own id type (`global`/`idgenerator` config in
`helm/vsss/values.yaml`) and its own AWE approval policies.

## Images

CI publishes four images to Docker Hub, all built from this repo's thin
Dockerfiles:

| Image | Built from |
|---|---|
| `openg2p/openg2p-vsss-staff-portal-api` | `docker/staff-portal-api/Dockerfile` |
| `openg2p/openg2p-vsss-partner-api` | `docker/partner-api/Dockerfile` |
| `openg2p/openg2p-vsss-celery` | `docker/celery/Dockerfile` |
| `openg2p/openg2p-vsss-db-seed` | `docker/db-seed/Dockerfile` |

There is **no VSSS staff UI image** — the chart uses the shared
`openg2p/openg2p-registry-staff-ui` published by the platform at `RP_VERSION`.

The namespace these are pulled from is a single value,
`global.vsssImageNamespace` (default `openg2p`). Point it at a personal
namespace for pre-release builds:

```bash
helm install vsss ./helm/vsss --set global.vsssImageNamespace=<your-namespace>
```

## Deploy

```bash
helm repo add openg2p https://openg2p.github.io/openg2p-helm
helm dependency build ./helm/vsss
helm install vsss ./helm/vsss \
  --set global.registryHostname=vsss.example.org
```

### No inbound connectors

VSSS registers through the staff portal and intake forms. The connector stack
and the three connector definitions this domain inherited from the MoWSA NSR
lineage (EDRMC WebSub, UD Social Registry WebSub, ODK) were Ethiopian — the
EDRMC definition still pointed at live production at `websub.hrp.edrmc.gov.et`,
and the ODK form was `nsr_registration_v13` with a woreda/zone/region mapper.
They have been removed, along with the inbound message rules, the NSR data
models and the sender-partner rows.

Adding a real inbound source needs all of these together: a data model under
`meta_data/data-models/`, key paths + semantic patterns + an incoming template
under `meta_data/registry-inbound-message-rules/`, a `g2p_partners` row for the
sender id (or the Partner API rejects every record with
`PARTNER_NOT_REGISTERED`), and the connector stack re-enabled in the chart.

See deployment docs at [docs.openg2p.org](https://docs.openg2p.org).

## Local development

The full local stack (infra, IAM, AWE, Master Data, registry, UI) is driven from
[openg2p-developer](https://github.com/OpenG2P/openg2p-developer):

```bash
make clone PROFILE=village-social-security-registry
make vsss-setup
make vsss-registry-run
```

## License

[MPL-2.0](LICENSE)
