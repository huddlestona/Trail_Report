from knn_model import prep_neighbors,dates_in_circle

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
    self.reports_df = self.df.loc[df['Trail']== self.hike][[self.condition,'Report','date_cos','date_sin','Votes']]
    neigh = KNeighborsClassifier(n_neighbors=5)
    X = self.reports_df['date_cos','date_sin','Votes']
    y = self.reports_df[condition]
    y = y.astype(bool)
    X_s = scale(X)
    neigh.fit(X_s,y)
    x_input = self.X_test['date_cos','date_sin','Votes']
    neighbors = neigh.kneighbors(x_input)
    self.text_indx = list(neighbors[1][0])


if __name__ == '__main__':
df = pd.read_csv('../data/olympics_merged.csv', sep = '|',lineterminator='\n')
