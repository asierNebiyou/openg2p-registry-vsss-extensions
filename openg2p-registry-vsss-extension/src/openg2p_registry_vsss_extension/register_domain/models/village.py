from sqlalchemy import String, Integer, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory, G2PGeo, G2PGeoHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm


class G2PRegisterVillage(G2PRegister, G2PGeo):
    """Uganda VSSS Village register (Gen2)."""

    __tablename__ = "g2p_register_villages"

    village_code: Mapped[str] = mapped_column(String, nullable=True)
    village_name: Mapped[str] = mapped_column(String, nullable=True)

    # Uganda admin cascade
    region: Mapped[str] = mapped_column(String, nullable=True)
    district: Mapped[str] = mapped_column(String, nullable=True)
    subcounty: Mapped[str] = mapped_column(String, nullable=True)
    parish: Mapped[str] = mapped_column(String, nullable=True)

    # Leadership / capacity (from Odoo village_registry)
    chairperson_name: Mapped[str] = mapped_column(String, nullable=True)
    chairperson_phone: Mapped[str] = mapped_column(String, nullable=True)
    secretary_name: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_name: Mapped[str] = mapped_column(String, nullable=True)

    household_count: Mapped[int] = mapped_column(Integer, nullable=True)
    population_estimate: Mapped[int] = mapped_column(Integer, nullable=True)

    grant_status: Mapped[str] = mapped_column(String, nullable=True)
    sacco_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_account_number: Mapped[str] = mapped_column(String, nullable=True)

    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    signed_grant_agreement: Mapped[bool] = mapped_column(Boolean, nullable=True)
    governance_records: Mapped[str] = mapped_column(String, nullable=True)
    financial_management: Mapped[str] = mapped_column(String, nullable=True)

    def get_record_name_fields(self) -> str:
        from openg2p_registry_extensions.register_domain.services import (
            G2PRegisterDomainServiceVillage,
        )
        return G2PRegisterDomainServiceVillage().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        from openg2p_registry_extensions.register_domain.services import (
            G2PRegisterDomainServiceVillage,
        )
        return G2PRegisterDomainServiceVillage().construct_search_text(self.to_dict())


class G2PIntakeFormVillage(G2PIntakeForm, G2PRegister, G2PGeo):
    __tablename__ = "g2p_intake_form_villages"

    village_code: Mapped[str] = mapped_column(String, nullable=True)
    village_name: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    district: Mapped[str] = mapped_column(String, nullable=True)
    subcounty: Mapped[str] = mapped_column(String, nullable=True)
    parish: Mapped[str] = mapped_column(String, nullable=True)
    chairperson_name: Mapped[str] = mapped_column(String, nullable=True)
    chairperson_phone: Mapped[str] = mapped_column(String, nullable=True)
    secretary_name: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_name: Mapped[str] = mapped_column(String, nullable=True)
    household_count: Mapped[int] = mapped_column(Integer, nullable=True)
    population_estimate: Mapped[int] = mapped_column(Integer, nullable=True)
    grant_status: Mapped[str] = mapped_column(String, nullable=True)
    sacco_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_account_number: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    signed_grant_agreement: Mapped[bool] = mapped_column(Boolean, nullable=True)
    governance_records: Mapped[str] = mapped_column(String, nullable=True)
    financial_management: Mapped[str] = mapped_column(String, nullable=True)

    def get_record_name_fields(self) -> str:
        from openg2p_registry_extensions.register_domain.services import (
            G2PRegisterDomainServiceVillage,
        )
        return G2PRegisterDomainServiceVillage().construct_intake_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        from openg2p_registry_extensions.register_domain.services import (
            G2PRegisterDomainServiceVillage,
        )
        return G2PRegisterDomainServiceVillage().construct_intake_search_text(self.to_dict())


class G2PRegisterHistoryVillage(G2PRegisterHistory, G2PGeoHistory):
    __tablename__ = "g2p_register_history_villages"

    village_code: Mapped[str] = mapped_column(String, nullable=True)
    village_name: Mapped[str] = mapped_column(String, nullable=True)
    region: Mapped[str] = mapped_column(String, nullable=True)
    district: Mapped[str] = mapped_column(String, nullable=True)
    subcounty: Mapped[str] = mapped_column(String, nullable=True)
    parish: Mapped[str] = mapped_column(String, nullable=True)
    chairperson_name: Mapped[str] = mapped_column(String, nullable=True)
    chairperson_phone: Mapped[str] = mapped_column(String, nullable=True)
    secretary_name: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_name: Mapped[str] = mapped_column(String, nullable=True)
    household_count: Mapped[int] = mapped_column(Integer, nullable=True)
    population_estimate: Mapped[int] = mapped_column(Integer, nullable=True)
    grant_status: Mapped[str] = mapped_column(String, nullable=True)
    sacco_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_name: Mapped[str] = mapped_column(String, nullable=True)
    bank_account_number: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    signed_grant_agreement: Mapped[bool] = mapped_column(Boolean, nullable=True)
    governance_records: Mapped[str] = mapped_column(String, nullable=True)
    financial_management: Mapped[str] = mapped_column(String, nullable=True)
