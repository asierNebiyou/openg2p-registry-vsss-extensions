from ..services import G2PRegisterDomainServiceIndividual
from sqlalchemy import String, Boolean, Numeric, select
from sqlalchemy.orm import Mapped, mapped_column, Session

from openg2p_registry_core.models import (
    G2PRegister, G2PRegisterHistory, G2PPerson, G2PGeo,
    G2PPersonHistory, G2PGeoHistory, G2PRegisterAuthentication
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from .household import G2PIntakeFormHousehold


# All Register classes should have the prefix G2PRegister
class G2PRegisterIndividual(G2PRegister, G2PPerson, G2PGeo, G2PRegisterAuthentication):
    __tablename__ = "g2p_register_individuals"

    # Identity. first_name, middle_name, last_name, birth_date, and gender
    # already exist on G2PPerson.
    additional_name: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    # Administrative Location. Region through village come from master data
    # via G2PGeo.geo_lowest_level_value_id and geo_code_hierarchy_json.
    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    # Bank Details
    has_sacco_account: Mapped[bool] = mapped_column(Boolean, nullable=True)
    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_account_number: Mapped[str] = mapped_column(String, nullable=True)

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

    additional_name: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    has_sacco_account: Mapped[bool] = mapped_column(Boolean, nullable=True)
    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_account_number: Mapped[str] = mapped_column(String, nullable=True)

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


class G2PRegisterHistoryIndividual(G2PRegisterHistory, G2PPersonHistory, G2PGeoHistory, G2PRegisterAuthentication):
    __tablename__ = "g2p_register_history_individuals"

    additional_name: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String, nullable=True)

    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    has_sacco_account: Mapped[bool] = mapped_column(Boolean, nullable=True)
    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_account_number: Mapped[str] = mapped_column(String, nullable=True)
