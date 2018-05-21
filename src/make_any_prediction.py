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

class New_Input(object):
    """A users input of desired trip.
    **Input parameters**
    ------------------------------------------------------------------------------
    hike: location to hike
    date: date of hike
    condition: condition to choose for y value.
    **Output**
    ------------------------------------------------------------------------------
    predicted_proba: float. Predicted probability of chosen condition on date/hike.
    top_text: list. Strings of top related text.
    """

    def __init__(self,hike,date,condition='condition|snow'):
        """Returns a New_Input object with hike choice as hike and date as date."""
        self.hike = hike
        self.date = pd.to_datetime(date)
        self.condition = condition
        self.weather,self.weather_dist = get_weather_data()
        self.df = pd.read_csv('../data/olympics_merged.csv', sep = '|',lineterminator='\n')
        self.df_trail = pd.read_csv('../data/WTA_trails_clean_w_medians.csv',lineterminator='\n')

    def get_new_neighbors(self):
        """Get's index of closest 20 neighbors in df."""
        neigh = prep_neighbors(self.df,self.condition)
        hike_knn_df = self.df.loc[self.df['Trail'] == self.hike][['highest_point','distance_from_median']]
        hike_knn_df['month'] = self.date.month
        hike_info = hike_knn_df.iloc[0]
        X = scale(hike_info)
        indx = neigh.kneighbors([X])
        self.indx_list = list(indx[1][0])

    def text_neighbors_indx(self):
        """
        Takes the df and y condition and returns a fit KNeighborsClassifier.

        **Input parameters**
        ------------------------------------------------------------------------------
        df: pandas df. Dataframe prepped by prep_for_knn
        condition: condition to choose for y value.
        **Output**
        ------------------------------------------------------------------------------
        neigh: Fit KNeighborsClassifier. Fit with highest_point,
        distance_from_median, month of report, all to scale.
        """
        self.reports_df = self.df.loc[self.df['Trail']== self.hike][[self.condition,'Report','date_cos','date_sin','Votes']]
        neigh = KNeighborsClassifier(n_neighbors=5)
        X_all = self.reports_df[['date_cos','date_sin','Votes']]
        X = X_all.fillna(0)
        y = self.reports_df[self.condition]
        y = y.astype(bool)
        X_s = scale(X)
        neigh.fit(X_s,y)
        x_input = self.X_test[['date_cos','date_sin','Votes']]
        neighbors = neigh.kneighbors(x_input)
        self.text_indx = list(neighbors[1][0])

    def get_knn_text(self):
        #called single_neigh in original
        self.text_neighbors_indx()
        n_text = []
        neighbors = self.reports_df.iloc[self.text_indx]['Report']
        for one in neighbors:
            n_text.append(str(one))
        self.n_text = "".join(set(n_text))

    def get_condition_averages(self):
        neighbors = self.df.iloc[self.indx_list]
        average = neighbors[self.condition].mean()
        return average

    def get_hike_info(self):
        self.hike_df = self.df_trail.loc[self.df_trail['hike_name'] == self.hike]

    def prep_data(self):
        self.get_new_neighbors()
        self.get_hike_info()
        self.hike_df[f'neighbors_average {self.condition}'] = self.get_new_neighbors()
        self.hike_df['date'] = self.date
        self.hike_df['month'] = self.date.month
        self.hike_df['year'] = self.date.year
        self.hike_df['last_year']= self.date.year -1
        self.hike_df['date_sin'],self.hike_df['date_cos'] = dates_in_circle(self.hike_df['date'])
        get_closest_station(self.hike_df,self.weather_dist)
        self.hike_all_df = merge_weather_trails(self.weather,self.hike_df)
        self.X_test = self.clean_for_model()

    def clean_for_model(self):
        self.add_hike_dummy()
        df_clean = self.hike_all_df.drop(['url','which_pass','super_region',
        'sub_region','closet_station','hike_name','last_year','month','year','date'], axis=1)
        df_full = df_clean.fillna(0)
        return df_full

    def add_hike_dummy(self):
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
            if one_hike == self.hike:
                self.hike_all_df[one_hike] = 1
            else:
                self.hike_all_df[one_hike] = 0

    def get_train_df(self):
        #add condition as input to call different columns in y_all. y_all should be all possible ys.
        new = ['neighbors_average condition|snow', 'neighbors_average condition|trail',
        'neighbors_average condition|bugs', 'neighbors_average condition|road']
        new.remove(f'neighbors_average {self.condition}')
        X_all = pd.read_csv('../data/olympics_Xall.csv',sep = '|',lineterminator='\n')
        self.X_train= X_all.drop(new,axis=1)
        y_all = pd.read_csv('../data/olympics_yall.csv',sep = '|',lineterminator='\n')
        self.y_train = y_all[self.condition]
        self.actual_cols = self.X_train.columns.tolist()

    def prep_input(self):
        self.prep_data()
        self.get_train_df()

    def make_prediction(self):
        X_test_ordered = self.X_test[self.actual_cols]
        model, pred = make_logistic(self.X_train,self.y_train,X_test_ordered)
        # probability = f"There is a {float(pred[:,1])} likelihood of having {condition} at {hike} on {hike_date}.'
        # hike_info = f'Previous reports for similar hike/weather combinations say'
        # text = [print(text) for text in top_text]
        return pred[:,1]

    def get_top_text(self):
        self.get_knn_text()
        top_sentences = []
        # for i,one in enumerate(n_text):
        sentences = self.n_text.split('.')
        top_sentences.append(self.get_top_sentences(sentences))
        return top_sentences

    def get_top_sentences(self,sentences):
        important = []
        for sentence in sentences:
            key_words = ['bring','snow','need','bugs','mud','washout','safe','danger','crampons','axe','ice','recommend','conditions']
            for word in key_words:
                if word in sentence:
                    important.append(sentence)
        if len(important) < 1:
            important.append('No relevent reports to show at this time!')
        return set(important)

if __name__ == '__main__':
    conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
    hike = 'Mount Rose'
    date = '05/06/18'
    condition = 'condition|bugs'
    snow =  New_Input(hike,date,condition)
    snow_pred = snow.make_prediction()
    top_text = snow.get_top_text()
    print (snow_pred)
