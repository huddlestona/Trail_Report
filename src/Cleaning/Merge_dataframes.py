import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
from io import BytesIO
import boto3


def get_weather_as_df(keys):
    s3 = boto3.client('s3')
    bucket_name = 'trailreportdata'
    files = b''
    for key in keys:
        response = s3.get_object(Bucket= bucket_name, Key= key)
        body = response['Body']
        csv = body.read()
        files+= csv
    f = BytesIO(files)
    return pd.read_csv(f)

def get_hike_distance(df1lat, df1long,df2lat, df2long):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(df1lat)
    lon1 = radians(df1long)
    lat2 = radians(df2lat)
    lon2 = radians(df2long)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def get_closest_station(df_hike,df_weather):
    closest_station = []
    station_distance = []
    for hike_idx in df_hike.index:
        hike_long = df_hike.loc[hike_idx,'long']
        hike_lat = df_hike.loc[hike_idx,'lat']
        distances = []
        for stat_idx in df_weather.index:
            stat_long = df_weather.loc[stat_idx,'LONGITUDE']
            stat_lat = df_weather.loc[stat_idx,'LATITUDE']
            distance = get_hike_distance(hike_lat, hike_long,stat_lat, stat_long)
            distances.append(distance)
        shortest_idx = np.argmax(distances)
        distance = max(distances)
        station = df_weather.loc[int(shortest_idx),'name']
        closest_station.append(station)
        station_distance.append(distance)
    df_hike['closet_station'] = closest_station
    df_hike['station_distance'] = station_distance

def merge_trail_files(df_trail,df_report):
    """ This function left joins trails and reports, adding trail data to the report you built"""
    df_reports = df_report.drop('Unnamed: 0',axis =1)
    df_trails = df_trail.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    merged = pd.merge(df_reports, df_trails, left_on='Trail', right_on='hike_name', how='left', sort=False)
    return merged

def clean_weather_df(weather_df):
    col = weather_df.columns
    drop_col = list(col[7::2])
    clean_num = weather_df.drop(319, axis=0)
    num_weather = clean_num.drop(drop_col,axis=1)
    just_num = num_weather.drop(['NAME','STATION'], axis=1)
    all_weatherdf = just_num.apply(pd.to_numeric)
    all_weatherdf['name']= num_weather['NAME']
    return all_weatherdf

def add_to_merged_df(df_all):
    df_all['Datetime'] = df_all['Date_type'].apply(lambda x: pd.to_datetime(x))
    df_all['last_year']= df_all['Datetime'].apply( lambda x: x.year-1)
    return df_all

def merge_weather_trails(df_weather,df_hike):
    df_trail_year = pd.merge(df_hike, df_weather, how='left', left_on=['closet_station','last_year'], right_on= ['name','DATE'])
    df_all_clean = df_trail_year.drop(['Date_type','DATE','name'], axis =1)
    return df_all_clean

def pred_x(all_x):
    all_x.drop(['Creator','Trail','_id', 'hike_name','url','super_region'], axis = 1)
    x['month'] = x['Datetime'].apply( lambda x: x.month + x.year)
    x['year'] = x['Datetime'].apply( lambda x: x.year)
    x['monthyear'] = x['Datetime'].apply( lambda x: str(x.month)+'-'+str(x.year))
    month_dum = pd.get_dummies(x['month'])
    year_dum = pd.get_dummies(x['year'])
    monthyear_dummies = pd.get_dummies(x['monthyear'])
    pass_dummies = pd.get_dummies(x['which_pass'])
    subregion_dummies = pd.get_dummies(x['sub_region'])
    all_x = pd.concat([x,monthyear_dummies,subregion_dummies], axis = 1)
    final_x = all_x.drop(['Unnamed: 0','Date_type','month','year','monthyear','sub_region','which_pass','Datetime','last_year','closet_station'], axis=1)
    X = final_x.fillna(0)
    return X

if __name__ == '__main__':
    df_trail = pd.read_csv('../../data/Olympics_189hike_data.csv')
    df_report = pd.read_csv('../../data/WTA_olympics_trailreports_clean.csv', sep = '|', lineterminator='\n')
    merged_df = merge_trail_files(df_trail,df_report)
    # merged_df.to_csv('../../data/WTA_olympics_allmerged.csv', sep = '|')
    ###
    keys = ['Global_sum_FIPS:53031 FIPS:53009.csv','Global_sum_FIPS:53045 FIPS:53027.csv']
    df_all_weather = get_weather_as_df(keys)
    df_weather_clean = clean_weather_df(df_all_weather)
    df_all = add_to_merged_df(merged_df)
    df_hike = df_all
    df_weather_distances = df_weather_clean[['LATITUDE','LONGITUDE','name']].drop_duplicates().reset_index()
    get_closest_station(df_hike,df_weather_distances)
    df_hikeweather = merge_weather_trails(df_weather_clean,df_hike)
    df_hikeweather.to_csv('../../data/WTA_olympics_merged_yearlyweather', sep = '|')
