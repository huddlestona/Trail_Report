"""This file holds functions that get new and prep new data, then make predictions."""
from .knn_model import prep_neighbors, dates_in_circle, prep_for_knn, make_forest
from .merge_weather import get_weather_data, get_closest_station, merge_weather_trails
from .get_text import text_knn,neigh_text,get_all_tops,get_top_sentences
import pandas as pd
import numpy as np
import math
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
import pickle
import boto3
from io import BytesIO
import os.path
import io


def get_data(hike, date, df_init, df_trail, weather, weather_dist):
    """Load,prep, and clean data needed from hikers input."""
    df = df_init.fillna(0)
    add_trail_id(df_init,df_trail,hike)
    hike_df = df_trail.loc[df_trail['hike_name'] == hike]
    date_stamp = pd.to_datetime(date)
    conditions = [
        'condition|snow',
        'condition|trail',
        'condition|bugs',
        'condition|road']
    for condition in conditions:
        hike_df[f'neighbors_average {condition}'] = get_new_neighbors(
            df, condition, hike, date_stamp)
    hike_df['date'] = date_stamp
    hike_df['month'] = date_stamp.month
    hike_df['year'] = date_stamp.year
    hike_df['last_year'] = date_stamp.year - 1
    hike_df['date_sin'], hike_df['date_cos'] = dates_in_circle(hike_df['date'])
    get_closest_station(hike_df, weather_dist)
    hike_all_df = merge_weather_trails(weather, hike_df)
    X_test = clean_for_model(hike_all_df)
    Text_X_test_all = hike_all_df[['date_cos','date_sin','PRCP',f'neighbors_average {condition}','trail_ID']]
    Text_X_test = Text_X_test_all.fillna(0)
    return X_test, Text_X_test


def add_trail_id(df,df_trail,hike):
    """ Counts numbers of each trail and gives unique trail ID. """
    num_reports = df.groupby('Trail').count()['Date']
    trail_id = []
    for num,count in enumerate(num_reports):
            appends = 0
            while appends < count:
                trail_id.append(num*1000)
                appends += 1
    df['trail_ID'] = trail_id
    df_trail['trail_ID'] = df.loc[df['Trail'] == hike]['trail_ID'].iloc[0]



def load_databases():
    """Load databases of hike and weather info."""
    df_trail,df_init = get_hike_data()
    weather,weather_dist = get_weather_data()
    return df_init, df_trail, weather, weather_dist

def get_weather_data():
    """Load weather data as pandas df."""
    weather_dist = pd.read_csv(
    'data/WA_weather_distances.csv',
    sep='|',
    lineterminator='\n')
    weather = pd.read_csv(
    'data/WA_weather_yearly.csv',
    sep='|',
    lineterminator='\n')
    return weather,weather_dist

def get_hike_data():
    """Load trail and report db from public s3 bucket."""
    #get_trail
    df_trail = pd.read_csv(
    'data/WTA_trails_clean_w_medians.csv',
    lineterminator='\n')
    #get_reports
    s3 = boto3.client('s3')
    bucket_name = 'trailreportdata'
    files = b''
    response = s3.get_object(Bucket=bucket_name, Key= 'WTA_all_merged.csv')
    body = response['Body']
    csv = body.read()
    files += csv
    f = BytesIO(files)
    df_init = pd.read_csv(f,sep = '|',lineterminator='\n')
    # with BytesIO() as trails:
    #     s3.Bucket(bucket_name).download_fileobj("WTA_trails_clean_w_medians.csv", trails)
    #     trails.seek(0)
    #     df_trail = pd.read_csv(trails)

    # with BytesIO() as reports:
    #     s3.Bucket(bucket_name).download_fileobj("WTA_all_merged.csv", reports)
    #     reports.seek(0)
    #     df = pd.read_csv(reports)

    return df_trail, df_init
    

