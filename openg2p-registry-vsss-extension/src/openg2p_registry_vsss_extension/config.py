from openg2p_registry_core.config import Settings as CoreSettings
from pydantic_settings import SettingsConfigDict

from . import __version__


class Settings(CoreSettings):
    model_config = SettingsConfigDict(
        env_prefix="registry_nsr_extensions_", env_file=".env", extra="allow"
    )

    openapi_title: str = "OpenG2P Registry NSR Extensions"
    openapi_description: str = """
        FastAPI Service for OpenG2P Registry NSR Extensions
        ***********************************
        Further details goes here
        ***********************************
        """
    openapi_version: str = __version__
