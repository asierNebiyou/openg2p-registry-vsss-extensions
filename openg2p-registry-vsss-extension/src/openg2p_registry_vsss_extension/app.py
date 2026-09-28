# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_registry_core.app import Initializer as CoreInitializer

from .register_domain.models import (
    G2PRegisterVillage, G2PRegisterHistoryVillage, G2PIntakeFormVillage,
    G2PRegisterHousehold, G2PRegisterHistoryHousehold, G2PIntakeFormHousehold,
    G2PRegisterIndividual, G2PRegisterHistoryIndividual, G2PIntakeFormIndividual,
)
from .register_domain.factory import G2PRegisterDomainFactory
from .register_domain.services import (
    G2PRegisterDomainServiceVillage,
    G2PRegisterDomainServiceHousehold,
    G2PRegisterDomainServiceIndividual,
)

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        CoreInitializer().initialize()

        G2PRegisterDomainServiceVillage()
        G2PRegisterDomainServiceHousehold()
        G2PRegisterDomainServiceIndividual()

        G2PRegisterDomainFactory()

    def migrate_database(self, args):
        async def migrate():
            _logger.info("Migrating VSSS extensions database")

            # Village tables
            await G2PRegisterVillage.create_migrate()
            await G2PRegisterHistoryVillage.create_migrate()
            await G2PIntakeFormVillage.create_migrate()

            # Household tables
            await G2PRegisterHousehold.create_migrate()
            await G2PRegisterHistoryHousehold.create_migrate()
            await G2PIntakeFormHousehold.create_migrate()

            # Individual tables
            await G2PRegisterIndividual.create_migrate()
            await G2PRegisterHistoryIndividual.create_migrate()
            await G2PIntakeFormIndividual.create_migrate()

        asyncio.run(migrate())
