import sqlite3
import sys
import pandas as pd
from sqlite3 import Error



query = "SELECT * FROM Members"
database = "sqlite_db_pythonsqlite.db" 
conn = sqlite3.connect(database)

df = pd.read_sql_query(query,conn)
print(df)
print("//////////////////////////")

