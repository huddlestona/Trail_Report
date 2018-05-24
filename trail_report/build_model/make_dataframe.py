"""
This file, when called in the terminal, will add new features,merge
in the weather dataframe, and save the final X and Y databases.
"""
from Cleaning.Merge_Weather import get_weather_data, merge_weather_trails, get_closest_station
from knn_model import prep_for_knn,prep_neighbors,get_neighbors
import pandas as pd

def split_x_y(df):
    """Fills in nas and splits data with y being the inputed conditon column."""
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    df_full = df.fillna(0)
    train_y = df_full[conditions]
    drop_list = conditions+['year','closet_station']
    train_X = df_full.drop(drop_list, axis = 1)
    return train_X,train_y

def clean_X(df):
    """Drops unneeded colums in df."""
    df_clean = df.drop(['Date','last_year','month'], axis=1)
    return df_clean

def add_knn(df):
    """
    Preps data for knn, runs knn, and adds knn past report values as column in df.
    **Input parameters**
    ------------------------------------------------------------------------------
    df: pandas dataframe of merged trail data and trail reports
    condition: condition being used as y.
    **Output**
    ------------------------------------------------------------------------------
    df_clean: pandas dataframe. Clean results to be merged, with neighbors added.
    """
    df_clean = prep_for_knn(df)
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    for condition in conditions:
        neigh = prep_neighbors(df_clean, condition)
        get_neighbors(neigh,df_clean,condition)
    return df_clean

def merge_all_files(df_clean):
    """Takes clean df and adds weather by nearest station."""
    df_weather,df_weather_dist = get_weather_data()
    get_closest_station(df_clean,df_weather_dist)
    df_merge = merge_weather_trails(df_weather,df_clean)
    return df_merge

if __name__ == '__main__':
    df = pd.read_csv('../data/olympics_merged.csv', sep = '|',lineterminator='\n')
    df_clean = add_knn(df)
    df_merge = merge_all_files(df_clean)
    df_final = clean_X(df_merge)
    train_X,train_y = split_x_y(df_final)
    train_X.to_csv('../data/olympics_Xall.csv', sep = '|',index_label=False)
    train_y.to_csv('../data/olympics_yall.csv', sep = '|', index_label=False)
