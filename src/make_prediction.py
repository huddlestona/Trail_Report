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

def add_hike_dummy(hike,df):
    hikes = ["Anderson Lake State Park", "Anderson Point", "Appleton Pass",
       "Aurora Creek", "Baldy", "Banner Forest", "Barnes Creek",
       "Big Cedar Tree - Quinault", "Big Creek", "Big Tree Trail",
       "Blue Mountain - Deer Park Snowshoe", "Bogachiel Peak",
       "Bogachiel River", "Boulder Lake (Olympics)", "Buckhorn Mountain",
       "Burfoot Park", "Cape Alava", "Cape Alava Loop (Ozette Triangle)",
       "Cape Flattery", "Capitol State Forest - Capitol Peak",
       "Capitol State Forest - McLane Creek",
       "Capitol State Forest - Mount Molly",
       "Capitol State Forest - Rock Candy Mountain",
       "Capitol State Forest - Sherman Creek Loop", "Cascade Rock",
       "Church Creek", "Clear Creek Trail",
       "Colonel Bob Trail - Colonel Bob Peak", "Constance Pass",
       "Copper Creek", "Cub Peak", "Deadfall", "Deer Park to Maiden Peak",
       "Deer Ridge", "Dirty Face Ridge", "Dodger Point",
       "Dosewallips River Road", "Dosewallips State Park - Steam Donkey Trail",
       "Dry Creek", "Duckabush River", "Dungeness Spit",
       "Eagle Point Snowshoe", "Elbo Creek", "Elk Lakes",
       "Elk Mountain to Maiden Peak", "Elwha River and Geyser Valley",
       "Elwha River and Lillian River", "Elwha To Hurricane Hill",
       "Fallsview Canyon (Falls View)", "Fletcher Canyon",
       "Fort Flagler State Park", "Foulweather Bluff Preserve Trail",
       "Gibbs Lake", "Gladys Divide", "Glines Canyon Overlook Trail",
       "Gold Mountain", "Grand Ridge", "Grand Valley",
       "Grand Valley via Grand Pass Trail", "Graves Creek",
       "Green Mountain - Gold Creek Trail", "Green Mountain - Wildcat Trail",
       "Griff Creek", "Guillemot Cove", "Hall of Mosses", "Hansville Greenway",
       "Happy Lake Ridge", "Harstine Island State Park", "Heart O' the Forest",
       "Heather Creek Trail via Upper Dungeness River", "Heather Park",
       "High Divide - Seven Lakes Basin Loop",
       "Hoh River Trail to Blue Glacier",
       "Hoh River Trail to Five Mile Island", "Home Lake", "Hurricane Hill",
       "Hurricane Ridge Snowshoe", "Illahee Forest Preserve",
       "Indian Island County Park", "Jefferson Ridge",
       "Kalaloch - Browns Point", "Kalaloch Creek Nature Trail",
       "Kestner Homestead", "Klahhane Ridge", "Klahhane Ridge Snowshoe",
       "Kloshe Nanitch", "Kopachuck State Park Trail", "Lake Angeles",
       "Lake Constance", "Lake of the Angels", "Lena Lake",
       "Lena Lake - Valley of Silent Men Snowshoe", "Lightning Peak",
       "Lillian Ridge", "Lillian River", "Little Quilcene River",
       "Lower Big Quilcene River", "Lower Dungeness River",
       "Lower Gray Wolf River", "Lower Pete's Creek","Lower South Fork Skokomish River", "Marmot Pass - Upper Big Quilcene",
       "Marmot Pass via Upper Dungeness River Trail",
       "Mary E. Theler Wetlands Nature Preserve", "Marymere Falls",
       "McCormick Forest Park", "Mildred Lakes",
       "Miller Peninsula-Thompson Spit", "Millersylvania State Park",
       "Mima Mounds", "Mink Lake", "Mink Lake to Little Divide",
       "Mount Angeles", "Mount Angeles Snowshoe", "Mount Ellinor",
       "Mount Jupiter", "Mount Muller", "Mount Rose", "Mount Storm King",
       "Mount Townsend", "Mount Townsend - Silver Lakes Traverse",
       "Mount Townsend Snowshoe", "Mount Walker", "Mount Zion", "Murhut Falls",
       "Ned Hill", "Newberry Hill Heritage Park", "North Coast Route",
       "North Fork Quinault River and Halfway House",
       "North Fork Skokomish River",
       "North Fork Skokomish River and Flapjack Lakes",
       "North Fork Sol Duc River", "Notch Pass", "Olympic Hot Springs",
       "PJ Lake", "Peabody Creek Trail", "Penrose Point State Park",
       "Pete's Creek - Colonel Bob Peak", "Priest Point Park",
       "Pyramid Mountain / Pyramid Peak", "Queets Campground Loop",
       "Queets River", "Quillayute River Slough",
       "Quinault National Recreation Trails",
       "Quinault River-Pony Bridge-Enchanted Valley", "Rain Shadow Loop",
       "Ranger Hole - Interrorem Nature Trail", "Royal Basin - Royal Lake",
       "Ruby Beach", "Second Beach", "Shi Shi Beach and Point of the Arches",
       "Silver Lakes", "Six Ridge", "Slab Camp Creek and Gray Wolf River",
       "Smokey Bottom (West Lake Mills)", "Snider-Jackson Traverse",
       "Sol Duc Falls", "South Coast Wilderness Trail - Toleak Point",
       "South Fork Hoh River - Big Flat", "Spider Lake", "Spoon Creek Falls",
       "Spruce Railroad Trail", "Staircase Rapids", "Striped Peak",
       "Sunnybrook Meadows", "Switchback", "The Brothers", "Third Beach",
       "Three Lakes", "Tubal Cain Mine", "Tubal Cain Mine to Buckhorn Lake",
       "Tumwater Falls Park", "Tunnel Creek",
       "Tunnel Creek - Dosewallips Trailhead", "Twanoh State Park",
       "Upper Dungeness River", "Upper Lena Lake",
       "Upper South Fork Skokomish River", "Valhalla Peak", "Wagonwheel Lake",
       "Watershed Park", "Welch Peaks", "West Elwha",
       "West Fork Dosewallips River", "West Fork Humptulips River",
       "Westport State Park - Westport Light Trail", "Wolf Creek",
       "Wynoochee Lake", "Wynoochee Pass to Sundown Lake"]
    for one_hike in hikes:
        if one_hike == hike:
            df[one_hike] = 1
        else:
            df[one_hike] = 0