def get_new_neighbors(df, condition, hike, date_stamp):
    """Get index of closest 20 neighbors in df."""
    neigh = prep_neighbors(df, condition)
    hike_knn_df = df.loc[df['Trail'] == hike][[
        'highest_point', 'distance_from_median']]
    hike_knn_df['month'] = date_stamp.month
    hike_info = hike_knn_df.iloc[0]
    X = scale(hike_info)
    indx = neigh.kneighbors([X])
    indx_list = list(indx[1][0])
    averages = get_condition_averages(df, indx_list, condition)
    return averages


def get_condition_averages(df, indx_list, condition):
    """Take average of all KNN condition reports."""
    neighbors = df.iloc[indx_list]
    average = neighbors[condition].mean()
    return average


def clean_for_model(hike_all_df):
    """Prep correct columns for model and fill NANS."""
    df_clean = hike_all_df.drop(['url',
                                 'which_pass',
                                 'super_region',
                                 'sub_region',
                                 'closet_station',
                                 'hike_name',
                                 'last_year',
                                 'month',
                                 'year',
                                 'date',
                                 'Unnamed: 0','DX90', 'FZF4', 'FZF3', ' Snoqualmie Pass', 'Waterfalls', 'FZF1', 'FZF8', 'FZF6', 'None', 'Sno-Parks Permit', 'Dogs not allowed', 'FZF0', 'FZF5', 'National Park Pass', 'Discover Pass', 'NaN', ' North Bend Area', ' Salmon La Sac/Teanaway', 'Coast', ' Chinook Pass - Hwy 410', ' SW - Longmire/Paradise', ' Mountain Loop Highway', ' Hood Canal', ' NE - Sunrise/White River', ' Mount Baker Area', ' Stevens Pass - West', ' Stevens Pass - East', ' North Cascades Highway - Hwy 20', " SE - Cayuse Pass/Steven's Canyon", ' Mount Adams Area', ' Leavenworth Area', ' Mount St. Helens', ' Northern Coast', ' White Pass/Cowlitz River Valley', 'WSF5', 'WDF5', 'WDF2', ' Goat Rocks', 'WSF2', 'AWND', ' Yakima', ' Seattle-Tacoma Area', ' Columbia River Gorge - WA', ' Blewett Pass', ' Pacific Coast', ' Methow/Sawtooth', ' Olympia', ' Lewis River Region', ' Tiger Mountain', ' Bellingham Area', ' Entiat Mountains/Lake Chelan', ' Pasayten', " Spokane Area/Coeur d'Alene", ' Dark Divide', ' Columbia River Gorge - OR', 'Wilderness permit. Self-issue at trailhead (no fee)', ' Wenatchee', 'National Monument Fee', 'Discover Pass, Sno-Parks Permit', ' Okanogan Highlands/Kettle River Range', 'National Monument Fee, Sno-Parks Permit', ' Palouse and Blue Mountains', ' Selkirk Range', ' Cougar Mountain', ' Squak Mountain', ' Tri-Cities', ' Kitsap Peninsula', ' Grand Coulee', 'None, Northwest Forest Pass', 'Refuge Entrance Pass', ' Potholes Region', ' Cle Elum Area', ' Whidbey Island', ' San Juan Islands', ' Long Beach Area', ' Vancouver Area', 'Oregon State Parks Day-Use', ' Orcas Island', 'Fall foilage', 'Backcountry camping permit. Register in person at ranger station (no fee)', 'Northwest Forest Pass, Sno-Parks Permit', 'PSUN', 'WDMV'],
                                axis=1)
    df_full = df_clean.fillna(0)
    return df_full


