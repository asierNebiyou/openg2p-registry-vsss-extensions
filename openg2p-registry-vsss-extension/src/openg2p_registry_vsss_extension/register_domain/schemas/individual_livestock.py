from typing import Optional
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema, G2PRegisterHistorySchema, G2PIntakeFormSchemaBase
)
from ..models.enums import LivestockSpeciesEnum, LivestockCountBandEnum


class G2PRegisterSchemaIndividualLivestock(G2PRegisterBaseSchema):
    livestock_species: Optional[LivestockSpeciesEnum] = None
    livestock_counts: Optional[LivestockCountBandEnum] = None


class G2PIntakeFormSchemaIndividualLivestock(G2PIntakeFormSchemaBase, G2PRegisterSchemaIndividualLivestock):
    pass


class G2PRegisterHistorySchemaIndividualLivestock(G2PRegisterHistorySchema):
    livestock_species: Optional[LivestockSpeciesEnum] = None
    livestock_counts: Optional[LivestockCountBandEnum] = None
