from enum import Enum


class Materials(Enum):
    GLASS = 'glass'
    GRANITE = 'granite'
    SANDSTONE = 'sandstone'
    STEEL = 'steel'
    OTHER = 'other'

    @classmethod
    def get_materials_list(cls):
        materials_list = []
        for material in cls:
            materials_list.append(material.value)
        return materials_list
