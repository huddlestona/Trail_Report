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
    average = neighbors[condition]
    print(hike,date,condition)
    return neighbors

def get_hike_info(hike,df):
    condition = 'condition|snow'
    hike_df = df.loc[df['Trail'] == hike]
    df_clean = prep_for_knn(hike_df)
    test = df_clean[df_clean['year'] >= 2017]
    return test

def prep_input_data(df_test):
    condition = 'condition|snow'
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    drop_list = conditions+['last_year','year',
    'station_distance','closet_station']
    test_X = df_test.drop(drop_list, axis = 1)
    test_X = test_X.fillna(0)
    return test_X

if __name__ == '__main__':
    df = pd.read_csv('../data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
    df_weather,df_weather_dist = get_weather_data()
    hike = input("Where would you like to hike? ")
    hike_date = input("When do you want to go? ")
    date = date = pd.to_datetime(hike_date)
    test = get_hike_info(hike,df)
    get_closest_station(test,df_weather_dist)
    df_test = merge_weather_trails(df_weather,test)
    test_X = prep_input_data(df_test)
    print (f"There is a perc. chance of snow on {hike_date} at {hike}")
