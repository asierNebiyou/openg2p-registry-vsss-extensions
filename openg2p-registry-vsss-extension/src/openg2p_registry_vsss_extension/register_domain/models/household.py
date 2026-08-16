from openg2p_registry_extensions.register_domain.services import G2PRegisterDomainServiceHousehold
from sqlalchemy import String, Integer, Boolean, Numeric, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB 
from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory, G2PGeo, G2PGeoHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from .enums import (HeadshipTypeEnum, HouseholdAssetsEnum, DwellingTypeEnum, RoofMaterialEnum, WallMaterialEnum, FloorMaterialEnum, 
                    TenureStatusEnum, WaterSourceTypeEnum, SanitationTypeEnum, LightingSourceEnum, CookingFuelTypeEnum
)


# All Register classes should have the prefix G2PRegister
class G2PRegisterHousehold(G2PRegister, G2PGeo):
    __tablename__ = "g2p_register_households"

    # Household Roster 
    household_size_total: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_adults: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_children_u5: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_school_age: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_elderly: Mapped[int] = mapped_column(Integer, nullable=True)
    elderly_member_present: Mapped[bool] = mapped_column(Boolean, nullable=True)

    household_head_person_id: Mapped[str] = mapped_column(String, nullable=True)
    headship_type: Mapped[HeadshipTypeEnum] = mapped_column(String, nullable=True)
    household_assets: Mapped[list[HouseholdAssetsEnum]] = mapped_column(JSONB, nullable=True)
    kebele_code: Mapped[str] = mapped_column(String, nullable=True)
    locality_ea_code: Mapped[str] = mapped_column(String, nullable=True)
    address_descriptor: Mapped[str] = mapped_column(String, nullable=True)

    # Uganda VSSS location / grant fields (from Odoo village_registry)
    village_code: Mapped[str] = mapped_column(String, nullable=True)
    village_name: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    district: Mapped[str] = mapped_column(String, nullable=True)
    subcounty: Mapped[str] = mapped_column(String, nullable=True)
    parish: Mapped[str] = mapped_column(String, nullable=True)
    grant_status: Mapped[str] = mapped_column(String, nullable=True)
    primary_contact_phone: Mapped[str] = mapped_column(String, nullable=True)
    national_id: Mapped[str] = mapped_column(String, nullable=True)

    # Location - GPS Coordinates
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_accuracy: Mapped[float] = mapped_column(Numeric, nullable=True)

    dwelling_type: Mapped[DwellingTypeEnum] = mapped_column(String, nullable=True)
    roof_material: Mapped[RoofMaterialEnum] = mapped_column(String, nullable=True)
    wall_material: Mapped[WallMaterialEnum] = mapped_column(String, nullable=True)
    floor_material: Mapped[FloorMaterialEnum] = mapped_column(String, nullable=True)
    tenure_status: Mapped[TenureStatusEnum] = mapped_column(String, nullable=True)
    water_source_type: Mapped[WaterSourceTypeEnum] = mapped_column(String, nullable=True)
    water_distance_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    sanitation_type: Mapped[SanitationTypeEnum] = mapped_column(String, nullable=True)
    lighting_source: Mapped[LightingSourceEnum] = mapped_column(String, nullable=True)
    cooking_fuel_type: Mapped[CookingFuelTypeEnum] = mapped_column(String, nullable=True)
    rooms_count: Mapped[int] = mapped_column(Integer, nullable=True)
    overcrowding_indicator: Mapped[float] = mapped_column(Numeric, nullable=True)

    def get_record_name_fields(self) -> str:
        """Return household fields used to build record_name."""
        return G2PRegisterDomainServiceHousehold().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return household fields used to build search_text."""
        return G2PRegisterDomainServiceHousehold().construct_search_text(self.to_dict())



# All Register History classes should have the prefix G2PRegisterHistory
# All Intake Form classes should have the prefix G2PIntakeForm
class G2PIntakeFormHousehold(G2PIntakeForm, G2PRegister, G2PGeo):
    __tablename__ = "g2p_intake_form_households"

    # Household Roster 
    household_size_total: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_adults: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_children_u5: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_school_age: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_elderly: Mapped[int] = mapped_column(Integer, nullable=True)
    elderly_member_present: Mapped[bool] = mapped_column(Boolean, nullable=True)

    household_head_person_id: Mapped[str] = mapped_column(String, nullable=True)
    headship_type: Mapped[HeadshipTypeEnum] = mapped_column(String, nullable=True)
    household_assets: Mapped[list[HouseholdAssetsEnum]] = mapped_column(JSONB, nullable=True)
    kebele_code: Mapped[str] = mapped_column(String, nullable=True)
    locality_ea_code: Mapped[str] = mapped_column(String, nullable=True)
    address_descriptor: Mapped[str] = mapped_column(String, nullable=True)

    # Uganda VSSS location / grant fields (from Odoo village_registry)
    village_code: Mapped[str] = mapped_column(String, nullable=True)
    village_name: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    district: Mapped[str] = mapped_column(String, nullable=True)
    subcounty: Mapped[str] = mapped_column(String, nullable=True)
    parish: Mapped[str] = mapped_column(String, nullable=True)
    grant_status: Mapped[str] = mapped_column(String, nullable=True)
    primary_contact_phone: Mapped[str] = mapped_column(String, nullable=True)
    national_id: Mapped[str] = mapped_column(String, nullable=True)

    # Location - GPS Coordinates
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_accuracy: Mapped[float] = mapped_column(Numeric, nullable=True)

    
    dwelling_type: Mapped[DwellingTypeEnum] = mapped_column(String, nullable=True)
    roof_material: Mapped[RoofMaterialEnum] = mapped_column(String, nullable=True)
    wall_material: Mapped[WallMaterialEnum] = mapped_column(String, nullable=True)
    floor_material: Mapped[FloorMaterialEnum] = mapped_column(String, nullable=True)
    tenure_status: Mapped[TenureStatusEnum] = mapped_column(String, nullable=True)
    water_source_type: Mapped[WaterSourceTypeEnum] = mapped_column(String, nullable=True)
    water_distance_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    sanitation_type: Mapped[SanitationTypeEnum] = mapped_column(String, nullable=True)
    lighting_source: Mapped[LightingSourceEnum] = mapped_column(String, nullable=True)
    cooking_fuel_type: Mapped[CookingFuelTypeEnum] = mapped_column(String, nullable=True)
    rooms_count: Mapped[int] = mapped_column(Integer, nullable=True)
    overcrowding_indicator: Mapped[float] = mapped_column(Numeric, nullable=True)

    def get_record_name_fields(self) -> str:
        """Return household fields used to build record_name."""
        return G2PRegisterDomainServiceHousehold().construct_intake_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return household fields used to build search_text."""
        return G2PRegisterDomainServiceHousehold().construct_search_text(self.to_dict())



