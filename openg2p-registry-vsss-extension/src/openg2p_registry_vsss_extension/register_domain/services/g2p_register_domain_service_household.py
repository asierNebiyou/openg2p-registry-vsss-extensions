import logging

from openg2p_registry_core.services import G2PRegisterDomainService
from openg2p_registry_core.models import G2PRegisterChangeRequest
from openg2p_registry_core.models.enum import ChangeActionEnum

from sqlalchemy.ext.asyncio import AsyncSession

from .domain_validation_utils import as_int, validation_error
from .utils.household_roster import (
    GEO_HIERARCHY_FIELDS,
    has_geo_affecting_changes,
    household_geo_payload,
    propagate_household_geo_to_members,
)

_logger = logging.getLogger('g2p-register-household-service')

class G2PRegisterDomainServiceHousehold(G2PRegisterDomainService):

    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            self._validate_household_size(record)
            self._validate_amount_required(record)

    def _validate_household_size(self, record: dict) -> None:
        household_size = as_int(record.get("household_size"))
        if household_size is not None and household_size < 0:
            validation_error("Household size cannot be negative")

    def _validate_amount_required(self, record: dict) -> None:
        amount_required = as_int(record.get("amount_required"))
        if amount_required is not None and amount_required < 0:
            validation_error("Amount required cannot be negative")

    async def pre_approve(self, change_request: G2PRegisterChangeRequest, session: AsyncSession):
        from openg2p_registry_core.models import G2PRegisterChangeRequestPayload
        from ..models.household import G2PRegisterHousehold

        payload_obj = await session.get(
            G2PRegisterChangeRequestPayload, change_request.change_request_id
        )
        if not payload_obj or not payload_obj.change_payload:
            return

        household = await session.get(
            G2PRegisterHousehold, change_request.internal_record_id
        )
        if not household:
            return

        for record in payload_obj.change_payload:
            if record.get("edit_action") == ChangeActionEnum.NO_CHANGE.value:
                continue
            if not has_geo_affecting_changes(record):
                continue

            merged_geo = {
                **household_geo_payload(household),
                **{
                    key: record[key]
                    for key in GEO_HIERARCHY_FIELDS
                    if key in record
                },
            }

            await propagate_household_geo_to_members(session, household, geo_payload=merged_geo)

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for household")

        keys = [
            "name",
            "functional_record_id",
            "polling_station",
            "bank_name",
            "account_number",
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

    def construct_intake_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing intake record name for household")
        return self.construct_record_name(payload, extra)

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for household")

        keys = ["name"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
