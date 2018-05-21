"""
This file, when called in the terminal, will return a predicted probaability
for the chosen condition, date, and hike.
"""
from knn_model import make_logistic,prep_neighbors,dates_in_circle
from Cleaning.Merge_Weather import get_weather_data,get_closest_station,merge_weather_trails

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
        self.df = pd.read_csv('../data/new_olympics_merged.csv', sep = '|',lineterminator='\n')
        self.df_trail = pd.read_csv('../data/WTA_trails_clean_w_medians.csv',lineterminator='\n')

    def get_new_neighbors(self):
        """Get's index of closest 20 neighbors in df."""
        neigh = prep_neighbors(self.df,condition)
        hike_df = self.df.loc[self.df['Trail'] == hike][['highest_point','distance_from_median']]
        hike_df['month'] = date.month
        hike_info = hike_df.iloc[0]
        X = scale(hike_info)
        indx = neigh.kneighbors([X])
        self.indx_list = list(indx[1][0])

    def get_top_text(self):
        #called single_neigh in original
        n_text = []
        neighbors = self.df.iloc[self.indx_list[0:3]]['Report']
        for one in neighbors:
            n_text.append(str(one))
        return "".join(set(n_text))

    def get_condition_averages(self):
        neighbors = self.df.iloc[self.indx_list]
        average = neighbors[self.condition].mean()
        return average


    def Make_Prediction(self):
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
