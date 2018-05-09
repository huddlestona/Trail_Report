from pymongo import MongoClient
import pymongo
import math
import pandas as pd
import numpy as np

mc = pymongo.MongoClient()
db = mc['wta']
trail_reports = db['trail_reports']
raw_html = db['html']
trail_page_raw_html = db['trail_html']

df_reports = pd.DataFrame(list(trail_reports.find()))
df_reports['Creator'] = df_reports['Creator'].apply(lambda x: x.strip('\n'))
df_reports['Date_type'] = pd.to_datetime(df_reports['Date'])
df_reports['conditions_split'] = df_reports[df_reports['Trail_condtions'].notna()]['Trail_condtions'].apply(lambda x: split_conditions(x))

def split_conditions(string):
    conditions = string.split('\n')[2].split(',')
    con_clean = [con.strip(' ') for con in conditions]
    return con_clean

conditions = ['snow','trail','bugs', 'road']
for cond in conditions:
    df_reports[f"condition|{cond}"] = df_reports['conditions_split'].apply(lambda x: cond in str(x))

trail_dummies = pd.get_dummies(df_reports['Trail'])
df_all = pd.concat([df_reports,trail_dummies], axis=1)

df_clean = df_all.drop(['conditions_split','Date','Trail_condtions','Trail'], axis=1)
