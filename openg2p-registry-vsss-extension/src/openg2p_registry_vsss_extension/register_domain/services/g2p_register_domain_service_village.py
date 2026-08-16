import logging

from openg2p_registry_core.services import G2PRegisterDomainService

_logger = logging.getLogger("g2p-register-village-service")


class G2PRegisterDomainServiceVillage(G2PRegisterDomainService):
    """Domain service for Uganda VSSS Village register."""

    async def validate_domain_attributes(self, records: list[dict]):
        for record in records:
            name = (record.get("village_name") or record.get("record_name") or "").strip()
            if not name and not (record.get("village_code") or "").strip():
                # Soft validation — allow drafts without both fields during intake
                continue

    def construct_record_name(self, data: dict) -> str:
        return (
            data.get("village_name")
            or data.get("village_code")
            or data.get("record_name")
            or "Village"
        )

    def construct_search_text(self, data: dict) -> str:
        parts = [
            data.get("village_name"),
            data.get("village_code"),
            data.get("district"),
            data.get("subcounty"),
            data.get("parish"),
            data.get("region"),
            data.get("chairperson_name"),
        ]
        return " ".join(str(p) for p in parts if p)

    def construct_intake_record_name(self, data: dict) -> str:
        return self.construct_record_name(data)

    def construct_intake_search_text(self, data: dict) -> str:
        return self.construct_search_text(data)
