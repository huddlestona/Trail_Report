"""
This file, when called in the terminal, will add new features,merge
in the weather dataframe, and save the final X and Y databases.
"""
from .merge_weather import get_weather_data, merge_weather_trails, get_closest_station
from .knn_model import prep_for_knn,prep_neighbors,get_neighbors
import pandas as pd

def split_x_y(df):
    """Fill in nas and splits data with y being the inputed conditon column."""
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    df_full = df.fillna(0)
    train_y = df_full[conditions]
    drop_list = conditions+['year','closet_station']
    train_X = df_full.drop(drop_list, axis = 1)
    return train_X,train_y

def clean_X(df):
    """Drop unneeded colums in df."""
    df_clean = df.drop(['Date','last_year','month','DX90', 'FZF4', 'FZF3', ' Snoqualmie Pass', 'Waterfalls', 'FZF1', 'FZF8', 'FZF6', 'None', 'Sno-Parks Permit', 'Dogs not allowed', 'FZF0', 'FZF5', 'National Park Pass', 'Discover Pass', 'NaN', ' North Bend Area', ' Salmon La Sac/Teanaway', 'Coast', ' Chinook Pass - Hwy 410', ' SW - Longmire/Paradise', ' Mountain Loop Highway', ' Hood Canal', ' NE - Sunrise/White River', ' Mount Baker Area', ' Stevens Pass - West', ' Stevens Pass - East', ' North Cascades Highway - Hwy 20', " SE - Cayuse Pass/Steven's Canyon", ' Mount Adams Area', ' Leavenworth Area', ' Mount St. Helens', ' Northern Coast', ' White Pass/Cowlitz River Valley', 'WSF5', 'WDF5', 'WDF2', ' Goat Rocks', 'WSF2', 'AWND', ' Yakima', ' Seattle-Tacoma Area', ' Columbia River Gorge - WA', ' Blewett Pass', ' Pacific Coast', ' Methow/Sawtooth', ' Olympia', ' Lewis River Region', ' Tiger Mountain', ' Bellingham Area', ' Entiat Mountains/Lake Chelan', ' Pasayten', " Spokane Area/Coeur d'Alene", ' Dark Divide', ' Columbia River Gorge - OR', 'Wilderness permit. Self-issue at trailhead (no fee)', ' Wenatchee', 'National Monument Fee', 'Discover Pass, Sno-Parks Permit', ' Okanogan Highlands/Kettle River Range', 'National Monument Fee, Sno-Parks Permit', ' Palouse and Blue Mountains', ' Selkirk Range', ' Cougar Mountain', ' Squak Mountain', ' Tri-Cities', ' Kitsap Peninsula', ' Grand Coulee', 'None, Northwest Forest Pass', 'Refuge Entrance Pass', ' Potholes Region', ' Cle Elum Area', ' Whidbey Island', ' San Juan Islands', ' Long Beach Area', ' Vancouver Area', 'Oregon State Parks Day-Use', ' Orcas Island', 'Fall foilage', 'Backcountry camping permit. Register in person at ranger station (no fee)', 'Northwest Forest Pass, Sno-Parks Permit', 'PSUN', 'WDMV'],
                                axis=1)
    return df_clean

def add_knn(df):
    """
    Prep data for knn, runs knn, and adds knn past report values as column in df.
    **Input parameters**
    ------------------------------------------------------------------------------
    df: pandas dataframe of merged trail data and trail reports
    condition: condition being used as y.
    **Output**
    ------------------------------------------------------------------------------
    df_clean: pandas dataframe. Clean results to be merged, with neighbors added.
    """
    df_clean = prep_for_knn(df)
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    for condition in conditions:
        neigh = prep_neighbors(df_clean, condition)
        get_neighbors(neigh,df_clean,condition)
    return df_clean

def add_trail_id(df):
    """ Counts numbers of each trail and gives unique trail ID. """
    num_reports = df.groupby('Trail').count()['Date']
    trail_id = []
    for num,count in enumerate(num_reports):
            appends = 0
            while appends < count:
                trail_id.append(num*1000)
                appends += 1
    df['trail_ID'] = trail_id

def merge_all_files(df_clean):
    """Take clean df and adds weather by nearest station."""
    df_weather,df_weather_dist = get_weather_data()
    get_closest_station(df_clean,df_weather_dist)
    df_merge = merge_weather_trails(df_weather,df_clean)
    return df_merge

def make_split_dataframes(df):
    """ Prep dataframe to be saved as X,y. """
    add_trail_id(df)
    df_clean = add_knn(df)
    df_merge = merge_all_files(df_clean)
    df_final = clean_X(df_merge)
    train_X,train_y = split_x_y(df_final)
    return train_X,train_y

if __name__ == '__main__':
    df = pd.read_csv('../../data/WTA_all_merged.csv', sep = '|',lineterminator='\n')
    train_X,train_y = make_split_dataframes(df)
    train_X.to_csv('../../data/Xall.csv', sep = '|',index_label=False)
    train_y.to_csv('../../data/yall.csv', sep = '|', index_label=False)
