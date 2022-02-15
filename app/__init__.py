""" Top level module
This module:
- Contains create_app()
- Registers extensions
"""

import os
from flask import Flask

# Import extensions
from .extensions import db, marshmellow

# Import config
from config import envToConfig


def create_app(env="development") -> Flask:
    app = Flask(__name__)

    env = os.getenv("FLASK_ENV") or env
    app.config.from_object(envToConfig[env])

    register_extensions(app)

    from .apis import apiBlueprint

    app.register_blueprint(apiBlueprint)

    return app


def register_extensions(app):
    db.init_app(app)
    marshmellow.init_app(app)
