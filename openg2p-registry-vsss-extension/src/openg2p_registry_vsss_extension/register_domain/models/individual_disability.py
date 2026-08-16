from ..services import G2PRegisterDomainServiceIndividualDisability
from sqlalchemy import Enum, select, String
from sqlalchemy.orm import Mapped, mapped_column, Session
from openg2p_registry_core.models import (
    G2PRegister, G2PRegisterHistory
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from .enums import DisabilityDomainEnum, DisabilitySeverityEnum
from .individual import G2PIntakeFormIndividual

# All Register classes should have the prefix G2PRegister
class G2PRegisterIndividualDisability(G2PRegister):
    __tablename__ = "g2p_register_individual_disability"

    disability_domains: Mapped[DisabilityDomainEnum] = mapped_column(String, nullable=True)
    disability_severity: Mapped[DisabilitySeverityEnum] = mapped_column(String, nullable=True)

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceIndividualDisability().construct_record_name(self.to_dict())
        
    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceIndividualDisability().construct_search_text(self.to_dict())


# All Register History classes should have the prefix G2PRegisterHistory
# All Intake Form classes should have the prefix G2PIntakeForm
class G2PIntakeFormIndividualDisability(G2PIntakeForm, G2PRegister):
    __tablename__ = "g2p_intake_form_individual_disability"

    disability_domains: Mapped[DisabilityDomainEnum] = mapped_column(String, nullable=True)
    disability_severity: Mapped[DisabilitySeverityEnum] = mapped_column(String, nullable=True)

    def get_record_name_fields(self) -> str:
        return G2PRegisterDomainServiceIndividualDisability().construct_record_name(self.to_dict())
        
    def get_search_text_fields(self) -> str:
        return G2PRegisterDomainServiceIndividualDisability().construct_search_text(self.to_dict())

    async def get_link_internal_record_id(self, session: Session):
        result = await session.execute(
            select(G2PIntakeFormIndividual).where(G2PIntakeFormIndividual.submission_id == self.submission_id)
        )
        individual = result.scalars().first()
        if individual:
            self.link_internal_record_id = individual.internal_record_id


# All Register History classes should have the prefix G2PRegisterHistory


class G2PRegisterHistoryIndividualDisability(G2PRegisterHistory):
    __tablename__ = "g2p_register_history_individual_disability"

    disability_domains: Mapped[DisabilityDomainEnum] = mapped_column(String, nullable=True)
    disability_severity: Mapped[DisabilitySeverityEnum] = mapped_column(String, nullable=True)

    
