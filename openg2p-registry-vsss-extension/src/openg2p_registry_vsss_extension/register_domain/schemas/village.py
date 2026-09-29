from typing import Optional

from pydantic import ConfigDict
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema,
    G2PRegisterHistorySchema,
    G2PIntakeFormSchemaBase,
    G2PGeoSchema,
    G2PGeoHistorySchema,
)


class G2PRegisterSchemaVillage(G2PRegisterBaseSchema, G2PGeoSchema):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    household_count: Optional[int] = None
    code: Optional[str] = None

    polling_station: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

    chairperson_name: Optional[str] = None
    chairperson_phone: Optional[str] = None
    treasurer_name: Optional[str] = None
    treasurer_phone: Optional[str] = None
    secretary_name: Optional[str] = None
    secretary_phone: Optional[str] = None


class G2PIntakeFormSchemaVillage(G2PIntakeFormSchemaBase, G2PRegisterSchemaVillage):
    model_config = ConfigDict(from_attributes=True)


class G2PRegisterHistorySchemaVillage(G2PRegisterHistorySchema, G2PGeoHistorySchema):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    household_count: Optional[int] = None
    code: Optional[str] = None

    polling_station: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

    chairperson_name: Optional[str] = None
    chairperson_phone: Optional[str] = None
    treasurer_name: Optional[str] = None
    treasurer_phone: Optional[str] = None
    secretary_name: Optional[str] = None
    secretary_phone: Optional[str] = None
