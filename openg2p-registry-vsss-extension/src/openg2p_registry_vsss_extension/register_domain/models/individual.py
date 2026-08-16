from ..services import G2PRegisterDomainServiceIndividual
from sqlalchemy import String, Integer, Boolean, Numeric, Date, Enum, select
from sqlalchemy.dialects.postgresql import JSONB 
from sqlalchemy.orm import Mapped, mapped_column, Session

from openg2p_registry_core.models import (
    G2PRegister, G2PRegisterHistory, G2PPerson, G2PGeo,
    G2PPersonHistory, G2PGeoHistory, G2PRegisterAuthentication
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from datetime import datetime
from .enums import (
    EmploymentStatusEnum, EmploymentStatusEnum, LivelihoodEnum, MobilePhoneTypeEnum,
    LivelihoodEnum, ProductiveAssetEnum, ResidencyStatusEnum, PreferredContactMethodEnum, CitizenshipCategoryEnum, AgeMethodEnum, RelationshipToHeadEnum,
    RidStatusEnum, DisabilityStatusEnum, DisplacementStatusEnum, PastoralistClassificationEnum, EducationalStatusEnum, PrefixEnum, GenderEnum
)
from .household import G2PIntakeFormHousehold


# All Register classes should have the prefix G2PRegister
class G2PRegisterIndividual(G2PRegister, G2PPerson, G2PGeo, G2PRegisterAuthentication):
    __tablename__ = "g2p_register_individuals"

    # Registry Keys and Identifiers
    prefix: Mapped[PrefixEnum] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[GenderEnum] = mapped_column(String, nullable=True)

    rid: Mapped[str] = mapped_column(String, nullable=True)
    rid_status: Mapped[RidStatusEnum] = mapped_column(
        Enum(RidStatusEnum), nullable=True, default=RidStatusEnum.PENDING
    )
    has_national_id = mapped_column(Boolean, nullable=True)

    # Contact and Location
    address_descriptor: Mapped[str] = mapped_column(String, nullable=True)
    kebele_code: Mapped[str] = mapped_column(String, nullable=True)
    locality_ea_code: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_accuracy: Mapped[float] = mapped_column(Numeric, nullable=True)
    primary_phone: Mapped[str] = mapped_column(String, nullable=True)
    alternate_phone: Mapped[str] = mapped_column(String, nullable=True)
    preferred_contact_method: Mapped[PreferredContactMethodEnum] = mapped_column(String, nullable=True)
    contact_person_name: Mapped[str] = mapped_column(String, nullable=True)
    contact_person_phone: Mapped[str] = mapped_column(String, nullable=True)

    # Demographics
    estimated_age: Mapped[int] = mapped_column(Integer, nullable=True)
    age_method: Mapped[AgeMethodEnum] = mapped_column(String, nullable=True)
    alias_names: Mapped[str] = mapped_column(String, nullable=True)
    citizenship_category: Mapped[CitizenshipCategoryEnum] = mapped_column(String, nullable=True)

    # Relationship to Head
    relationship_to_head: Mapped[RelationshipToHeadEnum] = mapped_column(String, nullable=True)
    dependency_indicator: Mapped[bool] = mapped_column(Boolean, nullable=True)
    residency_status: Mapped[ResidencyStatusEnum] = mapped_column(String, nullable=True)
    
    # Individual land fields
    land_access: Mapped[bool] = mapped_column(Boolean, nullable=True)
    land_size: Mapped[float] = mapped_column(Numeric, nullable=True)
    productive_assets: Mapped[list[ProductiveAssetEnum]] = mapped_column(JSONB, nullable=True)

    # Individual Livelihood fields
    educational_status: Mapped[EducationalStatusEnum] = mapped_column(String, nullable=True)
    primary_livelihood: Mapped[LivelihoodEnum] = mapped_column(String, nullable=True)
    secondary_livelihood: Mapped[LivelihoodEnum] = mapped_column(String, nullable=True)
    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(String, nullable=True)
    mobile_phone_type: Mapped[MobilePhoneTypeEnum] = mapped_column(String, nullable=True)

    #Indvidual Vulnerability fields
    disability_status: Mapped[DisabilityStatusEnum] = mapped_column(String, nullable=True)
    orphanhood_flag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    chronic_illness_flag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    displacement_status: Mapped[DisplacementStatusEnum] = mapped_column(String, nullable=True)
    pastoralist_classification: Mapped[PastoralistClassificationEnum] = mapped_column(String, nullable=True)
    high_mobility_indicator: Mapped[bool] = mapped_column(Boolean, nullable=True)
    plw_status: Mapped[bool] = mapped_column(Boolean, nullable=True)
    plw_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    is_head: Mapped[bool] = mapped_column(Boolean, nullable=True)

    def get_record_name_fields(self) -> str:
        """Return individual fields used to build record_name."""
        return G2PRegisterDomainServiceIndividual().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return individual fields used to build search_text."""
        return G2PRegisterDomainServiceIndividual().construct_search_text(self.to_dict())



# All Register History classes should have the prefix G2PRegisterHistory
# All Intake Form classes should have the prefix G2PIntakeForm
class G2PIntakeFormIndividual(G2PIntakeForm, G2PRegister, G2PPerson, G2PGeo):
    __tablename__ = "g2p_intake_form_individuals"

    # Registry Keys and Identifiers
    prefix: Mapped[PrefixEnum] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[GenderEnum] = mapped_column(String, nullable=True)

    rid: Mapped[str] = mapped_column(String, nullable=True)
    rid_status: Mapped[RidStatusEnum] = mapped_column(
        Enum(RidStatusEnum), nullable=True, default=RidStatusEnum.PENDING
    )
    has_national_id = mapped_column(Boolean, nullable=True)

    # Contact and Location
    address_descriptor: Mapped[str] = mapped_column(String, nullable=True)
    kebele_code: Mapped[str] = mapped_column(String, nullable=True)
    locality_ea_code: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_accuracy: Mapped[float] = mapped_column(Numeric, nullable=True)
    primary_phone: Mapped[str] = mapped_column(String, nullable=True)
    alternate_phone: Mapped[str] = mapped_column(String, nullable=True)
    preferred_contact_method: Mapped[PreferredContactMethodEnum] = mapped_column(String, nullable=True)
    contact_person_name: Mapped[str] = mapped_column(String, nullable=True)
    contact_person_phone: Mapped[str] = mapped_column(String, nullable=True)

    # Demographics
    estimated_age: Mapped[int] = mapped_column(Integer, nullable=True)
    age_method: Mapped[AgeMethodEnum] = mapped_column(String, nullable=True)
    alias_names: Mapped[str] = mapped_column(String, nullable=True)
    citizenship_category: Mapped[CitizenshipCategoryEnum] = mapped_column(String, nullable=True)

    # Relationship to Head
    relationship_to_head: Mapped[RelationshipToHeadEnum] = mapped_column(String, nullable=True)
    dependency_indicator: Mapped[bool] = mapped_column(Boolean, nullable=True)
    residency_status: Mapped[ResidencyStatusEnum] = mapped_column(String, nullable=True)
    
    # Individual land fields
    land_access: Mapped[bool] = mapped_column(Boolean, nullable=True)
    land_size: Mapped[float] = mapped_column(Numeric, nullable=True)
    productive_assets: Mapped[list[ProductiveAssetEnum]] = mapped_column(JSONB, nullable=True)

    # Individual Livelihood fields
    educational_status: Mapped[EducationalStatusEnum] = mapped_column(String, nullable=True)
    primary_livelihood: Mapped[LivelihoodEnum] = mapped_column(String, nullable=True)
    secondary_livelihood: Mapped[LivelihoodEnum] = mapped_column(String, nullable=True)
    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(String, nullable=True)
    mobile_phone_type: Mapped[MobilePhoneTypeEnum] = mapped_column(String, nullable=True)

    #Indvidual Vulnerability fields
    disability_status: Mapped[DisabilityStatusEnum] = mapped_column(String, nullable=True)
    orphanhood_flag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    chronic_illness_flag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    displacement_status: Mapped[DisplacementStatusEnum] = mapped_column(String, nullable=True)
    pastoralist_classification: Mapped[PastoralistClassificationEnum] = mapped_column(String, nullable=True)
    high_mobility_indicator: Mapped[bool] = mapped_column(Boolean, nullable=True)
    plw_status: Mapped[bool] = mapped_column(Boolean, nullable=True)
    plw_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    is_head: Mapped[bool] = mapped_column(Boolean, nullable=True)

    def get_record_name_fields(self) -> str:
        """Return individual fields used to build record_name."""
        return G2PRegisterDomainServiceIndividual().construct_intake_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return individual fields used to build search_text."""
        return G2PRegisterDomainServiceIndividual().construct_search_text(self.to_dict())

    async def get_link_internal_record_id(self, session: Session):
        result = await session.execute(
            select(G2PIntakeFormHousehold).where(G2PIntakeFormHousehold.submission_id == self.submission_id)
        )
        household = result.scalars().first()
        if household:
            self.link_internal_record_id = household.internal_record_id



# All Register History classes should have the prefix G2PRegisterHistory


class G2PRegisterHistoryIndividual(G2PRegisterHistory, G2PPersonHistory, G2PGeoHistory, G2PRegisterAuthentication):
    __tablename__ = "g2p_register_history_individuals"

    # Registry Keys and Identifiers
    prefix: Mapped[PrefixEnum] = mapped_column(String, nullable=True)
    full_name: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[GenderEnum] = mapped_column(String, nullable=True)
    rid: Mapped[str] = mapped_column(String, nullable=True)
    rid_status: Mapped[RidStatusEnum] = mapped_column(
        Enum(RidStatusEnum), nullable=True, default=RidStatusEnum.PENDING
    )
    has_national_id = mapped_column(Boolean, nullable=True)
    
    # Contact and Location
    address_descriptor: Mapped[str] = mapped_column(String, nullable=True)
    kebele_code: Mapped[str] = mapped_column(String, nullable=True)
    locality_ea_code: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_accuracy: Mapped[float] = mapped_column(Numeric, nullable=True)
    primary_phone: Mapped[str] = mapped_column(String, nullable=True)
    alternate_phone: Mapped[str] = mapped_column(String, nullable=True)
    preferred_contact_method: Mapped[PreferredContactMethodEnum] = mapped_column(String, nullable=True)
    contact_person_name: Mapped[str] = mapped_column(String, nullable=True)
    contact_person_phone: Mapped[str] = mapped_column(String, nullable=True)

    # Demographics
    estimated_age: Mapped[int] = mapped_column(Integer, nullable=True)
    age_method: Mapped[AgeMethodEnum] = mapped_column(String, nullable=True)
    alias_names: Mapped[str] = mapped_column(String, nullable=True)
    citizenship_category: Mapped[CitizenshipCategoryEnum] = mapped_column(String, nullable=True)

    # Relationship to Head
    relationship_to_head: Mapped[RelationshipToHeadEnum] = mapped_column(String, nullable=True)
    dependency_indicator: Mapped[bool] = mapped_column(Boolean, nullable=True)
    residency_status: Mapped[ResidencyStatusEnum] = mapped_column(String, nullable=True)

    # Individual land fields
    land_access: Mapped[bool] = mapped_column(Boolean, nullable=True)
    land_size: Mapped[float] = mapped_column(Numeric, nullable=True)
    productive_assets: Mapped[list[ProductiveAssetEnum]] = mapped_column(JSONB, nullable=True)

    # Individual Livelihood fields
    educational_status: Mapped[EducationalStatusEnum] = mapped_column(String, nullable=True)
    primary_livelihood: Mapped[LivelihoodEnum] = mapped_column(String, nullable=True)
    secondary_livelihood: Mapped[LivelihoodEnum] = mapped_column(String, nullable=True)
    employment_status: Mapped[EmploymentStatusEnum] = mapped_column(String, nullable=True)
    mobile_phone_type: Mapped[MobilePhoneTypeEnum] = mapped_column(String, nullable=True)

    #Indvidual Vulnerability fields
    disability_status: Mapped[DisabilityStatusEnum] = mapped_column(String, nullable=True)
    orphanhood_flag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    chronic_illness_flag: Mapped[bool] = mapped_column(Boolean, nullable=True)
    displacement_status: Mapped[DisplacementStatusEnum] = mapped_column(String, nullable=True)
    pastoralist_classification: Mapped[PastoralistClassificationEnum] = mapped_column(String, nullable=True)
    high_mobility_indicator: Mapped[bool] = mapped_column(Boolean, nullable=True)
    plw_status: Mapped[bool] = mapped_column(Boolean, nullable=True)
    plw_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)

    is_head: Mapped[bool] = mapped_column(Boolean, nullable=True)
