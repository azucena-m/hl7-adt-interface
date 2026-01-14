# HL7 ADT Interface Engine (Python & MySQL)

## 🏥 Project Overview
In a hospital environment, patient data must move seamlessly between the Electronic Health Record (EHR) and downstream systems (like Lab or Pharmacy). This project is a custom **Interface Engine** that consumes **HL7 v2.x ADT (Admit, Discharge, Transfer)** messages, parses clinical data, and synchronizes a real-time hospital census in a MySQL database.

### Key Features:
* **HL7 Parsing:** Extracts patient demographics (MRN, Name, DOB) and visit information (Nursing Unit) from raw pipe-delimited messages.
* **Data Normalization:** Strips HL7 sub-components (e.g., `^^^MRN`) to ensure clean data entry.
* **Idempotent 'Upsert' Logic:** Uses SQL `ON DUPLICATE KEY UPDATE` to ensure patient moves (transfers) update existing records rather than creating duplicates.
* **Production Readiness:** Includes a connection verification layer and comprehensive error handling.

## 🛠️ Tech Stack
* **Language:** Python 3.13
* **Database:** MySQL
* **Libraries:** `hl7`, `SQLAlchemy`, `PyMySQL`, `python-dotenv`

## 📂 Project Structure
* `main.py`: The core engine that reads HL7 files and updates the database.
* `database_setup.py`: Infrastructure script to initialize the database and tables.
* `sample_adt.hl7`: A sample clinical message used for testing.
* `.env`: Configuration for database credentials (secured via .gitignore).

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have a MySQL instance running and a Python virtual environment active.

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Database Setup and Running the Interface
```bash
python database_setup.py
python main.py
```

### Expected Output
```text
🚀 Starting the HL7 Interface Engine
🔗 Database connection verified.
✅ Successfully processed: JOHN DOE (MRN: PAT999)
```