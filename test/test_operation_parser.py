import os
import sys
import unittest
from data_sets import (
    index_independent_test_value_set,
    index_dependent_test_06,
)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT_DIR = os.path.dirname(CUR_DIR)

sys.path.append(PROJECT_ROOT_DIR)
import dice_distro


class TestParserBase(unittest.TestCase):
    def parse_command(self,command):
        command_list = command.split()
        return dice_distro.get_operator(
            param_list=command_list,
            should_validate=True,
        )

    def run_operation_against_collection(self,
        test_func,
        answer_func,
        value_test_collection
    ):
        for value_set in value_test_collection:
            self.assertEqual(test_func(value_set), answer_func(value_set))

class TestOperationParser(TestParserBase):
    def test_independent_index_01(self):
        operation_func = self.parse_command("""
            add 100 if mod 5 eq 2 else add 10 if mod 2 eq 1 else scale 0
        """)

        def expected_result(xx):
            return tuple(
                ii+100 if ii % 5 == 2 else ii+10 if ii % 2 == 1 else ii*0
                for ii in xx
            )

        self.run_operation_against_collection(
            operation_func,
            expected_result,
            index_independent_test_value_set,
        )

    def test_independent_index_02(self):
        operation_func = self.parse_command("""
            [ add 2 scale 2 ] if mod 3 eq 1 else [ scale -1 add -1 ] if mod 3 eq 2 else exp 3
        """)

        def expected_result(xx):
            return tuple(
                ( (ii+2)*2 ) if ii % 3 == 1 else (-ii-1) if ii % 3 == 2 else ii**3
                for ii in xx
            )

        self.run_operation_against_collection(
            operation_func,
            expected_result,
            index_independent_test_value_set,
        )

    def test_dependent_index_01(self):
        add1 = [ 9, 11, 13, 17, 23, 29]
        mod1 = [ 2, 3, 4, 5,  6,  7]
        cmp1 = [ 1, 2, 3, 4,  3,  2]
        add2 = [-4,-1,-3,-2,-12,-15]
        mod2 = [ 3, 5, 7, 9, 11, 13]
        cmp2 = [ 2, 3, 4, 5, 6, 7]
        mul3 = [0, 1, 2, 3, 4, 5]

        operation_func = self.parse_command("""
            add {add1} if mod {mod1} eq {eq1} else add {add2} if mod {mod2} eq {eq2} else scale {scale3}
        """.format(
            add1=" ".join(str(item) for item in add1),
            mod1=" ".join(str(item) for item in mod1),
            eq1=" ".join(str(item) for item in cmp1),
            add2=" ".join(str(item) for item in add2),
            mod2=" ".join(str(item) for item in mod2),
            eq2=" ".join(str(item) for item in cmp2),
            scale3=" ".join(str(item) for item in mul3),
        ))

        def expected_result(xx):
            return tuple(
                aa+add1[ii] if aa % mod1[ii] == cmp1[ii] else aa+add2[ii] if aa%mod2[ii]==cmp2[ii] else aa*mul3[ii]
                for ii,aa in enumerate(xx)
            )

        self.run_operation_against_collection(
            operation_func,
            expected_result,
            index_dependent_test_06,
        )



if __name__ == '__main__':
    unittest.main()
