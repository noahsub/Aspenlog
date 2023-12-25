import csv
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm
from config import get_file_path
from database.Constants.connection_constants import PrivilegeType
from database.Entities.database_connection import DatabaseConnection
from database.Entities.wind_speed_data import BASE, WindSpeedData
from database.Warnings.database_warnings import already_exists_warning

DATABASE = DatabaseConnection(database_name="NBCC-2020")


def create_wind_speed_data_table():
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)

    table_name = 'WindSpeedData'
    inspector = inspect(engine)
    if table_name in inspector.get_table_names():
        already_exists_warning(item=table_name, database_name=DATABASE.database_name)
        return

    else:
        BASE.metadata.bind = engine
        BASE.metadata.create_all(bind=engine)


def clean_wind_speed_data_table():
    connection = DATABASE.get_connection(privilege=PrivilegeType.ADMIN)
    cursor = DATABASE.get_cursor(connection)
    cursor.execute('DELETE FROM "WindSpeedData";')
    cursor.execute('ALTER SEQUENCE "WindSpeedData_ID_seq" RESTART WITH 1;')
    connection.commit()


def populate_wind_speed_data_table():
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    file_path = get_file_path("data-extraction/output/table_c1.csv")
    with open(file_path, 'r') as csv_file:
        # Skip first 3 lines, these are header lines and not data
        for _ in range(2):
            next(csv_file)

        # read data-extraction/output/table_c1.csv file
        csv_reader = csv.reader(csv_file)

        for row in tqdm(csv_reader, "Populating Wind Speed Data"):
            # Each row of the csv file contains 4 entries, hence we need to split the row into groups of two columns
            for i in range(1, 9, 2):
                entry = WindSpeedData(q_KPa=float(row[i]), V_ms=float(row[i+1]))
                controller.add(entry)

        controller.commit()


if __name__ == '__main__':
    create_wind_speed_data_table()
    clean_wind_speed_data_table()
    populate_wind_speed_data_table()
    DATABASE.close()
