import numpy as np
import pandas as pd

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


def clean_traildata(hike_df):
    """ Takes in the dataframe, cleans columns, and returns a clean df """
    region_to_subregion(hike_df)
    hike_df['total_distance'] = hike_df[~hike_df['distance'].isna()]['distance'].apply(lambda x: total_dst(x))
    hike_df['stars'] = hike_df[~hike_df['rating'].isna()]['rating'].apply(lambda x: stars(x))
    hike_df['number_votes'] = hike_df['number_votes'].apply(lambda x: float(x))
    hike_df['super_region'] = hike_df['super_region'].apply(lambda x: str(x).strip(' '))
    clean_hikes_df = hike_df.drop(['distance','rating','region'],axis=1)
    return clean_hikes_df

if __name__ == '__main__':
    hike_df = pd.read_csv('../../data/WTA_all_trail_data.csv')
    clean_hikes_df = clean_traildata(hike_df)
    clean_hikes_df.to_csv('../../data/WTA_all_trail_data_clean.csv')
