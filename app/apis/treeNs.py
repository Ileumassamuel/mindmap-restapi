from flask_restx import Namespace, Resource, fields
from app.models.mindmap import Leaf

ns = Namespace('tree', description='Tree related operations')

@ns.route("/<string:mapId>")
class Tree(Resource):
    @ns.produces(["text/plain"])
    @ns.doc("Get a map's tree")
    def get(self, mapId):
        """ Get a specific mind map's tree """
        leaves = Leaf.filterRootNodesByMap(mapId)
        tree = """root/
        some

        cool

        stuff

        """
        response.headers.set("Content-Type", "text/plain")

        level = 0

        # for leaf in leaves:
        #     tree += "\n" + getChildrenTree(leaf)

        return tree

def getChildrenTree(leaf: Leaf) -> str:
    children = leaf.children

    subTree = leaf.subPath

    return subTree
