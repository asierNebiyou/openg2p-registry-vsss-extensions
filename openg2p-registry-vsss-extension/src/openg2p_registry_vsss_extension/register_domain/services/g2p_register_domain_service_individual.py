import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from openg2p_registry_core.models import G2PRegisterChangeRequest
from openg2p_registry_core.models.enum import ChangeActionEnum
from openg2p_registry_core.services import G2PRegisterDomainService

from .disability_status_sync import sync_register_individual_disability_status
from .domain_validation_utils import as_bool, is_blank, validation_error
from .utils.household_roster import (
    affected_household_ids,
    calculate_age,
    has_roster_affecting_changes,
    member_payload,
    normalize_link,
    recompute_household_roster_for_household,
)

_logger = logging.getLogger('g2p-register-individual-service')


class G2PRegisterDomainServiceIndividual(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        _logger.info("Validating individual domain attributes")
        for record in records:
            self._validate_livelihood_distinct(record)
            self._validate_identifier(record)
        self._validate_single_household_head(records)

    def _validate_single_household_head(self, records: list[dict]) -> None:
        head_count = 0
        _logger.info("records to validate for household head: %s", records)
        for record in records:
            if record.get("edit_action") == "DELETE":
                continue

            if as_bool(record.get("is_head")):
                head_count += 1
                if head_count > 1:
                    validation_error(
                        "Only one household head is allowed per household"
                    )
        _logger.info(f"Household head count: {head_count}")

    def _validate_livelihood_distinct(self, record: dict) -> None:
        primary = record.get("primary_livelihood")
        secondary = record.get("secondary_livelihood")
        if (
            not is_blank(primary)
            and not is_blank(secondary)
            and str(primary).strip() == str(secondary).strip()
        ):
            validation_error(
                "Primary livelihood and secondary livelihood must be different"
            )

    def _validate_identifier(self, record: dict) -> None:
        """Require at least one of Fayda ID or RID."""
        if record.get("edit_action") == "DELETE":
            return

        foundational_id = record.get("foundational_id")
        rid = record.get("rid")
        has_fid = not is_blank(foundational_id)
        has_rid = not is_blank(rid)

        if not has_fid and not has_rid:
            # Legacy rows without identifiers may edit non-identifier sections; merge
            # clears spurious identifier fields to None before validation.
            if record.get("has_national_id") is None:
                return
            validation_error("Either Fayda ID or RID is required")

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for individual")

        keys = [
            "first_name",
            "middle_name",
            "last_name",
            "foundational_id",
            "functional_record_id",
            "primary_phone",
            "geo_code_hierarchy_json",
            "application_reference"
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

        keys = ["first_name", "middle_name", "last_name"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for individual")

        keys = ["first_name", "middle_name", "last_name"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()