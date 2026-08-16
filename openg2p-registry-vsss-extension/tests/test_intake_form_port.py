from pathlib import Path


SRC_ROOT = Path(__file__).resolve().parents[1] / "src" / "openg2p_registry_nsr_extension"


def _read(path: str) -> str:
    return (SRC_ROOT / path).read_text()


def test_models_export_intake_form_classes():
    content = _read("register_domain/models/__init__.py")
    assert "G2PIntakeFormHousehold" in content
    assert "G2PIntakeFormIndividual" in content
    assert "G2PIntakeFormIndividualProgram" in content
    assert "G2PIntakeFormHouseholdAsset" in content


def test_schemas_export_intake_form_classes():
    content = _read("register_domain/schemas/__init__.py")
    assert "G2PIntakeFormSchemaHousehold" in content
    assert "G2PIntakeFormSchemaIndividual" in content
    assert "G2PIntakeFormIndividualProgramSchema" in content
    assert "G2PIntakeFormHouseholdAssetSchema" in content


def test_app_migration_includes_intake_form_tables():
    content = _read("app.py")
    assert "G2PIntakeFormHousehold.create_migrate()" in content
    assert "G2PIntakeFormIndividual.create_migrate()" in content
    assert "G2PIntakeFormIndividualProgram.create_migrate()" in content
    assert "G2PIntakeFormHouseholdAsset.create_migrate()" in content


def test_pmt_service_is_exposed():
    content = _read("score_compute/services/__init__.py")
    assert "G2PScoreComputeServicePmtScore" in content
