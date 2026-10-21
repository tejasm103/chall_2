import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "mindverse-dev-inclusive-learning-key-32chars")
    JSON_SORT_KEYS = False
    
    # Database path resolution
    DB_ENV = os.environ.get("DATABASE")
    if DB_ENV:
        if os.path.isabs(DB_ENV):
            DATABASE = DB_ENV
        else:
            DATABASE = str(BASE_DIR / DB_ENV)
    else:
        DATABASE = str(BASE_DIR / "database" / "mindverse.db")
        
    # CORS Origins
    _raw_origins = os.environ.get(
        "FRONTEND_ORIGIN", 
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:8080,http://127.0.0.1:8080,http://localhost:5000,http://127.0.0.1:5000"
    )
    if _raw_origins.strip() == "*":
        CORS_ORIGINS = "*"
    else:
        CORS_ORIGINS = [orig.strip() for orig in _raw_origins.split(",") if orig.strip()]

    # Caregiver security settings
    CAREGIVER_DEFAULT_USER = os.environ.get("CAREGIVER_DEFAULT_USER", "caregiver")
    CAREGIVER_DEFAULT_PIN = os.environ.get("CAREGIVER_DEFAULT_PIN", "1234")


class DevelopmentConfig(Config):
    """Development configuration with debugging enabled."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration with temporary database."""
    DEBUG = False
    TESTING = True
    DATABASE = str(BASE_DIR / "database" / "test_mindverse.db")
    CORS_ORIGINS = "*"


class ProductionConfig(Config):
    """Production configuration with strict defaults."""
    DEBUG = False
    TESTING = False
    # Ensure SECRET_KEY is set in production
    SECRET_KEY = os.environ.get("SECRET_KEY", "prod-mindverse-secure-fallback-key-strictly-configured")


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
