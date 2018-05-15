from Cleaning.Merge_Weather import import_weather, merge_weather_trails

def prep_for_knn(df):
    df_new = df.drop(['Unnamed: 0','Unnamed: 0_x','Creator','Trail','Report',
    'Votes','_id','last_month','month','Unnamed: 0_y','hike_name','url',

    'super_region','sub_region','monthyear','which_pass'], axis=1)
    df_new['Date'] = pd.to_datetime(df_new['Date'])
    df_new['month'] = df_new['Date'].apply(lambda x: x.month)
    df_full = df_new.fillna(0)
    return df_full

def train_test_split(year,y_val):
    test = df_new[df_new['year'] >= year]
    train = df_new[df_new['year'] < year]
    return test,train

def get_neighbors(df):
    neigh = KNeighborsClassifier(n_neighbors=20)
    X = df[['highest_point','distance_from_median','month']]
    y = df['condition|snow']
    y = y.astype(bool)
    X_s = normalize(scale(X))
    neigh.fit(X_s,y)
    all_n = neigh.kneighbors()
    averages = []
    for idx_neighbors in all_n[1]:
        neighbors = df_d.iloc[idx_neighbors]
        averages.append(neighbors['condition|snow'].mean())
    df['neighbors_average'] = averages

def add_cols(test,train, df_weather_dist):
    get_neighbors(test)
    get_neighbors(train)
    get_closest_station(train,df_weather_dist)
    get_closest_station(test,df_weather_dist)

def get_knn_inputs(df_test,df_train):
    test_y = test['condition|snow']
    test_X = test.drop(['condition|snow', 'condition|trail','condition|bugs',
    'condition|road','Date','last_year','year','station_distance','closet_station'], axis = 1)
    train_y = train['condition|snow']
    train_X = train.drop(['condition|snow', 'condition|trail','condition|bugs',
    'condition|road','Date','last_year','year','station_distance','closet_station'], axis = 1)
    return train_X,train_y,test_X,test_y

def make_forest(X_train,y_train,X_test,y_test):
    model = RandomForestClassifier(n_estimators=500)
    fit = model.fit(X_train,y_train)
    pred = model.predict_proba(X_test)
    #later X_test will be the actual input
    return model, pred

if __name__ == '__main__':
    df = pd.read_csv('data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
    df_clean = prep_for_knn(df)
    test,train = train_test_split(2016)
    keys = ['Global_sum_FIPS:53031 FIPS:53009.csv','Global_sum_FIPS:53045 FIPS:53027.csv']
    df_weather = import_weather(keys)
    df_weather_dist = df_weather[['LATITUDE','LONGITUDE','name']].drop_duplicates().reset_index()
    add_cols(test,train, df_weather_dist)
    #merge and save full df
    df_test = merge_weather_trails(df_weather_clean,test)
    df_train = merge_weather_trails(df_weather_clean,train)
    train_X,train_y,test_X,test_y = get_knn_inputs(df_test,df_train)
    model,pred = make_forest(train_x,train_y,test_x,test_y)
    print (f'final predictions {pred}')
