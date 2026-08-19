import os
import sys
import importlib

def get_app():
    app_path = os.environ.get("CELERY_APP")
    if not app_path:
        print("Error: CELERY_APP environment variable is not set.")
        sys.exit(1)
    
    try:
        # Support both module:attr and module.attr
        if ":" in app_path:
            module_name, app_attr = app_path.split(":", 1)
        else:
            module_name, app_attr = app_path.rsplit(".", 1)
            
        module = importlib.import_module(module_name)
        return getattr(module, app_attr)
    except Exception as e:
        print(f"Error loading Celery app '{app_path}': {e}")
        sys.exit(1)

def _celery_tasks_dir():
    """Resolve tasks/ without importing task modules (tasks/__init__ eager-loads all workers)."""
    from pathlib import Path

    import openg2p_registry_celery_worker as celery_pkg

    return Path(celery_pkg.__file__).resolve().parent / "tasks"


def patch_partner_cr_auto_approve_worker() -> None:
    """Hot-patch change_request_ingest_worker when the celery image lacks PR #60."""
    path = _celery_tasks_dir() / "change_request_ingest_worker.py"
    if not path.is_file():
        print("change_request_ingest_worker not found; skipping partner CR auto-approve patch")
        return

    content = path.read_text()
    if "cr_auto_approve_for_partner" in content:
        return

    import_anchor = """from openg2p_registry_core.services.g2p_change_request_worker_service import (
    G2PChangeRequestWorkerService,
)"""
    import_patch = """from openg2p_registry_core.services.g2p_change_request_worker_service import (
    G2PChangeRequestWorkerService,
)
from openg2p_registry_core.services.g2p_register_change_request_service import (
    G2PRegisterChangeRequestService,
)"""
    if import_anchor not in content:
        raise RuntimeError(f"change_request_ingest_worker import anchor missing in {path}")

    block_anchor = """                classified.change_request_id = cr.change_request_id
                classified.ingestion_number_of_attempts += 1
                classified.ingestion_status = ProcessStatusEnum.PROCESSED.value
                classified.ingestion_latest_error_code = None
                classified.ingestion_date_time = datetime.now()
                session.add(classified)"""
    block_patch = block_anchor + """
                section = await session.get(G2PRegisterSection, classified.section_id)
                if section is not None and getattr(section, "cr_auto_approve_for_partner", False):
                    cr_change_request_service = G2PRegisterChangeRequestService.get_component()
                    await cr_change_request_service._approve_change_request_core(
                        change_request_id=cr.change_request_id,
                        session=session,
                        skip_verification=True,
                        approved_by="system",
                    )
                    await cr_change_request_service._fanout_outgest_for_change_request(cr, session)
                    _logger.info(
                        "Auto-approved partner change request %s (section=%s)",
                        cr.change_request_id,
                        classified.section_id,
                    )"""
    if block_anchor not in content:
        raise RuntimeError(f"change_request_ingest_worker block anchor missing in {path}")

    path.write_text(content.replace(import_anchor, import_patch, 1).replace(block_anchor, block_patch, 1))
    print(f"Patched partner CR auto-approve gate in {path}")


def patch_partner_intake_auto_approve_worker() -> None:
    """Hot-patch ingest_data_worker to auto-approve partner intake when section opts in."""
    path = _celery_tasks_dir() / "ingest_data_worker.py"
    if not path.is_file():
        print("ingest_data_worker not found; skipping partner intake auto-approve patch")
        return

    content = path.read_text()
    if (
        "cr_auto_approve_for_partner" in content
        and "approve_submission_with_session" in content
    ):
        return

    block_anchor = """            await _finalize_submission_async(submission_id, session)

            incoming_classified_data.ingestion_number_of_attempts += 1"""
    block_patch = """            await _finalize_submission_async(submission_id, session)
            # Partner auto-approve (VSSS): when any register section opts in, approve immediately
            # so intake_form_register_ingest beat can materialise the record.
            try:
                from sqlalchemy import select as _sa_select
                from openg2p_registry_core.models import G2PRegisterSection as _G2PRegisterSection

                _sections = (
                    await session.execute(
                        _sa_select(_G2PRegisterSection).where(
                            _G2PRegisterSection.register_id
                            == incoming_classified_data.register_id
                        )
                    )
                ).scalars().all()
                if any(getattr(s, "cr_auto_approve_for_partner", False) for s in _sections):
                    await G2PIntakeFormDataService.get_component().approve_submission_with_session(
                        submission_id, session, approved_by="system"
                    )
                    _logger.info(
                        "Auto-approved partner intake submission %s", submission_id
                    )
            except Exception as _auto_exc:  # noqa: BLE001 — never fail ingest on approve
                _logger.exception(
                    "Partner intake auto-approve failed for %s: %s",
                    submission_id,
                    _auto_exc,
                )

            incoming_classified_data.ingestion_number_of_attempts += 1"""
    if block_anchor not in content:
        raise RuntimeError(f"ingest_data_worker finalize anchor missing in {path}")

    path.write_text(content.replace(block_anchor, block_patch, 1))
    print(f"Patched partner intake auto-approve gate in {path}")


