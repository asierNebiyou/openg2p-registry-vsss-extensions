# vsss

Thin Helm wrapper for the **OpenG2P Village Social Security System (VSSS)**.

## What this chart owns

| Piece | Role |
|-------|------|
| `openg2p-registry` dependency (alias `registry`) | All registry services, IAM wiring, db-seed, id-generator, … |
| Values overlay | VSSS images, hostname, id pools, IAM tile name, seed toggles |
| `templates/connector/*` | VSSS connector stack (ODK / WebSub → Partner API) |

## Install

```bash
helm repo add openg2p https://openg2p.github.io/openg2p-helm
helm dependency build ./helm/vsss
helm install vsss ./helm/vsss \
  --set global.registryHostname=vsss.example.org
```

Images: `natiabebaw12/openg2p-vsss-{staff-portal-api,partner-api,celery,db-seed}` on Docker Hub.
Each image extends the matching `openg2p/openg2p-registry-*` base at the pinned
`RP_VERSION` / chart dependency version.
