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
schools_path = r'F:\Egna kreativa projekt\VScode\Concepts resources\schools_data.csv'
subjects_path = r'F:\Egna kreativa projekt\VScode\Concepts resources\subjects_data.csv'
grades_path = r'F:\Egna kreativa projekt\VScode\Concepts resources\grades_data.csv'
subsections_path = r'F:\Egna kreativa projekt\VScode\Concepts resources\subsections_data.csv'
central_contents_path = r'F:\Egna kreativa projekt\VScode\Concepts resources\central_contents_data.csv'
central_requirements_path = r'F:\Egna kreativa projekt\VScode\Concepts resources\central_requirements_data.csv'


def import_schools(file_path, engine):
    columns_to_keep = ['id', 'school']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df.to_sql('schools', engine, if_exists='append', index=False)

def import_subjects(file_path, engine):
    columns_to_keep = ['id', 'subject', 'foreign_id_school']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df.to_sql('subjects', engine, if_exists='append', index=False)

def import_grades(file_path, engine):
    columns_to_keep = ['id', 'grade', 'foreign_id_subject']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df['foreign_id_subject'] = df['foreign_id_subject'].apply(lambda x: x.split('-')[-1])
    df.to_sql('grades', engine, if_exists='append', index=False)

def import_subsections(file_path, engine):
    columns_to_keep = ['id', 'subsection', 'foreign_id_grade']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df['foreign_id_grade'] = df['foreign_id_grade'].apply(lambda x: x.split('-')[-1])
    df.to_sql('subsections', engine, if_exists='append', index=False)    

def import_central_contents(file_path, engine):
    columns_to_keep = ['id', 'central_content', 'foreign_id_subsection']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df['foreign_id_subsection'] = df['foreign_id_subsection'].apply(lambda x: x.split('-')[-1])
    df.to_sql('central_contents', engine, if_exists='append', index=False)

def import_central_requirements(file_path, engine):
    columns_to_keep = ['id', 'central_requirement', 'foreign_id_grade']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df['foreign_id_grade'] = df['foreign_id_grade'].apply(lambda x: x.split('-')[-1])
    df.to_sql('central_requirements', engine, if_exists='append', index=False)

# Define more functions as needed
