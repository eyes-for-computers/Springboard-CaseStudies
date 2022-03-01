import sqlite3
from sqlite3 import Error




#added argparse to speed up testing
import argparse
parser = argparse.ArgumentParser()

# added this to speed up testing
parser.add_argument("-e", "--execute", help="Command to execute")


args = parser.parse_args()


print(args.execute)




#def queryDB(command)
#query = input("New Query: ")

 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
 
    return conn

 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()

#added to query from terminal
    query1 = args.execute
    
#    query1 = """
#        SELECT *
#        FROM FACILITIES
#        """

    cur.execute(query1)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)


def main():
    database = "sqlite_db_pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn: 
        print("2. Query all tasks")
        select_all_tasks(conn)
 
 
if __name__ == '__main__':
    main()
