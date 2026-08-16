import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.enums import DisabilityStatusEnum
from .domain_validation_utils import is_blank

_logger = logging.getLogger("g2p-disability-status-sync")


def is_meaningful_disability_record(record: dict) -> bool:
    if record.get("edit_action") == "DELETE":
        return False
    return not is_blank(record.get("disability_domains")) or not is_blank(
        record.get("disability_severity")
    )


def has_disability_records(records: list[dict]) -> bool:
    return any(is_meaningful_disability_record(record) for record in records or [])


async def _load_disability_intake_rows(session: AsyncSession, submission_id: str) -> list:
    from ..models.individual_disability import G2PIntakeFormIndividualDisability

    result = await session.execute(
        select(G2PIntakeFormIndividualDisability).where(
            G2PIntakeFormIndividualDisability.submission_id == submission_id
        )
    )
    return result.scalars().all()


def _disability_status_from_rows(rows: list) -> DisabilityStatusEnum:
    records = [row.to_dict() if hasattr(row, "to_dict") else row for row in rows]
    return (
        DisabilityStatusEnum.YES
        if has_disability_records(records)
        else DisabilityStatusEnum.NO
    )


async def sync_intake_individual_disability_status(
    session: AsyncSession,
    submission_id: str,
) -> DisabilityStatusEnum | None:
    from ..models.individual import G2PIntakeFormIndividual

    result = await session.execute(
        select(G2PIntakeFormIndividual).where(
            G2PIntakeFormIndividual.submission_id == submission_id
        )
    )
    individual = result.scalar_one_or_none()
    if not individual:
        _logger.warning(
            "No intake individual row for submission %s; skipping disability_status sync",
            submission_id,
        )
        return None

    disability_rows = await _load_disability_intake_rows(session, submission_id)
    individual.disability_status = _disability_status_from_rows(disability_rows)
    session.add(individual)
    await session.flush()
    return individual.disability_status


async def sync_register_individual_disability_status(
    session: AsyncSession,
    register_row,
    submission_id: str | None = None,
) -> DisabilityStatusEnum | None:
    from ..models.individual import G2PIntakeFormIndividual, G2PRegisterIndividual

    if not isinstance(register_row, G2PRegisterIndividual):
        return None

    resolved_submission_id = submission_id
    if not resolved_submission_id:
        result = await session.execute(
            select(G2PIntakeFormIndividual).where(
                G2PIntakeFormIndividual.internal_record_id
                == register_row.internal_record_id
            )
        )
        intake_individual = result.scalar_one_or_none()
        if not intake_individual:
            return None
        resolved_submission_id = intake_individual.submission_id

    disability_rows = await _load_disability_intake_rows(session, resolved_submission_id)
    register_row.disability_status = _disability_status_from_rows(disability_rows)
    session.add(register_row)
    await session.flush()
    return register_row.disability_status