# All Register History classes should have the prefix G2PRegisterHistory


class G2PRegisterHistoryHousehold(G2PRegisterHistory, G2PGeoHistory):
    __tablename__ = "g2p_register_history_households"

    household_size_total: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_adults: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_children_u5: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_school_age: Mapped[int] = mapped_column(Integer, nullable=True)
    household_size_elderly: Mapped[int] = mapped_column(Integer, nullable=True)
    elderly_member_present: Mapped[bool] = mapped_column(Boolean, nullable=True)

    household_head_person_id: Mapped[str] = mapped_column(String, nullable=True)
    headship_type: Mapped[HeadshipTypeEnum] = mapped_column(String, nullable=True)
    household_assets: Mapped[list[HouseholdAssetsEnum]] = mapped_column(JSONB, nullable=True)
    kebele_code: Mapped[str] = mapped_column(String, nullable=True)
    locality_ea_code: Mapped[str] = mapped_column(String, nullable=True)
    address_descriptor: Mapped[str] = mapped_column(String, nullable=True)

    # Uganda VSSS location / grant fields (from Odoo village_registry)
    village_code: Mapped[str] = mapped_column(String, nullable=True)
    village_name: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    district: Mapped[str] = mapped_column(String, nullable=True)
    subcounty: Mapped[str] = mapped_column(String, nullable=True)
    parish: Mapped[str] = mapped_column(String, nullable=True)
    grant_status: Mapped[str] = mapped_column(String, nullable=True)
    primary_contact_phone: Mapped[str] = mapped_column(String, nullable=True)
    national_id: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_accuracy: Mapped[float] = mapped_column(Numeric, nullable=True)

    dwelling_type: Mapped[DwellingTypeEnum] = mapped_column(String, nullable=True)
    roof_material: Mapped[RoofMaterialEnum] = mapped_column(String, nullable=True)
    wall_material: Mapped[WallMaterialEnum] = mapped_column(String, nullable=True)
    floor_material: Mapped[FloorMaterialEnum] = mapped_column(String, nullable=True)
    tenure_status: Mapped[TenureStatusEnum] = mapped_column(String, nullable=True)
    water_source_type: Mapped[WaterSourceTypeEnum] = mapped_column(String, nullable=True)
    water_distance_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
    sanitation_type: Mapped[SanitationTypeEnum] = mapped_column(String, nullable=True)
    lighting_source: Mapped[LightingSourceEnum] = mapped_column(String, nullable=True)
    cooking_fuel_type: Mapped[CookingFuelTypeEnum] = mapped_column(String, nullable=True)
    rooms_count: Mapped[int] = mapped_column(Integer, nullable=True)
    overcrowding_indicator: Mapped[float] = mapped_column(Numeric, nullable=True)