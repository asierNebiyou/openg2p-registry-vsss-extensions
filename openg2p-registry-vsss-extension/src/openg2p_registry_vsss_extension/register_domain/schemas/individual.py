from typing import Optional
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema, G2PPersonSchema, G2PGeoSchema,
    G2PRegisterHistorySchema, G2PIntakeFormSchemaBase, G2PPersonHistorySchema, G2PGeoHistorySchema
)


class G2PRegisterSchemaIndividual(G2PRegisterBaseSchema, G2PPersonSchema, G2PGeoSchema):
    # first_name, middle_name, last_name, birth_date, and gender come from G2PPersonSchema.
    additional_name: Optional[str] = None
    phone: Optional[str] = None

    ug_region_id: Optional[str] = None
    ug_district_id: Optional[str] = None
    ug_subcounty_id: Optional[str] = None
    ug_parish_id: Optional[str] = None
    village_id: Optional[str] = None
    polling_station: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

    has_sacco_account: Optional[bool] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None


class G2PIntakeFormSchemaIndividual(G2PIntakeFormSchemaBase, G2PRegisterSchemaIndividual):
    pass


class G2PRegisterHistorySchemaIndividual(G2PRegisterHistorySchema, G2PPersonHistorySchema, G2PGeoHistorySchema):
    additional_name: Optional[str] = None
    phone: Optional[str] = None

    ug_region_id: Optional[str] = None
    ug_district_id: Optional[str] = None
    ug_subcounty_id: Optional[str] = None
    ug_parish_id: Optional[str] = None
    village_id: Optional[str] = None
    polling_station: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

    has_sacco_account: Optional[bool] = None
    bank_name: Optional[str] = None
    bank_account_number: Optional[str] = None
