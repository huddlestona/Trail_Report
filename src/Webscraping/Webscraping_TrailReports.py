"""This file, when called in the terminal will collect all of the trail reports
 for the hikes in the loaded CSV file and load the trail reports into a MongoDB"""
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pymongo
import math
import pandas as pd
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

def select_text(parent_element, css_selector):
    element = parent_element.select_one(css_selector)
    return get_text_if_not_none(element)

def get_text_if_not_none(element):
    if element is None:
        text = None
    else:
        text = element.text
    return text

def select_date(parent_element, css_selector):
    element = parent_element.select_one(css_selector)
    return get_date_if_not_none(element)

def get_date_if_not_none(element):
    if element is None:
        text = None
    else:
        text = element.attrs.get('title')
    return text

def parse_trip_report(title,trip_report_div):
    """Return a dictionary representing a single trip report."""
    creator = select_text(trip_report_div, 'div.CreatorInfo span a')
    date = select_date(trip_report_div, 'span.elapsed-time')
    report = select_text(trip_report_div,'div.show-with-full')
    trail_conditions = select_text(trip_report_div,'div.trail-issues')
    votes = select_text(trip_report_div,'span.UpvoteCount')
    return {
        "Trail": title,
        "Creator": creator,
        "Date": date,
        "Report": report,
        "Trail_condtions": trail_conditions,
        "Votes": votes
    }

def get_trail_report(title, hikeurl, params=None):
    """Accepts a url of the hike, saves all raw html of that hike, then finds all of the subsequent trip reports for that hike,
    scrapes them and inserts them into a MongoDB
    **Input parameters**
    ------------------------------------------------------------------------------
    title: string.  Hike name.
    hikeurl: string. Base URL for the request.
    params: dictionary.  Parameters to be included in the request.
    **Output**
    ------------------------------------------------------------------------------
    None. Appends entry to MongoDB using Pymongo
    """
    r = requests.get(hikeurl + '/@@related_tripreport_listing', params).text
    soup = BeautifulSoup(r, 'lxml')
    save_raw_html(r)
    for trip_report_div in soup.select('div#trip-reports div.item'):
        trip_report = parse_trip_report(title,trip_report_div)
        trail_reports.insert_one(trip_report)
    return None

def save_raw_html(r):
    raw_insert = {"raw_html": r}
    raw_html.insert_one(raw_insert)
    return None

def iterate_all_reports(title, hikeurl):
    """Determines the number of times to call getTripReports function based on
    the number of trip reports listed on the hike homepage.
    **Input parameters**
    ------------------------------------------------------------------------------
    title: string.  Hike name.
    hikeurl: string. Base URL for the request.
    **Output**
    ------------------------------------------------------------------------------
    None. Appends entry to MongoDB using pymongo.
    """
    #lists how many reports are on the page
    r = requests.get(hikeurl + '/@@related_tripreport_listing').text
    soup = BeautifulSoup(r, 'lxml')
    numit = math.ceil(float(soup.find('div', {'id': 'count-data'}).text)/5)
    for i in range(int(numit)):
        get_trail_report(title, hikeurl, params={'b_start:int': str(i*5)})
    return None

def save_trail_html(title,url):
    r = requests.get(url).text
    raw_insert = {'trail': title,
                  "raw_html": r}
    trail_page_raw_html.insert_one(raw_insert)
    return None

def TripReportBuilder(df):
    """Iterates through the rows of loaded pandas dataframe and calls
    iterateTripReports and save_trail_html for each hike/row
    **Input parameters**
    ------------------------------------------------------------------------------
    title: pandas dataframe. Dataframe must contain columns entitled 'numReports'
            and 'hike_name'.
    **Output**
    ------------------------------------------------------------------------------
    None. Calls following functions for input of data into MongoDB using Pymongo
    """
    count = 0
    for row in range(len(df)):
        if df['numReports'][row]:
            title = df['hike_name'][row]
            url = df['url'][row]
            iterate_all_reports(title, url)
            save_trail_html(title, url)
            count += 1
            print (f'Unique Trails {count}')
        else:
            continue
    return None

if __name__ == '__main__':
    mc = pymongo.MongoClient()
    db = mc['wta']
    trail_reports = db['trail_reports']
    raw_html = db['html']
    trail_page_raw_html = db['trail_html']
    trail_reports.drop()
    raw_html.drop()
    trail_page_raw_html.drop()
    hike_urls = pd.read_csv('../../data/Olympics_189hike_data.csv')
    TripReportBuilder(hike_urls)
