########################################################################################################################
# user_data_manager.py
# This file manages the user data for the application.
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

from datetime import datetime

import jsonpickle
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker

from backend.Constants.importance_factor_constants import ImportanceFactor
from backend.Entities.Building.building import Building
from backend.Entities.Building.cladding import Cladding
from backend.Entities.Building.dimensions import Dimensions
from backend.Entities.Building.roof import Roof
from backend.Entities.Location.location import Location
from backend.Entities.User.profile import Profile
from backend.Entities.User.user import User
from database.Constants.connection_constants import PrivilegeType
from database.Entities.database_connection import DatabaseConnection
from database.Entities.save_data import SaveData

########################################################################################################################
# GLOBALS
########################################################################################################################

# This dictionary stores all data across all users
ALL_USER_DATA = dict()


########################################################################################################################
# MANAGER
########################################################################################################################

def check_user_exists(username: str) -> None:
    """
    Checks if a user exists in the ALL_USER_DATA dictionary. If not, creates a new user object for the user.
    :param username: The username of the user
    :return: None
    """
    # If the user does not exist in the dictionary, create a new user object for the user
    if not ALL_USER_DATA.get(username):
        ALL_USER_DATA[username] = User(username)


def set_user_data(username: str, user_data: User) -> None:
    """
    Sets the user data in memory
    :param username: The username of the user
    :param user_data: The user data
    :return: None
    """
    # Set the user data in memory
    ALL_USER_DATA[username] = user_data


def set_user_profile(username: str, profile: Profile) -> None:
    """
    Sets the user profile in memory
    :param username: The username of the user
    :param profile: The user profile
    :return: None
    """
    # Set the user profile in memory
    ALL_USER_DATA[username].set_profile(profile)


def set_user_current_save_file(username: str, current_save_file: int) -> None:
    """
    Sets the current save file for the user
    :param username: The username of the user
    :param current_save_file: The id of the current save file
    :return: None
    """
    # Set the id of the current save file for the user
    ALL_USER_DATA[username].set_current_save_file(current_save_file)


def set_user_location(username: str, location: Location) -> None:
    """
    Sets the location for the user
    :param username: The username of the user
    :param location: The location object
    :return: None
    """
    # Set the location for the user
    ALL_USER_DATA[username].set_location(location)


def set_user_dimensions(username: str, dimensions: Dimensions) -> None:
    """
    Sets the dimensions for the user
    :param username: The username of the user
    :param dimensions: The dimensions object
    :return: The dimensions object
    """
    # Set the dimensions for the user
    ALL_USER_DATA[username].set_dimensions(dimensions)


def set_user_cladding(username: str, cladding: Cladding) -> None:
    """
    Sets the cladding for the user
    :param username: The username of the user
    :param cladding: The cladding object
    :return: The cladding object
    """
    ALL_USER_DATA[username].set_cladding(cladding)


def set_user_roof(username: str, roof: Roof) -> None:
    """
    Sets the roof for the user
    :param username: The username of the user
    :param roof: The roof object
    :return: None
    """
    ALL_USER_DATA[username].set_roof(roof)


def set_user_num_floors(username: str, num_floors: int) -> None:
    """
    Sets the number of floors for the user
    :param username: The username of the user
    :param num_floors: The number of floors
    :return: None
    """
    ALL_USER_DATA[username].set_num_floors(num_floors)


def set_user_mid_height(username: str, mid_height: float) -> None:
    """
    Sets the mid height for the user
    :param username: The username of the user
    :param mid_height: The mid height
    :return: None
    """
    ALL_USER_DATA[username].set_mid_height(mid_height)


def set_user_material_load(username: str, material_load) -> None:
    """
    Sets the material load for the user
    :param username: The username of the user
    :param material_load: The material load
    :return: None
    """
    ALL_USER_DATA[username].set_material_load(material_load)


def set_user_height_zones(username: str, height_zones) -> None:
    """
    Sets the height zones for the user
    :param username: The username of the user
    :param height_zones: The height zones
    :return:
    """
    ALL_USER_DATA[username].set_height_zones(height_zones)


def set_user_building(username: str, building: Building) -> None:
    """
    Sets the building for the user
    :param username: The username of the user
    :param building: The building object
    :return: None
    """
    ALL_USER_DATA[username].set_building(building)


def set_user_importance_category(username: str, importance_category: ImportanceFactor) -> None:
    """
    Sets the importance category for the user
    :param username: The username of the user
    :param importance_category: The importance category
    :return: None
    """
    ALL_USER_DATA[username].set_importance_category(importance_category)


def set_user_snow_load(username: str, snow_load) -> None:
    """
    Sets the snow load for the user
    :param username: The username of the user
    :param snow_load: The snow load
    :return: None
    """
    ALL_USER_DATA[username].set_snow_load(snow_load)


