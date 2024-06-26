import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import postgresql_data_import as postgresql_data_import
from dgraph_scripts import import_data_to_dgraph
from dgraph_scripts import dgraph_drop_all_data
from dgraph_scripts import dgraph_export_script
from dgraph_scripts import dgraph_import_schema


load_dotenv()

#-----------------------------------------------#
# This file is for executing database operations. 
# Functions are defined in separate files.
# Comment out / in functions as needed
#-----------------------------------------------#

#-----------------------------------------------#
# dgraph operations
#-----------------------------------------------#
import_data_to_dgraph.import_data_to_dgraph()
#dgraph_drop_all_data.drop_all_data()
#dgraph_export_script.export_schema()
#dgraph_import_schema.import_schema()
#-----------------------------------------------#


#-----------------------------------------------#
# import curriculum data to postgresql 
#-----------------------------------------------#
# Connect to PostgreSQL with sqlalchemy engine
#engine = create_engine(os.getenv("DATABASE_URL"))

#postgresql_data_import.import_schools(postgresql_data_import.schools_path, postgresql_data_import.engine)
#postgresql_data_import.import_subjects(postgresql_data_import.subjects_path, postgresql_data_import.engine)
#postgresql_data_import.import_grades(postgresql_data_import.grades_path, postgresql_data_import.engine)
#postgresql_data_import.import_subsections(postgresql_data_import.subsections_path, postgresql_data_import.engine)
#postgresql_data_import.import_central_contents(postgresql_data_import.central_contents_path, postgresql_data_import.engine)
#postgresql_data_import.import_central_requirements(postgresql_data_import.central_requirements_path, postgresql_data_import.engine)

#print("Data import completed successfully.")
#-----------------------------------------------#