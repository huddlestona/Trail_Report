""" Tests for webscraping.get_weather_data.py
"""
import unittest as unittest
import requests
from bs4 import BeautifulSoup
from webscraping import Webscraping_Weather
import chkcsv.py 

class Test(unittest.TestCase):

    s3 = boto3.client('s3')
    bucket_name = 'trailreportdata'

    def __init__(self):
        self.urls = [
        'https://www.ncei.noaa.gov/orders/cdo/1364038.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364041.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364042.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364043.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364044.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364046.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364047.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364048.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364051.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364052.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364053.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364054.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364055.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364058.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364059.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364060.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364061.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364062.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364063.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364064.csv',
        'https://www.ncei.noaa.gov/orders/cdo/1364066.csv'
    ]

    def test_get_past_weather_data(self):
        for url in self.urls:
            self.assertEqual(type(url), str)
            response = requests.get(url)
            if response.status_code != 200:
                print(f"{response.status_code} scraping {url}")
            else:
                data = response.content
                self.assertEqual(type(data),str) 
                filename = url.split("/")[-1]
                s3.put_object(Bucket=bucket_name, Body=data, Key=filename)

if __name__ == '__main__':
    unittest.main()

    