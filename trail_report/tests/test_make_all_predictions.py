""" Tests for build_model.make_all_predictions.py
"""

import unittest as unittest
import requests
from bs4 import BeautifulSoup
from build_model import make_all_predictions


class Test(unittest.TestCase):

    def test_load_databases(self):
        self.df_trail, self.df_init = get_hike_data()
        self.weather, self.weather_dist = get_weather_data()
        self.assertEqual(type(df_init), pandas.core.frame.DataFrame)
        self.assertEqual(type(df_trail), pandas.core.frame.DataFrame)
        self.assertEqual(type(weather), pandas.core.frame.DataFrame)
        self.assertEqual(type(weather_dist), pandas.core.frame.DataFrame)
    
    def test_get_weather_data():
    weather_dist = pd.read_csv(
        'data/WA_weather_distances.csv',
        sep='|',
        lineterminator='\n')
    weather = pd.read_csv(
        'data/WA_weather_yearly.csv',
        sep='|',
        lineterminator='\n')
    self.assertEqual(type(weather), pandas.core.frame.DataFrame)
    self.assertEqual(type(weather_dist), pandas.core.frame.DataFrame)

    def test_get_hike_data(self):
     df_trail = pd.read_csv(
        'data/WTA_trails_clean_w_medians.csv',
        lineterminator='\n')
    self.assertEqual(type(df_trail), pandas.core.frame.DataFrame)
    # get_reports
    s3 = boto3.client('s3')
    bucket_name = 'trailreportdata'
    files = b''
    response = s3.get_object(Bucket=bucket_name, Key='WTA_all_merged.csv')
    self.assertEqual('Body' in response.keys(),True)
    body = response['Body']
    self.assertEqual(type(body),bytes)
    csv = body.read()
    files += csv
    f = BytesIO(files)
    df_init = pd.read_csv(f, sep='|', lineterminator='\n')
    self.assertEqual(type(df_init), pandas.core.frame.DataFrame)

    def get_data(self):
        pass


    def test_main_dump(self):
            """Dump models to a pickle."""
    tp = TrailPred()
    tp.fit()
    # Save model
    file_path = "tp_sm.pkl"
    n_bytes = 2**31
    max_bytes = 2**31 - 1
    data = tp
    # write
    bytes_out = pickle.dumps(data)
    with open(file_path, 'wb') as f_out:
        for idx in range(0, n_bytes, max_bytes):
            f_out.write(bytes_out[idx:idx + max_bytes])


if __name__ == '__main__':
    unittest.main()
