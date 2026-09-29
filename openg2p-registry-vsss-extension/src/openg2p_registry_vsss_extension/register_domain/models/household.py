from openg2p_registry_extensions.register_domain.services import G2PRegisterDomainServiceHousehold
from sqlalchemy import String, Integer, Boolean, Numeric, Date
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory, G2PGeo, G2PGeoHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from datetime import datetime
from .enums import (
    FinancialManagementEnum,
    TrainingNeedsEnum,
    LoanRequirementEnum,
    AmountRequiredInEnum,
    GrantStatusEnum,
)


# All Register classes should have the prefix G2PRegister
class G2PRegisterHousehold(G2PRegister, G2PGeo):
    __tablename__ = "g2p_register_households"

    # Identity
    name: Mapped[str] = mapped_column(String, nullable=True)
    household_size: Mapped[int] = mapped_column(Integer, nullable=True)

    # Administrative Location. Region through village come from master data
    # via G2PGeo.geo_lowest_level_value_id and geo_code_hierarchy_json.
    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    # Financial Mapping
    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    branch_name: Mapped[str] = mapped_column(String, nullable=True)
    branch_code: Mapped[str] = mapped_column(String, nullable=True)
    account_number: Mapped[str] = mapped_column(String, nullable=True)
    ifsc_code: Mapped[str] = mapped_column(String, nullable=True)

    # Bank Details
    financial_management: Mapped[FinancialManagementEnum] = mapped_column(String, nullable=True)
    last_disbursement_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    last_disbursement_amount: Mapped[float] = mapped_column(Numeric, nullable=True)

    # Capacity & Needs
    training_needs: Mapped[TrainingNeedsEnum] = mapped_column(String, nullable=True)
    loan_requirement: Mapped[LoanRequirementEnum] = mapped_column(String, nullable=True)
    grand_required_in: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    amount_required: Mapped[int] = mapped_column(Integer, nullable=True)
    amount_required_in: Mapped[AmountRequiredInEnum] = mapped_column(String, nullable=True)
    signed_grant_agreement: Mapped[bool] = mapped_column(Boolean, nullable=True)
    grant_status: Mapped[GrantStatusEnum] = mapped_column(String, nullable=True)

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

    name: Mapped[str] = mapped_column(String, nullable=True)
    household_size: Mapped[int] = mapped_column(Integer, nullable=True)

    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    branch_name: Mapped[str] = mapped_column(String, nullable=True)
    branch_code: Mapped[str] = mapped_column(String, nullable=True)
    account_number: Mapped[str] = mapped_column(String, nullable=True)
    ifsc_code: Mapped[str] = mapped_column(String, nullable=True)

    financial_management: Mapped[FinancialManagementEnum] = mapped_column(String, nullable=True)
    last_disbursement_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    last_disbursement_amount: Mapped[float] = mapped_column(Numeric, nullable=True)

    training_needs: Mapped[TrainingNeedsEnum] = mapped_column(String, nullable=True)
    loan_requirement: Mapped[LoanRequirementEnum] = mapped_column(String, nullable=True)
    grand_required_in: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    amount_required: Mapped[int] = mapped_column(Integer, nullable=True)
    amount_required_in: Mapped[AmountRequiredInEnum] = mapped_column(String, nullable=True)
    signed_grant_agreement: Mapped[bool] = mapped_column(Boolean, nullable=True)
    grant_status: Mapped[GrantStatusEnum] = mapped_column(String, nullable=True)

    def get_record_name_fields(self) -> str:
        """Return household fields used to build record_name."""
        return G2PRegisterDomainServiceHousehold().construct_intake_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return household fields used to build search_text."""
        return G2PRegisterDomainServiceHousehold().construct_search_text(self.to_dict())


class G2PRegisterHistoryHousehold(G2PRegisterHistory, G2PGeoHistory):
    __tablename__ = "g2p_register_history_households"

    name: Mapped[str] = mapped_column(String, nullable=True)
    household_size: Mapped[int] = mapped_column(Integer, nullable=True)

    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    branch_name: Mapped[str] = mapped_column(String, nullable=True)
    branch_code: Mapped[str] = mapped_column(String, nullable=True)
    account_number: Mapped[str] = mapped_column(String, nullable=True)
    ifsc_code: Mapped[str] = mapped_column(String, nullable=True)

    financial_management: Mapped[FinancialManagementEnum] = mapped_column(String, nullable=True)
    last_disbursement_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    last_disbursement_amount: Mapped[float] = mapped_column(Numeric, nullable=True)

    training_needs: Mapped[TrainingNeedsEnum] = mapped_column(String, nullable=True)
    loan_requirement: Mapped[LoanRequirementEnum] = mapped_column(String, nullable=True)
    grand_required_in: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    amount_required: Mapped[int] = mapped_column(Integer, nullable=True)
    amount_required_in: Mapped[AmountRequiredInEnum] = mapped_column(String, nullable=True)
    signed_grant_agreement: Mapped[bool] = mapped_column(Boolean, nullable=True)
    grant_status: Mapped[GrantStatusEnum] = mapped_column(String, nullable=True)
