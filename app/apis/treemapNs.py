from flask_restx import Namespace, Resource, fields
from app.models.mindmap import Leaf

api = Namespace('treeMap', description='Tree related operations')

@api.route("/<string:mapId>")
class TreeMap(Resource):
    @api.doc("Get a map's tree")
    def get(self, mapId):
        """ Get a specific mind map's tree """
        leaves = Leaf.filterByMap(mapId)
        paths = [leaf.path for leaf in leaves]
        print(paths)
        return { "id": "vladdy" }
