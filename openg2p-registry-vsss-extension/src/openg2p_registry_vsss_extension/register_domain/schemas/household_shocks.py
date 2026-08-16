from typing import Optional
from datetime import date
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema, G2PRegisterHistorySchema, G2PIntakeFormSchemaBase
)
from ..models.enums import ShockTypeEnum


class G2PRegisterSchemaHouseholdShock(G2PRegisterBaseSchema):
    shocks_last_12m: Optional[ShockTypeEnum] = None
    shock_start_date: Optional[date] = None
    shock_end_date: Optional[date] = None


class G2PIntakeFormSchemaHouseholdShock(G2PIntakeFormSchemaBase, G2PRegisterSchemaHouseholdShock):
    pass


class G2PRegisterHistorySchemaHouseholdShock(G2PRegisterHistorySchema):
    shocks_last_12m: Optional[ShockTypeEnum] = None
    shock_start_date: Optional[date] = None
    shock_end_date: Optional[date] = None