def add_dummy_dates(date,df):
    years = [year for year in range(1997,2019)]
    months = [month for month in range(1,13)]
    for year in years:
        if year == date.year:
            df[year] = 1
        else:
            df[year] = 0
    for month in months:
        if month == date.month:
            df[month] = 1
        else:
            df[month] = 0

def clean_for_model(hike,date,df):
    add_hike_dummy(hike,df)
    add_dummy_dates(date,df)
    df_clean = df.drop(['Unnamed: 0','url','which_pass','super_region',
    'sub_region','closet_station','hike_name','last_year','month','year'], axis=1)
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
def make_prediction(X_train,y_train,X_test,model):
    model, pred = model(X_train,y_train,X_test)
    return model,pred


if __name__ == '__main__':
    df = pd.read_csv('../data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
    df_trail = pd.read_csv('../data/WTA_trails_clean_w_medians.csv',lineterminator='\n')
    X_train = pd.read_csv('../data/olympics_final_X',sep = '|',lineterminator='\n')
    y_train = pd.read_csv('../data/olympics_final_y',sep = '|',lineterminator='\n',header=None)
    y_train = y_train.drop([0], axis=1)
    df_weather,df_weather_dist = get_weather_data()
    # hike = input("Where would you like to hike? ")
    # hike_date = input("When do you want to go? ")
    hike = 'Mount Ellinor'
    hike_date = '03/12/18'
    condition = 'condition|snow'
    date = pd.to_datetime(hike_date)
    neighbor_average = get_new_neighbors(df,hike,date,condition)
    hike_df = get_hike_info(hike,df_trail)
    hike_df[f'neighbors_average {condition}'] = neighbor_average
    hike_df['month'] = date.month
    hike_df['year'] = date.year
    hike_df['last_year']= date.year -1
    get_closest_station(hike_df,df_weather_dist)
    hike_all_df = merge_weather_trails(df_weather,hike_df)
    X_test = clean_for_model(hike,date,hike_all_df)
    # X_test.to_csv('../data/olympics_X_test', sep = '|',index_label=False)
    model,pred = make_prediction(X_train,y_train,X_test,make_logistic)
    print (f"There is a {float(pred[:,1])} likelihood of having {condition} at {hike} on {hike_date}")
