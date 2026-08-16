import logging

from openg2p_registry_core.services import G2PRegisterDomainService
from openg2p_registry_core.schemas import ChangeRequestRequestPayload
from openg2p_registry_core.models import G2PRegisterChangeRequest
from openg2p_registry_core.models.enum import ChangeActionEnum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .domain_validation_utils import as_bool, as_float, as_int, validation_error
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


    def _validate_household_size(self, record: dict) -> None:
        household_size_total = as_int(record.get("household_size_total"))

        size_fields = {
            "adults": as_int(record.get("household_size_adults")),
            "children u5": as_int(record.get("household_size_children_u5")),
            "school age": as_int(record.get("household_size_school_age")),
            "elderly": as_int(record.get("household_size_elderly")),
        }

        if household_size_total is None:
            return

        for label, value in size_fields.items():
            if value is not None and value > household_size_total:
                validation_error(
                    f"Household size {label} cannot exceed household size total"
                )

        if all(value is not None for value in size_fields.values()):
            if sum(size_fields.values()) != household_size_total:
                validation_error(
                    "Household size total must equal the sum of household size "
                    "adults, children u5, school age, and elderly"
                )


    def _validate_overcrowding(self, record: dict) -> None:
        overcrowding = as_float(record.get("overcrowding_indicator"))
        household_size_total = as_int(record.get("household_size_total"))
        if overcrowding is not None and household_size_total is not None and overcrowding > household_size_total:
            validation_error("Overcrowding Indicator must not exceed household size total")


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
            "functional_record_id",
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


    def construct_intake_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing intake record name for household")

        keys = ["created_by", "application_reference"]
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
        _logger.info("Constructing record name for household")

        keys = ["created_by", "application_reference"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " - ".join(record_name).strip()