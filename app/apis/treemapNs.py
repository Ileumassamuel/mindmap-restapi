from flask_restx import Namespace, Resource, fields

api = Namespace('treeMap', description='Map related operations')

@api.route("/<string:mapId>")
class TreeMap(Resource):
    @api.doc("Get a map's tree")
    def get(self, mapId):
        """ Get a specific mind map's metadata """
        return { "id": "vladdy" }
