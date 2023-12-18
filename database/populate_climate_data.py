import os
import pandas as pd
from Entities.database_connection import DatabaseConnection
from database.Constants.connection_constants import PrivilegeType

csv_path = os.path.join("..", "data-extraction", "output", "table_c1.csv")

db = DatabaseConnection(database_name="test")
engine = db.get_engine(privilege=PrivilegeType.WRITE)

df = pd.read_csv(csv_path)
# might have to manually create schemas first
df.to_sql("Climate Data", engine, index=False, if_exists='append')
