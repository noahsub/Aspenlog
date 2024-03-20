########################################################################################################################
# populate_canadian_postal_code_data.py
# This file contains the code for populating the CanadianPostalCodeData table
#
# Please refer to the LICENSE and DISCLAIMER files for more information regarding the use and distribution of this code.
# By using this code, you agree to abide by the terms and conditions in those files.
#
# Author: Noah Subedar [https://github.com/noahsub]
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
from database.Entities.canadian_postal_code_data import CanadianPostalCodeData
from database.Entities.canadian_postal_code_data import BASE
from database.Entities.database_connection import DatabaseConnection
from database.Warnings.database_warnings import already_exists_warning

########################################################################################################################
# GLOBALS
########################################################################################################################

# The database connection
DATABASE = DatabaseConnection(database_name="NBCC-2020")


########################################################################################################################
# DATABASE FUNCTIONS
########################################################################################################################

def create_canadian_postal_code_data_table():
    """
    Creates the CanadianPostalCodeData table
    :return: None
    """
    # Get the engine
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)

    # Name of the table
    table_name = 'CanadianPostalCodeData'
    inspector = inspect(engine)
    # If the table already exists, we don't want to create it again

    if table_name in inspector.get_table_names():
        already_exists_warning(item=table_name, database_name=DATABASE.database_name)
        return

    # Otherwise, we create the table
    else:
        BASE.metadata.bind = engine
        BASE.metadata.create_all(bind=engine)


def clean_canadian_postal_code_data_table():
    """
    Cleans the ClimaticData table
    :return: None
    """
    # Get the connection and cursor
    connection = DATABASE.get_connection(privilege=PrivilegeType.ADMIN)
    cursor = DATABASE.get_cursor(connection)
    # Delete all entries in the table
    cursor.execute('DELETE FROM "CanadianPostalCodeData";')
    # Reset the ID sequence
    cursor.execute('ALTER SEQUENCE "CanadianPostalCodeData_ID_seq" RESTART WITH 1;')
    # Commit the changes
    connection.commit()


########################################################################################################################
# POPULATION FUNCTIONS
########################################################################################################################

def populate_canadian_postal_code_data_table():
    """
    Populates the CanadianPostalCodeData table
    :return: None
    """
    # Get the engine and controller
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    # get the path to the data/location/CanadianPostalCodes202312.csv file
    file_path = get_file_path("data/location/CanadianPostalCodes202312.csv")
    # read the file
    with open(file_path, 'r') as csv_file:
        # Skip first line, header line and not data
        next(csv_file)

        # read data/location/CanadianPostalCodes202312.csv file
        csv_reader = csv.reader(csv_file)

        # map column names to appropriate column index
        for row in tqdm(csv_reader, "Populating Canadian Postal Code Data"):

            # unpack entry_data to create a ClimaticData object
            entry = CanadianPostalCodeData(postal_code=row[0], city=row[1], province=row[2], time_zone=row[3], latitude=row[4], longitude=row[5])
            # prepare the entry to be added to the database
            controller.add(entry)
        # add all entries to the database
        print("Committing changes to database...")
        print("This may take a while...")
        controller.commit()

########################################################################################################################
# MAIN
########################################################################################################################

# ONLY RUN IF DATABASE NEEDS TO BE REPOPULATED
if __name__ == "__main__":
    print("WARNING: This script will repopulate the CanadianPostalCodeData table. If the database is already populated, this will delete existing data and repopulate the table, meaning any manual changes will be lost.")
    choice = input("Are you sure you want to continue? (y/n): ")
    if choice.lower() == 'y':
        create_canadian_postal_code_data_table()
        clean_canadian_postal_code_data_table()
        populate_canadian_postal_code_data_table()
        DATABASE.close()
    else:
        exit(0)