def patch_awe_bearer_from_keycloak() -> None:
    """Partner ingest finalize has no user bearer; fetch client-credentials token."""
    import json
    import urllib.parse
    import urllib.request

    from openg2p_registry_core.errors import G2PRegistryErrorCodes, G2PRegistryException
    from openg2p_registry_core.services.g2p_awe_integration_service import (
        G2PAweIntegrationService,
    )

    token_url = (os.environ.get("REGISTRY_CORE_KEYCLOAK_TOKEN_URL") or "").strip()
    client_id = (os.environ.get("REGISTRY_CORE_KEYCLOAK_CLIENT_ID") or "").strip()
    client_secret = (os.environ.get("REGISTRY_CORE_KEYCLOAK_CLIENT_SECRET") or "").strip()
    if not all([token_url, client_id, client_secret]):
        return

    def _fetch_token() -> str:
        data = urllib.parse.urlencode(
            {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            }
        ).encode()
        req = urllib.request.Request(token_url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())["access_token"]

    def _require_bearer(self, bearer_token: str | None) -> str:
        token = (bearer_token or "").strip() or _fetch_token()
        if not token:
            raise G2PRegistryException(
                code=G2PRegistryErrorCodes.AWE_BEARER_TOKEN_REQUIRED.value[1],
                message=G2PRegistryErrorCodes.AWE_BEARER_TOKEN_REQUIRED.value[0],
            )
        return token

    G2PAweIntegrationService._require_bearer = _require_bearer


def ensure_registry_services():
    """Register intake/AWE services omitted by the celery worker Initializer."""
    from openg2p_registry_core.helpers import AweHelper
    from openg2p_registry_core.services.g2p_awe_integration_service import (
        G2PAweIntegrationService,
    )
    from openg2p_registry_core.services.g2p_awe_policy_configuration_service import (
        G2PAwePolicyConfigurationService,
    )
    from openg2p_registry_core.services.g2p_document_service import G2PDocumentService
    from openg2p_registry_core.services.g2p_register_history_service import (
        G2PRegisterHistoryService,
    )
    from openg2p_registry_core.services.g2p_score_compute_service import (
        G2PScoreComputeService,
    )
    from openg2p_registry_core.services.g2p_verification_service import (
        G2PRegisterVerificationService,
    )
    from openg2p_registry_core.services.intake_form_data_service import (
        G2PIntakeFormDataService,
    )

    if G2PAwePolicyConfigurationService.get_component() is None:
        G2PAwePolicyConfigurationService()
    if G2PAweIntegrationService.get_component() is None:
        G2PAweIntegrationService()
    if G2PIntakeFormDataService.get_component() is None:
        G2PIntakeFormDataService()
    if G2PRegisterVerificationService.get_component() is None:
        G2PRegisterVerificationService()
    if G2PDocumentService.get_component() is None:
        G2PDocumentService()
    if G2PRegisterHistoryService.get_component() is None:
        G2PRegisterHistoryService()
    if G2PScoreComputeService.get_component() is None:
        G2PScoreComputeService()
    if AweHelper.get_component() is None:
        AweHelper()
    patch_awe_bearer_from_keycloak()


def patch_ingest_finalize() -> None:
    """Ensure AWE services exist before partner-ingest finalize (prefork-safe)."""
    import importlib

    idw = importlib.import_module("openg2p_registry_celery_worker.tasks.ingest_data_worker")

    original_finalize = getattr(idw, "_finalize_submission_async", None)
    if original_finalize is not None and not getattr(
        original_finalize, "_awe_services_patched", False
    ):

        async def finalize_with_services(submission_id: str, session) -> None:
            ensure_registry_services()
            return await original_finalize(submission_id, session)

        finalize_with_services._awe_services_patched = True
        idw._finalize_submission_async = finalize_with_services

    original_process = getattr(idw, "_process_ingestion_async", None)
    if original_process is not None and not getattr(
        original_process, "_awe_services_patched", False
    ):

        async def process_with_services(ingest_id: str) -> None:
            ensure_registry_services()
            patch_ingest_finalize()
            return await original_process(ingest_id)

        process_with_services._awe_services_patched = True
        idw._process_ingestion_async = process_with_services


def setup_worker_process_init(celery_app):
    """Register services in each prefork worker child (not inherited from parent)."""
    from celery.signals import worker_process_init

    @worker_process_init.connect(weak=False)
    def _register_services_on_fork(**kwargs):
        ensure_registry_services()
        patch_ingest_finalize()


def setup_task_prerun(celery_app):
    """Fallback: ensure services before every task (prefork child init can be unreliable)."""
    from celery.signals import task_prerun

    @task_prerun.connect(weak=False)
    def _register_services_before_task(**kwargs):
        ensure_registry_services()
        patch_ingest_finalize()


def main():
    patch_partner_cr_auto_approve_worker()
    patch_partner_intake_auto_approve_worker()
    celery_app = get_app()
    patch_ingest_finalize()
    setup_worker_process_init(celery_app)
    setup_task_prerun(celery_app)
    ensure_registry_services()

    # Add dynamic imports
    imports_str = os.environ.get("CELERY_IMPORTS", "")
    extra_imports = [i.strip() for i in imports_str.split(",") if i.strip()]
    
    if extra_imports:
        print(f"Adding imports: {extra_imports}")
        # Ensure include is a list
        current_include = list(celery_app.conf.include) if celery_app.conf.include else []
        celery_app.conf.update(include=current_include + extra_imports)
    
    # Run the worker/beat
    opts = os.environ.get("CELERY_OPTS", "worker --loglevel=info").split()
    print(f"Starting Celery with options: {opts}")
    
    # celery_app.start(argv=...) passes arguments to click.
    # Click expects the first argument to be the subcommand (e.g. 'worker').
    # We do NOT pass the program name 'celery' here.
    try:
        celery_app.start(argv=opts)
    except Exception as e:
        print(f"Error starting via app.start(): {e}")
        raise

if __name__ == "__main__":
    main()
