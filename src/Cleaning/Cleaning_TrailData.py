import numpy as np
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
pd.options.mode.chained_assignment = None  # default='warn'

def stars(string):
    """Extracts number of stars and returns start number as a single float."""
    lst = string.split()
    return float(lst[0])

def total_dst(string):
    """
    Extracts mileage from string and calculates total mileage
    depending on if the description says one-way or roundtrip.
    Returns a float.
    """
    miles = []
    try:
        for s in string.split():
            miles.append(float(s))
    except:
        miles.append(string)
    if 'roundtrip' in string:
        return miles[0]
    elif 'one-way' in string:
        return miles[0]*2
    else:
        return miles[0]

def region_to_subregion(db):
    """ Adds region and subregion to database."""
    split = db['region'].apply(lambda x: str(x).split('--'))
    super_region = []
    sub_region = []
    for trail in split:
        if len(trail) == 1:
            super_region.append(trail[0])
            sub_region.append('NaN')
        else:
            super_region.append(trail[0])
            sub_region.append(trail[1])
    db['super_region'] = super_region
    db['sub_region'] = sub_region


# Haversine formula example in Python
# Author: Wayne Dyck

def distance_corr(origin,destination):
    """Calculates distance between two lat/long and returns a float in km."""
    lat1, lon1 = origin
    lat2, lon2 = destination
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def get_medians(df):
    """
    Calculates median point for each sub_region.
    Returns a dictionary with sub_regions as keys and lat,long tuples as values.
    """
    medians = {}
    sub_regions = df['sub_region'].unique()
    for region in sub_regions:
        lat = df[df['sub_region'] == region]['lat'].mean()
        lon = df[df['sub_region'] == region]['lat'].mean()
        medians[region] = (lat,lon)
    return medians

def distance_from_median(df):
    """
    Calculated distance from median point for all hikes.
    Returns a list of distances.
    """
    distances = []
    medians = get_medians(df)
    all_hikes = list(df['hike_name'])
    for hike in all_hikes:
        one_hike = df.loc[df['hike_name']== hike]
        lat1 = one_hike['lat']
        lon1 = one_hike['long']
        origin = float(lat1),float(lon1)
        sub_region = one_hike['sub_region'].values[0]
        destination = medians[sub_region]
        distances.append(distance_corr(origin,destination))
    return distances


def clean_traildata(hike_df):
    """ Cleans columns, adds dummies, drops unused columns, and returns a clean df """
    region_to_subregion(hike_df)
    hike_df['total_distance'] = hike_df[~hike_df['distance'].isna()]['distance'].apply(lambda x: total_dst(x))
    hike_df['stars'] = hike_df[~hike_df['rating'].isna()]['rating'].apply(lambda x: stars(x))
    hike_df['number_votes'] = hike_df['number_votes'].apply(lambda x: float(x))
    hike_df['super_region'] = hike_df['super_region'].apply(lambda x: str(x).strip(' '))
    pass_dummies = pd.get_dummies(hike_df['which_pass'])
    subregion_dummies = pd.get_dummies(hike_df['sub_region'])
    merge_dummies = pd.concat([hike_df,pass_dummies,subregion_dummies],axis=1)
    clean_hikes_df = merge_dummies.drop(['distance','rating','region'],axis=1)
    dropped = clean_hikes_df.sort_values('numReports').drop_duplicates(subset='hike_name', keep= 'last')
    return dropped

if __name__ == '__main__':
    hikes_df = pd.read_csv('../../data/WTA_all_trail_data.csv')
    clean_hikes_df = clean_traildata(hikes_df)
    clean_hikes_df['distance_from_median']= distance_from_median(clean_hikes_df)
    clean_hikes_df.to_csv('../../data/WTA_trails_clean.csv')
