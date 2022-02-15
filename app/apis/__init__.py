from flask_restx import Api
from flask import Blueprint

from .mapNs import ns as mapNamespace
from .treeNs import ns as treeNamespace

apiBlueprint = Blueprint("api", __name__, url_prefix="/api/v1")

api = Api(apiBlueprint, title="API", description="Main routes.")

api.add_namespace(mapNamespace)
api.add_namespace(treeNamespace)
