# src/infrastructure/config/settings.py
from dataclasses import dataclass
from datetime import timedelta

@dataclass(frozen=True)
class AppSettings:
    """Centralized application settings."""
    environment: str = "dev"
    database_path: str = "deudas.db" # Default for development
    default_currency: str = "COP"  # Using COP as a potential local default if needed

    @classmethod
    def load(cls, env: str) -> 'AppSettings':
        """Loads settings based on the environment."""
        if env == "prod":
            # Production path uses extension for safety/consistency
            return cls(environment="prod", database_path=".deudas.db") 
        elif env == "dev":
            return cls(environment="dev", database_path="deudas.db")
        else:
            raise ValueError(f"Unknown environment specified: {env}")

# Constants can live here to replace hardcoded values
COUNTRY_CODE = "+52" 
DEFAULT_CURRENCY = "USD" # Using USD for Money VO consistency unless overridden