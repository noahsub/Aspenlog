########################################################################################################################
# IMPORTS
########################################################################################################################

from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from database.Constants.connection_constants import PrivilegeType
from database.Entities.authentication_data import AuthenticationData
from database.Entities.authentication_data import BASE
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

def create_authentication_data_table():
    """
    Creates the CanadianPostalCodeData table
    :return: None
    """
    # Get the engine
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)

    # Name of the table
    table_name = 'AuthenticationData'
    inspector = inspect(engine)
    # If the table already exists, we don't want to create it again

    if table_name in inspector.get_table_names():
        already_exists_warning(item=table_name, database_name=DATABASE.database_name)
        return

    # Otherwise, we create the table
    else:
        BASE.metadata.bind = engine
        BASE.metadata.create_all(bind=engine)


def clean_authentication_data_table():
    """
    Cleans the ClimaticData table
    :return: None
    """
    # Get the connection and cursor
    connection = DATABASE.get_connection(privilege=PrivilegeType.ADMIN)
    cursor = DATABASE.get_cursor(connection)
    # Delete all entries in the table
    cursor.execute('DELETE FROM "AuthenticationData";')
    # Commit the changes
    connection.commit()


def add_entry(authentication_data: AuthenticationData):
    new_connection = DatabaseConnection(database_name="NBCC-2020")
    engine = new_connection.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()
    controller.add(authentication_data)
    controller.commit()
    new_connection.close()


# ONLY RUN IF DATABASE NEEDS TO BE REPOPULATED
if __name__ == "__main__":
    print("WARNING: This script will repopulate the AuthenticationData table. THIS WILL DELETE ALL USERS AND RENDER THEM UNRECOVERABLE.")
    choice = input("Are you sure you want to continue? (y/n): ")
    if choice.lower() == 'y':
        create_authentication_data_table()
        clean_authentication_data_table()
        DATABASE.close()
    else:
        exit(0)
