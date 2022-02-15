from app import marshmellow

from .mindmap import MindMap
from .leaf import Leaf


class MindMapSchema(marshmellow.SQLAlchemySchema):
    class Meta:
        model = MindMap
        load_instance = True

    id = marshmellow.auto_field()
    leaves = marshmellow.auto_field()


class LeafSchema(marshmellow.SQLAlchemyAutoSchema):
    class Meta:
        model = Leaf
        load_instance = True
        include_fk = True
