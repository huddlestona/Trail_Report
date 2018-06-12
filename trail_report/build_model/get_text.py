"""This file is still in production. Will eventually be called in make_any_prediction.py"""
from knn_model import prep_neighbors, dates_in_circle
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import scale
from sklearn.preprocessing import normalize
import re

# class TrailText(object):

#     def __init__(self):
#         self.models = {}
#         self.conditions = ['condition|snow', 'condition|trail','condition|bugs','condition|road']
#         self.X_all = pd.read_csv('data/olympics_Xall.csv',sep = '|',lineterminator='\n')
#         self.y_all = pd.read_csv('data/olympics_yall.csv',sep = '|',lineterminator='\n')
#         self.hike_names = pd.read_csv('data/trail_names.csv',sep = '|', lineterminator='\n')
#         self.actual_cols = self.X_all.columns.tolist()

#     def prep_train(self,condition,hike):
#         y_train = self.y_all[condition]

#         X_train = self.X_all[['date_cos','date_sin','PRCP',f'neighbors_average {condition}']]
#         return y_train, X_train

#     def fit(self):
#         for condition in self.conditions:
#             y_train,X_train = self.prep_train(condition)
#             self.models[condition]= text_knn(X_train,y_train)

#     def predict(self):
#         self.pred = {}
#         for condition,model in self.models.items():
#             X = self.X_all[['date_cos','date_sin','PRCP',f'neighbors_average {condition}']]
#             indxs = model.kneighbors(X)
#             self.pred[condition] = list(indxs[1])
    
#     def get_all_text(self):
#         self.all_text = {}
#         for condition,indxs in self.pred.items():
#             condition_text = []
#             for one_rep in indxs:
#                 n_text = neigh_text(df,one_rep)
#                 top = get_all_tops(n_text,condition)
#                 condition_text.append(top)
#             self.all_text[condition] = condition_text

def text_knn(X_train,y_train):
    """ Get neighbors with all X values scaled except trail_id."""
    neigh = KNeighborsClassifier(n_neighbors=5)
    X_s = scale(X_train.drop('trail_ID',axis=1))
    X_frame = pd.DataFrame(X_s)
    X_frame['trail_ID'] = X_train[['trail_ID']]
    neigh.fit(X_frame,y_train)
    return neigh

def neigh_text(df,indxs):
    """ Get all text from KNN indexes."""
    n_text = {}
    reps= {}
    for i,idx_neighbors in enumerate(indxs):
        neighbors = df.iloc[idx_neighbors]['Report']
        date = df.iloc[idx_neighbors]['Date']
        reps[date]= neighbors
        n_text[i] = reps
    return reps

def get_all_tops(all_reps,condition):
    """Clean all knn_text and get senteces for condition reported."""
    consequitivedots = re.compile(r'\.{3,}')
    top_sentences = {}
    for date,rep in all_reps.items():
        no_dots = consequitivedots.sub('', rep)
        all_simple = no_dots.replace("!",".").replace("?",".")
        sentences = all_simple.split('.')
        top_sentences[date]= get_top_sentences(sentences,condition)
    # if len(top_sentences) < 1:
    #     top_sentences['No relivant reports'] = ''
    return top_sentences

def get_top_sentences(sentences,condition):
    """Get sentences with key words in conditions word bucket."""
    bug_keys = ['bugs','mosquito','mosquitos','bugspray','stung','nets']
    snow_keys = ['snow','need','bring','safe','danger','crampons','axe','ice','recommend','conditions','post-holing','slippery','slip']
    road_keys = ['washout','road','closed','potholes','4WD','low clearence','drive']
    trail_keys = ['mud','washout','help','lost','trail','signs']
    
    if condition == 'condition|snow':
        key_words = snow_keys
    elif condition == 'condition|trail':
        key_words = trail_keys
    elif condition == 'condition|bugs':
        key_words = bug_keys
    else:
        key_words = road_keys
    
    important = []
    for sentence in sentences:
        for word in key_words:
            if word in sentence:
                important.append(sentence)
    tops = set(important)
    if len(tops) == 0:
        tops = None 
    return tops

if __name__ == '__main__':
    tt = TrailText()
    tt.fit()
    tt.predict()
    tt.get_all_text()
    print (tt.all_text)