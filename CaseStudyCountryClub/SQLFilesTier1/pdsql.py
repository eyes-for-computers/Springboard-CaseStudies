import sqlite3
import sys
import pandas as pd
from sqlite3 import Error


"""
query = input("Query: ")#"SELECT * FROM Members"
database = "sqlite_db_pythonsqlite.db" 
conn = sqlite3.connect(database)
"""

print("//////////////////////////")

def main():
    try:
        while True:
            query = input("Query: ")#"SELECT * FROM Members"
            database = "sqlite_db_pythonsqlite.db" 
            conn = sqlite3.connect(database)
            df = pd.read_sql_query(query,conn)
            print(df)
    except: main()
 
if __name__ == '__main__':
    main()
