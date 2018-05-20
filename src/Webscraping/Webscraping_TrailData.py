"""
This file, when called in the terminal will collect all WTA hike urls
from given start url, save all the pernient data for that hike as a csv,
and save the hikes webpage in a MongoDB.
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sn
import re
import math
import csv

def iterate_all_reports(starturl):
    """
    Determines the number of hikes listed on the WTA trails page and get said number of report urls
    **Input parameters**
    ------------------------------------------------------------------------------
    starturl: string. Base URL for the request.
    **Output**
    ------------------------------------------------------------------------------
    hike_urls: list. Returns a list of all hike urls
    """
    hike_urls = []
    counter = 0
    r = requests.get(starturl).text
    soup = BeautifulSoup(r, 'lxml')
    trail_count = soup.select_one('span.search-count').text
    count = int("".join(filter(str.isdigit, trail_count)))
    numit = math.ceil(float(count)/30)
    for i in range(int(numit)):
        spot = f'b_start:int= {str(i*30)}'
        url = starturl+spot
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        for div in soup.findAll('a', attrs={'class': 'listitem-title'}):
            hike_urls.append(div['href'])
            counter += 1
        print ('Collected %d websites' % counter)
    return hike_urls

def trail_data_parser(url):
    """
    Parses URL with html soup and populates washington_hikes table with relevant data.
    **Input parameters**
    ------------------------------------------------------------------------------
    url: string. Single hikes url.
    **Output**
    ------------------------------------------------------------------------------
    row_data: array. single row for a pandas df.
    Data cleaning is completed in a seperate python script.
    """
    all_features = ['Mountain views',
            'Wildlife',
            'Old growth',
            'Rivers',
            'Good for kids',
            'Dogs not allowed',
            'Coast',
            'Lakes',
            'Waterfalls',
            'Fall foilage',
            'Wildflowers/Meadows',
            'Summits',
            'Ridges/passes',
            'Established campsites']

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    row_data = {}
    try:
        row_data['hike_name'] = soup.select_one('h1.documentFirstHeading').text
    except:
        row_data['hike_name'] = 'NaN'
    try:
        stats = soup.select('div.hike-stat div')
        all_stat = [s.text.strip('\n').strip(' ') for s in stats]
        row_data['region'] = all_stat[0]
        row_data['distance'] = all_stat[1]
        row_data['elevation_gain'] = int(re.findall('\d+', all_stat[3])[0])
        row_data['highest_point'] = int(re.findall('\d+',all_stat[4])[0])
        row_data['rating'] = all_stat[9]
        row_data['number_votes'] = int(re.findall('\d+',all_stat[11])[0])
    except:
        row_data['region'] = 'NaN'
        row_data['distance'] = 'NaN'
        row_data['elevation_gain'] = None
        row_data['highest_point'] = None
        row_data['rating'] = 'NaN'
        row_data['number_votes'] = 'NaN'
    try:
        trail_features = []
        for div in soup.select('div#hike-features div'):
            trail_features.append(div.attrs.get('data-title'))
        for feature in all_features:
            if feature in trail_features:
                row_data[feature] = 1
            else:
                row_data[feature] = 0
    except:
        None
    try:
        row_data['which_pass'] = soup.select_one('div.alert a').text
    except:
        row_data['which_pass'] = 'NaN'
    try:
        lat_long = soup.select('div.latlong span')
        full_lat_long = [float(l.text) for l in lat_long]
        row_data['lat'] = full_lat_long[0]
        row_data['long'] = full_lat_long[1]
    except:
        row_data['lat'] = None
        row_data['long'] = None
    try:
        row_data['numReports'] = soup.select_one('span.ReportCount').text
    except:
        row_data['numReports'] = None

    row_data['url'] = url
    return row_data


def build_csv(urls, csv_title):
    """Accepts a list of all hike urls, calls trail_data_parser to get trail
        data, and saves trail data as a new line in a csv titled csv_title.
    **Input parameters**
    ------------------------------------------------------------------------------
    urls: List of strings. Hike urls.
    csv_title: string. Title of csv to save to without .csv on end
    **Output**
    ------------------------------------------------------------------------------
    None. Saves all trail data for each url in urls as a new line in a csv file
    """
    fieldnames = ['Coast','Dogs not allowed',
                      'Established campsites','Fall foilage',
                      'Good for kids','Lakes','Mountain views',
                      'Old growth','Ridges/passes','Rivers','Summits',
                      'Waterfalls','Wildflowers/Meadows','Wildlife',
                      'distance','elevation_gain','highest_point',
                      'hike_name','lat','long','numReports',
                      'number_votes','rating','region',
                      'url','which_pass']
    with open(csv_title +'.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        counter = 0
        for lnk in urls:
            trail_data = trail_data_parser(lnk)
            writer.writerow(trail_data)
            counter += 1
            print (f"{counter} trails written to CSV")
    return None

if __name__ == '__main__':
    starturl= 'https://www.wta.org/go-outside/hikes?'
    #currently only works with this start url- can't switch pages on a search result page
    title = 'WTA_all_trail_data'
    urls = iterate_all_reports(starturl)
    build_csv(urls, title)
