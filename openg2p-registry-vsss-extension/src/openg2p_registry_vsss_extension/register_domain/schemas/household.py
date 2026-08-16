from typing import Optional
from openg2p_registry_core.schemas import G2PRegisterBaseSchema, G2PRegisterHistorySchema, G2PIntakeFormSchemaBase, G2PGeoSchema, G2PGeoHistorySchema
from ..models.enums import HeadshipTypeEnum, HouseholdAssetsEnum, WaterSourceTypeEnum, FloorMaterialEnum, SanitationTypeEnum, DwellingTypeEnum, RoofMaterialEnum, TenureStatusEnum, LightingSourceEnum, CookingFuelTypeEnum, WallMaterialEnum


class G2PRegisterSchemaHousehold(G2PRegisterBaseSchema, G2PGeoSchema):
    household_size_total: Optional[int] = None
    household_size_adults: Optional[int] = None
    household_size_children_u5: Optional[int] = None
    household_size_school_age: Optional[int] = None
    household_size_elderly: Optional[int] = None
    elderly_member_present: Optional[bool] = None

    household_head_person_id: Optional[str] = None
    headship_type: Optional[HeadshipTypeEnum] = None
    household_assets: Optional[list[HouseholdAssetsEnum]] = None
    # region_code: Optional[str] = None
    # zone_subcity_code: Optional[str] = None
    # woreda_code: Optional[str] = None
    kebele_code: Optional[str] = None
    locality_ea_code: Optional[str] = None
    address_descriptor: Optional[str] = None

    village_code: Optional[str] = None
    village_name: Optional[str] = None
    region: Optional[str] = None
    district: Optional[str] = None
    subcounty: Optional[str] = None
    parish: Optional[str] = None
    grant_status: Optional[str] = None
    primary_contact_phone: Optional[str] = None
    national_id: Optional[str] = None

    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    gps_accuracy: Optional[float] = None

    dwelling_type: Optional[DwellingTypeEnum] = None
    roof_material: Optional[RoofMaterialEnum] = None
    wall_material: Optional[WallMaterialEnum] = None
    floor_material: Optional[FloorMaterialEnum] = None
    tenure_status: Optional[TenureStatusEnum] = None
    water_source_type: Optional[WaterSourceTypeEnum] = None
    water_distance_minutes: Optional[int] = None
    sanitation_type: Optional[SanitationTypeEnum] = None
    lighting_source: Optional[LightingSourceEnum] = None
    cooking_fuel_type: Optional[CookingFuelTypeEnum] = None

    rooms_count: Optional[int] = None
    overcrowding_indicator: Optional[float] = None

class G2PIntakeFormSchemaHousehold(G2PIntakeFormSchemaBase, G2PRegisterSchemaHousehold):
    pass


class G2PRegisterHistorySchemaHousehold(G2PRegisterHistorySchema, G2PGeoHistorySchema):
    household_size_total: Optional[int] = None
    household_size_adults: Optional[int] = None
    household_size_children_u5: Optional[int] = None
    household_size_school_age: Optional[int] = None
    household_size_elderly: Optional[int] = None
    elderly_member_present: Optional[bool] = None
    
    household_head_person_id: Optional[str] = None
    headship_type: Optional[HeadshipTypeEnum] = None
    household_assets: Optional[list[HouseholdAssetsEnum]] = None
    # region_code: Optional[str] = None
    # zone_subcity_code: Optional[str] = None
    # woreda_code: Optional[str] = None
    kebele_code: Optional[str] = None
    locality_ea_code: Optional[str] = None
    address_descriptor: Optional[str] = None

    village_code: Optional[str] = None
    village_name: Optional[str] = None
    region: Optional[str] = None
    district: Optional[str] = None
    subcounty: Optional[str] = None
    parish: Optional[str] = None
    grant_status: Optional[str] = None
    primary_contact_phone: Optional[str] = None
    national_id: Optional[str] = None

    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    gps_accuracy: Optional[float] = None

    dwelling_type: Optional[DwellingTypeEnum] = None
    roof_material: Optional[RoofMaterialEnum] = None
    wall_material: Optional[WallMaterialEnum] = None
    floor_material: Optional[FloorMaterialEnum] = None
    tenure_status: Optional[TenureStatusEnum] = None
    water_source_type: Optional[WaterSourceTypeEnum] = None
    water_distance_minutes: Optional[int] = None
    sanitation_type: Optional[SanitationTypeEnum] = None
    lighting_source: Optional[LightingSourceEnum] = None
    cooking_fuel_type: Optional[CookingFuelTypeEnum] = None

    rooms_count: Optional[int] = None
    overcrowding_indicator: Optional[float] = None