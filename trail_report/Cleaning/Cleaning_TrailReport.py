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

def dates_in_circle(dates):
    """Turns the date into a sin and cos to rep day out of the year."""
    dates_ordered = dates.apply(lambda x: x.month*30 + x.day *(2*math.pi))
    dates_sin = dates_ordered.apply(lambda x: math.sin(x))
    dates_cos = dates_ordered.apply(lambda x: math.cos(x))
    return dates_sin, dates_cos

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
    df['month'] = df['Date'].apply( lambda x: x.month)
    df['year'] = df['Date'].apply( lambda x: x.year)
    df['date_sin'],df['date_cos'] = dates_in_circle(df['Date'])
    # year_dummies = pd.get_dummies(df['year'])
    # month_dummies = pd.get_dummies(df['month'])
    condition_dummies(df)
    # trail_dummies= pd.get_dummies(df['Trail'])
    # did not use these dummies
    # month_dum = pd.get_dummies(df['month'])
    # year_dum = pd.get_dummies(df['year'])
    # monthyear_dummies = pd.get_dummies(df['monthyear'])
    # df_all = pd.concat([df,year_dummies,month_dummies], axis=1)
    return df.drop(['conditions_split','Trail_condtions'], axis=1)

if __name__ == '__main__':
    mc = pymongo.MongoClient()
    db = mc['wta_all']
    trail_reports = db['trail_reports']
    df = pd.DataFrame(list(trail_reports.find()))
    clean__reports_df = clean_trailreport(df)
    clean__reports_df.to_csv('../../data/WTA_trailreports_clean.csv', sep = '|',index_label=False)
