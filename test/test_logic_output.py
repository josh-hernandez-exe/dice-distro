import os
import sys
import unittest

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT_DIR = os.path.dirname(CUR_DIR)

sys.path.append(PROJECT_ROOT_DIR)
import dice_distro


index_independent_test_value_set = [
    range(10),
    range(100),
    range(-10,0),
    range(-100,0),
    range(-100,100),
]

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
                ) and(
                    xx > 5 and xx < 8
                )
            )

        self.run_compare_against_collection(
            compare_func,
            expected_result,
            index_independent_test_value_set
        )

        # with self.assertRaises(TypeError):
        #     s.split(2)

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

index_dependent_test_06 = [
    range(-6,0),
    range(-12,0,2),
    range(-6,6,2),
    range(-6,12,3),
    range(-5,13,3),
    range(-7,11,3),
    range(6),
    range(1, 7),
    range(0,12,2),
    range(1,13,2),
    range(0,18,3),
    range(1,19,3),
    range(0,30,5),
    range(1,31,5),
    range(2,32,5),
    range(3,33,5),
    range(4,34,5),
    range(0,42+0,7),
    range(1,42+1,7),
    range(2,42+2,7),
    range(3,42+3,7),
    range(4,42+4,7),
    range(5,42+5,7),
    range(6,42+6,7),
    range(0,66+0,11),
    range(1,66+1,11),
    range(2,66+2,11),
    range(3,66+3,11),
    range(4,66+4,11),
    range(5,66+5,11),
    range(6,66+6,11),
    range(7,66+7,11),
    range(8,66+8,11),
    range(9,66+9,11),
    range(0,128+0,23),
    range(1,128+1,23),
    range(3,128+3,23),
    range(5,128+5,23),
    range(7,128+7,23),
    range(11,128+11,23),
    range(13,128+13,23),
    range(17,128+17,23),
    range(19,128+19,23),
]

class TestIndexDependentLogic(TestLogicBase):
    def test2(self):
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
