from typing import Optional
from openg2p_registry_core.schemas import (
    G2PRegisterBaseSchema, G2PRegisterHistorySchema, G2PIntakeFormSchemaBase
)
from ..models.enums import DisabilityDomainEnum, DisabilitySeverityEnum


class G2PRegisterSchemaIndividualDisability(G2PRegisterBaseSchema):
    disability_domains: Optional[DisabilityDomainEnum] = None
    disability_severity: Optional[DisabilitySeverityEnum] = None


class G2PIntakeFormSchemaIndividualDisability(G2PIntakeFormSchemaBase, G2PRegisterSchemaIndividualDisability):
    pass


class G2PRegisterHistorySchemaIndividualDisability(G2PRegisterHistorySchema):
    disability_domains: Optional[DisabilityDomainEnum] = None
    disability_severity: Optional[DisabilitySeverityEnum] = None
