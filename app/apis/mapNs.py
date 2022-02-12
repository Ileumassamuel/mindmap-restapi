from flask_restx import Namespace, Resource, fields

api = Namespace('maps', description='Map related operations')

mindMap = api.model('Mind Map', {
    'id': fields.String(required=True, description="The map identifier"),
})

leaf = api.model('Leaf', {
    'path': fields.String(description="The leaf path"),
    'text': fields.String(description="The leaf text"),
})

@api.route('/', strict_slashes=False)
class MindMapList(Resource):
    @api.doc('List of mind maps')
    def get(self):
        '''List of mind maps'''
        return ["mind map 1"]


    @api.doc("Create a map", body=mindMap)
    def post(self):
        """ Create a mind map """
        print(api.payload)
        return 3


@api.route("/<string:mapId>")
class MindMap(Resource):
    @api.doc("Get a specific map")
    @api.marshal_with(mindMap)
    def get(self, mapId):
        """ Get a specific mind map's metadata """
        return { "id": "vladdy" }


@api.route("/<string:mapId>/leaves")
class LeafList(Resource):
    @api.doc("Get a specific map")
    @api.marshal_with(mindMap)
    def get(self, mapId):
        """ Get a specific mind map's leaves """
        return { "id": "vladdy" }


@api.route("/<string:mapId>/leaves/<string:leafId>")
class Leaf(Resource):
    @api.doc(
        "Get a specific leaf", 
        responses={
            200: ("Leaf fetched", leaf)
        }
    )
    @api.marshal_with(leaf)
    def get(self, mapId, leafId):
        """ Get a specific mind map's leaf """
        return { "path": leafId, "text": "Welcome" }

    @api.marshal_with(leaf)
    def put(self, mapId, leafId):
        """ Modify a specific mind map's leaf """
        return { "path": leafId, "text": "Welcome" }
