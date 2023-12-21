from sqlalchemy import inspect

from database.Constants.connection_constants import PrivilegeType
from database.Entities.climatic_data import BASE
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


if __name__ == "__main__":
    create_climatic_data_table()
