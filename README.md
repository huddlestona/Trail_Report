# Trail_Report
## Using machine learning to predict probability of impactful hiking trail conditions in Washington to increase trail accessibility and safety.

### Motivation

As an avid hiker, I’ve spent a lot of time on  [Washington Trail Association's](https://www.wta.org/)(WTA) website, scrolling through trail reports to determine current conditions. This often ends with little insight gained, and a risky decision between possibly getting stuck in snow or hiking a popular trail and hoping for a parking spot. I realized providing the probability of trail and road conditions on an easy to access platform could increase a hiker’s likelihood of checking out a less-popular trail, or any trail at all. This would thin out trail use, save time, and increases hiker awareness and safety.

### Product:[Trail-Report.com](http:\\www.trail-report.com)

At trail-report.com you can choose a hike from the dropdown list, select the date you would like to go, and it will return the probability another hiker would report snow, trail, road, or bug conditions on your hike.

Currently, the model is applied to hikes in the Olympic Peninsula. All Washington hikes will be deployed in the near future, alongside text snippets of relevant past reports.

Website created using Flask and self-hosted on AWS.

### Data Used

**Trail Information and Trail Reports:** Scraped through requests and BeautifulSoup from [WTA](https://www.wta.org/). Trail reports begin in 1997 and are continuously scraped to keep the model up to date.

Example of scraped trail information:

![Trail-Infomation](imgs/trail_info_example.png)


Example of scraped trail report:

![Trail-Report](imgs/trail_report_example.png)

**Weather Trends:** Collected as CSVs from [Climate.gov](https://www.climate.gov/maps-data/dataset/past-weather-zip-code-data-table). Trails connected with closest weather station data by lat/log coordinates.

### Modeling

Due to multiple ways to report warnings of trail conditions on [WTA](https://www.wta.org/), my model is built to work with 4 different y variables:
- Significant Snow
- Poor Road Conditions
- Lots Of Bugs/Mosquitos
- Notable Trail Problems

These were measured as boolean values- weather a trail report warned reader of a condition. Logistic Regression, Random Forest, and Gradient boosted models were all tried. While logistic regression gave insight on the type of correlation features had when determining snow conditions, it performed significantly worse predicting other conditions(snow AUC: .95, other conditions: .65 AUC(avg). Using a random forest model was much more consistent across the board with an average AUC score of: .86. A random forest model was ultimately chosen to best represent the data, and further tuned decreasing the log-loss to a 0.44.

To fill in the gaps on trails with less trail reports, KNearestNeighbors was used. Within each sub-region- hike elevation, distance from a median point, and date. The most important aspect of the date were month and day. To capture the date in a non-linear form it was expressed as the cos and sin of the date in radians (with a year representing one circle). With these features, we were able to determine most relevant past trail reports to the model, and get an average of their report of each condition. This model on it's own had an AUC of .62, and became an important feature in the final model.

### Access the project

After cloning the repo the following commands can be run in the terminal from the main folder.

#### Website

`bash run_web_app.sh`


### Future Work
- Add relevant text snippets for each feature using KNN on past trail reports. This feature is currently in production and will be implemented shortly.
- Applying model to all of Washington. Program is currently scaled to scrape and build the model on all WTA reports. Due to the volume of past reports, an AWS EC2 instance or related service is highly recommended for the scraping process. This data is currently being retrieved and will be implemented on the website in the future.
- Combine model with a recommender system to recommend hikers hikes based on their inputed hike preferences and trail conditions.

### Sources
  1. Washington Trails Association. [WTA](https://www.wta.org/).
  2. Images on website used with permission from personal sources.
  3. Jade Tabony's WTA trail recommender system project used as a reference for webscraping - [Repo](https://github.com/Jadetabony/wta_hikes)
