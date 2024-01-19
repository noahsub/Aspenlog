########################################################################################################################
# populate_wind_speed_data.py
# This file contains the code for populating the WindSpeedData table
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import csv
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
from config import get_file_path
from database.Constants.connection_constants import PrivilegeType
from database.Entities.database_connection import DatabaseConnection
from database.Entities.wind_speed_data import BASE, WindSpeedData
from database.Warnings.database_warnings import already_exists_warning


########################################################################################################################
# GLOBALS
########################################################################################################################

# The database connection
DATABASE = DatabaseConnection(database_name="NBCC-2020")


########################################################################################################################
# DATABASE FUNCTIONS
########################################################################################################################

def create_wind_speed_data_table():
    """
    Creates the WindSpeedData table
    :return: None
    """
    # Get the engine
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)

    # Name of the table
    table_name = 'WindSpeedData'
    inspector = inspect(engine)
    # If the table already exists, we don't want to create it again
    if table_name in inspector.get_table_names():
        already_exists_warning(item=table_name, database_name=DATABASE.database_name)
        return
    # Otherwise, we create the table
    else:
        BASE.metadata.bind = engine
        BASE.metadata.create_all(bind=engine)


def clean_wind_speed_data_table():
    """
    Cleans the WindSpeedData table
    :return: None
    """
    # Get the connection and cursor
    connection = DATABASE.get_connection(privilege=PrivilegeType.ADMIN)
    cursor = DATABASE.get_cursor(connection)
    # Delete all entries in the table
    cursor.execute('DELETE FROM "WindSpeedData";')
    # Reset the ID sequence
    cursor.execute('ALTER SEQUENCE "WindSpeedData_ID_seq" RESTART WITH 1;')
    # Commit the changes
    connection.commit()


########################################################################################################################
# POPULATION FUNCTIONS
########################################################################################################################

def populate_wind_speed_data_table():
    """
    Populates the WindSpeedData table
    :return: None
    """
    # Get the engine and controller
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    # Open the data-extraction/output/table_c1.csv file
    file_path = get_file_path("data-extraction/output/table_c1.csv")
    # Read the file
    with open(file_path, 'r') as csv_file:
        # Skip first 3 lines, these are header lines and not data
        for _ in range(2):
            next(csv_file)

        # read data-extraction/output/table_c1.csv file
        csv_reader = csv.reader(csv_file)

        # Iterate through each row of the csv file
        for row in tqdm(csv_reader, "Populating Wind Speed Data"):
            # Each row of the csv file contains 4 entries, hence we need to split the row into groups of two columns
            for i in range(1, 9, 2):
                entry = WindSpeedData(q_KPa=float(row[i]), V_ms=float(row[i+1]))
                # Add the entry to the controller
                controller.add(entry)
        # Commit the changes
        controller.commit()

# ONLY RUN IF DATABASE NEEDS TO BE REPOPULATED
if __name__ == '__main__':
    print("WARNING: This script will repopulate the WindSpeedData table. If the database is already populated, this will delete existing data and repopulate the table, meaning any manual changes will be lost.")
    choice = input("Are you sure you want to continue? (y/n): ")
    if choice.lower() == 'y':
        create_wind_speed_data_table()
        clean_wind_speed_data_table()
        populate_wind_speed_data_table()
        DATABASE.close()
    else:
        exit(0)

