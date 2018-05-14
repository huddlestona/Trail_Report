""" this file when called in the terminal will merge the trail, report,
and weather dataframes. It also cleans the weathr data"""
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
from io import BytesIO
import boto3

#get weather and prep for merge
def get_weather_as_df(keys):
    """Uses keys to import all weather csvs, downloaded from national weather association
    **Input parameters**
    ------------------------------------------------------------------------------
    keys: list. All links for weather saved in s3
    **Output**
    ------------------------------------------------------------------------------
    csv: pandas df. All opened csvs as a df
    """
    s3 = boto3.client('s3')
    bucket_name = 'trailreportdata'
    files = b''
    for key in keys:
        response = s3.get_object(Bucket= bucket_name, Key= key)
        body = response['Body']
        csv = body.read()
        files+= csv
    f = BytesIO(files)
    csv = pd.read_csv(f)
    return csv

def get_hike_distance(df1lat, df1long,df2lat, df2long):
    """
    **Input parameters**
    ------------------------------------------------------------------------------
    df1lat: int.
    df1long: int.
    df2lat: int.
    df2long: int.
    all inputs are pulled from lat and long in the df
    **Output**
    ------------------------------------------------------------------------------
    distance: int. distance between two points in km
    """
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
    """
    Calls get_hike_distance on each hike for each weather station.
    Adds columns to df_hike

    **Input parameters**
    ------------------------------------------------------------------------------
    df_hike: pandas df
    df_weather: pandas df
    **Output**
    ------------------------------------------------------------------------------
    None. Adds columns to df_hike: closest station and station_distance
    """
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


def clean_weather_df(weather_df):
    """
    Takes the weather_df and returns a dataframe with the station name
    and numeric weather

    **Input parameters**
    ------------------------------------------------------------------------------
    weather_df: pandas df
    **Output**
    ------------------------------------------------------------------------------
    all_weatherdf: pandas df
    """
    col = weather_df.columns
    drop_col = list(col[7::2])
    clean_num = weather_df.drop(319, axis=0)
    num_weather = clean_num.drop(drop_col,axis=1)
    just_num = num_weather.drop(['NAME','STATION'], axis=1)
    all_weatherdf = just_num.apply(pd.to_numeric)
    all_weatherdf['name']= num_weather['NAME']
    return all_weatherdf

#merge all trails together

def merge_trail_files(df_trail,df_report):
    """
    This function left joins trails and reports, adding trail data to the report you built
    **Input parameters**
    ------------------------------------------------------------------------------
    df_trail: pandas df
    df_report: pandas df
    **Output**
    ------------------------------------------------------------------------------
    Merged: Pandas df of reports with added trail information
    """

    # df_reports = df_report.drop('Unnamed: 0',axis =1)
    # df_trails = df_trail.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    merged = pd.merge(df_report, df_trail, left_on='Trail', right_on='hike_name', how='left', sort=False)
    return merged

#to use wheneber reopened as a csv
def change_datetime(df_all):
    """ take the dateframe and turns the Datetime catagory into datetime form"""
    df_all['Datetime'] = df_all['Date'].apply(lambda x: pd.to_datetime(x))
    return df_all

def merge_weather_trails(df_weather,df_hike):
    """ Adds weather info to df_hike"""
    df_trail_year = pd.merge(df_hike, df_weather, how='left', left_on=['closet_station','last_year'], right_on= ['name','DATE'])
    df_all_clean = df_trail_year.drop(['Date','DATE','name'], axis =1)
    return df_all_clean


if __name__ == '__main__':
    #import and merge trail info and trail reports
    df_trail = pd.read_csv('../../data/Hood_canal_clean.csv')
    df_report = pd.read_csv('../../data/WTA_olympics_trailreports_clean.csv', sep = '|', lineterminator='\n')
    merged_df = merge_trail_files(df_trail,df_report)
    # df_hike = change_datetime(merged_df)
    # saves merged without weather
    merged_df.to_csv('../../data/new_hood_canal_merged.csv', sep = '|')
    #keys for getting weather to add
    # keys = ['Global_sum_FIPS:53031 FIPS:53009.csv','Global_sum_FIPS:53045 FIPS:53027.csv']
    # #imports weather and cleans
    # df_all_weather = get_weather_as_df(keys)
    # df_weather_clean = clean_weather_df(df_all_weather)
    # df_weather_distances = df_weather_clean[['LATITUDE','LONGITUDE','name']].drop_duplicates().reset_index()
    # get_closest_station(df_hike,df_weather_distances)
    # #merge and save full df
    # df_hikeweather = merge_weather_trails(df_weather_clean,df_hike)
    # df_hikeweather.to_csv('../../data/Hood_canal_all.csv', sep = '|')
