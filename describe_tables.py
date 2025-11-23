# Describe tables in a MySQL database

import os
import sys
import pymysql
from pathlib import Path
from typing import IO
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

# Global variables for the database:
db_host="localhost"
db_protocol="tcp"
db_port=3336

def describe_table(table: tuple) -> str:
    """Print table description in a nice way for humans"""

    header = '''
| Field | Type | Null | Key | Default | Extra |
| ----- | ---- | ---- | --- | ------- | ----- |
''' 

    str_tmp = ""
    for row in table:
        str_tmp += "| " + " | ".join(str(rr) for rr in row) + " |\n"

    str_table = header + str_tmp

    # print(str_table)

    return str_table
        
def main():
    load_dotenv()
    db_irts_user = os.environ["IRTS_USER"]
    db_irts_passwd = os.environ["IRTS_USER_PASSWD"]
    #db_name = os.environ["IRTS_DB"]
    if len(sys.argv) != 2:
        raise ValueError(f"Usage {sys.argv[0]} <db_name>")
    else:
        db_name = sys.argv[1]
    
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

    db_tables_file = Path(f"{db_name}_tables.md")
    print(db_tables_file)
    with open(db_tables_file, "w") as ff:
        tables = [row[0] for row in cur]
        str_table = ""
        print("Processing tables")
        for table in tables:
            if table == "groups":
                # "Fix" tables with names that can conflict with
                # system (MySQL) tables.
                table = f"`{table}`"
            print(f"Table: {table}")
            ff.write((f"## {table}"))
            cmd = f"describe {table}"
            cur.execute(cmd)
            table_desc = cur.fetchall()
            str_table = describe_table(table_desc)
            ff.write(str_table)
            ff.write("")


    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
    print("Have a nice day.")

