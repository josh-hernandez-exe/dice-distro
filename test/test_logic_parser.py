import os
import sys
import unittest

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT_DIR = os.path.dirname(CUR_DIR)

sys.path.append(PROJECT_ROOT_DIR)
import dice_distro

class TestLogicParser(unittest.TestCase):
    def test1(self):
        with self.assertRaises(Exception):
            dice_distro.determine_compare_func("eq")

if __name__ == '__main__':
    unittest.main()
