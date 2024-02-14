from backend.Entities.User.user import User

ALL_USER_DATA = dict()

def check_user_exists(username):
    if not ALL_USER_DATA.get(username):
        ALL_USER_DATA[username] = User(username)

def set_user_data(username, user_data):
    ALL_USER_DATA[username] = user_data


def set_user_profile(username, profile):
    ALL_USER_DATA[username].set_profile(profile)


def set_user_location(username, location):
    ALL_USER_DATA[username].set_location(location)


def set_user_building(username, building):
    ALL_USER_DATA[username].set_building(building)


def get_user_data(username):
    return ALL_USER_DATA.get(username)


def get_user_profile(username):
    return ALL_USER_DATA.get(username).get_profile()


def get_user_location(username):
    return ALL_USER_DATA.get(username).get_location()


def get_user_building(username):
    return ALL_USER_DATA.get(username).get_building()
