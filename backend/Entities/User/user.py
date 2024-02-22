from typing import Dict, List, Optional

from openpyxl.worksheet.dimensions import Dimension

from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Entities.Building.building import Building
from backend.Entities.Building.cladding import Cladding
from backend.Entities.Building.height_zone import HeightZone
from backend.Entities.Building.roof import Roof
from backend.Entities.Location.location import Location
from backend.Entities.User.profile import Profile


class User:
    username: str
    profile: Optional[Profile]
    current_save_file: Optional[int]
    location: Optional[Location]
    dimensions: Optional[Dimension]
    cladding: Optional[Cladding]
    roof: Optional[Roof]
    num_floors: Optional[int]
    mid_height: Optional[float]
    material_load: Optional[Dict[int, float]]
    height_zones: Optional[List[HeightZone]]
    building: Optional[Building]
    importance_category: Optional[ImportanceFactor]

    def __init__(self, username: str):
        self.username = username
        self.profile = None
        self.current_save_file = None
        self.location = None
        self.dimensions = None
        self.cladding = None
        self.roof = None
        self.num_floors = None
        self.mid_height = None
        self.material_load = None
        self.height_zones = None
        self.building = None
        self.importance_category = None

    def set_profile(self, profile: Profile):
        self.profile = profile

    def set_current_save_file(self, current_save_file: int):
        self.current_save_file = current_save_file

    def set_location(self, location: Location):
        self.location = location

    def set_dimensions(self, dimensions: Dimension):
        self.dimensions = dimensions

    def set_cladding(self, cladding: Cladding):
        self.cladding = cladding

    def set_roof(self, roof: Roof):
        self.roof = roof

    def set_num_floors(self, num_floors: int):
        self.num_floors = num_floors

    def set_mid_height(self, mid_height: float):
        self.mid_height = mid_height

    def set_material_load(self, material_load: Dict[int, float]):
        self.material_load = material_load

    def set_height_zones(self, height_zones: List[HeightZone]):
        self.height_zones = height_zones

    def set_building(self, building: Building):
        self.building = building

    def set_importance_category(self, importance_category: ImportanceFactor):
        self.importance_category = importance_category

    def get_username(self):
        return self.username

    def get_profile(self):
        return self.profile

    def get_current_save_file(self):
        return self.current_save_file

    def get_location(self):
        return self.location

    def get_dimensions(self):
        return self.dimensions

    def get_cladding(self):
        return self.cladding

    def get_roof(self):
        return self.roof

    def get_num_floors(self):
        return self.num_floors

    def get_mid_height(self):
        return self.mid_height

    def get_material_load(self):
        return self.material_load

    def get_height_zones(self):
        return self.height_zones

    def get_building(self):
        return self.building

    def get_importance_category(self):
        return self.importance_category
