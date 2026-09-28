import logging

from openg2p_registry_core.services import G2PRegisterDomainService

_logger = logging.getLogger("g2p-register-village-service")


class G2PRegisterDomainServiceVillage(G2PRegisterDomainService):
    """Domain service for Uganda VSSS Village register."""

    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            name = (record.get("name") or record.get("record_name") or "").strip()
            code = (record.get("code") or "").strip()
            if not name and not code:
                continue

    def construct_record_name(self, data: dict) -> str:
        return (
            data.get("name")
            or data.get("code")
            or data.get("record_name")
            or "Village"
        )

    def construct_search_text(self, data: dict) -> str:
        parts = [
            data.get("name"),
            data.get("code"),
            data.get("polling_station"),
            data.get("chairperson_name"),
            data.get("chairperson_phone"),
            data.get("treasurer_name"),
            data.get("secretary_name"),
        ]
        return " ".join(str(p) for p in parts if p)

    def construct_intake_record_name(self, data: dict) -> str:
        return self.construct_record_name(data)

    def construct_intake_search_text(self, data: dict) -> str:
        return self.construct_search_text(data)
