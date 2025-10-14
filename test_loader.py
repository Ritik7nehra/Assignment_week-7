# test_loader.py
import unittest
import numpy as np
from loader import load_locations

class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        locations = ["Museum of Modern Art", "USS Alabama Battleship Memorial Park"]
        df = load_locations(locations, sleep_between=1.0)
        self.assertEqual(len(df), 2)
        self.assertEqual(df.loc[0, "Location"], locations[0])
        self.assertEqual(df.loc[1, "Location"], locations[1])
        expected = [(40.7618552, -73.9782438), (30.684373, -88.015316)]
        tol = 1e-3
        for i, (lat_exp, lon_exp) in enumerate(expected):
            self.assertFalse(np.isnan(df.loc[i, "Latitude"]))
            self.assertFalse(np.isnan(df.loc[i, "Longitude"]))
            self.assertAlmostEqual(df.loc[i, "Latitude"], lat_exp, delta=tol)
            self.assertAlmostEqual(df.loc[i, "Longitude"], lon_exp, delta=tol)

    def test_invalid_location(self):
        df = load_locations(["asdfqwer1234"], sleep_between=1.0)
        self.assertEqual(df.loc[0, "Location"], "asdfqwer1234")
        self.assertTrue(np.isnan(df.loc[0, "Latitude"]))
        self.assertTrue(np.isnan(df.loc[0, "Longitude"]))
        self.assertTrue(np.isnan(df.loc[0, "Type"]))

if __name__ == "__main__":
    unittest.main(verbosity=2)
