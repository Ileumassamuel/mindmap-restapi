from app import db
from app.models.mindmap import MindMap
from app.models.leaf import Leaf

from tests.utils.base import BaseTestCase


class TestLeafBlueprint(BaseTestCase):
    mapId = "my-map"

    def setUp(self):
        super().setUp()
        map = MindMap(id=TestLeafBlueprint.mapId)
        db.session.add(map)
        db.session.commit()


    def testFindByMapAndPath(self):
        """ Test the findByMapAndPath classmethod """

        # Create a mock leaf
        path = 'i'

        leaf = Leaf(
            path=path, 
            subPath='i', 
            mapId=TestLeafBlueprint.mapId, 
            parent=None, 
            text='cool'
        )
        
        db.session.add(leaf)
        db.session.commit()

        foundMap = Leaf.findByMapAndPath(TestLeafBlueprint.mapId, path)
        self.assertEquals(leaf.id, foundMap.id)

    def testSaveToDb(self):
        """ Test the saveToDb classmethod """

        path = 'i'

        leaf = Leaf(
            path=path, 
            subPath='i', 
            mapId=TestLeafBlueprint.mapId, 
            parent=None, 
            text='cool'
        )

        leaf.saveToDb()

        foundMap = Leaf.query.filter_by(mapId=TestLeafBlueprint.mapId, path=path).first()
        self.assertEquals(foundMap.id, leaf.id)

    def testFindDeepestLeaf(self):
        """ Test the findDeepestLeaf staticmethod """

        # Create mock leaves
        leaf1 = Leaf(
            path='i', 
            subPath='i', 
            mapId=TestLeafBlueprint.mapId, 
            parent=None, 
            text='cool'
        )

        leaf2 = Leaf(
            path='i/like', 
            subPath='like', 
            mapId=TestLeafBlueprint.mapId, 
            parent=leaf1, 
            text='stuff'
        )

        db.session.add(leaf1)
        db.session.commit()

        deepestLeaf = Leaf.findDeepestLeaf(TestLeafBlueprint.mapId, "i/like/potatoes")
        self.assertEquals(deepestLeaf.id, leaf2.id)
