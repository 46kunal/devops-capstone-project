"""Security configuration for the Customer Accounts service."""

from flask_cors import CORS
from flask_talisman import Talisman


def configure_security(app):
    """Apply response headers and a restricted CORS policy."""
    Talisman(app, force_https=False, content_security_policy={"default-src": "'self'"})
    CORS(app, resources={r"/accounts*": {"origins": app.config["CORS_ORIGINS"]}})
