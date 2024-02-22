from datetime import datetime

import jsonpickle
from sqlalchemy import select, desc
from sqlalchemy.orm import sessionmaker

from backend.Entities.User.user import User
from database.Constants.connection_constants import PrivilegeType
from database.Entities.database_connection import DatabaseConnection
from database.Entities.save_data import SaveData
from database.Population.populate_save_data import DATABASE

ALL_USER_DATA = dict()


def check_user_exists(username):
    if not ALL_USER_DATA.get(username):
        ALL_USER_DATA[username] = User(username)


def set_user_data(username, user_data):
    ALL_USER_DATA[username] = user_data


def set_user_profile(username, profile):
    ALL_USER_DATA[username].set_profile(profile)


def set_user_current_save_file(username, current_save_file):
    ALL_USER_DATA[username].set_current_save_file(current_save_file)


def set_user_location(username, location):
    ALL_USER_DATA[username].set_location(location)


def set_user_dimensions(username, dimensions):
    ALL_USER_DATA[username].set_dimensions(dimensions)


def set_user_cladding(username, cladding):
    ALL_USER_DATA[username].set_cladding(cladding)


def set_user_roof(username, roof):
    ALL_USER_DATA[username].set_roof(roof)


def set_user_num_floors(username, num_floors):
    ALL_USER_DATA[username].set_num_floors(num_floors)


def set_user_mid_height(username, mid_height):
    ALL_USER_DATA[username].set_mid_height(mid_height)


def set_user_material_load(username, material_load):
    ALL_USER_DATA[username].set_material_load(material_load)


def set_user_height_zones(username, height_zones):
    ALL_USER_DATA[username].set_height_zones(height_zones)


def set_user_building(username, building):
    ALL_USER_DATA[username].set_building(building)


def set_user_importance_category(username, importance_category):
    ALL_USER_DATA[username].set_importance_category(importance_category)


def set_user_save_data(username: str, json_data: str, id: int = None):
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = Session()

    existing_entry = None
    if id is not None:
        existing_entry = controller.query(SaveData).filter((SaveData.Username == username) & (SaveData.ID == id)).first()

    if existing_entry is not None:
        # modify existing entry, by overriding JsonData and DateModified to use current time
        existing_entry.JsonData = json_data
        existing_entry.DateModified = datetime.now()
    else:
        # create new entry with the current time
        new_entry = SaveData(Username=username, DateModified=datetime.now(), JsonData=json_data)
        controller.add(new_entry)
        controller.commit()
        id = new_entry.ID

    controller.commit()
    controller.close()
    new_connection.close()

    return id



def get_user_profile(username):
    return ALL_USER_DATA.get(username).get_profile()


def get_user_current_save_file(username):
    return ALL_USER_DATA.get(username).get_current_save_file()


def get_user_location(username):
    return ALL_USER_DATA.get(username).get_location()


def get_user_dimensions(username):
    return ALL_USER_DATA.get(username).get_dimensions()


def get_user_cladding(username):
    return ALL_USER_DATA.get(username).get_cladding()


def get_user_roof(username):
    return ALL_USER_DATA.get(username).get_roof()


def get_user_num_floors(username):
    return ALL_USER_DATA.get(username).get_num_floors()


def get_user_mid_height(username):
    return ALL_USER_DATA.get(username).get_mid_height()


def get_user_material_load(username):
    return ALL_USER_DATA.get(username).get_material_load()


def get_user_height_zones(username):
    return ALL_USER_DATA.get(username).get_height_zones()


def get_user_building(username):
    return ALL_USER_DATA.get(username).get_building()


def get_user_importance_category(username):
    return ALL_USER_DATA.get(username).get_importance_category()


def get_user_data(username):
    return jsonpickle.encode(ALL_USER_DATA.get(username), indent=4)


def get_all_user_save_data(username):
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    result = controller.query(SaveData).filter(SaveData.Username == username).order_by(desc(SaveData.DateModified)).all()
    controller.close()
    new_connection.close()
    return result


def get_user_save_file(username: str, id: int):
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    result = controller.query(SaveData).filter((SaveData.Username == username) & (SaveData.ID == id)).first()
    controller.close()
    new_connection.close()
    return result
