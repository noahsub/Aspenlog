########################################################################################################################
# populate_climate_data.py
# This file contains the code for populating the ClimaticData table
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import ast
import csv
import uuid
from tqdm import tqdm
from geopy.extra.rate_limiter import RateLimiter
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from config import get_file_path
from database.Constants.connection_constants import PrivilegeType
from database.Entities.climatic_data import BASE, ClimaticData
from database.Entities.database_connection import DatabaseConnection
from database.Warnings.database_warnings import already_exists_warning
from geopy.geocoders import Nominatim

########################################################################################################################
# GLOBALS
########################################################################################################################

# The database connection
DATABASE = DatabaseConnection(database_name="NBCC-2020")


########################################################################################################################
# DATABASE FUNCTIONS
########################################################################################################################

def create_climatic_data_table():
    """
    Creates the ClimaticData table
    :return: None
    """
    # Get the engine
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)

    # Name of the table
    table_name = 'ClimaticData'
    inspector = inspect(engine)
    # If the table already exists, we don't want to create it again
    if table_name in inspector.get_table_names():
        already_exists_warning(item=table_name, database_name=DATABASE.database_name)
        return

    # Otherwise, we create the table
    else:
        BASE.metadata.bind = engine
        BASE.metadata.create_all(bind=engine)


def clean_climatic_data_table():
    """
    Cleans the ClimaticData table
    :return: None
    """
    # Get the connection and cursor
    connection = DATABASE.get_connection(privilege=PrivilegeType.ADMIN)
    cursor = DATABASE.get_cursor(connection)
    # Delete all entries in the table
    cursor.execute('DELETE FROM "ClimaticData";')
    # Reset the ID sequence
    cursor.execute('ALTER SEQUENCE "ClimaticData_ID_seq" RESTART WITH 1;')
    # Commit the changes
    connection.commit()


########################################################################################################################
# POPULATION FUNCTIONS
########################################################################################################################

def populate_climatic_data_table():
    """
    Populates the ClimaticData table
    :return: None
    """
    # Get the engine and controller
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    # get the path to the data-extraction/output/table_c2.csv file
    file_path = get_file_path("data-extraction/output/table_c2.csv")
    # read the file
    with open(file_path, 'r') as csv_file:
        # Skip first 3 lines, these are header lines and not data
        for _ in range(3):
            next(csv_file)

        # read data-extraction/output/table_c2.csv file
        csv_reader = csv.reader(csv_file)

        # map column names to appropriate column index
        for row in tqdm(csv_reader, "Populating Climatic Data"):
            column_mapping = {
                'ProvinceAndLocation': 1,
                'Elev_m': 2,
                'Jan_2_5_percent_C': 3,
                'Jan_1_percent_C': 4,
                'July_Dry_C': 5,
                'July_Wet_C': 6,
                'DegreeDaysBelow18C': 7,
                'Rain_15_Min_mm': 8,
                'OneDayRain_1_50_mm': 9,
                'Ann_Rain_mm': 10,
                'MoistIndex': 11,
                'Ann_Tot_Ppn_mm': 12,
                'DrivingRainWindPressures_Pa_1_5': 13,
                'SnowLoad_kPa_1_50_Ss': 14,
                'SnowLoad_kPa_1_50_Sr': 15,
                'HourlyWindPressures_kPa_1_10': 16,
                'HourlyWindPressures_kPa_1_50': 17
            }

            # store the data of the entry in a dictionary
            entry_data = {}
            # go through each column and set value
            for column in column_mapping:
                # the only column that should be a string
                if column == 'ProvinceAndLocation':
                    entry_data[column] = row[column_mapping[column]]
                # if an empty string is found as a value, we set that value to null in the database
                elif row[column_mapping[column]] == '':
                    entry_data[column] = None
                # otherwise, we use an abstract syntax tree to parse the value appropriately
                else:
                    entry_data[column] = ast.literal_eval(row[column_mapping[column]])

            # unpack entry_data to create a ClimaticData object
            entry = ClimaticData(**entry_data, Latitude=0, Longitude=0)
            # prepare the entry to be added to the database
            controller.add(entry)
        # add all entries to the database
        controller.commit()


def update_location():
    """
    Updates the location of each entry in the ClimaticData table
    :return: None
    """
    # Get the engine and controller
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    # Create a geolocator and geocode rate limiter
    geolocator = Nominatim(user_agent=str(uuid.uuid4()).replace('-', ''))
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    # For each entry in the ClimaticData table
    for entry in tqdm(controller.query(ClimaticData).all(), desc="Updating Locations"):
        # Get the location information
        location = entry.ProvinceAndLocation
        location_info = geocode(location, timeout=10)

        # If the location information is None, we set the latitude and longitude to None
        if location_info is None:
            entry.Latitude = None
            entry.Longitude = None
        # Otherwise, we set the latitude and longitude to the location information
        else:
            entry.Latitude = location_info.latitude
            entry.Longitude = location_info.longitude

    # Commit the changes
    controller.commit()


########################################################################################################################
# MAIN
########################################################################################################################


# ONLY RUN IF DATABASE NEEDS TO BE REPOPULATED
if __name__ == "__main__":
    print("WARNING: This script will populate the ClimaticData table. If the database is already populated, this will delete existing data and repopulate the table, meaning any manual changes will be lost.")
    choice = input("Are you sure you want to continue? (y/n): ")
    if choice.lower() == 'y':
        create_climatic_data_table()
        clean_climatic_data_table()
        populate_climatic_data_table()
        update_location()
        DATABASE.close()
    else:
        exit(0)
