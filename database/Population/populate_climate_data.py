import csv

from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from config import get_file_path
from database.Constants.connection_constants import PrivilegeType
from database.Entities.climatic_data import BASE, ClimaticData
from database.Entities.database_connection import DatabaseConnection
from database.Warnings.database_warnings import already_exists_warning

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


def populate_climatic_data_table():
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    controller = session()

    file_path = get_file_path("data-extraction/output/table_c2.csv")
    with open(file_path, 'r') as csv_file:
        # Skip first 3 lines, these are header lines and not data
        for _ in range(3):
            next(csv_file)

        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            entry = ClimaticData(ProvinceAndLocation=row[1])
            controller.add(entry)
        controller.commit()


if __name__ == "__main__":
    create_climatic_data_table()
    populate_climatic_data_table()
