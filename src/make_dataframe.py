from Cleaning.Merge_Weather import get_weather_data, merge_weather_trails, get_closest_station
from knn_model import prep_for_knn,prep_neighbors,get_neighbors
import pandas as pd




def split_x_y(df,condition):
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    df_full = df.fillna(0)
    train_y = df_full[condition]
    drop_list = conditions+['year','closet_station']
    train_X = df_full.drop(drop_list, axis = 1)
    return train_X,train_y

def clean_X(df):
    df_clean = df.drop(['Date','last_year','month'], axis=1)
    return df_clean

if __name__ == '__main__':
    condition = 'condition|snow'
    df = pd.read_csv('../data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
    df_clean = prep_for_knn(df)
    df_weather,df_weather_dist = get_weather_data()
    neigh = prep_neighbors(df_clean, condition)
    get_neighbors(neigh,df_clean,condition)
    get_closest_station(df_clean,df_weather_dist)
    #merge and save full df
    df_merge = merge_weather_trails(df_weather,df_clean)
    df_final = clean_X(df_merge)
    train_X,train_y = split_x_y(df_merge,condition)
    train_X.to_csv('../data/olympics_final_X_date', sep = '|',index_label=False)
    train_y.to_csv('../data/olympics_final_y_date', sep = '|', index_label=False)
