from typing import Optional
from datetime import date
from openg2p_registry_core.schemas import G2PRegisterBaseSchema, G2PRegisterHistorySchema, G2PIntakeFormSchemaBase, G2PGeoSchema, G2PGeoHistorySchema
from ..models.enums import (
    FinancialManagementEnum,
    TrainingNeedsEnum,
    LoanRequirementEnum,
    AmountRequiredInEnum,
    GrantStatusEnum,
)


class G2PRegisterSchemaHousehold(G2PRegisterBaseSchema, G2PGeoSchema):
    name: Optional[str] = None
    household_size: Optional[int] = None

    polling_station: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    branch_code: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None

    financial_management: Optional[FinancialManagementEnum] = None
    last_disbursement_date: Optional[date] = None
    last_disbursement_amount: Optional[float] = None

    training_needs: Optional[TrainingNeedsEnum] = None
    loan_requirement: Optional[LoanRequirementEnum] = None
    grand_required_in: Optional[date] = None
    amount_required: Optional[int] = None
    amount_required_in: Optional[AmountRequiredInEnum] = None
    signed_grant_agreement: Optional[bool] = None
    grant_status: Optional[GrantStatusEnum] = None


class G2PIntakeFormSchemaHousehold(G2PIntakeFormSchemaBase, G2PRegisterSchemaHousehold):
    pass


class G2PRegisterHistorySchemaHousehold(G2PRegisterHistorySchema, G2PGeoHistorySchema):
    name: Optional[str] = None
    household_size: Optional[int] = None

    polling_station: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    branch_code: Optional[str] = None
    account_number: Optional[str] = None
    ifsc_code: Optional[str] = None

    financial_management: Optional[FinancialManagementEnum] = None
    last_disbursement_date: Optional[date] = None
    last_disbursement_amount: Optional[float] = None

    training_needs: Optional[TrainingNeedsEnum] = None
    loan_requirement: Optional[LoanRequirementEnum] = None
    grand_required_in: Optional[date] = None
    amount_required: Optional[int] = None
    amount_required_in: Optional[AmountRequiredInEnum] = None
    signed_grant_agreement: Optional[bool] = None
    grant_status: Optional[GrantStatusEnum] = None
