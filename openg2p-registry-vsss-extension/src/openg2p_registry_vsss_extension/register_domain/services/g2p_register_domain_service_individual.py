import logging

from sqlalchemy.ext.asyncio import AsyncSession
from openg2p_registry_core.models import G2PRegisterChangeRequest
from openg2p_registry_core.models.enum import ChangeActionEnum
from openg2p_registry_core.services import G2PRegisterDomainService

from .utils.household_roster import (
    affected_household_ids,
    has_roster_affecting_changes,
    member_payload,
    normalize_link,
    recompute_household_roster_for_household,
)

_logger = logging.getLogger('g2p-register-individual-service')


class G2PRegisterDomainServiceIndividual(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        _logger.info("Validating individual domain attributes")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for individual")

        keys = [
            "first_name",
            "middle_name",
            "last_name",
            "additional_name",
            "phone",
            "foundational_id",
            "functional_record_id",
            "polling_station",
            "bank_name",
            "bank_account_number",
            "application_reference",
        ]
        search_text = []
        if extra:
            search_text.extend(
                str(value).strip() for value in extra if str(value).strip()
            )
        search_text.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(search_text).strip()

    async def pre_approve(self, change_request: G2PRegisterChangeRequest, session: AsyncSession):
        from openg2p_registry_core.models import G2PRegisterChangeRequestPayload
        from ..models.individual import G2PRegisterIndividual

        payload_obj = await session.get(
            G2PRegisterChangeRequestPayload, change_request.change_request_id
        )
        if not payload_obj or not payload_obj.change_payload:
            return

        individual = await session.get(
            G2PRegisterIndividual, change_request.internal_record_id
        )
        if not individual:
            return

        for record in payload_obj.change_payload:
            if record.get("edit_action") == ChangeActionEnum.NO_CHANGE.value:
                continue
            if not has_roster_affecting_changes(record):
                continue

            old_link = normalize_link(individual.link_internal_record_id)
            merged_member = member_payload(individual, record)
            if "link_internal_record_id" in record:
                new_link = normalize_link(record.get("link_internal_record_id"))
                household_ids = affected_household_ids(old_link, new_link)
            elif old_link:
                household_ids = {old_link}
            else:
                continue

            for household_id in household_ids:
                await recompute_household_roster_for_household(
                    session,
                    household_id,
                    changed_member_id=change_request.internal_record_id,
                    changed_member_payload=merged_member,
                )

    async def post_ingest(self, register_id: str, register_row, session: AsyncSession):
        link_internal_record_id = normalize_link(
            getattr(register_row, "link_internal_record_id", None)
        )
        if not link_internal_record_id:
            return

        await recompute_household_roster_for_household(session, link_internal_record_id)

    def construct_intake_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing intake record name for individual")
        return self.construct_record_name(payload, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for individual")

        keys = ["first_name", "middle_name", "last_name", "additional_name"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
