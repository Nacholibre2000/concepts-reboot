import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#-----------------------------------------------#
# This file is for defining database import operations.
#-----------------------------------------------#


# Load environment variables from .env file
load_dotenv()

# Initialize the SQLAlchemy engine
engine = create_engine(os.getenv("DATABASE_URL"))

# Define the paths to your CSV files
schools_path = 'F:\\Egna kreativa projekt\\VScode\\Concepts resources\\schools.csv'
subjects_path = 'path/to/your/subjects.csv'
# Define more paths as needed

def import_schools(file_path, engine):
    columns_to_keep = ['id', 'school']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df.to_sql('schools', engine, if_exists='append', index=False)

def import_subjects(file_path, engine):
    columns_to_keep = ['id', 'subject', 'foreign_id_school']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df.to_sql('subjects', engine, if_exists='append', index=False)

# Define more functions as needed
