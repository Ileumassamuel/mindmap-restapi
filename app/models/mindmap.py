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

    id = Column(db.Integer, primary_key=True)
    mapId = Column(db.String(64), db.ForeignKey('maps.id'), nullable=False)

    path = Column(db.String(64))
    text = Column(db.Text)

    def __init__(self, **kwargs):
        super(Leaf, self).__init__(**kwargs)
