from sqlalchemy.orm.collections import attribute_mapped_collection
from typing import List
from app import db
from .mindmap import MindMap

# Aliases
Column = db.Column
Model = db.Model
relationship = db.relationship


class Leaf(Model):
    __tablename__ = 'leaves'

    id = Column(db.Integer(), primary_key=True, nullable=False)
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
                currentPath = subPaths.pop(0)
                rootLeaf = Leaf(mapId=_mapId, path=currentPath, subPath=currentPath, parent=None)
                currentParent = rootLeaf

            for _subPath in subPaths:
                if _subPath != "":
                    currentPath = (currentPath + "/" + _subPath)
                    newLeaf = Leaf(mapId=_mapId, path=currentPath, subPath=_subPath, parent=currentParent)
                    currentParent = newLeaf

            currentParent.text = _text

            if deepestLeaf == None:
                rootLeaf.saveToDb()
            else:
                db.session.merge(rootLeaf)
                db.session.commit()

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
        subPaths = normalizedPath.split('/')
        rootPath = subPaths.pop(0)
        previousLeaf = Leaf.findByMapAndPath(_mapId, rootPath)

        for _subPath in subPaths:
            currentLeaf = previousLeaf.children.get(_subPath, None) if previousLeaf != None else None

            if currentLeaf == None:
                break

            previousLeaf = currentLeaf

        return previousLeaf

    @classmethod
    def findById(cls, _id) -> "Leaf":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def findByMapAndPath(cls, _mapId, _path) -> "Leaf":
        return cls.query.filter_by(mapId=_mapId, path=_path).first()

    @classmethod
    def filterByMap(cls, _mapId) -> List["Leaf"]:
        return cls.query.filter_by(mapId=_mapId).all()

    @classmethod
    def filterRootNodesByMap(cls, _mapId) -> List["Leaf"]:
        return cls.query.filter(Leaf.path == Leaf.subPath, Leaf.mapId == _mapId).all()

    @classmethod
    def getAll(cls) -> List["Leaf"]:
        return cls.query.all()

    def __repr__(self):
        return f"<Leaf of {self.mapId} at {self.path}>"
