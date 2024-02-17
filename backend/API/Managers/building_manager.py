from typing import List, Tuple, Optional

from backend.API.Managers.user_data_manager import get_user_dimensions, get_user_cladding, get_user_roof
from backend.Entities.Building.building import BuildingDefaultHeightDefaultMaterialBuilder, \
    BuildingCustomHeightDefaultMaterialBuilder
from backend.Entities.Building.height_zone import HeightZone


def process_building_data(num_floor: int, h_opening: float, zones: List[Tuple[int, float, float]], username):
    if h_opening is None:
        h_opening = 0
    dimensions = get_user_dimensions(username)
    cladding = get_user_cladding(username)
    roof = get_user_roof(username)
    height_zones = [HeightZone(zone_num=x[0], elevation=x[1]) for x in zones]
    material_load = [x[2] for x in zones]

    # Case default height zones and simple material load
    if height_zones is None and isinstance(material_load, (list, float)):
        building_builder = BuildingDefaultHeightDefaultMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.set_num_floor(num_floor)
        building_builder.set_h_opening(h_opening)
        building_builder.generate_height_zones()
        building_builder.set_material_load(material_load)
        return building_builder.get_building()
    # Case custom height zones and simple material load
    elif height_zones is not None and isinstance(material_load, (list, float)):
        building_builder = BuildingCustomHeightDefaultMaterialBuilder()
        building_builder.set_dimensions(dimensions)
        building_builder.set_cladding(cladding)
        building_builder.set_roof(roof)
        building_builder.set_num_floor(num_floor)
        building_builder.set_h_opening(h_opening)
        building_builder.generate_height_zones(height_zones)
        building_builder.set_material_load(material_load)
        return building_builder.get_building()
    else:
        raise NotImplementedError