import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from dotenv import load_dotenv
import psycopg2
import json

username = 'postgres'
password = 'postgre'
database_name = 'AndeanMythology'
host = 'localhost'
port = '5432'  

connection_string = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

db_config = {
    'dbname': database_name,
    'user': username,
    'password': password,
    'host': host,
    'port': port
}


engine = create_engine(connection_string)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_database_schema(db_config) -> str:
    connection = None
    try:

        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Retrieve All Tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()

        # Initialize the schema dictionary
        database_schema = {}

        # Retrieve Schema Information for Each Table
        for table in tables:
            table_name = table[0]

            # Get column details for each table
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable, column_default 
                FROM information_schema.columns 
                WHERE table_name = %s
            """, (table_name,))
            columns = cursor.fetchall()

            # Get primary key information
            cursor.execute(f"""
                SELECT kcu.column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu 
                  ON kcu.constraint_name = tc.constraint_name
                WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY'
            """, (table_name,))
            primary_keys = cursor.fetchall()

            # Organize the table schema
            database_schema[table_name] = {
                "columns": [{
                    "column_name": col[0],
                    "data_type": col[1],
                    "is_nullable": col[2],
                    "column_default": col[3]
                } for col in columns],
                "primary_keys": [key[0] for key in primary_keys]
            }

        # Convert the Schema to JSON
        database_schema_json = json.dumps(database_schema, indent=4)
        return database_schema_json

    except Exception as e:
        print("Error")
        return f"Error: {e}"

    finally:
        if connection:
            cursor.close()
            connection.close()

a = get_database_schema(db_config)
print(a)