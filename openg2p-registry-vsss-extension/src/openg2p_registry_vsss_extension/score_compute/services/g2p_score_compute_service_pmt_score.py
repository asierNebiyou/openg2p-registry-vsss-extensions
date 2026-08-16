import logging
from typing import Any

from openg2p_registry_core.interfaces.g2p_score_compute_interface import (
    G2PScoreComputeInterface,
)

_logger = logging.getLogger(__name__)


class G2PScoreComputeServicePmtScore(G2PScoreComputeInterface):
    """
    PMT score from contributing-attribute config (DB) and field values (queue snapshot).
    """

    async def compute_score(
        self,
        link_internal_record_id: str,
        contributing_attribute_config: list[dict[str, Any]],
        contributing_attribute_values: dict[str, Any],
    ) -> float:
        values = contributing_attribute_values or {}

        _logger.info(
            "Computing PMT_SCORE for registrant %s with %d config row(s), %d value(s)",
            link_internal_record_id,
            len(contributing_attribute_config),
            len(values),
        )

        if not contributing_attribute_config:
            _logger.warning("PMT_SCORE: contributing_attribute_config is empty; returning 0.0")
            return 0.0

        total = 0.0
        for attribute_config in contributing_attribute_config:
            attribute_name = attribute_config.get("attribute_name")
            if not attribute_name:
                continue

            attribute_value_snapshot = values.get(attribute_name)
            attribute_weightage = float(attribute_config.get("attribute_weightage") or 0.0)
            attribute_computation_required = bool(attribute_config.get("attribute_computation_required"))
            attribute_computation_value = attribute_config.get("attribute_computation_value") or {}
            if not isinstance(attribute_computation_value, dict):
                attribute_computation_value = {}

            partial = self._partial_for_attribute(
                attribute_value_snapshot=attribute_value_snapshot,
                computation_required=attribute_computation_required,
                computation_map=attribute_computation_value,
            )
            total += partial * attribute_weightage

        out = round(float(total), 4)
        _logger.info("Computed PMT_SCORE=%s for registrant %s", out, link_internal_record_id)
        return out

    @staticmethod
    def _partial_for_attribute(
        *,
        attribute_value_snapshot: Any,
        computation_required: bool,
        computation_map: dict[str, Any],
    ) -> float:
        """
        Contribution for one attribute before applying attribute_weightage.

        - If computation_required and computation_map is non-empty: look up raw in the map.
        - Otherwise: coerce raw to float; non-numeric → 0.0.
        """
        if computation_required and computation_map:
            key: Any = attribute_value_snapshot
            if key is not None and not isinstance(key, str):
                key = str(key)
            if key in computation_map:
                return float(computation_map[key])
            str_key = str(key) if key is not None else ""
            for mk, mv in computation_map.items():
                if str(mk) == str_key:
                    return float(mv)
            return 0.0

        if attribute_value_snapshot is None:
            return 0.0
        try:
            return float(attribute_value_snapshot)
        except (TypeError, ValueError):
            return 0.0
