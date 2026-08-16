from ..services import G2PRegisterDomainServiceIndividualLivestock
from sqlalchemy import String, Enum, select
from sqlalchemy.orm import Mapped, mapped_column, Session
from openg2p_registry_core.models import (
    G2PRegister, G2PRegisterHistory
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from .enums import LivestockSpeciesEnum, LivestockCountBandEnum
from .individual import G2PIntakeFormIndividual



class G2PRegisterIndividualLivestock(G2PRegister):
    __tablename__ = "g2p_register_individual_livestock"

    livestock_species: Mapped[LivestockSpeciesEnum] = mapped_column(String, nullable=True)
    livestock_counts: Mapped[LivestockCountBandEnum] = mapped_column(String, nullable=True)


    def get_record_name_fields(self) -> str:
        """Return individual livestock fields used to build record_name."""
        return G2PRegisterDomainServiceIndividualLivestock().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return individual livestock fields used to build search_text."""
        return G2PRegisterDomainServiceIndividualLivestock().construct_search_text(self.to_dict())


# All Intake Form classes should have the prefix G2PIntakeForm
class G2PIntakeFormIndividualLivestock(G2PIntakeForm, G2PRegister):
    __tablename__ = "g2p_intake_form_individual_livestock"

    livestock_species: Mapped[LivestockSpeciesEnum] = mapped_column(String, nullable=True)
    livestock_counts: Mapped[LivestockCountBandEnum] = mapped_column(String, nullable=True)


    def get_record_name_fields(self) -> str:
        """Return individual livestock fields used to build record_name."""
        return G2PRegisterDomainServiceIndividualLivestock().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return individual livestock fields used to build search_text."""
        return G2PRegisterDomainServiceIndividualLivestock().construct_search_text(self.to_dict())

    async def get_link_internal_record_id(self, session: Session):
        result = await session.execute(
            select(G2PIntakeFormIndividual).where(G2PIntakeFormIndividual.submission_id == self.submission_id)
        )
        individual = result.scalars().first()
        if individual:
            self.link_internal_record_id = individual.internal_record_id


class G2PRegisterHistoryIndividualLivestock(G2PRegisterHistory):
    __tablename__ = "g2p_register_history_individual_livestock"

    livestock_species: Mapped[LivestockSpeciesEnum] = mapped_column(String, nullable=True)
    livestock_counts: Mapped[LivestockCountBandEnum] = mapped_column(String, nullable=True)
