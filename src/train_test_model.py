""" The file, when called in the terminal, will return the AUC for the model with the current data."""
from knn_model import prep_for_knn,make_forest,make_logistic
from Cleaning.Merge_Weather import get_weather_data, merge_weather_trails, get_closest_station
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report

def train_test_split(df,year):
    """Splits data by year input."""
    test = df[df['year'] >= year]
    train = df[df['year'] < year]
    return test,train

def add_cols(test,train, df_weather_dist,condition):
    """adds KNN column and closest station column to train and test df."""
    neigh_train = prep_neighbors(train, condition)
    neigh_test = prep_neighbors(train, condition)
    get_neighbors(neigh_test,test,condition)
    get_neighbors(neigh_train,train, condition)
    get_closest_station(train,df_weather_dist)
    get_closest_station(test,df_weather_dist)

def get_knn_inputs(test,train,condition):
    """Preps train and test by dropping columns and filling nas."""
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    test_y = test[condition]
    drop_list = conditions+['year','closet_station']
    test_X = test.drop(drop_list, axis = 1)
    train_y = train[condition]
    train_X = train.drop(drop_list, axis = 1)
    test_X = test_X.fillna(0)
    train_X = train_X.fillna(0)
    return train_X,train_y,test_X,test_y

def merge_weather(test,train):
    """Get's weather, get's new columns, and merges weather in."""
    df_weather,df_weather_dist = get_weather_data()
    add_cols(test,train, df_weather_dist)
    df_test = merge_weather_trails(df_weather,test)
    df_train = merge_weather_trails(df_weather,train)
    return df_test,df_train

if __name__ == '__main__':
    df = pd.read_csv('../data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
    df_clean = prep_for_knn(df)
    test,train = train_test_split(df_clean,2016)
    df_test,df_train = merge_weather(test,train)
    #merge and save full df
    train_X,train_y,test_X,test_y = get_knn_inputs(df_test,df_train)
    model,pred = make_forest(train_X,train_y,test_X)
    print (f'final predictions {pred}')
