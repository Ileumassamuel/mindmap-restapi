"""
Extensions module
Each extension is initialized when app is created.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
marshmellow = Marshmallow()
