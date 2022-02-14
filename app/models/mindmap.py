from sqlalchemy.orm.collections import attribute_mapped_collection
from typing import List
from app import db

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

    # __table_args__ = (db.UniqueConstraint('mapId', 'path'),)
    uniqueConstraint = db.UniqueConstraint('mapId', 'path')


    def __init__(self, **kwargs):
        super(Leaf, self).__init__(**kwargs)

    def saveToDb(self) -> None:
        db.session.add(self)
        db.session.commit()

    def deleteFromDb(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def findById(cls, _id) -> "Leaf":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def findByMapAndPath(cls, mapId, path) -> "ItemModel":
        return cls.query.filter_by(mapId=mapId, path=path).first()

    @classmethod
    def filterByMap(cls, mapId) -> List["ItemModel"]:
        return cls.query.filter_by(mapId=mapId).all()

    @classmethod
    def getAll(cls) -> List["Leaf"]:
        return cls.query.all()

    def __repr__(self):
        return f"<Leaf of {self.mapId} at {self.path}>"
