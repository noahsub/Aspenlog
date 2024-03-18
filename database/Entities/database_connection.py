########################################################################################################################
# database_connection.py
# This file contains the class for the database connection
#
# This code may not be reproduced, disclosed, or used without the specific written permission of the owners
# Author(s): https://github.com/noahsub, https://github.com/alastairsim
########################################################################################################################

########################################################################################################################
# IMPORTS
########################################################################################################################

import os
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv

from config import get_file_path
from database.Constants.connection_constants import PrivilegeType


########################################################################################################################
# DATABASE CONNECTION CLASS
########################################################################################################################

class DatabaseConnection:
    """
    Class for the database connection
    """
    # The host of the database
    host: str
    # The port of the database
    port: int
    # The admin username of the database
    admin_username: str
    # The admin password of the database
    admin_password: str
    # The write username of the database
    write_username: str
    # The write password of the database
    write_password: str
    # The read username of the database
    read_username: str
    # The read password of the database
    read_password: str
    # The name of the database
    database_name: str
    # The list of connections
    connections: list[psycopg2.extensions.connection]
    # The list of cursors
    cursors: list[psycopg2.extensions.cursor]
    # The list of engines
    engines: list[sqlalchemy.Engine]

    def __init__(self, database_name: str):
        """
        Initializes the database connection
        :param database_name: The name of the database
        """
        # Load the .env file
        load_dotenv(get_file_path('database/.env'))
        # Read and store the values retrieved from the .env file
        self.host = os.getenv('HOST')
        self.port = int(os.getenv('PORT'))
        self.admin_username = os.getenv('ADMIN_USERNAME')
        self.admin_password = os.getenv('ADMIN_PASSWORD')
        self.write_username = os.getenv('WRITE_USERNAME')
        self.write_password = os.getenv('WRITE_PASSWORD')
        self.read_username = os.getenv('READ_USERNAME')
        self.read_password = os.getenv('READ_PASSWORD')
        self.database_name = database_name
        # initialize connection, cursors, and engines lists
        self.connections = []
        self.cursors = []
        self.engines = []

    def get_credentials(self, privilege):
        """
        Gets the credentials for the given privilege
        :param privilege: The privilege level
        :return: The username and password for the given privilege
        """
        # Map the privilege to the username and password
        privileges = {
            PrivilegeType.ADMIN: (self.admin_username, self.admin_password),
            PrivilegeType.WRITE: (self.write_username, self.write_password),
            PrivilegeType.READ: (self.read_username, self.read_password)
        }
        # get the username and password for the given privilege
        user, password = privileges[privilege]
        # return the username and password
        return user, password

    def get_connection(self, privilege: PrivilegeType) -> psycopg2.extensions.connection:
        """
        Gets the connection for the given privilege
        :param privilege: The privilege level
        :return: A psycopg2 connection to the database
        """
        # Get the username and password for the given privilege
        user, password = self.get_credentials(privilege)

        # Create a connection to the database
        connection = psycopg2.connect(
            dbname=self.database_name,
            user=user,
            password=password,
            host=self.host,
            port=self.port
        )
        # Add the connection to the list of connections
        self.connections.append(connection)
        # Return the connection
        return connection

    def get_cursor(self, connection: psycopg2.extensions.connection) -> psycopg2.extensions.cursor:
        """
        Gets the cursor for the given connection
        :param connection: The psycopg2 connection to the database
        :return: A psycopg2 cursor to the database
        """
        # Create a cursor for the given connection
        cursor = connection.cursor()
        # Add the cursor to the list of cursors
        self.cursors.append(cursor)
        # Return the cursor
        return cursor

    def get_engine(self, privilege: PrivilegeType) -> sqlalchemy.Engine:
        """
        Gets the engine for the given privilege
        :param privilege: The privilege level
        :return: A sqlalchemy engine for the database
        """
        # Get the username and password for the given privilege
        user, password = self.get_credentials(privilege)
        # Create an engine for the database
        connection_url = f'postgresql+psycopg2://{user}:{password}@{self.host}:{self.port}/{self.database_name}'
        engine = create_engine(connection_url)
        # Add the engine to the list of engines
        self.engines.append(engine)
        # Return the engine
        return engine

    def close(self):
        """
        Closes all connections, cursors, and engines
        :return: None
        """
        # Close all cursors
        for cursor in self.cursors:
            cursor.close()
        # Clear the list of cursors
        self.cursors.clear()

        # Close all connections
        for connection in self.connections:
            connection.close()
        # Clear the list of connections
        self.connections.clear()

        # Close all engines
        for engine in self.engines:
            engine.dispose()
        # Clear the list of engines
        self.engines.clear()

    def __str__(self):
        """
        Returns a string representation of the database connection
        :return:
        """
        # Print each attribute and its value on a new line
        return (f"{'HOST:':<16} {self.host}\n"
                f"{'PORT:':<16} {self.port}\n"
                f"{'ADMIN USERNAME:':<16} {self.admin_username}\n"
                f"{'ADMIN PASSWORD:':<16} {self.admin_password}\n"
                f"{'WRITE USERNAME:':<16} {self.write_username}\n"
                f"{'WRITE PASSWORD:':<16} {self.write_password}\n"
                f"{'READ USERNAME:':<16} {self.read_username}\n"
                f"{'READ PASSWORD:':<16} {self.read_password}\n"
                f"{'DATABASE:':<16} {self.database_name}")

