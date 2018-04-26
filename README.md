# Trail_Report
## Using Machine Learning to predict hiking trail conditions and features to increase trail accessability and safety in off-seasons   

### Business Understanding:

Often when looking for a hike in winter and spring, it is hard to get a sense of what current trail conditions are like. It is common to go read the recent reports and realize no one has written a report in the last 5 years for the season you are hiking in. A predictive report will give off-season hikers more confidence in exploring different areas. This report would have users input a trail and a date, and return the likelihood of snow on the trails, need for season specific gear, if the wildflowers are in bloom, etc. 

### Data Understanding:

I plan to use WTA trip reports(using python NLP modules), WTA trail information (elevation, log/lat, length, etc.), past eather paterns, and current/future weather patterns to predict future key words that would be written in trail reports. I will use the past two years trail reports as training data (may increase in size due to some trails not having trip reports for a few years back). 

### Data Gathering:

**WTA:** Trip reports and trail information, gathered through requests and scraping 

**Past Weather Reports:** CSV form from https://www.climate.gov/maps-data/dataset/past-weather-zip-code-data-table
- Plan to pull from all of washington and align with data by closest lat/log and elevation

**Current weather:** Various public APIs, limit of 1000 pulls per day without paying. Will either use limited location reports or limited days for reports. Currently getting in touch with previous students who have worked with weather data. 

### Data Preparation:

**Trip Reports**:

- Overall:  Report info, date/time, conditions, warnings, photo descriptions, if photo was posted
- Each report: Use NLP to pull out keywords that indicate snow/ice or other trail conditions. Create catagorical features.
- Trail overall: Elevation gain, lat/log, use during seasons in the past

**Past Weather**:

- Collect in a CSV, for each trip report add features for the weather for that day as well as a summary of the 3 months (or other lengths) leading up to the date

**Current Weather**:

- Take current days weather and the past month-3 months weather average into datebase
- Also account for future weather predictions

### Modeling:

**Output**: 

Trail conditions: Starting focus will be snow/ice amount. Could add flower blooming/waterfall strength/ fallen trees/ etc. This will be a list of potential things a hiker should be aware of going to the trail, with the likelihood of each aspect. (75% chance snow on trail, 20% chance need to bring crampons)

**Model Type**:

I plan to use Supervised learning, testing all basic model types. Could potentially use some unsupervised learning to gain insight into how to catagorize trails across different seasons. Potential use of a neaural network- need more research.

Training group will be all data collected up to a certain date (plan on cutoff being Jan 2016). All trip reports after that will be used to test. See if keywords in new trip reports match predicted key words and snow levels found by the model. Also will go hike places and see if the conditions are as predicted/ have other people report back when they go hiking.

**Potential issues**: 

Some trip reports have very little reports to base off. More reports during the summer and spring may add skew. May not be able to accuratly use predicitve weather. 

### Deployment

Website for consumers to search for trip reports on  
