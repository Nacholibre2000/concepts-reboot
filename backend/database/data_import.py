import pandas as pd

# Path to your CSV file
file_path = 'F:\Egna kreativa projekt\VScode\Concepts resources\schools.csv'

def import_schools(file_path, engine):
    columns_to_keep = ['id', 'school']
    df = pd.read_csv(file_path, usecols=columns_to_keep)
    df.to_sql('subjects', engine, if_exists='append', index=False)