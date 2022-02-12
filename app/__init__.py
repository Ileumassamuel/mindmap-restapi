""" Top level module
This module:
- Contains create_app()
- Registers extensions
"""

from flask import Flask

# Import extensions
from .extensions import db, marshmellow

# Import config
from config import envToConfig


def create_app(env) -> Flask:
    app = Flask(__name__)
    app.config.from_object(envToConfig[env])

    register_extensions(app)

    from .apis import apiBlueprint

    app.register_blueprint(apiBlueprint)

    return app


def register_extensions(app):
    db.init_app(app)
    marshmellow.init_app(app)
