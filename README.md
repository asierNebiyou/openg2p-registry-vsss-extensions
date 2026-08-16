# openg2p-registry-vsss-extensions

Village Social Security System (VSSS) customization layer for the [OpenG2P Registry Platform](https://docs.openg2p.org/products/registry).

## Repository layout

```
openg2p-registry-vsss-extension/   Python domain extension (__variant__ = vsss)
docker/                            VSSS-branded Docker images
helm/vsss/                         Self-sufficient Helm chart
translation/                       Staff Portal language packs
```

## Local developer

Use [openg2p-developer](https://github.com/OpenG2P/openg2p-developer):

```bash
make clone PROFILE=village-social-security-registry
make vsss-setup
make vsss-registry-run
```

## License

[MPL-2.0](LICENSE)
