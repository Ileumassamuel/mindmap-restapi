from flask import Response
from flask_restx import Namespace, Resource, fields
from app.models.mindmap import Leaf, MindMap

ns = Namespace('tree', description='Tree related operations')

@ns.route("/<string:mapId>")
class Tree(Resource):
    @ns.produces(["text/plain", "application/json"])
    @ns.doc("Get a map's tree")
    def get(self, mapId):
        """ Get a specific mind map's tree """
        foundMindMap = MindMap.findById(mapId)

        if foundMindMap != None:
            leaves = Leaf.filterRootNodesByMap(mapId)
            tree = "root/"

            level = 0

            for leaf in leaves:
                tree += "\n" + getLeafTree(leaf, 1)

            return Response(tree, mimetype='text/plain')
        else:
            return { "message": "Map not found" }, 404


def getLeafTree(leaf: Leaf, level: int) -> str:
    mapId = leaf.mapId
    children = leaf.children

    indenting = 2 * "\t" * level
    tree = indenting + leaf.subPath

    if len(children) != 0:
        rootPath = leaf.path
        tree += "/"

        for childSubPath in children:
            childPath = f"{rootPath}/{childSubPath}"
            child = Leaf.findByMapAndPath(mapId, childPath)

            tree += "\n" + getLeafTree(child, level + 1)

    return tree
