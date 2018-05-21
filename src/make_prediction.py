"""
This file, when called in the terminal, will return a predicted probaability
for the chosen condition, date, and hike.
"""
from knn_model import make_logistic,prep_neighbors,dates_in_circle
from Cleaning.Merge_Weather import get_weather_data,get_closest_station,merge_weather_trails
import pandas as pd
import numpy as np
import math
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize

def get_new_neighbors(df,hike,date,condition):
    """
    Get's mean condition results and top_sentces from knn.

    **Input parameters**
    ------------------------------------------------------------------------------
    df: pandas df. Dataframe prepped by prep_for_knn
    hike: location to hike
    date: date of hike
    condition: condition to choose for y value.
    **Output**
    ------------------------------------------------------------------------------
    neigh: Fit KNeighborsClassifier. Fit with highest_point,
    distance_from_median, month of report, all to scale.
    """
    neigh = prep_neighbors(df,condition)
    hike_df = df.loc[df['Trail'] == hike][['highest_point','distance_from_median']]
    hike_df['month'] = date.month
    hike_info = hike_df.iloc[0]
    X = scale(hike_info)
    indx = neigh.kneighbors([X])
    indx_list = list(indx[1][0])
    neighbors = df.iloc[indx_list]
    average = neighbors[condition].mean()
    hike_text = single_neigh(df,indx_list)
    top_sentences = get_all_tops(hike_text)
    return average,top_sentences

def neigh_text(neigh,df):
    '''works on full datatframe'''
    all_n = neigh.kneighbors(n_neighbors=2)
    n_text = {}
    for i,idx_neighbors in enumerate(all_n[1]):
        reps= []
        neighbors = df.iloc[idx_neighbors]['Report']
        for one in neighbors:
            reps.append(str(one))
        one_set = ''.join(reps)
        n_text[i] = one_set
    return n_text

def single_neigh(df,indx_list):
    n_text = []
    neighbors = df.iloc[indx_list[0:3]]['Report']
    for one in neighbors:
        n_text.append(str(one))
    return "".join(set(n_text))

def get_all_tops(n_text):
    top_sentences = []
    # for i,one in enumerate(n_text):
    sentences = n_text.split('.')
    top_sentences.append(get_top_sentences(sentences))
    return top_sentences

def get_top_sentences(sentences):
    important = []
    for sentence in sentences:
        key_words = ['bring','snow','need','bugs','mud','washout','safe','danger','crampons','axe','ice','recommend','conditions']
        for word in key_words:
            if word in sentence:
                important.append(sentence)
    if len(important) < 1:
        important.append('No relevent reports to show at this time!')
    return set(important)


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
            df[str(year)] = 1
        else:
            df[str(year)] = 0
    for month in months:
        if month == date.month:
            df[str(month)] = 1
        else:
            df[str(month)] = 0

def clean_for_model(hike,date,df):
    add_hike_dummy(hike,df)
    add_dummy_dates(date,df)
    df_clean = df.drop(['Unnamed: 0','url','which_pass','super_region',
    'sub_region','closet_station','hike_name','last_year','month','year','date'], axis=1)
    df_full = df_clean.fillna(0)
    return df_full

def Make_Prediction(hike,hike_date,condition):
    X_train = pd.read_csv('../data/olympics_final_X',sep = '|',lineterminator='\n')
    y_all = pd.read_csv('../data/olympics_final_y',sep = '|',lineterminator='\n',header=None)
    y_train = y_all[1]
    actual_cols = X_train.columns.tolist()
    #need different ys for each conditions
    X_test,top_text = get_X_test(hike,hike_date,condition)
    X_test_ordered = X_test[actual_cols]
    model, pred = make_logistic(X_train,y_train,X_test_ordered)
    # probability = f"There is a {float(pred[:,1])} likelihood of having {condition} at {hike} on {hike_date}.'
    # hike_info = f'Previous reports for similar hike/weather combinations say'
    # text = [print(text) for text in top_text]
    return pred,top_text


def get_X_test(hike,hike_date,condition):
    df = pd.read_csv('../data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
    df_trail = pd.read_csv('../data/WTA_trails_clean_w_medians.csv',lineterminator='\n')
    df_weather,df_weather_dist = get_weather_data()
    date = pd.to_datetime(hike_date)
    neighbor_average,top_text = get_new_neighbors(df,hike,date,condition)
    hike_df = get_hike_info(hike,df_trail)
    hike_df[f'neighbors_average {condition}'] = neighbor_average
    hike_df['date'] = date
    # hike_df['top_sentences'] = len(top_text)
    hike_df['month'] = date.month
    hike_df['year'] = date.year
    hike_df['last_year']= date.year -1
    hike_df['date_sin'],hike_df['date_cos'] = dates_in_circle(hike_df['date'])
    get_closest_station(hike_df,df_weather_dist)
    hike_all_df = merge_weather_trails(df_weather,hike_df)
    X_test = clean_for_model(hike,date,hike_all_df)
    # X_test.to_csv('../data/X_test_testit.csv', sep = '|',index_label=False)
    return X_test,top_text

def all_predictions(hike,hike_date):
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    predictions = []
    for condition in conditions:
        pred = Make_Prediction(hike,hike_date,condition)
        predictions.append(pred)
    return predictions


if __name__ == '__main__':
    hike = 'Mount Rose'
    hike_date = '05/06/18'
    condition = 'condition|snow'
    pred,top_text = Make_Prediction(hike,hike_date,condition)
    print(pred)
    # predictions = all_predictions(hike,hike_date)
    # [print(pred) for pred in predictions]
