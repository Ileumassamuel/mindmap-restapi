import json
from flask.testing import FlaskClient
from flask import Response

from app import db
from app.models.mindmap import MindMap

from tests.utils.base import BaseTestCase


def getMap(client: FlaskClient, mapId: str) -> Response:
    return client.get(
        f"/api/v1/maps/{mapId}",
        content_type="application/json"
    )

def putMap(client: FlaskClient, map) -> Response:
    return client.put(
        f"/api/v1/maps",
        json=map,
        content_type="application/json"
    )


class TestMapBlueprint(BaseTestCase):
    def testMapGet(self):
        """ Test getting a map from the DB"""
        
        # Create a mock mind map
        mapId = "my-map"
        map = MindMap(id=mapId)

        db.session.add(map)
        db.session.commit()

        mapResp = getMap(self.client, mapId)
        mapData = json.loads(mapResp.data.decode())

        self.assertTrue(mapResp.status)
        self.assertEquals(mapResp.status_code, 200)
        self.assertEquals(mapData["id"], mapId)

        # Test a 404 request
        mapResp404 = getMap(self.client, "nonexistent")
        self.assertEquals(mapResp404.status_code, 404)

    def testMapPut(self):
        """ Test putting a map """

        mapId = "my-cool-map"
        map = { "id": mapId }

        mapResp = putMap(self.client, map)
        mapData = json.loads(mapResp.data.decode())

        self.assertTrue(mapResp.status)
        self.assertEquals(mapResp.status_code, 200)
        self.assertIsNotNone(MindMap.findById(mapId))
