import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
USER = os.getenv('DB_USER')
PASSWORD = os.getenv('DB_PASSWORD')
HOST =  os.getenv('DB_HOST')
DATABASE = os.getenv('DB_NAME')
safe_password = urllib.parse.quote_plus(PASSWORD)

# Connect to MySql to create the database
admin_engine = create_engine(f'mysql+pymysql://{USER}:{safe_password}@{HOST}/')
with admin_engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DATABASE}"))

# Connect to the database and reate the table
db_engine = create_engine(f'mysql+pymysql://{USER}:{safe_password}@{HOST}/{DATABASE}')
with db_engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS hospital_census (
            id INT AUTO_INCREMENT PRIMARY KEY,
            mrn VARCHAR(50) UNIQUE,
            patient_name VARCHAR(20),
            dob VARCHAR(20),
            current_unit VARCHAR(50),         
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP          
        );
    """))
    conn.commit()
    print("Table 'hospital_census' was created successfully" )