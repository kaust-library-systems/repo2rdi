# Describe tables in a MySQL database

import os
import pymysql
from dotenv import load_dotenv

# Global variables for the database:
db_host="localhost"
db_protocol="tcp"
db_port=3336

def describe_table(table: tuple) -> None:
    """Print table description in a nice way for humans"""

    for row in table:
        print("|".join(str(rr) for rr in row))
        
def main():
    load_dotenv()
    db_irts_user = os.environ["IRTS_USER"]
    db_irts_passwd = os.environ["IRTS_USER_PASSWD"]
    db_name = os.environ["IRTS_DB"]
    
    try:
        conn = pymysql.connect(host=db_host,
            database=db_name,
            user=db_irts_user, 
            password=db_irts_passwd,
            port=db_port)
        if conn.open:
            print("Connection OK")
    except Exception as ee:
        print("Error while connecting to database: ", ee)

    cur = conn.cursor()

    cur.execute("show tables")

    tables = [row[0] for row in cur]

    # for table in tables:
    #     cmd = f"describe {table}"
    #     cur.execute(cmd)
    #     table_desc = cur.fetchall()
    #     print(type(table_desc))
    #     describe_table(table_desc)

    table = tables[0]
    cmd = f"describe {table}"
    cur.execute(cmd)
    table_desc = cur.fetchall()
    describe_table(table_desc)


    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
    print("Have a nice day.")

