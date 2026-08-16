from typing import Optional, List, Dict
from datetime import date, datetime
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema, G2PPersonSchema, G2PGeoSchema,
    G2PRegisterHistorySchema, G2PIntakeFormSchemaBase, G2PPersonHistorySchema, G2PGeoHistorySchema
)
from ..models.enums import (
    DisabilityStatusEnum, DisplacementStatusEnum, LivelihoodEnum, EmploymentStatusEnum, MobilePhoneTypeEnum, PastoralistClassificationEnum,
    ProductiveAssetEnum, ResidencyStatusEnum,
    PreferredContactMethodEnum, CitizenshipCategoryEnum,
    AgeMethodEnum, RelationshipToHeadEnum,RidStatusEnum, EducationalStatusEnum, PrefixEnum, GenderEnum
)


class G2PRegisterSchemaIndividual(G2PRegisterBaseSchema, G2PPersonSchema, G2PGeoSchema):
    prefix: Optional[PrefixEnum] = None
    full_name: Optional[str] = None
    gender: Optional[GenderEnum] = None

    address_descriptor: Optional[str] = None
    kebele_code: Optional[str] = None
    locality_ea_code: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    gps_accuracy: Optional[float] = None
    primary_phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    preferred_contact_method: Optional[PreferredContactMethodEnum] = None
    contact_person_name: Optional[str] = None
    contact_person_phone: Optional[str] = None

    estimated_age: Optional[int] = None
    age_method: Optional[AgeMethodEnum] = None
    marital_status: Optional[str] = None
    alias_names: Optional[str] = None
    citizenship_category: Optional[CitizenshipCategoryEnum] = None

    rid: Optional[str] = None
    rid_status: Optional[RidStatusEnum] = RidStatusEnum.PENDING
    has_national_id: Optional[bool] = None

    relationship_to_head: Optional[RelationshipToHeadEnum] = None
    dependency_indicator: Optional[bool] = None
    residency_status: Optional[ResidencyStatusEnum] = None

    land_access: Optional[bool] = None
    land_size: Optional[float] = None
    productive_assets: Optional[list[ProductiveAssetEnum]] = None

    educational_status: Optional[EducationalStatusEnum] = None
    primary_livelihood: Optional[LivelihoodEnum] = None
    secondary_livelihood: Optional[LivelihoodEnum] = None
    employment_status: Optional[EmploymentStatusEnum] = None
    mobile_phone_type: Optional[MobilePhoneTypeEnum] = None

    disability_status: Optional[DisabilityStatusEnum] = None
    orphanhood_flag: Optional[bool] = None
    chronic_illness_flag: Optional[bool] = None
    displacement_status: Optional[DisplacementStatusEnum] = None
    pastoralist_classification: Optional[PastoralistClassificationEnum] = None
    high_mobility_indicator: Optional[bool] = None
    plw_status: Optional[bool] = None
    plw_date: Optional[date] = None

    is_head: Optional[bool] = None


class G2PIntakeFormSchemaIndividual(G2PIntakeFormSchemaBase, G2PRegisterSchemaIndividual):
    pass


class G2PRegisterHistorySchemaIndividual(G2PRegisterHistorySchema, G2PPersonHistorySchema, G2PGeoHistorySchema):
    prefix: Optional[PrefixEnum] = None
    full_name: Optional[str] = None
    gender: Optional[GenderEnum] = None
    address_descriptor: Optional[str] = None
    kebele_code: Optional[str] = None
    locality_ea_code: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    gps_accuracy: Optional[float] = None
    primary_phone: Optional[str] = None
    alternate_phone: Optional[str] = None
    preferred_contact_method: Optional[PreferredContactMethodEnum] = None
    contact_person_name: Optional[str] = None
    contact_person_phone: Optional[str] = None
    marital_status: Optional[str] = None
    alias_names: Optional[str] = None
    citizenship_category: Optional[CitizenshipCategoryEnum] = None
    rid: Optional[str] = None
    rid_status: Optional[RidStatusEnum] = RidStatusEnum.PENDING
    has_national_id: Optional[bool] = None
    relationship_to_head: Optional[RelationshipToHeadEnum] = None
    dependency_indicator: Optional[bool] = None
    residency_status: Optional[ResidencyStatusEnum] = None

    land_access: Optional[bool] = None
    land_size: Optional[float] = None
    productive_assets: Optional[list[ProductiveAssetEnum]] = None

    educational_status: Optional[EducationalStatusEnum] = None
    primary_livelihood: Optional[LivelihoodEnum] = None
    secondary_livelihood: Optional[LivelihoodEnum] = None
    employment_status: Optional[EmploymentStatusEnum] = None
    mobile_phone_type: Optional[MobilePhoneTypeEnum] = None

    disability_status: Optional[DisabilityStatusEnum] = None
    orphanhood_flag: Optional[bool] = None
    chronic_illness_flag: Optional[bool] = None
    displacement_status: Optional[DisplacementStatusEnum] = None
    pastoralist_classification: Optional[PastoralistClassificationEnum] = None
    high_mobility_indicator: Optional[bool] = None
    plw_status: Optional[bool] = None
    plw_date: Optional[date] = None
    
    is_head: Optional[bool] = None