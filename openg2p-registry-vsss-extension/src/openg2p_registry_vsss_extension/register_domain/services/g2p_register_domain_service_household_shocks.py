import logging
from datetime import date

from openg2p_registry_core.services import G2PRegisterDomainService
from openg2p_registry_core.schemas import ChangeRequestRequestPayload
from .domain_validation_utils import parse_date, validation_error

_logger = logging.getLogger('g2p-register-householdshock-service')

class G2PRegisterDomainServiceHouseholdShock(G2PRegisterDomainService):
    async def validate_domain_attributes(self, records: list[dict]):
        self._validate_shock_date_range(records)

    def _validate_shock_date_range(self, records: list[dict]) -> None:
        for record in records:
            # Skip DELETE records from validation
            if record.get("edit_action") == "DELETE":
                continue

            start_date = parse_date(record.get("shock_start_date"))
            end_date = parse_date(record.get("shock_end_date"))
            if start_date is None or end_date is None:
                continue

            if end_date < start_date:
                validation_error("Shock End Date must be on or after Shock Start Date")

        self._validate_shock_entries_no_overlap(records)


    def _validate_shock_entries_no_overlap(self, records: list[dict]) -> None:
        active_records = [
            record for record in records
            if record.get("edit_action") != "DELETE"
        ]

        entries: list[tuple[str, date | None, date | None]] = []

        for record in active_records:
            shocks_last_12m, start_date, end_date = self._shock_date_range(record)
            if not shocks_last_12m:
                continue
            for existing_name, existing_start, existing_end in entries:
                if existing_name != shocks_last_12m:
                    continue

                if self._date_ranges_overlap(
                    existing_start,
                    existing_end,
                    start_date,
                    end_date,
                ):
                    validation_error(
                        f"Duplicate shock '{shocks_last_12m}' with overlapping dates is not allowed"
                    )
            entries.append((shocks_last_12m, start_date, end_date))

    @staticmethod
    def _shock_date_range(record: dict) -> tuple[str | None, date | None, date | None]:
        shocks_last_12m = record.get("shocks_last_12m")
        if shocks_last_12m is not None:
            shocks_last_12m = str(shocks_last_12m).strip() or None
        return (
            shocks_last_12m,
            parse_date(record.get("shock_start_date")),
            parse_date(record.get("shock_end_date")),
        )

    @staticmethod
    def _date_ranges_overlap(
        start_a: date | None,
        end_a: date | None,
        start_b: date | None,
        end_b: date | None,
    ) -> bool:
        if start_a is None or start_b is None:
            return True
        effective_end_a = end_a or date.max
        effective_end_b = end_b or date.max
        return start_a <= effective_end_b and start_b <= effective_end_a

    def construct_search_text(self, payload: dict, extra: list[str] = None) -> str:
        _logger.info("Constructing search text for householdshock")

        keys = ["functional_record_id", 'shocks_last_12m']
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
        _logger.info("Constructing record name for householdshock")

        keys = ["shocks_last_12m", "functional_record_id"]
        record_name = []
        if extra:
            record_name.extend(str(item).strip() for item in extra if str(item).strip())
        record_name.extend(
            str(payload.get(key) or "").strip()
            for key in keys
            if str(payload.get(key) or "").strip()
        )

        return " ".join(record_name).strip()
