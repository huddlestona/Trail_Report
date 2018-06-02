import re
import pandas as import pd
from trail_report.build_model.make_all_predictions import load_databases

def get_all_cond_neighs(X,y):
    """run knn for all conditions"""
    all_indxs = {}
    conditions = ['condition|snow','condition|trail','condition|bugs','condition|road']
    for condition in condtions:
        indxs = get_text_neighbors(condition,X,y)
        all_indxs[condition] = indxs
    return all_indxs


def get_text_neighbors(condition,X,y):
    """run knn for one condition."""
    knn_cols = X[['date_cos','date_sin','PRCP',f'neighbors_average {condition}']]
    knn_y = y[condition]
    neigh = KNeighborsClassifier(n_neighbors=5)
    X_s = scale(knn_cols)
    neigh.fit(X_s,y)
    indxs = neigh.kneighbors()[1]
    return indxs


def neigh_text(df,indxs):
    """Get all text and dates for whole df as a dict"""
    n_text = {}
    for i,idx_neighbors in enumerate(indxs):
        reps= {}
        neighbors = df.iloc[idx_neighbors]['Report']
        date = df.iloc[idx_neighbors]['Date']
        for one_hike,date in zip(neighbors,date):
            reps[date]=(str(one_hike))
        n_text[i] = reps
    return n_text

def get_top_sentences(sentences):
    """Get most-relted sentence for chosen condition. """"
    important = []
    for sentence in sentences:
        consequitivedots.sub('', test_sec)
        key_words = ['bring','snow','need','bugs','mud','washout','safe','danger','crampons','axe','ice','recommend','conditions','help']
        for word in key_words:
            if word in sentence:
                important.append(sentence)
    if len(important) < 1:
        important.append('No relevent reports to show at this time!')
    return set(important)

    #make top sentences for each individual condition- with specific words.

def get_all_tops(all_reps):
    """Cleans and gets all top sentences for all reports"""
    consequitivedots = re.compile(r'\.{3,}')
    top_sentences = {}
    # for i,one in enumerate(n_text):
    for date,rep in all_reps.items():
        no_dots = consequitivedots.sub('', rep)
        all_simple = no_dots.replace("!",".").replace("?",".")
        sentences = all_simple.split('.')
        top_sentences[date]= (get_top_sentences(sentences))
    return top_sentences


if __name__ == '__main__':
    df, df_trail, weather, weather_dist = load_databases()
    reports = df['Report']
    X = pd.read_csv("data/olympics_Xall.csv",delimiter='|')
    y = pd.read_csv("data/olympics_yall.csv",delimiter='|')
    X['report'] = reports

