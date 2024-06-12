import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import data_import

#-----------------------------------------------#
# This file is for executing database operations. 
# Functions are defined in separate files.
# Comment out / in functions as needed
#-----------------------------------------------#

# Load environment variables from .env file
load_dotenv()

# Initialize the SQLAlchemy engine
engine = create_engine(os.getenv("DATABASE_URL"))

# Define the paths to your CSV files
schools_path = r'F:\Egna kreativa projekt\VScode\Concepts resources\schools.csv'
# subjects_path = r'path/to/your/subjects.csv'

# Import data
data_import.import_schools(data_import.schools_path, data_import.engine)

#def import_subjects(file_path, engine):
#    columns_to_keep = ['id', 'subject', 'foreign_id_school']
#    df = pd.read_csv(file_path, usecols=columns_to_keep)
#    df.to_sql('subjects', engine, if_exists='append', index=False)

print("Data import completed successfully.")
