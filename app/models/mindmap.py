from app import db

# Aliases
Column = db.Column
Model = db.Model
relationship = db.relationship


class Map(Model):
    __tablename__ = 'maps'

    id = Column(db.String(64), primary_key=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f"<Map {self.id}>"


class Leaf(Model):
    id = Column(db.Integer, primary_key=True)
    mapId = Column(db.String(64))

    path = Column(db.String(64))
    text = Column(db.Text)

    children = relationship("Child")
    parentId = Column(db.Integer, db.ForeignKey('parent.id'))

    def __init__(self, **kwargs):
        super(Leaf, self).__init__(**kwargs)
