from Cleaning.Merge_Weather import get_weather_data, merge_weather_trails, get_closest_station
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import math
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report

conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']

def prep_for_knn(df):
    df_new = df.drop(['Unnamed: 0','Unnamed: 0_x','Creator','Trail','Report',
    'Votes','_id','Unnamed: 0_y','hike_name','url',

    'super_region','sub_region','which_pass'], axis=1)
    df_new['Date'] = pd.to_datetime(df_new['Date'])
    df_new['month'] = df_new['Date'].apply(lambda x: x.month)
    df_new['date_sin'],df_new['date_cos'] = dates_in_circle(df_new['Date'])
    df_full = df_new.fillna(0)
    return df_full

def dates_in_circle(dates):
    dates_ordered = dates.apply(lambda x: x.month*30 + x.day *(2*math.pi))
    dates_sin = dates_ordered.apply(lambda x: math.sin(x))
    dates_cos = dates_ordered.apply(lambda x: math.cos(x))
    return dates_sin, dates_cos

def train_test_split(df,year):
    test = df[df['year'] >= year]
    train = df[df['year'] < year]
    return test,train

def prep_neighbors(df,condition):
    neigh = KNeighborsClassifier(n_neighbors=20)
    X = df[['highest_point','distance_from_median','month']]
    y = df[condition]
    y = y.astype(bool)
    X_s = scale(X)
    neigh.fit(X_s,y)
    return neigh

def get_neighbors(neigh,df,condition):
    all_n = neigh.kneighbors()
    averages = []
    for idx_neighbors in all_n[1]:
        neighbors = df.iloc[idx_neighbors]
        averages.append(neighbors[condition].mean())
    df[f'neighbors_average {condition}'] = averages

def add_cols(test,train, df_weather_dist,condition):
    neigh_train = prep_neighbors(train, condition)
    neigh_test = prep_neighbors(train, condition)
    get_neighbors(neigh_test,test,condition)
    get_neighbors(neigh_train,train, condition)
    get_closest_station(train,df_weather_dist)
    get_closest_station(test,df_weather_dist)

def get_knn_inputs(test,train,condition):
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    test_y = test[condition]
    drop_list = conditions+['year','closet_station']
    test_X = test.drop(drop_list, axis = 1)
    train_y = train[condition]
    train_X = train.drop(drop_list, axis = 1)
    test_X = test_X.fillna(0)
    train_X = train_X.fillna(0)
    return train_X,train_y,test_X,test_y

def make_forest(X_train,y_train,X_test):
    model = RandomForestClassifier(n_estimators=500)
    fit = model.fit(X_train,y_train)
    pred = model.predict_proba(X_test)
    return model, pred

def make_logistic(X_train,y_train,X_test):
    model = LogisticRegression()
    model.fit(X_train, y_train)
    pred = model.predict_proba(X_test)
    return model,pred
if __name__ == '__main__':
    df = pd.read_csv('../data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
    df_clean = prep_for_knn(df)
    test,train = train_test_split(df_clean,2016)
    df_weather,df_weather_dist = get_weather_data()
    add_cols(test,train, df_weather_dist)
    #merge and save full df
    df_test = merge_weather_trails(df_weather,test)
    df_train = merge_weather_trails(df_weather,train)
    train_X,train_y,test_X,test_y = get_knn_inputs(df_test,df_train)

    model,pred = make_forest(train_X,train_y,test_X)
    print (f'final predictions {pred}')
