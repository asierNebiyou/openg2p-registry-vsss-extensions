import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1] / "src" / "openg2p_registry_nsr_extension"
sys.path.insert(0, str(ROOT.parent))

import openg2p_registry_nsr_extension

sys.modules.setdefault("openg2p_registry_extensions", openg2p_registry_nsr_extension)

mock_core_services = ModuleType("openg2p_registry_core.services")
mock_core_services.G2PRegisterDomainService = type("G2PRegisterDomainService", (), {})
sys.modules["openg2p_registry_core.services"] = mock_core_services

domain_utils_mod = importlib.util.spec_from_file_location(
    "domain_validation_utils",
    ROOT / "register_domain/services/domain_validation_utils.py",
)
domain_utils_module = importlib.util.module_from_spec(domain_utils_mod)
assert domain_utils_mod.loader is not None
domain_utils_mod.loader.exec_module(domain_utils_module)
sys.modules[
    "openg2p_registry_nsr_extension.register_domain.services.domain_validation_utils"
] = domain_utils_module

register_domain_pkg = ModuleType("openg2p_registry_nsr_extension.register_domain")
register_domain_pkg.services = ModuleType("openg2p_registry_nsr_extension.register_domain.services")
register_domain_pkg.models = ModuleType("openg2p_registry_nsr_extension.register_domain.models")
sys.modules["openg2p_registry_nsr_extension.register_domain"] = register_domain_pkg
sys.modules["openg2p_registry_nsr_extension.register_domain.services"] = register_domain_pkg.services
sys.modules["openg2p_registry_nsr_extension.register_domain.models"] = register_domain_pkg.models

enums_spec = importlib.util.spec_from_file_location(
    "openg2p_registry_nsr_extension.register_domain.models.enums",
    ROOT / "register_domain/models/enums.py",
)
enums_module = importlib.util.module_from_spec(enums_spec)
assert enums_spec.loader is not None
enums_spec.loader.exec_module(enums_module)
sys.modules["openg2p_registry_nsr_extension.register_domain.models.enums"] = enums_module
DisabilityStatusEnum = enums_module.DisabilityStatusEnum

sync_mod_spec = importlib.util.spec_from_file_location(
    "openg2p_registry_nsr_extension.register_domain.services.disability_status_sync",
    ROOT / "register_domain/services/disability_status_sync.py",
)
sync_module = importlib.util.module_from_spec(sync_mod_spec)
assert sync_mod_spec.loader is not None
sync_mod_spec.loader.exec_module(sync_module)

has_disability_records = sync_module.has_disability_records


class TestHasDisabilityRecords:
    def test_empty_rows(self):
        assert has_disability_records([]) is False

    def test_blank_domain_and_severity_ignored(self):
        assert has_disability_records(
            [{"disability_domains": "", "disability_severity": None}]
        ) is False

    def test_domain_only_counts(self):
        assert has_disability_records([{"disability_domains": "PHYSICAL"}]) is True

    def test_severity_only_counts(self):
        assert has_disability_records([{"disability_severity": "MILD"}]) is True

    def test_delete_rows_ignored(self):
        assert has_disability_records(
            [{"edit_action": "DELETE", "disability_domains": "PHYSICAL"}]
        ) is False

    def test_finalize_derives_yes_from_disability_rows(self):
        has_rows = has_disability_records([{"disability_domains": "PHYSICAL"}])
        assert has_rows is True
        assert (
            DisabilityStatusEnum.YES if has_rows else DisabilityStatusEnum.NO
        ) == DisabilityStatusEnum.YES

    def test_finalize_derives_no_without_disability_rows(self):
        has_rows = has_disability_records([])
        assert has_rows is False
        assert (
            DisabilityStatusEnum.YES if has_rows else DisabilityStatusEnum.NO
        ) == DisabilityStatusEnum.NO
