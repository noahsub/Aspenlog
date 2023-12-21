from database.Constants.connection_constants import PrivilegeType
from database.Entities.climatic_data import BASE
from database.Entities.database_connection import DatabaseConnection

DATABASE = DatabaseConnection(database_name="NBCC-2020")

def create_climatic_data_table():
    engine = DATABASE.get_engine(privilege=PrivilegeType.ADMIN)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_climatic_data_table()
