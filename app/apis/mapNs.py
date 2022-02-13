from flask_restx import Namespace, Resource, fields
from app.models.schemas import MindMapSchema
from app.models.mindmap import MindMap

api = Namespace('maps', description='Map related operations')

mindMap = api.model('Mind Map', {
    'id': fields.String(required=True, description="The mind map identifier"),
})

leaf = api.model('Leaf', {
    'path': fields.String(description="The leaf path"),
    'text': fields.String(description="The leaf text"),
})

mindMapSchema = MindMapSchema()
mindMapListSchema = MindMapSchema(many=True)

@api.route('/', strict_slashes=False)
class MindMapListResource(Resource):
    @api.doc('List of mind maps')
    def get(self):
        '''List of mind maps'''
        return mindMapListSchema.dump(MindMap.getAll()), 200


    @api.expect(mindMap)
    @api.doc("Create a map")
    def post(self):
        """ Create a mind map """
        mindMapData = mindMapSchema.load(api.payload)
        mindMapData.saveToDb()
        return mindMapSchema.dump(mindMapData), 201


@api.route("/<string:mapId>")
class MindMapResource(Resource):
    @api.doc("Get a specific map")
    @api.marshal_with(mindMap)
    def get(self, mapId):
        """ Get a specific mind map's metadata """
        return { "id": "vladdy" }


@api.route("/<string:mapId>/leaves")
class LeafListResource(Resource):
    @api.doc("Get a specific map")
    @api.marshal_with(mindMap)
    def get(self, mapId):
        """ Get a specific mind map's leaves """
        return { "id": "vladdy" }


@api.route("/<string:mapId>/leaves/<string:leafId>")
class LeafResource(Resource):
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
