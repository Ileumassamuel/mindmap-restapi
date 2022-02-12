from app import marshmellow

from .mindmap import Leaf, MindMap

class MindMapSchema(marshmellow.SQLAlchemyAutoSchema):
    class Meta:
        model = MindMap
        load_instance = True
