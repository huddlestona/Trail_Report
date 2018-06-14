""" This file holds functions to import and merge in weather data."""
import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
from io import BytesIO
import boto3


def get_weather_as_df(keys):
    """
    Use keys to import all weather csvs, downloaded from national weather association
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
        response = s3.get_object(Bucket=bucket_name, Key=key)
        body = response['Body']
        csv = body.read()
        files += csv
    f = BytesIO(files)
    csv = pd.read_csv(f)
    return csv


def get_hike_distance(df1lat, df1long, df2lat, df2long):
    """
    Get distance of two points from eachother.
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


def get_closest_station(df_hike, df_weather):
    """
    Call get_hike_distance on each hike for each weather station.
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
        hike_long = df_hike.loc[hike_idx, 'long']
        hike_lat = df_hike.loc[hike_idx, 'lat']
        distances = []
        for stat_idx in df_weather.index:
            stat_long = df_weather.loc[stat_idx, 'LONGITUDE']
            stat_lat = df_weather.loc[stat_idx, 'LATITUDE']
            distance = get_hike_distance(
                hike_lat, hike_long, stat_lat, stat_long)
            distances.append(distance)
        shortest_idx = np.argmax(distances)
        distance = max(distances)
        station = df_weather.loc[int(shortest_idx), 'name']
        closest_station.append(station)
        station_distance.append(distance)
    df_hike['closet_station'] = closest_station
    df_hike['station_distance'] = station_distance


def clean_weather_df(weather_df):
    """
    Take the weather_df and returns a dataframe with the station name
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
    clean_num = weather_df[weather_df['LATITUDE'].str.contains(
        "LATITUDE") == False]
    num_weather = clean_num.drop(drop_col, axis=1)
    just_num = num_weather.drop(['NAME', 'STATION'], axis=1)
    all_weatherdf = just_num.apply(pd.to_numeric)
    all_weatherdf['name'] = num_weather['NAME']
    return all_weatherdf


def merge_weather_trails(df_weather, df_hike):
    """ Add weather info to df_hike"""
    df_trail_year = pd.merge(
        df_hike, df_weather, how='left', left_on=[
            'closet_station', 'last_year'], right_on=[
            'name', 'DATE'])
    df_all_clean = df_trail_year.drop(['DATE', 'name'], axis=1)
    return df_all_clean


def import_weather(keys):
    """Get weather for mentioned keys."""
    # imports weather and cleans
    df_all_weather = get_weather_as_df(keys)
    return clean_weather_df(df_all_weather)


def get_weather_data():
    """
    Retrieve weather for written keys,prep two dataframes.
    **Input parameters**
    ------------------------------------------------------------------------------
    None. Retreives data internally.
    **Output**
    ------------------------------------------------------------------------------
    df_weather: Pandas dataframe. All goverment weather.
    df_weather_dist: Pandas dataframe. Lat/Long for every weather station.
    """
    keys = ['1364038.csv',
            '1364041.csv',
            '1364042.csv',
            '1364043.csv',
            '1364044.csv',
            '1364046.csv',
            '1364047.csv',
            '1364048.csv',
            '1364051.csv',
            '1364052.csv',
            '1364053.csv',
            '1364054.csv',
            '1364055.csv',
            '1364058.csv',
            '1364059.csv',
            '1364060.csv',
            '1364061.csv',
            '1364062.csv',
            '1364063.csv',
            '1364064.csv',
            '1364066.csv']
    df_weather = import_weather(keys)
    df_weather_dist = df_weather[[
        'LATITUDE', 'LONGITUDE', 'name']].drop_duplicates().reset_index()
    return df_weather, df_weather_dist


if __name__ == '__main__':
    df_weather, df_weather_dist = get_weather_data()
    df_weather.to_csv(
        '../../data/WA_weather_yearly.csv',
        sep='|',
        index_label=False)
    df_weather_dist.to_csv(
        '../../data/WA_weather_distances.csv',
        sep='|',
        index_label=False)
