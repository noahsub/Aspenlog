from backend.Entities.Building.building import Building
from backend.Entities.Location.location import Location
from backend.Entities.User.profile import Profile


class User:
    username: str
    profile: Profile
    location: Location
    building: Building

    def __init__(self, username: str):
        self.username = username

    def set_profile(self, profile: Profile):
        self.profile = profile

    def set_location(self, location: Location):
        self.location = location

    def set_building(self, building: Building):
        self.building = building

    def get_username(self):
        return self.username

    def get_profile(self):
        return self.profile

    def get_location(self):
        return self.location

    def get_building(self):
        return self.building

