from sqlalchemy import String, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from openg2p_registry_core.models import G2PRegister, G2PRegisterHistory, G2PGeo, G2PGeoHistory
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm


class G2PRegisterVillage(G2PRegister, G2PGeo):
    """Uganda VSSS Village register (Gen2)."""

    __tablename__ = "g2p_register_villages"

    # Identity
    name: Mapped[str] = mapped_column(String, nullable=True)
    household_count: Mapped[int] = mapped_column(Integer, nullable=True)
    code: Mapped[str] = mapped_column(String, nullable=True)

    # Administrative Location. Region through village come from master data
    # via G2PGeo.geo_lowest_level_value_id and geo_code_hierarchy_json.
    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    # Leadership
    chairperson_name: Mapped[str] = mapped_column(String, nullable=True)
    chairperson_phone: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_name: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_phone: Mapped[str] = mapped_column(String, nullable=True)
    secretary_name: Mapped[str] = mapped_column(String, nullable=True)
    secretary_phone: Mapped[str] = mapped_column(String, nullable=True)

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

    name: Mapped[str] = mapped_column(String, nullable=True)
    household_count: Mapped[int] = mapped_column(Integer, nullable=True)
    code: Mapped[str] = mapped_column(String, nullable=True)

    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    chairperson_name: Mapped[str] = mapped_column(String, nullable=True)
    chairperson_phone: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_name: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_phone: Mapped[str] = mapped_column(String, nullable=True)
    secretary_name: Mapped[str] = mapped_column(String, nullable=True)
    secretary_phone: Mapped[str] = mapped_column(String, nullable=True)

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

    name: Mapped[str] = mapped_column(String, nullable=True)
    household_count: Mapped[int] = mapped_column(Integer, nullable=True)
    code: Mapped[str] = mapped_column(String, nullable=True)

    polling_station: Mapped[str] = mapped_column(String, nullable=True)
    gps_latitude: Mapped[float] = mapped_column(Numeric, nullable=True)
    gps_longitude: Mapped[float] = mapped_column(Numeric, nullable=True)

    chairperson_name: Mapped[str] = mapped_column(String, nullable=True)
    chairperson_phone: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_name: Mapped[str] = mapped_column(String, nullable=True)
    treasurer_phone: Mapped[str] = mapped_column(String, nullable=True)
    secretary_name: Mapped[str] = mapped_column(String, nullable=True)
    secretary_phone: Mapped[str] = mapped_column(String, nullable=True)
