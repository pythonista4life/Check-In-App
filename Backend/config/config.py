import os
from dotenv import load_dotenv

load_dotenv("secrets.env")

# This function provides a dictionary of app configuration settings.
def get_config():
    return {
        "API_TITLE": "Stores REST API",
        "API_VERSION": "v1",
        "OPENAPI_VERSION": "3.0.3",
        "OPENAPI_URL_PREFIX": "/",
        "OPENAPI_SWAGGER_UI_PATH": "/swagger-ui",
        "OPENAPI_SWAGGER_UI_URL": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/",
        "SQLALCHEMY_DATABASE_URI": os.getenv("DATABASE_URL", "sqlite:///data.db"),
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "PROPAGATE_EXCEPTIONS": True,
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "MAIL_SERVER": os.getenv("MAIL_SERVER"),
        "MAIL_PORT": os.getenv("MAIL_PORT"),
        "MAIL_USE_TLS": os.getenv("MAIL_USE_TLS"),
        "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
        "MAIL_PASSWORD": os.getenv("MAIL_PASSWORD"),
    }