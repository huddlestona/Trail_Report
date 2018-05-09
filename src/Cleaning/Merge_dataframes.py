import pandas as pd
import numpy as np


df_trail = pd.read_csv('data/Olympics_189hike_data.csv')
df_report = pd.read_csv('data/WTA_olympics_trailreports_clean.csv', sep = '|', lineterminator='\n')

def merge_files(df_trail,df_report):
    """ This function left joins trails and reports, adding trail data to the report you built"""
    
df_reports = df_report.drop('Unnamed: 0',axis =1)
df_trails = df_trail.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
result = pd.merge(df_reports, df_trails, left_on='Trail', right_on='hike_name', how='left', sort=False)
