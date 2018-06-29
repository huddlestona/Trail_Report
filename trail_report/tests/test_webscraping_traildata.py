""" Tests for webscraping_traildata.py
"""

import unittest as unittest
import requests
from bs4 import BeautifulSoup
from src import get_data
import re
import math
import csv
from webscraping.Webscraping_TrailData import *


class Test(unittest.TestCase):
    def __init__(self):
        self.starturl = 'https://www.wta.org/go-outside/hikes?'
        self.assertEqual(type(self.starturl),str)
        self.title = 'WTA_all_trail_data_2'
    
    def test_iterate_all_reports(self):
        hike_urls = []
        counter = 0
        r = requests.get(starturl).text
        self.assertEqual(type(r),str)
        soup = BeautifulSoup(r, 'lxml')
        trail_count = soup.select_one('span.search-count').text
        count = int("".join(filter(str.isdigit, trail_count)))
        self.assertEqual(type(count),int)
        numit = math.ceil(float(count) / 30)
        self.assertEqual(type(numit),float)
        for i in range(int(numit)):
            spot = f'b_start:int= {str(i*30)}'
            url = starturl + spot
            self.assertEqual(type(url),str)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            for div in soup.findAll('a', attrs={'class': 'listitem-title'}):
                self.assertTrue('href'in div)
                hike_urls.append(div['href'])
                counter += 1
            print('Collected %d websites' % counter)
        return hike_urls

    def test_build_csv(self):
        pass


if __name__ == '__main__':
    unittest.main()