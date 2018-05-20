import pandas as pd
import numpy as np
import math
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']

def prep_for_knn(df):
    df_new = df.drop(['Creator','Trail','Report',
    'Votes','_id','hike_name','url',
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
