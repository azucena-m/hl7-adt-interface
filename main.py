import sys
import hl7
import os
import urllib.parse
from dotenv import load_dotenv 
from sqlalchemy import create_engine, text
from sqlalchemy.dialects.mysql import insert

# CONFIGURATION
load_dotenv()
try:
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    HOST = os.getenv('DB_HOST')
    DATABASE = os.getenv('DB_NAME')
    safe_password = urllib.parse.quote_plus(PASSWORD)
    
    # Connection string
    connection_url = f'mysql+pymysql://{USER}:{safe_password}@{HOST}/{DATABASE}'
    engine = create_engine(connection_url)
    
except TypeError:
    print("ERROR: Missing credentials in .env file. Please check your configuration.")
    sys.exit(1) #only need one engine that connects directly to DB for updates

 # THE PARSER
def parse_adt_message(raw_hl7):
    # Standardize the message (handles different line endings)
    raw_hl7 = raw_hl7.replace('\n', '\r')
    h = hl7.parse(raw_hl7)

    pid = h.segment('PID')
    pv1 = h.segment('PV1')

    return {
        "mrn": pid[3][0][0],
        "patient_name": f"{pid[5][0][1]} {pid[5][0][0]}",
        "dob": pid[7][0],
        "current_unit": pv1[3][0][0]
        }

# THE SMART UPSERT  
def upsert_patient(patient_data):
    with engine.begin() as conn:
     # SQL logic: if MRN exists, update the unit, if not, insert a new row.
        sql = text(""" 
            INSERT INTO hospital_census (mrn, patient_name, dob, current_unit)
                VALUES (:mrn, :patient_name, :dob, :current_unit)
                ON DUPLICATE KEY UPDATE
                current_unit = VALUES(current_unit);
            """)
        conn.execute(sql, patient_data)
    print(f"Successfully processed: {patient_data['patient_name']} (MRN: {patient_data['mrn']})")           

def verify_connection():
    try:
        # Connect and ping the database
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("Database connection verified.")
    except Exception as e:
        # Check if the error is specifically about a missing database
        if "Unknown database" in str(e):
            print(f"DATABASE MISSING: The database '{DATABASE}' does not exist.")
            print("ACTION REQUIRED: Run 'python database_setup.py' first!")
        else:
            print(f"DATABASE ERROR: {e}")
        sys.exit(1)

# EXECUTION
if __name__ == "__main__":
    print("Starting the HL7 Interface Engine")

    #Check the connection
    verify_connection()

    # Open and read the sample HL7 file
    file_path = 'sample_adt.hl7'
    try:
        with open(file_path, 'r') as f:
            # read the content of the file
            raw_message = f.read()

            if not raw_message.strip():
                print(f"Warning: {file_path} is empty")
            else:
                # process the data
                parsed_data = parse_adt_message(raw_message)
                upsert_patient(parsed_data)
    
    except FileNotFoundError:
        print(f"ERROR: The file '{file_path}' was not fuond. Please ensure that it exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

        
    # Sample HL7 message
    # sample_msg = "MSH|^~\\&|EPIC|HOSP|LAB|HOSP|202305011030||ADT^A01|12345|P|2.3\rPID|1||PAT999^^^MRN||DOE^JOHN||19700101|M\rPV1|1|I|ICU^ROOM10^BED2|||||||||||||||ADMIT"

  