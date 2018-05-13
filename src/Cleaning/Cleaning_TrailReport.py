""" This file when called in the terminal will import Trail Report Data from
 Mongo, create dummies and clean features, and save the cleaned db as a csv"""

from pymongo import MongoClient
import pymongo
import math
import pandas as pd
import numpy as np

def split_conditions(string):
    ''' splits each string on conditions to a list'''
    conditions= string.split('\n')[2].split(',')
    con_clean= [con.strip(' ') for con in conditions]
    return con_clean

def condition_dummies(df):
    '''takes conditions from the dataframe and adds dummy variable for conditions'''
    full_conditions= df[df['Trail_condtions'].notna()]['Trail_condtions']
    df['conditions_split'] = full_conditions.apply(lambda x: split_conditions(x))
    conditions= ['snow','trail','bugs', 'road']
    for cond in conditions:
        df[f"condition|{cond}"] = df['conditions_split'].apply(lambda x: cond in str(x))

def clean_trailreport(df):
    """
    **Input parameters**
    ------------------------------------------------------------------------------
    df: pandas dataframe with trail report info
    **Output**
    ------------------------------------------------------------------------------
    clean_reports_df: pandas dataframe with clean features with extra text,
    add time features, and dummy variables
    """
    df['Creator']= df ['Creator'].apply(lambda x: x.strip('\n'))
    df['Date']= pd.to_datetime(df['Date'])
    df['last_year']= df['Date'].apply( lambda x: x.year-1)
    df['last_month']= df['Date'].apply( lambda x: x.year-1)
    df['month'] = df['Datetime'].apply( lambda x: x.month + x.year)
    df['year'] = df['Datetime'].apply( lambda x: x.year)
    df['monthyear'] = df['Datetime'].apply( lambda x: str(x.month)+'-'+str(x.year))
    condition_dummies(df)
    trail_dummies= pd.get_dummies(df['Trail'])
    month_dum = pd.get_dummies(df['month'])
    year_dum = pd.get_dummies(df['year'])
    monthyear_dummies = pd.get_dummies(df['monthyear'])
    pass_dummies = pd.get_dummies(df['which_pass'])
    subregion_dummies = pd.get_dummies(df['sub_region'])
    df_all = pd.concat([df,trail_dummies,monthyear_dummies,pass_dummies,subregion_dummies], axis=1)
    return df_all.drop(['conditions_split','Trail_condtions'], axis=1)

if __name__ == '__main__':
    mc = pymongo.MongoClient()
    db = mc['wta']
    trail_reports = db['trail_reports']
    df = pd.DataFrame(list(trail_reports.find()))
    clean__reports_df = clean_trailreport(df)
    clean__reports_df.to_csv('../../data/WTA_olympics_trailreports_clean.csv', sep = '|')
