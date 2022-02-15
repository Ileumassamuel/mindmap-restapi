from flask_restx import Namespace, Resource, fields, reqparse
from app.models.schemas import MindMapSchema, LeafSchema
from app.models.mindmap import MindMap, Leaf

parser = reqparse.RequestParser()
parser.add_argument('path', type=str, help="Leaf must exist")

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

leafSchema = LeafSchema()
leafListSchema = LeafSchema(many=True)

@api.route('/', strict_slashes=False)
class MindMapListResource(Resource):
    @api.doc('List of mind maps')
    def get(self):
        '''List of mind maps'''
        return mindMapListSchema.dump(MindMap.getAll()), 200


    @api.expect(mindMap)
    @api.doc("Create a map")
    def put(self):
        """ Create a mind map """
        mindMapData = mindMapSchema.load(api.payload)
        mindMapData.saveToDb()
        return mindMapSchema.dump(mindMapData), 201


@api.route("/<string:mapId>")
class MindMapResource(Resource):
    @api.doc("Get a specific map")
    def get(self, mapId):
        """ Get a specific mind map's metadata """
        foundMindMap = MindMap.findById(mapId)

        if foundMindMap != None:
            return mindMapSchema.dump(foundMindMap), 200
        else:
            return { "message": "Map not found" }, 404


@api.route("/<string:mapId>/leaves")
class LeafListResource(Resource):
    @api.expect(parser)
    # @api.marshal_list_with(leaf)
    @api.doc("Get a specific map")
    def get(self, mapId):
        """ Get a specific mind map's leaves """
        foundMindMap = MindMap.findById(mapId)
        args = parser.parse_args()
        path = args["path"]

        if foundMindMap != None:
            if path != None:
                foundLeaf = Leaf.findByMapAndPath(mapId, path)

                if foundLeaf != None:
                    return leafSchema.dump(foundLeaf), 200
                else:
                    return { "message": "Leaf not found" }, 404
            else:
                return leafListSchema.dump(Leaf.getAll()), 200
        else:
            return { "message": "Map not found" }, 404


    @api.expect(leaf)
    # @api.marshal_with(leaf)
    @api.doc("Create a specific leaf")
    def put(self, mapId):
        """ Create/Update a leaf on a map """
        path = api.payload["path"]
        text = api.payload["text"]

        cuLeaf = Leaf.createOrUpdateLeaf(mapId, path, text)

        if cuLeaf != None:
            return leafSchema.dump(cuLeaf), 200
        else:
            return { "message": "Map not found" }, 404
