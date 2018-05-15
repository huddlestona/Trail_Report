from knn_model import *
from Cleaning.Merge_Weather import *

def get_new_neighbors(df,hike,date,condition):
    neigh = prep_neighbors(df,condition)
    hike_df = df.loc[df['Trail'] == hike][['highest_point','distance_from_median']]
    hike_df['month'] = date.month
    hike_info = hike_df.iloc[0]
    X = scale(hike_info)
    indx = neigh.kneighbors([X])
    indx_list = list(indx[1][0])
    neighbors = df.iloc[indx_list]
    average = neighbors[condition].mean()
    return average

def get_hike_info(hike,df):
    condition = 'condition|snow'
    hike_df = df.loc[df['hike_name'] == hike]
    return hike_df

def clean_for_model(df):
    df_clean = df.drop(['Unnamed: 0','hike_name','url','which_pass','super_region',
    'sub_region','closet_station'], axis=1)
    df_full = df_clean.fillna(0)
    return df_full

# def prep_input_data(df_test):
#     condition = 'condition|snow'
#     conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
#     drop_list = conditions+['last_year','year',
#     'station_distance','closet_station']
#     test_X = df_test.drop(drop_list, axis = 1)
#     test_X = test_X.fillna(0)
#     return test_X

if __name__ == '__main__':
    df = pd.read_csv('../data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
    trail_df = pd.read_csv('../data/WTA_trails_clean_w_medians.csv',lineterminator='\n')
    df_weather,df_weather_dist = get_weather_data()
    hike = input("Where would you like to hike? ")
    hike_date = input("When do you want to go? ")
    condition = 'condition|snow'
    date = pd.to_datetime(hike_date)
    neighbor_average = get_new_neighbors(df,hike,date,condition)
    hike_df = get_hike_info(hike,df)
    hike_df[f'neighbors_average {condition}'] = neighbor_average
    get_closest_station(hike_df,df_weather_dist)
    hike_all_df = merge_weather_trails(df_weather,hike_df)
    X_test = clean_for_model(hike_all_df)
    print (f"There is a perc. chance of snow on {hike_date} at {hike}")