def set_user_save_data(username: str, json_data: str, id: int = None) -> int:
    """
    Sets the save data for the user
    :param username: The username of the user
    :param json_data: The JSON data to save
    :param id: The id of the save file
    :return: The id of the save file
    """
    # Connect to the database
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = Session()

    # Check if the entry already exists
    existing_entry = None
    # If an id is provided, check if the entry exists
    if id is not None:
        existing_entry = controller.query(SaveData).filter(
            (SaveData.Username == username) & (SaveData.ID == id)).first()

    # If the entry exists, modify it. Otherwise, create a new entry
    if existing_entry is not None:
        # modify existing entry, by overriding JsonData and DateModified to use current time
        prev_data = jsonpickle.decode(existing_entry.JsonData)
        for key, value in jsonpickle.decode(json_data).items():
            prev_data[key] = value

        existing_entry.JsonData = jsonpickle.encode(prev_data)
        existing_entry.DateModified = datetime.now()
    # Create new entry with the current time
    else:
        new_entry = SaveData(Username=username, DateModified=datetime.now(), JsonData=json_data)
        controller.add(new_entry)
        controller.commit()
        id = new_entry.ID

    # Commit and close the connection
    controller.commit()
    controller.close()
    new_connection.close()

    # Return the id of the save file
    return id


def get_user_profile(username: str) -> Profile:
    """
    Gets the profile for the user
    :param username: The username of the user
    :return: The profile object
    """
    return ALL_USER_DATA.get(username).get_profile()


def get_user_current_save_file(username: str) -> int:
    """
    Gets the current save file for the user
    :param username: The username of the user
    :return:
    """
    return ALL_USER_DATA.get(username).get_current_save_file()


def get_user_location(username: str) -> Location:
    """
    Gets the location for the user
    :param username: The username of the user
    :return: The location object
    """
    return ALL_USER_DATA.get(username).get_location()


def get_user_dimensions(username: str) -> Dimensions:
    """
    Gets the dimensions for the user
    :param username: The username of the user
    :return: The dimensions object
    """
    return ALL_USER_DATA.get(username).get_dimensions()


def get_user_cladding(username: str) -> Cladding:
    """
    Gets the cladding for the user
    :param username: The username of the user
    :return: The cladding object
    """
    return ALL_USER_DATA.get(username).get_cladding()


def get_user_roof(username: str) -> Roof:
    """
    Gets the roof for the user
    :param username: The username of the user
    :return: The roof object
    """
    return ALL_USER_DATA.get(username).get_roof()


def get_user_num_floors(username: str) -> int:
    """
    Gets the number of floors for the user
    :param username: The username of the user
    :return: The number of floors
    """
    return ALL_USER_DATA.get(username).get_num_floors()


def get_user_mid_height(username: str):
    """
    Gets the mid height for the user
    :param username: The username of the user
    :return: The mid height
    """
    return ALL_USER_DATA.get(username).get_mid_height()


def get_user_material_load(username: str):
    """
    Gets the material load for the user
    :param username: The username of the user
    :return:The material load
    """
    return ALL_USER_DATA.get(username).get_material_load()


def get_user_height_zones(username: str):
    """
    Gets the height zones for the user
    :param username: The username of the user
    :return:The height zones
    """
    return ALL_USER_DATA.get(username).get_height_zones()


def get_user_building(username: str) -> Building:
    """
    Gets the building for the user
    :param username: The username of the user
    :return: The building object
    """
    return ALL_USER_DATA.get(username).get_building()


def get_user_importance_category(username: str):
    """
    Gets the importance category for the user
    :param username: The username of the user
    :return: The importance category
    """
    return ALL_USER_DATA.get(username).get_importance_category()


def get_user_snow_load(username: str):
    """
    Gets the snow load for the user
    :param username: The username of the user
    :return: The snow load
    """
    return ALL_USER_DATA.get(username).get_snow_load()


def get_user_data(username: str):
    """
    Gets the user data for the user
    :param username: The username of the user
    :return: A JSON representation of the user data
    """
    return jsonpickle.encode(ALL_USER_DATA.get(username), indent=4)


def get_all_user_save_data(username: str):
    """
    Gets all the save data for the user
    :param username: The username of the user
    :return: The save data for the user
    """
    # Connect to the database
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    # Get all the save data for the user
    result = controller.query(SaveData).filter(SaveData.Username == username).order_by(
        desc(SaveData.DateModified)).all()
    # Close the connection
    controller.close()
    new_connection.close()
    # Return the save data
    return result


def get_user_save_file(username: str, id: int):
    """
    Gets the save file for the user
    :param username: The username of the user
    :param id: The id of the save file
    :return: The save file with the given id
    """
    # Connect to the database
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    # Get the save file with the given id
    result = controller.query(SaveData).filter((SaveData.Username == username) & (SaveData.ID == id)).first()
    # Close the connection
    controller.close()
    new_connection.close()
    # Return the save file
    return result


def delete_user_save_file(username: str, id: int):
    """
    Deletes the save file for the user
    :param username: The username of the user
    :param id: The id of the save file
    :return: None
    """
    # Connect to the database
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    # Get the save file with the given id
    result = controller.query(SaveData).filter((SaveData.Username == username) & (SaveData.ID == id)).first()
    # Delete the save file
    controller.delete(result)
    # Commit and close the connection
    controller.commit()
    controller.close()
    new_connection.close()


def get_user_save_file_json(username: str, id: int):
    """
    Gets the JSON data for the save file with the given id
    :param username: The username of the user
    :param id: The id of the save file
    :return: The JSON data for the save file
    """
    save_file = get_user_save_file(username, id)
    return save_file.JsonData
