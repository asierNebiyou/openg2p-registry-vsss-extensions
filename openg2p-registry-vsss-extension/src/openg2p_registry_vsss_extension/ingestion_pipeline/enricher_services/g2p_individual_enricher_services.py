import logging
from typing import Dict
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from openg2p_registry_core.interfaces import G2PPayloadEnricherInterface
from openg2p_registry_core.models import MaritalStatusEnum, GenderEnum
from ...register_domain.models import G2PRegisterIndividual


_logger = logging.getLogger('g2p-payload-enricher-service')

# DCI Payload Enrichers
class G2PDciIndividualCreateEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PDciIndividualCreateEnricherService")

        parent_link_internal_record_id = None

        # Try to find a parent individual using parent1_identifier
        parent1_identifier_data = data.get('parent1_identifier')
        if isinstance(parent1_identifier_data, dict):
            identifier_value = parent1_identifier_data.get('identifier_value')
            if identifier_value:
                _logger.debug(f"Checking for parent individual with parent1_identifier: {identifier_value}")
                parent_individual = session.execute(
                    select(G2PRegisterIndividual).filter_by(foundational_id=identifier_value)
                ).scalar_one_or_none()

                if parent_individual:
                    parent_link_internal_record_id = parent_individual.link_internal_record_id
                    _logger.info(f"Found parent individual via parent1_identifier. Link record ID: {parent_link_internal_record_id}")

        # If parent1_identifier didn't yield a result, try parent2_identifier
        if parent_link_internal_record_id is None:
            parent2_identifier_data = data.get('parent2_identifier')
            if isinstance(parent2_identifier_data, dict):
                identifier_value = parent2_identifier_data.get('identifier_value')
                if identifier_value:
                    _logger.debug(f"Checking for parent individual with parent2_identifier: {identifier_value}")
                    parent_individual = session.execute(
                        select(G2PRegisterIndividual).filter_by(foundational_id=identifier_value)
                    ).scalar_one_or_none()

                    if parent_individual:
                        parent_link_internal_record_id = parent_individual.link_internal_record_id
                        _logger.info(f"Found parent individual via parent2_identifier. Link record ID: {parent_link_internal_record_id}")

        if parent_link_internal_record_id:
            data['link_internal_record_id'] = parent_link_internal_record_id
        else:
            _logger.warning("Could not find a parent individual using either parent1_identifier or parent2_identifier.")
            data["link_internal_record_id"] = None
        
        # Normalize and map marital_status values to G2P standard values.
        marital_status_mapping = {
            "s": MaritalStatusEnum.SINGLE.value,
            "u": MaritalStatusEnum.SINGLE.value,
            "m": MaritalStatusEnum.MARRIED.value,
            "w": MaritalStatusEnum.WIDOWED.value,
            "d": MaritalStatusEnum.DIVORCED.value,
            "a": MaritalStatusEnum.SEPARATED.value,
            "l": MaritalStatusEnum.SEPARATED.value,
            "widow": MaritalStatusEnum.WIDOWED.value,
            "married": MaritalStatusEnum.MARRIED.value,
            "unmarried": MaritalStatusEnum.SINGLE.value,
            "divorced": MaritalStatusEnum.DIVORCED.value,
            "annulled": MaritalStatusEnum.SEPARATED.value,
            "never married": MaritalStatusEnum.SINGLE.value,
            "legally separated": MaritalStatusEnum.SEPARATED.value,
        }

        marital_status = data.get("marital_status")
        if isinstance(marital_status, str):
            marital_status_normalized = marital_status.strip().lower()
            g2p_value = marital_status_mapping.get(marital_status_normalized)
            if g2p_value:
                data["marital_status"] = g2p_value
            else:
                data["marital_status"] = MaritalStatusEnum.UNKNOWN.value
                
        # Transform birth_date and death_date to only Date (YYYY-MM-DD)
        for date_field in ["birth_date", "death_date"]:
            value = data.get(date_field)
            if isinstance(value, str) and value.strip():
                try:
                    if "T" in value:
                        date_str = value.split("T")[0]
                    else:
                        date_str = value

                    parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
                    data[date_field] = parsed_date.strftime("%Y-%m-%d")
                except Exception as e:
                    _logger.warning(f"Could not parse {date_field}: {value} ({str(e)})")

        return data

class G2PDciIndividualUpdateEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PDciIndividualUpdateEnricherService")
        return data

class G2PDciIndividualDeleteEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PDciIndividualDeleteEnricherService")
        return data

class G2PDciVcIndividualCreateEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PDciVcIndividualCreateEnricherService")

        parent_link_internal_record_id = None

        jwt_payload = data.get('jwt', {}).get('payload', {})
        parents_data = jwt_payload.get('parents')
            
        if isinstance(parents_data, dict):
            parents_data = [parents_data]
        elif not isinstance(parents_data, list):
            parents_data = []

        for parent in parents_data:
            if isinstance(parent, dict):
                identifier_value = parent.get('identifier')
                if identifier_value:
                    _logger.debug(f"Checking for parent individual with identifier: {identifier_value}")
                    parent_individual = session.execute(
                        select(G2PRegisterIndividual).filter_by(foundational_id=identifier_value)
                    ).scalar_one_or_none()

                    if parent_individual:
                        parent_link_internal_record_id = parent_individual.link_internal_record_id
                        _logger.info(f"Found parent individual via identifier. Link record ID: {parent_link_internal_record_id}")
                        break
        
        if parent_link_internal_record_id:
            data['link_internal_record_id'] = parent_link_internal_record_id

        return data

class G2PDciVcIndividualUpdateEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PDciVcIndividualUpdateEnricherService")
        return data

class G2PDciVcIndividualDeleteEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PDciVcIndividualDeleteEnricherService")
        return data

# SPDCI Payload Enrichers
class G2PSpdciIndividualCreateEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PSpdciIndividualCreateEnricherService")
        return data

class G2PSpdciIndividualUpdateEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PSpdciIndividualUpdateEnricherService")
        return data

class G2PSpdciIndividualDeleteEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PSpdciIndividualDeleteEnricherService")
        return data

# UNDP Payload Enrichers
class G2PUndpIndividualCreateEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PUndpIndividualCreateEnricherService")
        return data

class G2PUndpIndividualUpdateEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PUndpIndividualUpdateEnricherService")
        return data

class G2PUndpIndividualDeleteEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, data: Dict, session: Session) -> Dict:
        _logger.info("Processing G2PUndpIndividualDeleteEnricherService")
        return data
