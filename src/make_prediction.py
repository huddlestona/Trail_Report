
def get_hike_info(hike,df):
    conidtion = 'condition|snow'
    hike_df = df.loc[df['Trail'] == hike]
    df_clean = prep_for_knn(hike_df)
    test = df_clean[df_clean['year'] >= year]
    get_neighbors(test,conditon)
    return test

def prep_input_data(df_test):
    conidtion = 'condition|snow'
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
    test = get_hike_info(hike,df)
    get_closest_station(test,df_weather_dist)
    df_test = merge_weather_trails(df_weather,test)
    test_X = prep_input_data(df_test)    
    print (f"There is a perc. chance of snow on {hike_date} at {hike}")
