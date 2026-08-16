import logging

from openg2p_registry_core.services import G2PRegisterDomainService
from sqlalchemy.ext.asyncio import AsyncSession

from .disability_status_sync import sync_register_individual_disability_status
from .domain_validation_utils import validation_error

_logger = logging.getLogger('g2p-register-individualdisability-service')

class G2PRegisterDomainServiceIndividualDisability(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        self._validate_no_duplicate_disability_domain(records)

    async def post_ingest(self, register_id: str, register_row, session: AsyncSession):
        from ..models.individual import G2PRegisterIndividual

        link_internal_record_id = getattr(register_row, "link_internal_record_id", None)
        if not link_internal_record_id:
            return

        parent = await session.get(G2PRegisterIndividual, link_internal_record_id)
        if parent:
            await sync_register_individual_disability_status(session, parent)

    def _validate_no_duplicate_disability_domain(self, records: list[dict]) -> None:
        seen: set[str] = set()
        for record in records:
            # Skip DELETE records from validation
            if record.get("edit_action") == "DELETE":
                continue
            value = record.get("disability_domains")
            if value is None or str(value).strip() == "":
                continue
            normalized = str(value).strip()
            if normalized in seen:
                validation_error("Duplicate disability domain entries are not allowed")
            seen.add(normalized)

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for individualdisability")

        keys = ["functional_record_id", 'disability_domains', 'disability_severity']
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

    def construct_record_name(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing record name for individualdisability")

        keys = ["disability_domains", "functional_record_id"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
