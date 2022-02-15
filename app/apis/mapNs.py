from flask import request
from flask_restx import Namespace, Resource, fields
from app.models.schemas import MindMapSchema, LeafSchema
from app.models.mindmap import MindMap
from app.models.leaf import Leaf

ns = Namespace('maps', description='Map related operations')

mindMap = ns.model('Mind Map', {
    'id': fields.String(required=True, description="The mind map identifier"),
})

leaf = ns.model('Leaf', {
    'path': fields.String(description="The leaf path"),
    'text': fields.String(description="The leaf text"),
})

mindMapSchema = MindMapSchema()
mindMapListSchema = MindMapSchema(many=True)

leafSchema = LeafSchema()
leafListSchema = LeafSchema(many=True)

@ns.route('/', strict_slashes=False)
class MindMapListResource(Resource):
    @ns.doc('List of mind maps')
    def get(self):
        '''List of mind maps'''
        return mindMapListSchema.dump(MindMap.getAll()), 200


    @ns.expect(mindMap)
    @ns.doc("Create a map")
    def put(self):
        """ Create a mind map """
        mindMapData = mindMapSchema.load(ns.payload)
        mindMapData.saveToDb()
        return mindMapSchema.dump(mindMapData), 200


@ns.route("/<string:mapId>")
class MindMapResource(Resource):
    @ns.doc("Get a specific map")
    def get(self, mapId):
        """ Get a specific mind map's metadata """
        foundMindMap = MindMap.findById(mapId)

        if foundMindMap != None:
            return mindMapSchema.dump(foundMindMap), 200
        else:
            return { "message": "Map not found" }, 404


@ns.route("/<string:mapId>/leaves")
class LeafListResource(Resource):
    @ns.doc(
        "Get a specific map",
        params={
            "path": { 'description': 'Leaf must exist' }
        }
    )
    def get(self, mapId):
        """ Get a specific mind map's leaves """
        foundMindMap = MindMap.findById(mapId)

        if foundMindMap != None:
            path = request.args.get("path")

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


    @ns.expect(leaf)
    @ns.doc("Create a specific leaf")
    def put(self, mapId):
        """ Create/Update a leaf on a map """
        path = ns.payload["path"]
        text = ns.payload["text"]

        cuLeaf = Leaf.createOrUpdateLeaf(mapId, path, text)

        if cuLeaf != None:
            return leafSchema.dump(cuLeaf), 200
        else:
            return { "message": "Map not found" }, 404