class TrailPred(object):

    def __init__(self):
        """ Get data and save preped models."""
        self.pred_models = {}
        self.text_models = {}
        self.conditions = [
            'condition|snow',
            'condition|trail',
            'condition|bugs',
            'condition|road']
        self.X_train = pd.read_csv(
            'data/Xall.csv',
            sep='|',
            lineterminator='\n')
        self.y_all = pd.read_csv(
            'data/yall.csv',
            sep='|',
            lineterminator='\n')
        self.actual_cols = self.X_train.columns.tolist()

    def prep_train(self, condition):
        """Make train set for for single condition."""
        y_train = self.y_all[condition]
        Text_X_train = self.X_train[['date_cos','date_sin','PRCP',f'neighbors_average {condition}','trail_ID']]
        return y_train, Text_X_train

    def fit(self):
        """ Fit model for each condition."""
        for condition in self.conditions:
            y_train, Text_X_train = self.prep_train(condition)
            self.pred_models[condition] = make_forest(self.X_train, y_train)
            self.text_models[condition]= text_knn(Text_X_train,y_train)

    def predict(self, X_test):
        """ Make prediction for each condition."""
        pred = {}
        for condition, model in self.pred_models.items():
            pred[condition] = model.predict_proba(X_test[self.actual_cols])
        return pred

    def predict_text(self, Text_X_test,df,hike):
        """ Get index of KNN text."""
        self.text_pred = {}
        for condition,model in self.text_models.items():
            indxs = model.kneighbors(Text_X_test)[1][0]
            hikes = df.iloc[indxs]['Trail']
            actual_indxs = []
            for indx,trail in zip(indxs,hikes):
                if trail == hike:
                    actual_indxs.append(indx)
            self.text_pred[condition] = list(actual_indxs)
        self.get_all_text(df)

    def get_all_text(self,df):
        """ Collect and clean KNN text."""
        self.all_text = {}
        no_reports = 'No relevant reports from this hike right now! Let WTA know how the hike was for you, and we will update our database!'
        for condition,indxs in self.text_pred.items():
            if len(indxs) < 1:
                self.all_text[condition] = no_reports
            else:
                n_text = neigh_text(df,indxs)
                top = get_all_tops(n_text,condition)
                # condition_text = []
                # for one_rep in indxs:
                #     n_text = neigh_text(df,one_rep)
                #     top = get_all_tops(n_text,condition)
                #     condition_text.append(top)
                if len(top) < 1:
                    self.all_text[condition] = no_reports
                else:
                    self.all_text[condition] = top


def get_pickle():
    """
    Access pickle of all fit models from public s3 bucket
    **Input parameters**
    ------------------------------------------------------------------------------
    None.
    **Output**
    ------------------------------------------------------------------------------
    tp: dictionary built by class tp. Keys: conditions, values:fit models
    """
    s3 = boto3.resource('s3')
    with BytesIO() as data:
        s3.Bucket("trailreportdata").download_fileobj("tp_sm.pkl", data)
        data.seek(0)    # move back to the beginning after writing
        tp = pickle.load(data)
    return tp


def main_dump():
    """Dump models to a pickle."""
    df_init, df_trail, weather, weather_dist = load_databases()
    tp = TrailPred()
    tp.fit()
    #Save model
    file_path = "tp_sm.pkl"
    n_bytes = 2**31
    max_bytes = 2**31 - 1
    data = tp
    ## write
    bytes_out = pickle.dumps(data)
    with open(file_path, 'wb') as f_out:
        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx+max_bytes])

def get_relivant_text(reports):
    returns = ''
    for group in reports:
        for year,parts in group.items():
            returns += f"On {year} Reports say: <br /> <br />"
            for sent in parts:
                returns += u'\u2022 '
                returns += sent
                returns += "<br />"
            returns += "<br />"
    return returns

def main_pred():
    """Get pickle and make prediction."""
    hike = 'Mount Rose'
    date = '05/22/18'
    df_init, df_trail, weather, weather_dist = load_databases()
    X_test, Text_X_test = get_data(hike, date,df_init, df_trail, weather, weather_dist)
    # with open('tp.pkl','rb') as f:
    #     tp = pickle.load(f)
    tp = get_pickle()
    tp.predict_text(Text_X_test,df_init)
    pred = tp.predict(X_test)
    snow_text = get_relivant_text(tp.all_text['condition|snow'])
    trail_text = get_relivant_text(tp.all_text['condition|trail'])
    bugs_text= get_relivant_text(tp.all_text['condition|bugs'])
    road_text = get_relivant_text(tp.all_text['condition|road'])
    print (pred,snow_text,trail_text,bugs_text,road_text)


if __name__ == '__main__':
    main_dump()
