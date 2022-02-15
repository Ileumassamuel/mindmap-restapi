from sqlalchemy.orm.collections import attribute_mapped_collection
from typing import List
from app import db
from app.utils import generateLeadingPaths

# Aliases
Column = db.Column
Model = db.Model
relationship = db.relationship


class MindMap(Model):
    __tablename__ = 'maps'

    id = Column(db.String(64), primary_key=True, nullable=False)

    def __init__(self, **kwargs):
        super(MindMap, self).__init__(**kwargs)

    def saveToDb(self) -> None:
        db.session.add(self)
        db.session.commit()

    def deleteFromDb(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findById(cls, _id) -> "MindMap":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def getAll(cls) -> List["MindMap"]:
        return cls.query.all()

    def __repr__(self):
        return f"<Mind map {self.id}>"


class Leaf(Model):
    __tablename__ = 'leaves'

    id = Column(db.Integer(), primary_key=True)
    mapId = Column(db.String(64), db.ForeignKey('maps.id'), nullable=False)

    path = Column(db.String(64), nullable=False)
    subPath = Column(db.String(50), nullable=False)

    text = Column(db.Text())

    parentId = Column(db.Integer(), db.ForeignKey('leaves.id'))
    children = relationship(
            "Leaf",
            # cascade deletions
            cascade="all, delete-orphan",
            backref=db.backref('parent', remote_side=[id]),
            collection_class=attribute_mapped_collection("subPath")
        )

    mindmap = db.relationship("MindMap", backref="leaves")
    uniqueConstraint = db.UniqueConstraint('mapId', 'path')

    def __init__(self, **kwargs):
        super(Leaf, self).__init__(**kwargs)

    def saveToDb(self) -> None:
        db.session.add(self)
        db.session.commit()

    def deleteFromDb(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def createOrUpdateLeaf(_mapId, _path, _text):
        """Creates a leaf on a given map

        Args:
            _mapId (str): The map's identifier
            _path (str): The leaf's path
            _text (str): The leaf's text

        Returns:
            - The created/Updated leaf if the map exists
            - None otherwise.
        """
        foundMindMap = MindMap.findById(_mapId)

        if foundMindMap != None:
            deepestLeaf = Leaf.findDeepestLeaf(_mapId, _path)

            currentPath = deepestLeaf.path if deepestLeaf != None else ""
            pathDiff = _path.removeprefix(currentPath).strip('/')
            subPaths = pathDiff.split('/')

            rootLeaf = deepestLeaf
            currentParent = rootLeaf

            if deepestLeaf == None:
                rootPath = subPaths.pop(0)
                rootLeaf = Leaf(mapId=_mapId, path=currentPath, subPath=rootPath, parent=None)
                currentParent = rootLeaf

            for subPath in subPaths:
                currentPath = (currentPath + "/" + subPath)
                newLeaf = Leaf(mapId=_mapId, path=currentPath, subPath=subPath, parent=currentParent)
                currentParent = newLeaf

            currentParent.text = _text

            rootLeaf.saveToDb()
            return currentParent

        return None

    @staticmethod
    def findDeepestLeaf(_mapId, _path) -> "Leaf":
        """Find the deepest existing leaf in a map given a path

        Args:
            _mapId (str): The identifier of the given map
            _path (str): The path on the given map

        Returns:
            The deepest existing leaf of the given path or None if there are no
            leaves on the path.
        """
        normalizedPath = _path.strip('/')
        previousLeaf = None

        for leadingPath in generateLeadingPaths(normalizedPath):
            currentLeaf = Leaf.findByMapAndPath(_mapId, leadingPath)

            # The root leaf does not exist
            if previousLeaf == None and currentLeaf == None:
                return None
            # There is a deepest leaf
            elif previousLeaf != None and currentLeaf == None:
                return previousLeaf
            # The deepest leaf is the last in the path
            elif currentLeaf == normalizedPath:
                return currentLeaf

            previousLeaf = currentLeaf

    @classmethod
    def findById(cls, _id) -> "Leaf":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def findByMapAndPath(cls, _mapId, _path) -> "ItemModel":
        return cls.query.filter_by(mapId=_mapId, path=_path).first()

    @classmethod
    def filterByMap(cls, _mapId) -> List["ItemModel"]:
        return cls.query.filter_by(mapId=_mapId).all()

    @classmethod
    def getAll(cls) -> List["Leaf"]:
        return cls.query.all()

    def __repr__(self):
        return f"<Leaf of {self.mapId} at {self.path}>"
