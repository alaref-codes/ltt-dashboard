import os
from pydantic_settings import BaseSettings

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{os.path.join(PROJECT_ROOT, 'data', 'churn.db')}"
    jwt_secret: str = "dev-only-secret-change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480
    model_dir: str = os.path.join(PROJECT_ROOT, "ml", "models")

    risk_threshold_medium: int = 30
    risk_threshold_high: int = 60
    risk_threshold_critical: int = 80

    model_config = {
        "env_file": os.path.join(PROJECT_ROOT, ".env"),
        "protected_namespaces": ("settings_",),
    }


settings = Settings()
