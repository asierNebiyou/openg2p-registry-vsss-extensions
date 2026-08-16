import logging

from sqlalchemy import event, inspect, select, update

from openg2p_registry_core.models import G2PIntakeFormSubmission, IntakeFormStatusEnum

from ..services.disability_status_sync import has_disability_records

_logger = logging.getLogger("g2p-nsr-intake-submission-listeners")
_registered = False


def _submission_became_final(target: G2PIntakeFormSubmission) -> bool:
    if target.draft_status != IntakeFormStatusEnum.FINAL.value:
        return False
    state = inspect(target)
    history = state.attrs.draft_status.history
    if not history.has_changes():
        return False
    return bool(history.added) and history.added[-1] == IntakeFormStatusEnum.FINAL.value


def _sync_disability_status_on_finalize(connection, submission_id: str) -> None:
    from ..models.enums import DisabilityStatusEnum
    from ..models.individual import G2PIntakeFormIndividual
    from ..models.individual_disability import G2PIntakeFormIndividualDisability

    disability_rows = connection.execute(
        select(
            G2PIntakeFormIndividualDisability.disability_domains,
            G2PIntakeFormIndividualDisability.disability_severity,
        ).where(G2PIntakeFormIndividualDisability.submission_id == submission_id)
    ).all()

    records = [
        {"disability_domains": domains, "disability_severity": severity}
        for domains, severity in disability_rows
    ]
    status = (
        DisabilityStatusEnum.YES.value
        if has_disability_records(records)
        else DisabilityStatusEnum.NO.value
    )

    updated = connection.execute(
        update(G2PIntakeFormIndividual)
        .where(G2PIntakeFormIndividual.submission_id == submission_id)
        .values(disability_status=status)
    )
    if updated.rowcount == 0:
        _logger.warning(
            "No intake individual row for submission %s during finalize sync",
            submission_id,
        )


def _after_submission_update(mapper, connection, target: G2PIntakeFormSubmission) -> None:
    if not _submission_became_final(target):
        return

    _logger.info(
        "Syncing disability_status for finalized intake submission %s",
        target.submission_id,
    )
    _sync_disability_status_on_finalize(connection, target.submission_id)


def register_intake_submission_listeners() -> None:
    global _registered
    if _registered:
        return
    event.listen(G2PIntakeFormSubmission, "after_update", _after_submission_update)
    _registered = True
    _logger.info("Registered NSR intake submission finalize listeners")
