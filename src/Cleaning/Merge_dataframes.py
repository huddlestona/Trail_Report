import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
from io import BytesIO
import boto3

keys = ['Global_sum_FIPS:53031 FIPS:53009.csv','Global_sum_FIPS:53045 FIPS:53027.csv']

def get_weather_as_df(keys):
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
        station = df_weather.loc[int(shortest_idx),'NAME']
        closest_station.append(station)
        station_distance.append(distance)
    df_hike['closet_station'] = closest_station
    df_hike['station_distance'] = station_distance

def merge_files(df_trail,df_report):
    """ This function left joins trails and reports, adding trail data to the report you built"""
    df_reports = df_report.drop('Unnamed: 0',axis =1)
    df_trails = df_trail.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    merged = pd.merge(df_reports, df_trails, left_on='Trail', right_on='hike_name', how='left', sort=False)
    return merged



if __name__ == '__main__':
    df_trail = pd.read_csv('../../data/Olympics_189hike_data.csv')
    df_report = pd.read_csv('../../data/WTA_olympics_trailreports_clean.csv', sep = '|', lineterminator='\n')
    merged_df = merge_files(df_trail,df_report)
    merged_df.to_csv('../../data/WTA_olympics_allmerged.csv', sep = '|')
    ###
    df2 = pd.read_csv('../weather_data/1340157.csv')
    df_hike = merged_df
    df_weather = df_weather_spot = df2[['LATITUDE','LONGITUDE','NAME']].drop_duplicates().reset_index()
