from pymongo import MongoClient
import pymongo
import math
import pandas as pd
import numpy as np

def split_conditions(string):
    conditions = string.split('\n')[2].split(',')
    con_clean = [con.strip(' ') for con in conditions]
    return con_clean

def condition_dummies(df):
    conditions = ['snow','trail','bugs', 'road']
    for cond in conditions:
        df[f"condition|{cond}"] = df['conditions_split'].apply(lambda x: cond in str(x))

def clean_trailreport(df):
    df['Creator'] = df ['Creator'].apply(lambda x: x.strip('\n'))
    df['Date_type'] = pd.to_datetime(df['Date'])
    full_conditions = df[df['Trail_condtions'].notna()]['Trail_condtions']
    df['conditions_split'] = full_conditions.apply(lambda x: split_conditions(x))
    condition_dummies(df)
    trail_dummies = pd.get_dummies(df['Trail'])
    df_all = pd.concat([df,trail_dummies], axis=1)
    return df_all.drop(['conditions_split','Date','Trail_condtions','Trail'], axis=1)

if __name__ == '__main__':
    mc = pymongo.MongoClient()
    db = mc['wta']
    trail_reports = db['trail_reports']
    df = pd.DataFrame(list(trail_reports.find()))
    clean__reports_df = clean_trailreport(df)
    clean__reports_df.to_csv('../../data/WTA_olympics_trailreports_clean.csv')
    
