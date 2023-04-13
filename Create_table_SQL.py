from sqlalchemy import create_engine
from sqlalchemy import text

db_string = "postgresql://root:root@localhost:5432/store"
engine = create_engine(db_string)
connection = engine.connect()

create_user_table_query = """
    CREATE TABLE IF NOT EXISTS User (
    ID SERIAL PRIMARY KEY,
    firstname   TEXT,
    lastname    TEXT,
    age     INT,
    email   CHAR(50),
    job  CHAR(50)
);"""

create_application_table_query = """
    CREATE TABLE IF NOT EXISTS application (
    ID SERIAL PRIMARY KEY,
    appname TEXT,
    username TEXT,
    lastconnection DATE,
    user_id INT references User(ID)
);"""


connection.execute(text(create_user_table_query))
connection.execute(text(create_application_table_query))
connection.commit()
connection.close()