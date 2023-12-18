import pandas as pd
import psycopg2
import os
from Entities.database_connection import DatabaseConnection

csv_path = os.path.join("..", "data-extraction", "output", "table_c1.csv")

db = DatabaseConnection(database_name="test")
engine = db.get_engine(priviledge="write")

df = pd.read_csv(csv_path)
# might have to manually create schemas first
df.to_sql("Climate Data", engine, index=False, if_exists='append')