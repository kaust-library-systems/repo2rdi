# Describe tables in a MySQL database

import os
import pymysql
from dotenv import load_dotenv

# Global variables for the database:
db_host="localhost"
db_user="root"
db_protocol="tcp"
db_port=3336

def main():
    load_dotenv()
    db_root_passwd = os.environ["MYSQL_ROOT_PASSWORD"]

    try:
        conn = pymysql.connect(host=db_host,
            user=db_user, 
            password=db_root_passwd,
            port=db_port)
        if conn.open:
            print("Connection OK")
    except Exception as ee:
        print("Error while connecting to database: ", ee)


    cur = conn.cursor()

    cur.execute("show databases")
    print(cur.description)
    print()

    for row in cur:
        print(row)
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
    print("Have a nice day.")

