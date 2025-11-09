CLAUDE
=====

# Description

Query the database `irts` and generate a list of publications from KAUST faculty.

# Stack

Database: MySQL 8.0.43
Programming Language: Python
Python package to access MySQL: pymysql
Python package to read the `.env` file to read the details of the MySQL connection: python-dotenv
Python package manager: uv

# IRTS Database

Present the relevant tables to be used.

Below is the schema of the `metadata` table:

```
mysql> describe metadata;
+-----------------+--------------+------+-----+-------------------+-------------------+
| Field           | Type         | Null | Key | Default           | Extra             |
+-----------------+--------------+------+-----+-------------------+-------------------+
| rowID           | int          | NO   | PRI | NULL              | auto_increment    |
| source          | varchar(50)  | NO   | MUL | NULL              |                   |
| idInSource      | varchar(150) | NO   | MUL | NULL              |                   |
| parentRowID     | int          | YES  | MUL | NULL              |                   |
| field           | varchar(200) | NO   | MUL | NULL              |                   |
| place           | int          | NO   | MUL | 1                 |                   |
| value           | longtext     | NO   | MUL | NULL              |                   |
| added           | timestamp    | NO   | MUL | CURRENT_TIMESTAMP | DEFAULT_GENERATED |
| deleted         | timestamp    | YES  | MUL | NULL              |                   |
| replacedByRowID | int          | YES  |     | NULL              |                   |
+-----------------+--------------+------+-----+-------------------+-------------------+
10 rows in set (0.00 sec)
```

## Query

```sql
SELECT m.idInSource, m.parentRowID FROM `metadata` m
    WHERE `source` LIKE 'local'
    AND field = 'local.employment.type'
    AND value LIKE 'Faculty'
    AND `deleted` IS NULL
    AND parentRowID IN (
        SELECT `parentRowID` FROM metadata
        WHERE source LIKE 'local'
        AND `idInSource` = m.idInSource
        AND field = 'local.person.title'
        AND value NOT LIKE '%Instructional%'
        AND deleted IS NULL
    );
```



