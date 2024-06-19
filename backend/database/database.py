import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import data_import
import pydgraph


#-----------------------------------------------#
# This file is for executing database operations. 
# Functions are defined in separate files.
# Comment out / in functions as needed
#-----------------------------------------------#



#-----------------------------------------------#
# Import data to postgresql
# Load environment variables from .env file
#load_dotenv()

# Initialize the SQLAlchemy engine
#engine = create_engine(os.getenv("DATABASE_URL"))
#data_import.import_schools(data_import.schools_path, data_import.engine)
#data_import.import_subjects(data_import.subjects_path, data_import.engine)
#data_import.import_grades(data_import.grades_path, data_import.engine)
#data_import.import_subsections(data_import.subsections_path, data_import.engine)
#data_import.import_central_contents(data_import.central_contents_path, data_import.engine)
#data_import.import_central_requirements(data_import.central_requirements_path, data_import.engine)

#print("Data import completed successfully.")
#-----------------------------------------------#