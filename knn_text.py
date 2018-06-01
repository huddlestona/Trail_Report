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

def get_hike_reports(df,hike):
return df.loc[df['Trail']== hike][[condition,'Report','date_cos','date_sin','Votes']]

def text_neighbors_indx(df,hike):
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
self.reports_df = self.df.loc[df['Trail']== self.hike][[self.condition,'Report','date_cos','date_sin','PRCP']]
neigh = KNeighborsClassifier(n_neighbors=5)
X = self.reports_df['date_cos','date_sin','Votes']
y = self.reports_df[condition]
y = y.astype(bool)
X_s = scale(X)
neigh.fit(X_s,y)
x_input = self.X_test['date_cos','date_sin','Votes']
neighbors = neigh.kneighbors(x_input)
self.text_indx = list(neighbors[1][0])