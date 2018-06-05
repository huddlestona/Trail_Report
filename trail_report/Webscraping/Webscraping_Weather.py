import requests
import boto3
import pandas as pd
from io import BytesIO
import numpy as np

def get_past_weather_data(urls):
    for url in urls:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"{response.status_code} scraping {url}")
        else:
            data = response.content
            filename = url.split("/")[-1]
            s3.put_object(Bucket= bucket_name, Body= data, Key= filename)
            print(f'{filename} downloaded')

if __name__ == '__main__':
    s3 = boto3.client('s3')
    bucket_name = 'trailreportdata'
    urls = [
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
    get_past_weather_data(urls)
