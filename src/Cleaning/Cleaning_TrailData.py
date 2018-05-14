import numpy as np
import pandas as pd
import math
pd.options.mode.chained_assignment = None  # default='warn'

def stars(string):
    '''Extracts number of stars'''
    lst = string.split()
    return float(lst[0])

def total_dst(string):
    """Extracts mileage from string and calculates total mileage depending on if
    description says one-way or roundtrip."""
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
    """ Adds region and subregion to database"""
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
    # #turns string 'nan' to float 'NaN'
    # db['subregion'] = db[db['super_region'] == 'nan']['super_region']= 'NaN'

# Haversine formula example in Python
# Author: Wayne Dyck

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def distance_from_median(df):
    ''' Calculated distance from median point. Median is just for hood canal'''
    lat2 = 47.7748
    lon2 = -123.1038
    destination = lat2,lon2
    all_hikes = list(df['hike_name'].unique())
    distances = []
    for hike in all_hikes:
        lat1 = df.loc[df['hike_name']== hike]['lat']
        lon1 = df.loc[df['hike_name']== hike]['long']
        origin = float(lat1),float(lon1)
        distances.append(distance(origin,destination))
    return distances


def clean_traildata(hike_df):
    """ Takes in the dataframe, cleans columns, and returns a clean df """
    region_to_subregion(hike_df)
    hike_df['total_distance'] = hike_df[~hike_df['distance'].isna()]['distance'].apply(lambda x: total_dst(x))
    hike_df['stars'] = hike_df[~hike_df['rating'].isna()]['rating'].apply(lambda x: stars(x))
    hike_df['number_votes'] = hike_df['number_votes'].apply(lambda x: float(x))
    hike_df['super_region'] = hike_df['super_region'].apply(lambda x: str(x).strip(' '))
    pass_dummies = pd.get_dummies(hike_df['which_pass'])
    subregion_dummies = pd.get_dummies(hike_df['sub_region'])
    merge_dummies = pd.concat([hike_df,pass_dummies,subregion_dummies],axis=1)
    clean_hikes_df = merge_dummies.drop(['distance','rating','region'],axis=1)
    return clean_hikes_df

if __name__ == '__main__':
    hike_df = pd.read_csv('../../data/WTA_all_trail_data.csv')
    clean_hikes_df = clean_traildata(hike_df)
    hood_df = clean_hikes_df.loc[clean_hikes_df['sub_region'] == ' Hood Canal']
    hood_df['distance_from_median']= distance_from_median(hood_df)
    hood_df.to_csv('../../data/Hood_canal_clean.csv')
