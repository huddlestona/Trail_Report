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



if __name__ == '__main__':
df = pd.read_csv('../data/olympics_merged.csv', sep = '|',lineterminator='\n')
