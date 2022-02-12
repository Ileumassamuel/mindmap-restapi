from flask_restx import Namespace, Resource, fields

api = Namespace('maps', description='Map related operations')

mindMap = api.model('Mind Map', {
    'id': fields.String(required=True, description="The map identifier"),
})

@api.route('/')
class MindMapList(Resource):
    @api.doc('List of mind maps')
    def get(self):
        '''List of mind maps'''
        return ["mind map 1"]


@api.route("/<string:mapId>")
class MindMap(Resource):
    @api.doc("Get a specific map")
    @api.marshal_with(mindMap)
    def get(self, mapId):
        """ Get a specific mind map's tree """
        return { "id": "vladdy" }

    def post(self, content):
        """ Create a mind map """
        return content


leaf = api.model('Leaf', {
    'path': fields.String(description="The leaf path"),
    'text': fields.String(description="The leaf text"),
})


@api.route("/<string:mapId>/leaves/<string:leafId>")
class Leaf(Resource):
    @api.doc("Get a specific leaf")
    @api.marshal_with(leaf)
    def get(self, mapId, leafId):
        """ Get a specific mind map's leaf """
        return { "path": leafId, "text": "Welcome" }

    def post(self, content):
        """ Create a leaf """
        return content
