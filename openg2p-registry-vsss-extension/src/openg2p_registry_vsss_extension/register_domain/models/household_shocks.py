from ..services import G2PRegisterDomainServiceHouseholdShock
from sqlalchemy import String, Enum, Date, select
from sqlalchemy.orm import Mapped, mapped_column, Session
from datetime import date
from openg2p_registry_core.models import (
    G2PRegister, G2PRegisterHistory
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from .enums import ShockTypeEnum
from .household import G2PIntakeFormHousehold



class G2PRegisterHouseholdShock(G2PRegister):
    __tablename__ = "g2p_register_household_shocks"

    # link_internal_record_id = internal_record_id of Household
    shocks_last_12m: Mapped[ShockTypeEnum] = mapped_column(String, nullable=True)
    shock_start_date: Mapped[date] = mapped_column(Date, nullable=True)
    shock_end_date: Mapped[date] = mapped_column(Date, nullable=True)


    def get_record_name_fields(self) -> str:
        """Return household shocks fields used to build record_name."""
        return G2PRegisterDomainServiceHouseholdShock().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return household shocks fields used to build search_text."""
        return G2PRegisterDomainServiceHouseholdShock().construct_search_text(self.to_dict())

# All Intake Form classes should have the prefix G2PIntakeForm
class G2PIntakeFormHouseholdShock(G2PIntakeForm, G2PRegister):
    __tablename__ = "g2p_intake_form_household_shocks"

    # link_internal_record_id = internal_record_id of Household
    shocks_last_12m: Mapped[ShockTypeEnum] = mapped_column(String, nullable=True)
    shock_start_date: Mapped[date] = mapped_column(Date, nullable=True)
    shock_end_date: Mapped[date] = mapped_column(Date, nullable=True)


    def get_record_name_fields(self) -> str:
        """Return household shocks fields used to build record_name."""
        return G2PRegisterDomainServiceHouseholdShock().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return household shocks fields used to build search_text."""
        return G2PRegisterDomainServiceHouseholdShock().construct_search_text(self.to_dict())

    async def get_link_internal_record_id(self, session: Session):
        result = await session.execute(
            select(G2PIntakeFormHousehold).where(G2PIntakeFormHousehold.submission_id == self.submission_id)
        )
        household = result.scalars().first()
        if household:
            self.link_internal_record_id = household.internal_record_id


class G2PRegisterHistoryHouseholdShock(G2PRegisterHistory):
    __tablename__ = "g2p_register_history_household_shocks"

    shocks_last_12m: Mapped[ShockTypeEnum] = mapped_column(String, nullable=True)
    shock_start_date: Mapped[date] = mapped_column(Date, nullable=True)
    shock_end_date: Mapped[date] = mapped_column(Date, nullable=True)
