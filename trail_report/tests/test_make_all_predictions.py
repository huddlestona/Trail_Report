""" Tests for .py
"""

import unittest as unittest
import requests
from bs4 import BeautifulSoup
from build_model import make_all_predictions


class Test(unittest.TestCase):
    def test_main_dump(self):
            """Dump models to a pickle."""
    df_init, df_trail, weather, weather_dist = load_databases()
    self.assertEqual(type(df_init), pandas.core.frame.DataFrame)
    self.assertEqual(type(df_trail), pandas.core.frame.DataFrame)
    self.assertEqual(type(weather), pandas.core.frame.DataFrame)
    self.assertEqual(type(weather_dist), pandas.core.frame.DataFrame)
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
