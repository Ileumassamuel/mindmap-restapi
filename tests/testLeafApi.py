from urllib.parse import quote
import json
from flask.testing import FlaskClient
from flask import Response

from app import db
from app.models.mindmap import MindMap
from app.models.leaf import Leaf

from tests.utils.base import BaseTestCase


def getLeaf(client: FlaskClient, mapId: str, path: str) -> Response:
    return client.get(
        f"/api/v1/maps/{mapId}/leaves?path={quote(path)}",
        content_type="application/json"
    )

def putLeaf(client: FlaskClient, mapId: str, leaf) -> Response:
    return client.put(
        f"/api/v1/maps/{mapId}/leaves",
        json=leaf,
        content_type="application/json"
    )


class TestLeafBlueprint(BaseTestCase):
    mapId = "my-map"

    def setUp(self):
        super().setUp()
        map = MindMap(id=TestLeafBlueprint.mapId)
        db.session.add(map)
        db.session.commit()

    def testLeafGet(self):
        """ Test getting a leaf from the DB"""
        
        # Create a mock leaf
        path = "i"
        subPath = path
        text = "test text"
        leaf = Leaf(
            path=path, 
            subPath=subPath, 
            mapId=TestLeafBlueprint.mapId, 
            parent=None, 
            text=text
        )

        db.session.add(leaf)
        db.session.commit()

        leafResp = getLeaf(self.client, TestLeafBlueprint.mapId, path)
        leafData = json.loads(leafResp.data.decode())

        self.assertTrue(leafResp.status)
        self.assertEquals(leafResp.status_code, 200)
        self.assertEquals(leafData["path"], path)
        self.assertEquals(leafData["text"], text)

        # Test a 404 request
        leafResp404 = getLeaf(
            self.client, 
            mapId=TestLeafBlueprint.mapId,
            path="nonexistent"
        )
        self.assertEquals(leafResp404.status_code, 404)

    def testLeafPut(self):
        """ Test putting a leaf """

        # Create a mock leaf
        path = "i/like/potatoes"
        text = "because reasons"
        leaf = { "path": path, "text": text }

        leafResp = putLeaf(self.client, TestLeafBlueprint.mapId, leaf)
        leafData = json.loads(leafResp.data.decode())

        self.assertTrue(leafResp.status)
        self.assertEquals(leafResp.status_code, 200)

        foundLeaf = Leaf.findByMapAndPath(TestLeafBlueprint.mapId, path)

        self.assertIsNotNone(foundLeaf)
        self.assertEquals(foundLeaf.text, text)
