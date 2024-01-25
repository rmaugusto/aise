import numpy as np
from aise.reward import Reward

import unittest

class TestReward(unittest.TestCase):

    def test_moving_away_from_wall(self):

        #array = np.array([10,20,30,31,42,50,49,49])
        array = np.array([90,90,90,90,90,90,90,90,90])

        last_five = array[-5:]

        # Check if each element is greater than or equal to the previous one
        #    return np.all(differences >= 0) and np.any(differences > 0)

        differences = np.diff(last_five)
        if np.all(differences >= 0):
            print('aumentando...')

        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == '__main__':
    unittest.main()