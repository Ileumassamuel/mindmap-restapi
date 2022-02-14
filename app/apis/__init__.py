from flask_restx import Api
from flask import Blueprint

from .mapNs import api as mapNamespace
from .treemapNs import api as treemapNamespace

apiBlueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(apiBlueprint, title="API", description="Main routes.")

api.add_namespace(mapNamespace)
api.add_namespace(treemapNamespace)
