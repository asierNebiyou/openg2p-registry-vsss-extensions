from typing import Optional

from pydantic import ConfigDict
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
)


class G2PRegisterSchemaVillage(G2PRegisterBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    village_code: Optional[str] = None
    village_name: Optional[str] = None
    region: Optional[str] = None
    district: Optional[str] = None
    subcounty: Optional[str] = None
    parish: Optional[str] = None
    chairperson_name: Optional[str] = None
    chairperson_phone: Optional[str] = None
    secretary_name: Optional[str] = None
    treasurer_name: Optional[str] = None
    household_count: Optional[int] = None
    population_estimate: Optional[int] = None
    grant_status: Optional[str] = None
    sacco_name: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    signed_grant_agreement: Optional[bool] = None
    governance_records: Optional[str] = None
    financial_management: Optional[str] = None


class G2PIntakeFormSchemaVillage(G2PIntakeFormSchemaBase, G2PRegisterSchemaVillage):
    model_config = ConfigDict(from_attributes=True)


class G2PRegisterHistorySchemaVillage(G2PRegisterHistorySchema, G2PRegisterSchemaVillage):
    model_config = ConfigDict(from_attributes=True)
