from app import db
from app.models.mindmap import MindMap

from tests.utils.base import BaseTestCase


class TestMapModel(BaseTestCase):
    def testFindId(self):
        """ Test the findId classmethod """

        # Create mock map
        mapId = "my-map"
        map = MindMap(id=mapId)

        db.session.add(map)
        db.session.commit()

        foundMap = MindMap.findById(mapId)
        self.assertIsNotNone(foundMap)
