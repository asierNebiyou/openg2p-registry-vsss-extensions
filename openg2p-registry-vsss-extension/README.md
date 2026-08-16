# OpenG2P Registry VSSS Extension

Uganda **Village Savings & Support System (VSSS)** domain extension for OpenG2P Registry Gen2.

Installs as the shared import package `openg2p_registry_extensions` (same remapping pattern as NSR). Only one domain extension can be installed at a time.

## Registers

| Mnemonic | Prefix | Description |
|----------|--------|-------------|
| Village | VSS | Village / SACCO grant unit |
| Household | VSH | Household under a village |
| Individual | VSI | Household members |

## Install (local)

```bash
# One-shot: install extension, migrate, seed metadata + sample villages
scripts/setup-vsss-registry.sh

# Then start Staff API + UI
scripts/run-vsss-registry-demo.sh
```

Schema for Village / VSSS household fields / intake is created by
`python -m openg2p_registry_staff_portal_api.main migrate` (VSSS extension migrate).
Seed scripts only insert metadata and demo rows — they do not “patch” the DB.
