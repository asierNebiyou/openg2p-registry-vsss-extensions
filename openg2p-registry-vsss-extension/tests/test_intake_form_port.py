"""Guard: every VSSS register is wired end to end.

For each register/sub-table the VSSS domain owns there must be:
  * a model triple   — G2PRegister<X>, G2PRegisterHistory<X>, G2PIntakeForm<X>
  * a schema triple  — G2PRegisterSchema<X>, G2PRegisterHistorySchema<X>,
                       G2PIntakeFormSchema<X>
  * create_migrate() calls in app.py for all three model classes

This file was previously a verbatim copy of the mowsa-nsr test: it asserted
NSR's table inventory (HouseholdAsset, which VSSS does not have) and NSR's
schema naming (`G2PIntakeFormIndividualProgramSchema` rather than VSSS's
`G2PIntakeFormSchemaIndividualProgram`), so it could never pass here. Nothing
ran it, because the old helm-publish.yml workflow ran no tests at all.

Driving the assertions off one list means adding a register to the extension
without wiring it up fails here instead of at runtime.
"""

from pathlib import Path

import pytest

SRC_ROOT = Path(__file__).resolve().parents[1] / "src" / "openg2p_registry_vsss_extension"

# The registers and sub-tables the VSSS domain owns. Village is VSSS-only;
# NSR has no equivalent.
REGISTERS = [
    "Household",
    "HouseholdProgram",
    "HouseholdShock",
    "Individual",
    "IndividualDisability",
    "IndividualLivestock",
    "IndividualProgram",
    "Village",
]


def _read(path: str) -> str:
    return (SRC_ROOT / path).read_text()


@pytest.fixture(scope="module")
def models_init() -> str:
    return _read("register_domain/models/__init__.py")


@pytest.fixture(scope="module")
def schemas_init() -> str:
    return _read("register_domain/schemas/__init__.py")


@pytest.fixture(scope="module")
def app_py() -> str:
    return _read("app.py")


@pytest.mark.parametrize("register", REGISTERS)
def test_models_export_the_register_triple(models_init: str, register: str) -> None:
    for prefix in ("G2PRegister", "G2PRegisterHistory", "G2PIntakeForm"):
        name = f"{prefix}{register}"
        assert name in models_init, f"{name} is not exported from models/__init__.py"


@pytest.mark.parametrize("register", REGISTERS)
def test_schemas_export_the_register_triple(schemas_init: str, register: str) -> None:
    for prefix in ("G2PRegisterSchema", "G2PRegisterHistorySchema", "G2PIntakeFormSchema"):
        name = f"{prefix}{register}"
        assert name in schemas_init, f"{name} is not exported from schemas/__init__.py"


@pytest.mark.parametrize("register", REGISTERS)
def test_app_migration_covers_the_register_triple(app_py: str, register: str) -> None:
    for prefix in ("G2PRegister", "G2PRegisterHistory", "G2PIntakeForm"):
        call = f"{prefix}{register}.create_migrate()"
        assert call in app_py, f"app.py never calls {call}"


def test_app_migrates_the_intake_form_submission_table(app_py: str) -> None:
    # Submission rows are the parent of every intake-form row; without this the
    # intake tables migrate with no parent to reference.
    assert "G2PIntakeFormSubmission.create_migrate()" in app_py


def test_pmt_score_service_is_present() -> None:
    content = _read("score_compute/services/g2p_score_compute_service_pmt_score.py")
    assert "class G2PScoreComputeServicePmtScore" in content


def test_village_is_vsss_only_and_fully_wired(models_init: str, schemas_init: str) -> None:
    # The Village register is the headline VSSS addition over NSR — assert it
    # explicitly so a bad merge from the NSR lineage cannot quietly drop it.
    assert "G2PRegisterVillage" in models_init
    assert "G2PIntakeFormVillage" in models_init
    assert "G2PRegisterSchemaVillage" in schemas_init
    assert "G2PIntakeFormSchemaVillage" in schemas_init
