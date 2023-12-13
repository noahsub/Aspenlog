import os

import psycopg2
from dotenv import load_dotenv


class DatabaseConnection:
    host: str
    port: int
    admin_username: str
    admin_password: str
    write_username: str
    write_password: str
    read_username: str
    read_password: str
    database_name: str

    def __init__(self, database_name: str):
        # Load the .env file
        load_dotenv()
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

    def get_cursor(self, priviledge: ):
        try:
            connection = psycopg2.connect(
                dbname=self.database_name,
                user=
            )

    def __str__(self):
        return (f"{'HOST:':<16} {self.host}\n"
                f"{'PORT:':<16} {self.port}\n"
                f"{'ADMIN USERNAME:':<16} {self.admin_username}\n"
                f"{'ADMIN PASSWORD:':<16} {self.admin_password}\n"
                f"{'WRITE USERNAME:':<16} {self.write_username}\n"
                f"{'WRITE PASSWORD:':<16} {self.write_password}\n"
                f"{'READ USERNAME:':<16} {self.read_username}\n"
                f"{'READ PASSWORD:':<16} {self.read_password}\n"
                f"{'DATABASE:':<16} {self.database_name}")



if __name__ == '__main__':
    dc = DatabaseConnection(database_name="test")
    print(dc)
