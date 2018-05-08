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
    """Determines the number of hikes listed on the WTA trails page and get said number of report urls
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
    """Parses URL into hiking dataset.
    Parser collects html soup and populates
    washington_hikes table with relevant data. Data cleaning is completed in a
    seperate python script."""

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
        row_data['hike_name'] = None
    try:
        stats = soup.select('div.hike-stat div')
        all_stat = [s.text.strip('\n').strip(' ') for s in stats]
        row_data['region'] = all_stat[0]
        row_data['distance'] = all_stat[1]
        row_data['elevation_gain'] = all_stat[3]
        row_data['highest_point'] = all_stat[4]
        row_data['rating'] = all_stat[9]
        row_data['number_votes'] = all_stat[11]
    except:
        row_data['region'] = None
        row_data['distance'] = None
        row_data['elevation_gain'] = None
        row_data['highest_point'] = None
        row_data['rating'] = None
        row_data['number_votes'] = None
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
        row_data['which_pass'] = None
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


with open('olympics_trail_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Coast',
 'Dogs not allowed',
 'Established campsites',
 'Fall foilage',
 'Good for kids',
 'Lakes',
 'Mountain views',
 'Old growth',
 'Ridges/passes',
 'Rivers',
 'Summits',
 'Waterfalls',
 'Wildflowers/Meadows',
 'Wildlife',
 'distance',
 'elevation_gain',
 'highest_point',
 'hike_name',
 'lat',
 'long',
 'numReports',
 'number_votes',
 'rating',
 'region',
 'url',
 'which_pass']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for lnk in olympics_urls:
        trail_data = trail_data_parser(lnk)
        writer.writerow(trail_data)

if __name __ == '__main__':
    urls = iterate_all_reports(starturl)

    
