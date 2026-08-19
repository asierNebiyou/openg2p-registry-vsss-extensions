# vsss

Self-sufficient Helm chart for the **OpenG2P Village Social Security System (VSSS)**.

This chart owns its templates directly. It was derived from the OpenG2P
Registry Gen 2 base chart (`openg2p-registry`) — those templates and defaults
now live in this chart, so it **no longer depends on `openg2p-registry`**. The
only VSSS-specific differences from the base defaults are:

1. VSSS-branded Docker images for the VSSS components.
2. `global.registryVariant: vsss`.
3. ID Generator `idTypes`: `individual` (12) + `household` (10).

Everything else (deployments, services, gateways/virtualservices, db-seed Job,
logging, helper subcharts, …) comes from the inlined base-chart templates.

## Sub-dependencies

Same set as the base chart, declared in `Chart.yaml` and fetched from the
OpenG2P Helm repo (the packaged `.tgz` are gitignored, as in the base chart):

| Subchart | Version |
|---|---|
| common | 2.30.0 |
| postgres-init | 1.1.0 |
| redis | 19.6.4 |
| openg2p-id-generator (alias `idgenerator`) | 1.0.0 |
| keycloak-init | 1.1.2 |
| openg2p-awe | 1.0.0 |

Run `helm dependency build` (or `update`) before packaging/installing from a
fresh checkout.

## Versioning

Branch-name-equals-version convention:

| Branch | `Chart.yaml.version` |
|---|---|
| `develop` | `0.0.0-develop` |
| `1.0.0`   | `1.0.0` |
| `1.1.0`   | `1.1.0` |
| `1.1.1`   | `1.1.1` |
| `1.1.2`   | `1.1.2` |

## Images

| Component | Image |
|---|---|
| staffPortalApi | `asierneb/openg2p-vsss-staff-portal-api:develop` *(OpenG2P Hub repo does not exist yet)* |
| partnerApi | `asierneb/openg2p-vsss-partner-api:develop` |
| staffPortalUi | `openg2p/openg2p-registry-staff-portal-ui:1.1.1` *(OpenG2P; `1.1.2` is not on Hub)* |
| celeryBeatProducer / celeryWorker | `asierneb/openg2p-vsss-celery:develop` *(same image — mode picked by env vars)* |
| dbSeed | `asierneb/openg2p-vsss-db-seed:develop` |
| connector (api/worker/beat/consumer) | `asierneb/openg2p-connector-service:nsr-slashfix-202605221435` |
| connector UI | `asierneb/openg2p-connector-ui:nsr` |

All VSSS API/celery/db-seed images are built by this repo's docker workflows;
the Staff Portal UI image is built by the `registry-platform` repo.

## ID Generator `idTypes`

```yaml
idgenerator:
  idGenerator:
    appConfig:
      idTypes:
        individual:
          idLength: 12
        household:
          idLength: 10
```

## Installing

### From this repo (dev / CI)

```bash
cd helm/openg2p-vsss
helm dependency build
helm install vsss . \
  --namespace vsss \
  --create-namespace \
  --set global.registryHostname=vsss.example.com
```

Component URLs are auto-computed from `global.registryHostname`
(default `{{ .Release.Name }}.{{ .Release.Namespace }}.openg2p.org`).

### With sample data (dev / test only)

```bash
helm install vsss . --set dbSeed.loadSampleData=true
```

## Connector

The chart deploys the OpenG2P Connector alongside the registry
(`connector.enabled`, default `true`): `connector-api` (REST + WebSub webhook
receiver), `connector-worker` (Celery), `connector-beat` (scheduler,
singleton), and the admin SPA `connector-ui`. It gets its own release-scoped
database (`<release>_connector`, provisioned by postgres-init; tables are
created by the service on startup), shares this release's Redis on db `/1`,
and hands records to the registry via `http://<release>-partner-api/partner/ingest_data`.

Routing: `global.connectorHostname` (default
`connector-<registryHostname>`) is served by an Istio VirtualService — API
prefixes (`/connectors`, `/runs`, `/dlq`, `/metadata`, `/health`, `/webhook`)
go to the API, everything else to the UI. WebSub hubs must be able to reach
`https://<connectorHostname>/webhook/by-slug/<slug>`.

Everything the connector needs on the registry side ships with the chart:

- **Registry DB** — db-seed loads `connector_websub_data_models.sql`,
  `connector_websub_rules.sql` (key paths, semantic patterns, incoming
  templates) and `connector_websub_documents.sql` from the extension's
  `meta_data/`.
- **MinIO** — `dbSeed.loadTemplates=true` (default) uploads the Jinja
  transformation templates (`edrmc_websub_individual.j2`,
  `edrmc_websub_household.j2`, `ud_websub_individual.j2`) to the templates
  bucket.
- **Master data** — `dbSeed.seedMasterData=true` (default) inserts
  `g2p_partners` rows for the sender ids `edrmc-websub`, `ud-sr-websub`
  and `odk-vsss` into the shared master-data DB (Partner API rejects unknown
  senders).
- **Connector definitions** — a post-install/post-upgrade Job
  (`connector.seed`) upserts the EDRMC WebSub, UD Social Registry WebSub and
  ODK VSSS connector definitions through the connector API (idempotent,
  matched by name) and syncs WebSub subscriptions.

Credentials are never stored in values. Create the seed Secret (before or
after install — connectors with missing credentials are skipped and picked
up on the next `helm upgrade`):

```bash
kubectl -n <namespace> create secret generic <release>-connector-seed \
  --from-literal=EDRMC_WEBSUB_CLIENT_SECRET=... \
  --from-literal=EDRMC_WEBSUB_WEBHOOK_SECRET=... \
  --from-literal=UD_WEBSUB_CLIENT_SECRET=... \
  --from-literal=UD_WEBSUB_WEBHOOK_SECRET=... \
  --from-literal=ODK_EMAIL=... \
  --from-literal=ODK_PASSWORD=...
```

To point at a pre-existing connector DB (e.g. UD's `nsr_connector`),
override `global.connectorDB`, `global.connectorDBUser`,
`global.connectorDBSecret` and `global.connectorDBUserPasswordKey`.

## Rancher catalog

The chart ships a `questions.yaml` for Rancher UI installs (hostnames,
per-component enable toggles, image repo/tag overrides, db-seed toggles,
id-type note). Advanced users should edit `values.yaml` directly.
