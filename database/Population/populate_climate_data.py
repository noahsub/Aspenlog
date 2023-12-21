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

DATABASE = DatabaseConnection(database_name="NBCC-2020")


def create_climatic_data_table():
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)

    table_name = 'ClimaticData'
    inspector = inspect(engine)
    if table_name in inspector.get_table_names():
        already_exists_warning(item=table_name, database_name=DATABASE.database_name)
        return

    else:
        BASE.metadata.bind = engine
        BASE.metadata.create_all(bind=engine)


def clean_climatic_data_table():
    connection = DATABASE.get_connection(privilege=PrivilegeType.ADMIN)
    cursor = DATABASE.get_cursor(connection)
    cursor.execute('DELETE FROM "ClimaticData";')
    cursor.execute('ALTER SEQUENCE "ClimaticData_ID_seq" RESTART WITH 1;')
    connection.commit()


def populate_climatic_data_table():
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    file_path = get_file_path("data-extraction/output/table_c2.csv")
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
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    geolocator = Nominatim(user_agent=str(uuid.uuid4()).replace('-', ''))
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    for entry in tqdm(controller.query(ClimaticData).all(), desc="Updating Locations"):
        location = entry.ProvinceAndLocation
        location_info = geocode(location, timeout=10)

        if location_info is None:
            entry.Latitude = None
            entry.Longitude = None
        else:
            entry.Latitude = location_info.latitude
            entry.Longitude = location_info.longitude

    controller.commit()


if __name__ == "__main__":
    create_climatic_data_table()
    clean_climatic_data_table()
    populate_climatic_data_table()
    update_location()
