import os
import sys
import unittest

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT_DIR = os.path.dirname(CUR_DIR)

from data_sets import (
    index_independent_test_value_set,
    index_dependent_test_06,
)

sys.path.append(PROJECT_ROOT_DIR)
import dice_distro

class TestLogicBase(unittest.TestCase):
    def run_compare_against_collection(self,
        test_func,
        answer_func,
        value_test_collection
    ):
        for value_set in value_test_collection:
            self.run_compare_against_test_set(test_func, answer_func, value_set)

    def run_compare_against_test_set(self,
        test_func,
        answer_func,
        value_test_set
    ):
        for index, value in enumerate(value_test_set):
            self.assertEqual(test_func(value,index), answer_func(value,index))

class TestIndexIndependentLogic(TestLogicBase):
    def test1(self):
        compare_func = dice_distro.determine_compare_func("""
            eq 1 or not [ ge 2 and le 3 ] and [ gt 5 and lt 8  ]
        """.split())

        def expected_result(xx, *args):
            return (
                xx == 1
                or not (
                    xx >= 2 and xx <= 3
                ) and (
                    xx > 5 and xx < 8
                )
            )

        self.run_compare_against_collection(
            compare_func,
            expected_result,
            index_independent_test_value_set
        )

    def test2(self):
        compare_func = dice_distro.determine_compare_func("""
            mod 5 lt 2 or mod 7 gt 3 and mod 3 eq 1
        """.split())

        def expected_result(xx, *args):
            return (
                xx % 5 < 2
                or
                xx % 7 > 3
                and
                xx % 3 == 1
            )

        self.run_compare_against_collection(
            compare_func,
            expected_result,
            index_independent_test_value_set,
        )

class TestIndexDependentLogic(TestLogicBase):
    def test1(self):
        mod_array_0 = [2, 3, 4, 5,  6,  7]
        cmp_array_0 = [1, 2, 3, 4,  3,  2]
        mod_array_1 = [3, 5, 7, 9, 11, 13]
        cmp_array_1 = [2, 3, 4, 5, 6, 7]
        mod_array_2 = [9, 11, 13, 17, 23, 29]
        cmp_array_2 = [0, 1, 2, 3, 4, 5]

        compare_func = dice_distro.determine_compare_func("""
            mod {} lt {} or mod {} gt {} and mod {} eq {}
        """.format(
            " ".join(str(item) for item in mod_array_0),
            " ".join(str(item) for item in cmp_array_0),
            " ".join(str(item) for item in mod_array_1),
            " ".join(str(item) for item in cmp_array_1),
            " ".join(str(item) for item in mod_array_2),
            " ".join(str(item) for item in cmp_array_2),
        ).split())

        def expected_result(xx, index):
            return (
                xx % mod_array_0[index] < cmp_array_0[index]
                or
                xx % mod_array_1[index] > cmp_array_1[index]
                and
                xx % mod_array_2[index] == cmp_array_2[index]
            )

        self.run_compare_against_collection(
            compare_func,
            expected_result,
            index_dependent_test_06,
        )


if __name__ == '__main__':
    unittest.main()
