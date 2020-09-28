import unittest
from pyniviz import tools
import pandas as pd
import datetime
import numpy as np

class TestTools(unittest.TestCase):

    def setUp(self):

        variable = 'element density (kg m-3)'

        self.list_of_dfs = tools.read_pro('../examples/sample.pro')

        self.info = tools.create_grid(self.list_of_dfs,variable)

    def tearDown(self):
        pass

    def test_read_pro(self):

        self.assertIsInstance(self.list_of_dfs, list)

        self.assertIsInstance(self.list_of_dfs[0], pd.DataFrame)

        self.assertEqual(self.list_of_dfs[0]['dates'].iloc[0],
                         datetime.datetime(year=2020,month=1,day=27))

        self.assertEqual(self.list_of_dfs[0]['dates'].iloc[0],
                         self.list_of_dfs[0]['dates'].iloc[-1])

    def test_create_grid(self):

        self.assertIsInstance(self.info['grid'], np.ndarray)

        # Grid should not be all nans
        self.assertEqual(np.isnan(self.info['grid']).all(), False)



if __name__ == '__main__':
    unittest.main()