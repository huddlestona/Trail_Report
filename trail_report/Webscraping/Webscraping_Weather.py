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
    urls = ['https://www.ncei.noaa.gov/orders/cdo/1340157.csv',
    'https://www.ncei.noaa.gov/orders/cdo/1340154.csv',
    'https://www.ncei.noaa.gov/orders/cdo/1340149.csv',
    'https://www.ncei.noaa.gov/orders/cdo/1340148.csv',
    'https://www.ncei.noaa.gov/orders/cdo/1340144.csv',
    'https://www.ncei.noaa.gov/orders/cdo/1340141.csv',
    'https://www.ncei.noaa.gov/orders/cdo/1340136.csv',
    'https://www.ncei.noaa.gov/orders/cdo/1340127.csv']
    get_past_weather_data(urls)
