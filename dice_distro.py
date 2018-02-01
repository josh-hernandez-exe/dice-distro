from __future__ import print_function

import argparse
import decimal
import functools
import importlib
import itertools
import json
import math
import operator
import os
import random
import sys

from collections import Counter

if (2, 0) <= sys.version_info < (3, 0):
    zip = itertools.izip

def prod_values(xx,
    # the following are done for runtime optimizations
    mul=operator.mul,
    reduce=functools.reduce,
):
    return reduce(mul, xx, 1)

"""
The following are definitions of "basic operations"
used for dice output manipulation
"""
def _id(xx): return xx
def _sum(xx,sum=sum): return sum(xx),
def _min(xx,min=min): return min(xx),
def _max(xx,max=max): return max(xx),
def _prod(xx, prod_values=prod_values): return prod_values(xx),
def _sort(xx,tuple=tuple,sorted=sorted): return tuple(sorted(xx))

def _bit_or(xx,
    # the following are done for runtime optimizations
    or_=operator.or_,
    reduce=functools.reduce,
):
    return reduce(or_, xx, 0),

def _bit_xor(xx,
    # the following are done for runtime optimizations
    xor=operator.xor,
    reduce=functools.reduce,
):
    return reduce(xor, xx),

def _bit_and(xx,
    # the following are done for runtime optimizations
    and_=operator.and_,
    reduce=functools.reduce,
):
    return reduce(and_, xx),

OPERATIONS_DICT = {
    'id':_id,
    'sum':_sum,
    'min':_min,
    'max':_max,
    'sort':_sort,
    'prod':_prod,
    'bit-or': _bit_or,
    'bit-xor': _bit_xor,
    'bit-and': _bit_and,
    'add': None, # This will get defined later if used
    'scale': None, # This will get defined later if used
    'exp': None, # This will get defined later if used
    'set-to': None, # This will get defined later if used
    'bound': None, # This will get defined later if used
    'select': None, # This will get defined later if used
    'reroll': None, # This will get defined later if used,
    'slice-apply': None, # This will get defined later if used,
}

CUSTOM_OPERATIONS_DICT = dict()

BASIC_OPERATIONS = set(
    key for key, value in OPERATIONS_DICT.items() if value is not None
)

def rounding_half_up(xx,
    # the following are done for runtime optimizations
    Decimal=decimal.Decimal,
    quantize=decimal.Decimal.quantize,
    one=decimal.Decimal('1'),
    rounding=decimal.ROUND_HALF_UP,
):
    return quantize(Decimal(xx), one,rounding=rounding)

def rounding_half_down(xx,
    # the following are done for runtime optimizations
    Decimal=decimal.Decimal,
    quantize=decimal.Decimal.quantize,
    one=decimal.Decimal('1'),
    rounding=decimal.ROUND_HALF_DOWN,
):
    return quantize(Decimal(xx), one,rounding=rounding)

ROUNDING_OPTIONS = {
    'r-ceil': math.ceil,
    'r-floor': math.floor,
    'r-truncate': int,
    'r-half-up': rounding_half_up,
    'r-half-down': rounding_half_down,
}

# set of operations that support an if-block
IF_ABLE_OPERATIONS = set([
    'add',
    'scale',
    'exp',
    'set-to',
    'bound',
    'reroll',
])

ELSE_ABLE_OPERATIONS = set([
    'add',
    'scale',
    'exp',
    'set-to',
    'bound',
])

def _ne(aa, bb, cc=None): return aa != bb
def _eq(aa, bb, cc=None): return aa == bb
def _gt(aa, bb, cc=None): return aa > bb
def _ge(aa, bb, cc=None): return aa >= bb
def _lt(aa, bb, cc=None): return aa < bb
def _le(aa, bb, cc=None): return aa <= bb

BASIC_COMPARE_DICT = {
    'ne': _ne,
    'eq': _eq,
    'gt': _gt,
    'ge': _ge,
    'lt': _lt,
    'le': _le,
}

LOGIC_START_KEYWORD = 'if'

LOGIC_ELSE_KEYWORD = 'else'

LOGIC_END_KEYWORD = 'then'

LOGIC_KEYWORDS = set([
    LOGIC_START_KEYWORD,
    LOGIC_ELSE_KEYWORD,
    LOGIC_END_KEYWORD,
])

BOOLEAN_LOGIC_OPERATOR_ORDER = ['not', 'and', 'or']
BOOLEAN_LOGIC_OPERATORS = set(BOOLEAN_LOGIC_OPERATOR_ORDER)

COMPARE_KEYWORDS_SET = set.union(
    set([
        'mod',
    ]),
    set(BASIC_COMPARE_DICT.keys()),
    BOOLEAN_LOGIC_OPERATORS,
)

BRACKET_CHARS = ["[", "]"]

# Die defaults
DEFAULT_DIE_START = int(1)
DEFAULT_DIE_STEP = int(1)
DEFAULT_DIE_WEIGHT = int(1)

class CustomFormatter(argparse.HelpFormatter):
    """
    Utilized code from:
        - https://github.com/bewest/argparse/blob/master/argparse.py
            class RawDescriptionHelpFormatter(HelpFormatter)
            class ArgumentDefaultsHelpFormatter(HelpFormatter)
            RawTextHelpFormatter._split_lines
        - https://bitbucket.org
            /ruamel
            /std.argparse
            /src
            /cd5e8c944c5793fa9fa16c3af0080ea31f2c6710
            /__init__.py?at=default&fileviewer=file-view-default

    R| - Raw text, no indentation will be added
    D| - Pad with white space
    """
    def __init__(self, *args, **kw):
        self._add_defaults = None
        super(CustomFormatter, self).__init__(*args, **kw)

    def _split_lines(self, text, width):
        # this is the RawTextHelpFormatter._split_lines
        if text.startswith('R|'):
            return text[2:].splitlines()
        elif text.startswith('D|'):
            return [item.strip() for item in text[2:].splitlines()]

        return argparse.HelpFormatter._split_lines(self, text, width)

    def _fill_text(self, text, width, indent):
        # this is the RawDescriptionHelpFormatter._fill_text
        if text.startswith('R|'):
            return text[2:]

        if text.startswith('D|'):
            text = text[2:]

        return argparse.HelpFormatter._fill_text(self, text, width, indent)

    def _get_help_string(self, action):
        _help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    _help += ' (default: %(default)s)'
        return _help

def parse_number(compare_func, type_string, type=int):
    if not issubclass(type, (int, float)):
        raise Exception('Type passed must be either int or float')

    if not hasattr(compare_func, '__call__'):
        raise Exception('A function must be passed to parse_number.')

    def parse_number_compare(value):
        ivalue = type(value)
        if not compare_func(ivalue):
            raise argparse.ArgumentTypeError(
                "{} is an invalid {} value of type {}".format(
                    value,
                    type_string,
                    str(type),
            ))
        return ivalue

    return parse_number_compare

parser = argparse.ArgumentParser(
    formatter_class=CustomFormatter,
    description="\n".join([
        "This program is used to calculate the distributions of",
        "dice rolling (using brute force enumeration) with operations",
        "applied to results of the roll (via brute force calculations).",
    ]),
)

parser.add_argument(
    "--show-args",
    action='store_true',
    help=" ".join([
        "This is used for debuging purposes.",
        "This will print out the parameters used to console,",
        "before running a calculation",
    ]),
)

"""
========================================================================================
Single Die Options
========================================================================================
"""

single_type_group = parser.add_argument_group(
    title='Single Die Type Options',
    description='Use these flags when wanting to roll a specific die type.',
)

single_type_group.add_argument(
    "--num-dice", "-n",
    type=parse_number(lambda xx: xx > 0, 'positive'),
    default=1,
    help="Number of dice simulated",
)

single_type_group_side_option = single_type_group.add_mutually_exclusive_group()

single_type_group_side_option.add_argument(
    "--die-sides", "-d",
    type=parse_number(lambda xx: xx > 0, 'positive'),
    help=" ".join([
        "Number of sides the dice simulated should have.",
        "The value given must be a positive integer.",
        "The values on the die will start from '--die-start' and",
        "fill up the sides of the die incrementing by '--die-step'.",
        "This and '--die-values' are mutually exclusive options."
    ]),
)

single_type_group.add_argument(
    "--die-start",
    type=int,
    default=DEFAULT_DIE_START,
    help=" ".join([
        "If using '--die-sides' this defines the lowest value of the die.",
        "This option is ignored if '--die-sides' is not used.",

    ]),
)

single_type_group.add_argument(
    "--die-step",
    type=int,
    default=DEFAULT_DIE_STEP,
    help=" ".join([
        "If using '--die-sides' this defines the increments",
        "between values on the sides of the die.",
        "This option is ignored if '--die-sides' is not used.",
    ]),
)

single_type_group_side_option.add_argument(
    "--die-values",
    type=int,
    nargs="+",
    default=[],
    help=" ".join([
        "The values the die should have.",
        "Values are expected to be integers.",
        "This and '--die-sides' are mutually exclusive options.",
    ]),
)

single_type_group.add_argument(
    "--die-weights",
    type=parse_number(lambda xx: xx > 0, 'positive', float),
    nargs="+",
    default=[],
    help=" ".join([
        "The weighting of the sides a die.",
        "Values are expected to be integers or floats.",
    ]),
)


"""
========================================================================================
Multi Die Options
========================================================================================
"""
multi_type_group = parser.add_argument_group(
    title='Multi Die Type Options',
    description=" ".join([
        'Use these flags when wanting to roll multiple types of dies at once.',
        'When using flags from this group, the \'--multi-die-sides\' flag is required.',
    ]),
)

multi_type_group.add_argument(
    "--multi-die-sides",
    type=parse_number(lambda xx: xx > 0, 'positive'),
    nargs="+",
    help=" ".join([
        "Number of sides the dice simulated should have.",
        "This parameter is always used in when creating non-identical",
        "dice to roll (multi-die-type) and thus is required."
        "The value given must be a positive integer.",
        "The values on the die will start from '--die-start'",
        "and fill up the sides of the die incrementing by '--die-step'",
        ", unless you use '--multi-die-values' to specify each value on each die."
    ]),
)

multi_type_group.add_argument(
    "--multi-die-start",
    type=int,
    nargs="+",
    help=" ".join([
        "If using '--die-sides' this defines the lowest value of the die.",
        "This option is ignored if '--die-sides' is not used.",
        "These values must be in parallel to '--multi-die-sides'",
    ]),
)

multi_type_group.add_argument(
    "--multi-die-step",
    type=int,
    nargs="+",
    help=" ".join([
        "If using '--die-sides' this defines the increments between",
        "values on the sides of the die.",
        "This option is ignored if '--die-sides' is not used.",
        "These values must be in parallel to '--multi-die-sides'",
    ]),
)

multi_type_group.add_argument(
    "--multi-die-values",
    type=int,
    nargs="+",
    default=[],
    help=" ".join([
        "The values the die should have.",
        "Values are expected to be integers.",
        "If using this option, '--multi-die-sides' must set.",
        "The values are grabed in order.",
    ]),
)

multi_type_group.add_argument(
    "--multi-die-weights",
    type=parse_number(lambda xx: xx > 0, 'positive', float),
    nargs="+",
    default=[],
    help=" ".join([
        " The weighting of the sides a dice.",
        "Values are expected to be integers or floats.",
        "If using this option, '--multi-die-sides' must set.",
        "The values are grabed in order.",
    ]),
)

"""
========================================================================================
Operation Options
========================================================================================
"""
op_group = parser.add_argument_group(
    title='Operation Options',
    description='Options how to deal with the result of rolls of the dice.',
)

op_group.add_argument(
    "--apply",
    type=str,
    nargs="*",
    default=['id'],
    help="\n".join([
        "D|"
        # Intro block
        "The operation that will be applied to the values rolled.",
        "Operations can be chained, but it is up to the user to make",
        "sure that the outputs of one are correct inputs for the other.",
        # Explain if-block synatx
        "Some operations can be applied conditionally, denoted by an",
        "if-block between the operation string and its parameters.",
        "Denote the end by using the keyword '{}'".format(LOGIC_END_KEYWORD),
        "of the conditional statement",
        "if more operation or parameters are needed.",
        "Example Syntax:",
        "'--apply op1 if cond1... then params1... then op2 if cond2... then params2...'",
        "Note that if the last operation does not need parameters",
        "but has an if-block, the final 'then' is not needed.",
        # End of into block
        # Define id operation
        "---------------",
        "The 'id' operation refers to the identity operation, which will",
        "leave the input unchanged.",
        # Define math operations operation
        "---------------",
        "The following operations:",
        "'sum', 'min', 'max', 'set', 'prod', 'bit-or', 'bit-xor', 'bit-and'",
        "apply their assosiated operation to all the dice.",
        "An optional parameter can be given for a block-size, for block-wise application.",
        "If the a block-size parameter is used, the results will be treated",
        "as distinguishable dice.",
        # Define sort operation
        "---------------",
        "The 'sort' operation sorts the result.",
        "This has the effect of enumerating the results as",
        "if the we treated the dice as indistiguishable.",
        # Define add operation
        "---------------",
        "The 'add' operation will add a static value to all results",
        "(you can specify the value per die).",
        # Define bound operation
        "---------------",
        "The 'bound' operation will keep the values within specified upper and",
        "lower bound (can be spcified per die).",
        # Define reroll operation
        "---------------",
        "The 'reroll' will assume ordered dice rolls.",
        "To be useful, 'reroll' should be given an if block",
        "otherwise, the die is always rerolled and the final roll will just be used.",
        # Define scale
        "---------------",
        "The 'scale' operation multiplies the value of the die by the parameter(s) given",
        "The parameter(s) can be floating point values but the result(s) will be rounded.",
        "The rounding option must be given before any of the numeric scale parameter(s).",
        "The rounding options are:",
        "'r-ceil', 'r-floor', 'r-truncate', 'r-half-up', 'r-half-down'",
        # Define exp
        "---------------",
        "The 'exp' operation exponentiates the die value by the parameter(s).",
        "A parameter 'as-base' can be passed before any of the numeric parameter(s).",
        "This parameter will cause the parameter(s) passed to be used as the base and the",
        "die value as the exponent.",
        "The parameter(s) can be floating point values but the result(s) will be rounded.",
        "The rounding option must be given before any of the numeric scale parameter(s).",
        "The rounding options are:",
        "'r-ceil', 'r-floor', 'r-truncate', 'r-half-up', 'r-half-down'",
        # Define slice-apply operation
        "---------------",
        "The 'slice-apply' will take an block-size parameter to split the current",
        "dice pool into blocks.",
        "The immideate subsequent operation is applied to each block independently.",
        "Operations applied after the immideate subsequent one will be applied to the",
        "whole dice pool again (unless 'slice-apply' is used again).",
        # Define select operation
        "---------------",
        "The 'select' operation requires at least one integer parameter.",
        "This parameter is the index of the item in the sorted array.",
        "Example-Select-1: '--apply select  0' is the same as min.",
        "Example-Select-2: '--apply select  1' returns the second lowest value.",
        "Example-Select-3: '--apply select -1' is the same as max.",
        "Example-Select-4: '--apply select -2' returns the second highest value.",
    ]),
)

op_group.add_argument(
    "--memorize-input",
    action='store_true',
    help=" ".join([
        "An option for cashing results when applying the operation to a set of dice.",
        "This will hash the results of a roll, and save the result.",
        "This speeds up some calculations, but adds overhead since you",
        "must calculate the hash of the input.",
        "This flag is not useful if input doesn't repeat."
    ]),
)

op_group.add_argument(
    "--skip-checks",
    action='store_false',
    dest="should_valdiate_input",
    help=" ".join([
        "This option will skip add a validation step to make sure the dice input",
        "from one operation is approximate for the next.",
        "This flag will speed up run time at the expense of more obscure errors.",
    ]),
)

op_group.add_argument(
    "--custom",
    type=str,
    nargs="*",
    default=[],
    help=" ".join([
        "These files will be imported by the program as python files.",
        "Make sure that all file names are unique, as well as all",
        "function names between files. Any function prefixed with '_'",
        "will also not be included.",
        "Any function accessable can be used as operations in",
        "the '--apply' command string. Your functions should expect the",
        "first parameter to be a tuple of ints (the dice rolls).",
        "If you pass your operation parameters, they will be passed as",
        "positional args after the first.",
        "The function must either return an ints or an ordered",
        "list/tuple of ints."
    ]),
)

"""
========================================================================================
Bar Options
========================================================================================
"""
bar_group = parser.add_argument_group(
    title='Bar Options',
    description='Options related to the bar rendering',
)

bar_group.add_argument(
    "--bar-size",
    type=parse_number(lambda xx: xx >= 0, 'non-negative'),
    default=2,
    help=" ".join([
        "The approximate number of '--bar-char'(s) that count as 1 percent.",
        "If '--bar-size' is set to zero, then no bars will be displayed.",
    ]),
)

bar_group.add_argument(
    "--bar-char",
    type=str,
    default="=",
    help=" ".join([
        "The fill string used for the bar charts.",
        "One percent is represented as this string repeated '--bar-size' times.",
    ]),
)

bar_group.add_argument(
    "--bar-prefix",
    type=str,
    default="|",
    help=" ".join([
        "A prefix string used before the bar chart but after the display of percentage.",
        "Will not be displayed if '--bar-size' is set to zero.",
    ]),
)

"""
========================================================================================
Display Output Options
========================================================================================
"""
display_output_group = parser.add_argument_group(
    title='Display Output Options',
    description='Options related to displaying calculated information',
)

display_output_group.add_argument(
    "--sort",
    type=str,
    choices=["key", "value"],
    default='key',
    help=" ".join([
        "This defines how the output is sorted.",
        "Key refers to the die results.",
        "Value refers to the counts or the probability of the results.",
    ]),
)

display_output_group.add_argument(
    "--no-output",
    action='store_false',
    dest='display_output',
    default=True,
    help=" ".join([
        "If this flag is set, there will be no output displayed."
    ]),
)

display_format_exclusive_options = display_output_group.add_mutually_exclusive_group()

display_format_exclusive_options.add_argument(
    "--result-decimal-place", "-rdp",
    type=parse_number(lambda xx: xx > 0, 'positive'),
    default=2,
    help=" ".join([
        "The number of digits that will be displayed after the decimal place.",
        "Can be used when displaying percentages or floating point counts",
        "(which only happen when the die weights are floating point values).",
    ]),
)

display_format_exclusive_options.add_argument(
    "--show-counts",
    action="store_true",
    help=" ".join([
        "This flag will cause the counts to be displayed instead of the percentage.",
    ]),
)

"""
========================================================================================
Simulate Options
========================================================================================
"""
simulate_group = parser.add_argument_group(
    title='Simulate Options',
    description=' '.join([
        'Options related to simulating the dice rolls rather than enumerating all the outcomes.',
        'Useful if the compute time of calculating all the outcomes takes too long.',
        'This will only provide an approximation of the results.',
    ]),
)

simulate_group.add_argument(
    '--simulate',
    dest='simulate_num_iterations',
    type=parse_number(lambda xx: xx > 0, 'positive'),
    default=None,
    help=" ".join([
        "The number of simulated dice rols that will occur.",
        "If this option is not provided, then enumerating all outcomes will take place.",
    ]),
)

"""
========================================================================================
File Save/Load Options
========================================================================================
"""
file_save_load_options = parser.add_argument_group(
    title='Save/Load Options',
    description=' '.join([
        'Options related to saving data and loading data'
    ]),
)

file_save_load_options.add_argument(
    '--load',
    dest='load_file_paths',
    type=str,
    nargs="*",
    default=None,
    help=" ".join([
        "The file path of where you want the data loaded from.",
        "NOTE: If this parameter is used, all dice generation parameters will be ignored.",
    ]),
)


file_save_load_options.add_argument(
    '--save',
    dest='save_file_path',
    type=str,
    default=None,
    help=" ".join([
        "The file path of where you want the data saved.",
    ]),
)

def always_true(*args, **kwargs):
    return True

def apply_not(func):
    def not_func(*args, **kwargs):
        return not func(*args, **kwargs)
    return not_func

def apply_and(*funcs):
    _all=all # For runtime optimizations
    def and_func(*args, **kwargs):
        return _all(func(*args, **kwargs) for func in funcs)
    return and_func

def apply_or(*funcs):
    _any=any # For runtime optimizations
    def or_func(*args, **kwargs):
        return _any(func(*args, **kwargs) for func in funcs)
    return or_func

def docstring_format(*args, **kwargs):
    def decorator(func):
        func.__doc__ = func.__doc__.format(*args, **kwargs)
        return func
    return decorator

def indent_text(text,indent=4*" "):
    if not text:
        return ''

    return "\n".join(indent + line for line in text.split("\n"))

def dice_input_checker(func):
    func_str_info = "\n".join([
        "Func Name: {}".format(func.__name__),
        "Doc String: {}".format(func.__doc__)
    ])

    def check_is_tuple(xx, kind):
        if not isinstance(xx, tuple):
            raise Exception(
                "\n".join([
                    func_str_info,
                    '{} of operation is not an instance of `list` or `tuple`. Given: {}'.format(
                        kind.title(),
                        str(xx),
                    ),
                ])
            )

    def check_all_int(xx, kind):
        if not all(isinstance(item, int) for item in xx):
            raise Exception(
                "\n".join([
                    func_str_info,
                    'Entries in the {} list/tuple are not integers. Given: {}'.format(
                        kind.lower(),
                        str(xx),
                    ),
                ])
            )

    @functools.wraps(func)
    def wrapper(xx,
        # the following are done for runtime optimizations
        func=func,
        check_is_tuple=check_is_tuple,
        check_all_int=check_all_int,
    ):
        check_is_tuple(xx, 'input')
        check_all_int(xx, 'input')

        result = func(xx)

        check_is_tuple(result, 'output')
        check_all_int(result, 'output')

        return result

    return wrapper

def memorize(func,
    # the following are done for runtime optimizations
    tuple=tuple,
    frozenset=frozenset,
):
    cashe = dict()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (tuple(args), frozenset(kwargs.items()))

        if key in cashe: return cashe[key]

        result = func(*args, **kwargs)
        cashe[key] = result

        return result

    return wrapper

def find_max_digits(iterable):
    if not all(isinstance(xx, (int, float)) for xx in iterable):
        raise Exception('All items in the iterable must be ints or floats.')

    return max(len(str(xx)) for xx in iterable)

def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def simple_clean_params(param_list):
    """
    This function expects the parameter list
    It will split up the brackets so that each bracket is it's own entry
    as well as remove any extra white space
    """
    temp_list = list(param_list)
    for bracket in BRACKET_CHARS:
        _temp_list = []
        for item1 in temp_list:
            if bracket in item1:
                item2 = item1.split(bracket)
                _temp_list.extend(
                    item3
                    for item3 in intersperse(item2, bracket) if item3
                )
            elif item1:
                _temp_list.append(item1)

        temp_list = _temp_list

    return temp_list

def custom_func_wrapper(
    custom_func,
    cur_params=tuple(),
    should_validate=True,
):

    @functools.wraps(custom_func)
    def custom_operation(xx,
        # the following are done for runtime optimizations
        any=any,
        int=int,
        list=list,
        tuple=tuple,
        isinstance=isinstance,
        custom_func=custom_func,
        cur_params=cur_params,
        should_validate=should_validate,
    ):
        result = custom_func(xx, *cur_params)

        if not should_validate:
            # short ciruit the checks
            pass

        elif isinstance(result, int):
            result = (result,)
        elif isinstance(result, list):
            result = tuple(result)
        elif not isinstance(result, tuple):
            raise Exception("Custom function has returned a value that is not supported.")

        if should_validate and any(not isinstance(item, int) for item in result):
            raise Exception("Values passed are not all ints.")

        return result

    return custom_operation

def composed_func_wrapper(
    first_func,
    second_func,
):
    @docstring_format(
        indent_text(first_func.__doc__),
        indent_text(second_func.__doc__),
    )
    def composite_operation(xx,
        # the following are done for runtime optimizations
        first_func=first_func,
        second_func=second_func,
    ):
        """
        Composite Operation
        --------------------
        First Operation Doc:
        {}
        --------------------
        Second Operation Doc:
        {}
        --------------------
        """
        return second_func(first_func(xx))

    return composite_operation

def load_custom_files(file_paths):
    custom_dirs = set()
    file_names = set()

    for path in file_paths:
        abs_path = os.path.abspath(path)
        file_dir = os.path.dirname(abs_path)
        prefix_path, _ = os.path.splitext(abs_path)
        basename = os.path.basename(prefix_path)

        if basename in file_names:
            raise Exception("File name is not unique")

        if not os.path.isfile(abs_path):
            raise Exception("File path give is not a valid file: {}".format(path))

        file_names.add(basename)
        custom_dirs.add(file_dir)

    for dir_path in custom_dirs:
        sys.path.append(dir_path)

    for module_name in file_names:
        the_module = importlib.import_module(module_name)

        for attr_name in dir(the_module):
            if attr_name.startswith("_"): continue

            attr_object = getattr(the_module, attr_name, None)
            if hasattr(attr_object, "__call__"):
                if attr_name in CUSTOM_OPERATIONS_DICT:
                    raise Exception('operation_name collision, please make sure you ')

                CUSTOM_OPERATIONS_DICT[attr_name] = attr_object

def get_single_dice(args):
    """
    Create a tuple of 'args.num_dice' many dice
    where each die is the same.
    """
    if all([
        isinstance(args.die_sides, int) and args.die_sides > 0,
        isinstance(args.die_values, (list, tuple)) and args.die_values,
    ]):
        raise Exception("Both die sides are given and die values are given. Only pass one")

    elif isinstance(args.die_sides, int) and args.die_sides > 0:
        face_values = range(
            args.die_start,
            args.die_start + args.die_step * args.die_sides,
            args.die_step,
        )

    elif args.die_values:
        face_values = args.die_values

    else:
        raise Exception('Must pass in one of \'--die\' or \'--die-values\'')

    if isinstance(args.die_weights, (list, tuple)) and args.die_weights:
        if len(face_values) != len(args.die_weights):
            raise Exception(
                "The number of die counts must the same as the number of face values present on the die."
            )
        weight_values = args.die_weights

    else:
        weight_values = [DEFAULT_DIE_WEIGHT for _ in face_values]

    return tuple(tuple(zip(face_values, weight_values)) for _ in range(args.num_dice))

def get_multi_dice(args):
    """
    Create a tuple of dice were each die may not have the same number
    of sides as any other die
    """
    dice = []

    if not isinstance(args.multi_die_sides, (list, tuple)) or not args.multi_die_sides:
        raise Exception(
            "The parameter '--multi-die-sides' is a required parameter for multi-die-type rolls"
        )

    if (
        isinstance(args.multi_die_weights, (list, tuple)) and
        args.multi_die_weights and
        len(args.multi_die_weights) != sum(args.multi_die_sides)
    ):
        raise Exception(
            "The number of weights given should be equal to the facees on all dies that will be rolled."
        )

    if isinstance(args.multi_die_values, (list, tuple)) and args.multi_die_values:
        """
        Process args to return dice were each die has unique specified values
        Values are specified from 'args.multi_die_values' and values are grouped
        into sections specified by args.multi_die_sides.
        """
        if isinstance(args.multi_die_weights, (list, tuple)) and args.multi_die_weights:
            iterator = zip(args.multi_die_values, args.multi_die_weights)
        else:
            iterator = zip(args.multi_die_values, itertools.repeat(DEFAULT_DIE_WEIGHT))

        die = []
        for die_face in iterator:
            die.append(die_face)
            if len(die) == args.multi_die_sides[len(dice)]:
                dice.append(tuple(die))
                die = []

        if len(dice) != len(args.multi_die_sides):
            raise Exception("Not enough die values were given")

        if sum(len(item) for item in dice) != len(args.multi_die_values):
            raise Exception("Not all die values were used")

    else:
        """
        Process args to return dice you specify a:
        - start value
        - increment vlaue
        - number of steps to take (number of sides on the die)
        """
        if isinstance(args.multi_die_start, (list, tuple)) and args.multi_die_start:
            if len(args.multi_die_start) != len(args.multi_die_sides):
                raise Exception("Multi die starts must have parallel values to multi die sides")

            start_values = args.multi_die_start
        else:
            start_values = tuple(DEFAULT_DIE_START for _ in args.multi_die_sides)

        if isinstance(args.multi_die_step, (list, tuple)) and args.multi_die_step:
            if len(args.multi_die_step) != len(args.multi_die_step):
                raise Exception("Multi die steps must have parallel values to multi die sides")

            step_values = args.multi_die_step
        else:
            step_values = tuple(DEFAULT_DIE_STEP for _ in args.multi_die_sides)

        if isinstance(args.multi_die_weights, (list, tuple)) and args.multi_die_weights:
            weight_value_sets = []
            temp_list = list(args.multi_die_weights)
            for nn in args.multi_die_sides:
                weight_value_sets.append(temp_list[:nn])
                temp_list = temp_list[nn:]
        else:
            weight_value_sets = [[DEFAULT_DIE_WEIGHT]*nn for nn in args.multi_die_sides]

        for start, step, size, weights in zip(start_values, step_values, args.multi_die_sides, weight_value_sets):
            dice.append(tuple(zip(range(start, start + step * size, step), weights)))

    return tuple(dice)

def get_dice(args):
    is_using_single_type = any([
        isinstance(args.die_values, (list, tuple)) and args.die_values,
        isinstance(args.die_sides, int) and args.die_sides > 0,
    ])

    is_using_multi_type = isinstance(args.multi_die_sides, (list, tuple)) and args.multi_die_sides

    if is_using_single_type and is_using_multi_type:
        raise Exception(" ".join([
            "You cannot use both types of die generation.",
            "Single die type and multi die type are mutually exclusive die generation schemes."
        ]))
    elif is_using_multi_type:
        return get_multi_dice(args)
    elif is_using_single_type:
        return get_single_dice(args)
    else:
        raise Exception("No flags were given for dice generation.")

def get_outcome_simulator(dice, num_iterations):
    """
    Return an iterator that randomly selects dice a fixed number of times
    """
    return zip(*(
        itertools.starmap(
            random.choice,
            itertools.repeat((die,), num_iterations)
        )
        for die in dice
    ))

def get_outcome_generator(args):
    """
    based off the args return an iterator that
    enumerates all the possible dice rolls
    or simulates dice rolls.
    """
    dice = get_dice(args)
    iterator = None

    if not isinstance(args.simulate_num_iterations, int):
        iterator = itertools.product(*dice)

    elif args.simulate_num_iterations > 0:
        iterator = get_outcome_simulator(dice, args.simulate_num_iterations)
    else:
        raise Exception('The number of simulation iterations must be a positive integer')

    # an iterator that yields (dice_outcome, count)
    return zip(iterator, itertools.repeat(DEFAULT_DIE_WEIGHT))


def determine_compare_func(param_list):
    if not param_list: return always_true

    """
    parse input into groups delimited by brackets and logical operations
    everything that is not a bracket or a logical operation should be parameters
    that can be parsed into a conditional function
    """
    param_groups_1 = []
    _var = {
        'group': list(),
    }
    def _add_group():
        if len(_var['group']) > 0:
            param_groups_1.append(_var['group'])
            _var['group'] = []

    for item in param_list:
        if item in BRACKET_CHARS or item in BOOLEAN_LOGIC_OPERATORS:
            _add_group()
            param_groups_1.append(item)
        else:
            _var['group'].append(item)

    _add_group()

    # turn parameters into functions
    param_group_funcs = [
        determine_compare_func_helper(item) if isinstance(item, (list, tuple)) else item
        for item in param_groups_1
    ]

    return _parse_param_logic(param_group_funcs)

def _parse_param_logic(logic_param_groups):
    """
    We need a recursive parser.

    This function expects input formated by 'determine_compare_func'
    An example input is expected to be of the form:
    [ func_a, 'or', func_b, 'and', 'not', '[', func_c, 'or', '[', func_d, 'and', func_e, ']', ']' ]
    """

    # re-parse into a tree structure based off the brackets
    param_groups_2 = []
    stack = []
    for index, item in enumerate(logic_param_groups):
        if item == BRACKET_CHARS[0]:
            stack.append(index)
        elif item == BRACKET_CHARS[1]:
            open_index = stack.pop()
            if not stack:
                # found matching close bracket to first opening bracket
                param_groups_2.append(logic_param_groups[open_index+1:index])
        elif not stack:
            param_groups_2.append(item)

    """
    Example state after loop:
    [ func_a, 'or', func_b, 'and', 'not', [ func_c, 'or', '[', func_d, 'and', func_e, ']' ] ]
    Note how the last entry is an actual list now with contents that can be
    recursively sent to  '_parse_param_logic' for parsing.
    Also notice that inside any list entry, there is NOT another list
    if there are brackets, the recursive call will take of that.
    """

    if stack:
        raise Exception('Parsing Error of if-block')

    # we recursively parse anything in brackets
    param_groups_3 = []
    while param_groups_2:
        item = param_groups_2.pop(0)

        if isinstance(item, (list, tuple)):
            param_groups_3.append(_parse_param_logic(item))
        else:
            param_groups_3.append(item)

    """
    parse operations
    We want an order of operations of: [not, and, or]
    We modify the list in place when applying a logical operation
    """
    for operation in BOOLEAN_LOGIC_OPERATOR_ORDER:
        index = 0
        while index < len(param_groups_3):
            item = param_groups_3[index]
            if item != operation:
                index += 1
                continue
            elif item == 'not':
                if len(param_groups_3) < index+1:
                    raise Exception('No Contitional found for `not` to be applied to')

                right_func = param_groups_3[index+1]
                if not hasattr(right_func, '__call__'):
                    raise Exception('Parsing Error of if-block')

                param_groups_3[index] = apply_not(right_func)
                del param_groups_3[index+1]

            elif item == 'and' or item == 'or':
                left_func = param_groups_3[index-1]
                right_func = param_groups_3[index+1]

                if len(param_groups_3) < index+1:
                    raise Exception('Item found for `{}` to be applied to'.format(item))

                if any(not hasattr(func, '__call__') for func in [left_func, right_func]):
                    raise Exception('Parsing Error of if-block')

                operator_apply = apply_and if item == 'and' else apply_or
                new_func = operator_apply(left_func, right_func)

                param_groups_3[index-1] = new_func
                del param_groups_3[index+1]
                del param_groups_3[index]

    if len(param_groups_3) > 1 or not hasattr(param_groups_3[0], '__call__'):
        raise Exception('Parsing Error of if-block')

    return param_groups_3[0]

def determine_compare_func_helper(param_list):
    if not param_list: return None

    _vars = {
        'param_list': list(param_list),
    }

    def _determine_compare_func():
        """
        This function edits the passed parameter list in place
        """
        if not _vars['param_list']:
            raise Exception(
                'Not enough arguments given to determine comparision function for conditional.'
            )

        comparison_str = _vars['param_list'].pop(0)

        if comparison_str in BASIC_COMPARE_DICT:
            return BASIC_COMPARE_DICT[comparison_str]
        elif comparison_str == 'mod':
            try:
                mod_values = tuple(int(item) for item in itertools.takewhile(
                    lambda xx: xx not in COMPARE_KEYWORDS_SET,
                    _vars['param_list']
                ))
                _vars['param_list'] = _vars['param_list'][len(mod_values):]
            except:
                raise Exception("The parameter for `mod` comparision must be an integer")

            other_comparison = _determine_compare_func()

            if len(mod_values) == 1:
                def _compre_func(aa, bb, cc=None,
                    other_comparison=other_comparison,
                    mod_value=mod_values[0],
                ):
                    return other_comparison(aa % mod_value, bb)
            else:
                def _compre_func(aa, bb, cc=None,
                    other_comparison=other_comparison,
                    mod_values=mod_values,
                ):
                    return other_comparison(aa % mod_values[cc], bb)

            return _compre_func
        else:
            raise Exception('Comparison string invalid')

    compare_func_helper = _determine_compare_func()

    try:
        compare_values = tuple(int(item) for item in _vars['param_list'])
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    if not compare_values:
        raise Exception('No compare values where given.')

    @docstring_format(
        param_list=str(param_list),
    )
    def compare_func(value, index,
        # Run time optimizations with variable loopup speed
        compare_values=compare_values,
        compare_func_helper=compare_func_helper,
        is_single_compare=len(compare_values) == 1,
        is_many_compare=len(compare_values) > 1,
    ):
        """
        Compare Func
        params: {param_list}
        """
        if is_single_compare:
            return compare_func_helper(value, compare_values[0], index)
        elif is_many_compare:
            return compare_func_helper(value, compare_values[index], index)

    return compare_func

def _get_param_iterator(xx, *parameter_collection):
    """
    This get iterator function is specific to if-else-able
    operations
    """
    # Run time optimizations with variable loopup speed
    len=tuple.__len__
    repeat=itertools.repeat

    zip_list = []
    zip_list_append = zip_list.append
    zip_list_append(xx)

    for parameter_list in parameter_collection:
        if len(parameter_list) == 1:
            zip_list_append(repeat(parameter_list[0]))
        else:
            zip_list_append(parameter_list)

    return zip(*zip_list)

def get_basic_operation(operation_str, param_list = []):
    """
    The following operations are basic and normally do not need parameters
    The only parameter these can take is one for dice parsing which will result in
    an array like result.
    """

    if not param_list:
        @docstring_format(operation_str)
        def basic_operation(xx,
            # Run time optimizations with variable loopup speed
            operation=OPERATIONS_DICT[operation_str],
        ):
            """Basic Operation: {}"""
            return operation(xx)

        _operator = basic_operation

    elif len(param_list) == 1:
        # parse dice in groups

        _operator = get_slice_apply_operation(
            param_list[0],
            [operation_str],
            should_memorize = False,
        )

    else:
        raise Exception('This operation either takes no parameters or one.')

    return _operator

def get_add_operation(param_list):
    if len(param_list) < 1:
        raise Exception(
            "The 'add' operation requires at least one parameter to determine add value."
        )

    try:
        add_values = tuple(int(item) for item in param_list)
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    @docstring_format(
        add_values=str(add_values),
    )
    def add_func(xx,
        # Run time optimizations with variable loopup speed
        tuple=tuple,
        _get_param_iterator=_get_param_iterator,
        add_values=add_values,
    ):
        """
        Add Function
        Add Values: {add_values}
        """

        return tuple(item+add for item, add in _get_param_iterator(xx, add_values))

    return add_func

def get_set_to_operation(param_list):
    if len(param_list) < 1:
        raise Exception(
            "The 'set-to' operation requires at least one parameter to determine set value."
        )

    try:
        set_to_values = tuple(int(item) for item in param_list)
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    @docstring_format(
        set_to_values=str(set_to_values),
    )
    def set_to_func(xx,
        # Run time optimizations with variable loopup speed
        tuple=tuple,
        _get_param_iterator=_get_param_iterator,
        set_to_values=set_to_values,
    ):
        """
        Set-To Function
        Shift Values: {set_to_values}
        """

        return tuple(set_value for _, set_value in _get_param_iterator(xx, set_to_values))

    return set_to_func

def get_scale_operation(param_list):
    if len(param_list) < 1:
        raise Exception(
            "The 'scale' operation requires at least one parameter to determine add value."
        )

    param_list_copy = list(param_list)

    round_options = 'r-truncate' # set default value

    if param_list_copy[0] in ROUNDING_OPTIONS:
        round_options = param_list_copy.pop(0)

    def scale_operation_round(aa,bb,
        # Run time optimizations with variable loopup speed
        int=int,
        round_func=ROUNDING_OPTIONS[round_options],
    ):
        return int(round_func(aa*bb))

    try:
        scale_values = tuple(float(item) for item in param_list_copy)
    except:
        raise Exception("The parameter(s) passed must be in float(s)")
    else:
        if not scale_values:
            raise Exception("No parameters passed apply the scale operation")

    @docstring_format(
        scale_values=str(scale_values),
    )
    def scale_func(xx,
        # Run time optimizations with variable loopup speed
        tuple=tuple,
        _get_param_iterator=_get_param_iterator,
        scale_operation_round=scale_operation_round,
        scale_values=scale_values,
    ):
        """
        Scale Function
        Scale Values: {scale_values}
        """

        return tuple(
            scale_operation_round(item, scale_factor)
            for item, scale_factor in _get_param_iterator(xx, scale_values)
        )

    return scale_func

def get_exp_operation(param_list):
    if len(param_list) < 1:
        raise Exception(
            "The 'exp' operation requires at least one parameter to determine set value."
        )

    param_list_copy = list(param_list)

    # determin if there are extra optional parameters
    done_extra_parsing = False
    round_func = None

    def exp_operation(aa,bb): return aa**bb # default operation

    while not done_extra_parsing:
        item = param_list_copy[0]

        if item == 'as-base':
            # apply the operation where the parameters passed are treated as the base
            param_list_copy.pop(0)

            # redefine the exp operation
            def exp_operation(aa,bb): return bb**aa

        elif item in ROUNDING_OPTIONS:
            param_list_copy.pop(0)
            round_func = ROUNDING_OPTIONS[item]
        else:
            done_extra_parsing = True

    if round_func is None:
        round_func = ROUNDING_OPTIONS['r-truncate']

    def exp_op_round(aa,bb,
        # Run time optimizations with variable loopup speed
        int=int,
        round_func=round_func,
        exp_operation=exp_operation,
    ):
        return int(round_func(exp_operation(aa, bb)))

    try:
        exp_values = tuple(float(item) for item in param_list_copy)
    except:
        raise Exception("The parameter(s) passed must be in float(s)")
    else:
        if not exp_values:
            raise Exception("No parameters passed apply the exponentiation operation")

    @docstring_format(
        exp_values=str(exp_values),
    )
    def exp_func(xx,
        # Run time optimizations with variable loopup speed
        tuple=tuple,
        _get_param_iterator=_get_param_iterator,
        exp_op_round=exp_op_round,
        exp_values=exp_values,
    ):
        """
        Exp Function
        Shift Values: {exp_values}
        """
        return tuple(
            exp_op_round(item, exp_val) for item, exp_val in _get_param_iterator(xx, exp_values)
        )

    return exp_func

def get_bound_operation(param_list):
    if len(param_list) < 2:
        raise Exception(
            "The 'bound' operation requires at least two parameters to determine min/max bounds."
        )

    if len(param_list) % 2 != 0:
        raise Exception(
            "The 'bound' operation requires parameters in pairs to determine min/max bounds."
        )

    try:
        temp_value = tuple(int(item) for item in param_list)
    except:
        raise Exception("The parameters passed must be in integers")
    else:
        lower_bounds = temp_value[0::2]
        upper_bounds = temp_value[1::2]

    if len(lower_bounds) != len(upper_bounds):
        raise Exception(" ".join([
            "Error during parsing parameters for 'bound'",
            "miss match on lower and upper bound sizes",
        ]))

    for low, high in zip(lower_bounds, upper_bounds):
        if low > high:
            raise Exception('Lower bound is larger than upper bound.')

    def bound_value_func(item, lower, upper):
        if item <= lower: return lower
        elif item >= upper: return upper
        else: return item

    @docstring_format(
        lower_bounds=str(lower_bounds),
        upper_bounds=str(upper_bounds),
    )
    def bound_func(xx,
        # Run time optimizations with variable loopup speed
        tuple=tuple,
        _get_param_iterator=_get_param_iterator,
        bound_value_func=bound_value_func,
        lower_bounds=lower_bounds,
        upper_bounds=upper_bounds,
    ):
        """
        Bound Function
        Lower Bounds: {lower_bounds}
        Upper Bounds: {upper_bounds}
        """
        return tuple(
            bound_value_func(item, lower, upper)
            for item, lower, upper in _get_param_iterator(xx, lower_bounds, upper_bounds)
        )

    return bound_func

def get_reroll_operation(param_list, comparison_func):
    if param_list:
        raise Exception("Reroll doesn't take any parameters")

    @docstring_format(
        param_list=str(param_list),
        conditional_info=comparison_func.__doc__,
    )
    def reroll_func(xx,
        # Run time optimizations with variable loopup speed
        len=tuple.__len__,
        enumerate=enumerate,
        comparison_func=comparison_func,
    ):
        """
        Reroll If Contitional Function
        Conditional: {conditional_info}
        """
        x_len = len(xx)
        for index, item in enumerate(xx):
            if index + 1 == x_len:
                # last item, can't reroll anymore
                return (item,)

            if comparison_func(item, index):
                continue

            # keep result
            return (item,)

        # should never happen, but just in case
        return (xx[-1],)

    return reroll_func

def get_select_operation(param_list):
    if len(param_list) < 1:
        raise Exception(
            "The 'select' operation requires at least one parameter which is the select index."
        )

    try:
        select_indices = tuple(int(item) for item in param_list)
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    @docstring_format(
        select_indices=str(select_indices),
    )
    def multi_select_func(xx,
        # Run time optimizations with variable loopup speed
        tuple=tuple,
        list=list,
        sorted=sorted,
        select_indices=select_indices,
    ):
        """
        Multi Select Function
        Select Indices: {select_indices}
        """
        sorted_list = sorted(list(xx))

        return tuple(sorted_list[ii] for ii in select_indices)

    return multi_select_func

def get_slice_apply_operation(
    slice_params,
    other_param_list,
    should_memorize=False,
    should_validate=True,
):
    if len(slice_params) != 1:
        raise Exception("The 'slice-apply' operation requires the first parameter to slice size.")

    try:
        slice_size = int(slice_params[0])
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    if not other_param_list:
        raise Exception(
            "The 'slice-apply' operation requires extra parameters for another operation."
        )

    # only grab info for the second function
    # since it is this function that will be split off

    (
        second_operator_str,
        second_operator_params,
        _param_list,
        second_bracketed_operation,
    ) = parse_next_command(
        other_param_list,
        should_memorize=should_memorize,
        should_validate=should_validate,
    )

    if second_bracketed_operation is not None:
        second_operator = second_bracketed_operation
    else:
        second_operator = get_operator(
            param_list=[second_operator_str]+second_operator_params,
            should_memorize=should_memorize,
            should_validate=should_validate,
        )

    # third operation is needed to be considered so that each subsequent
    # operation acts on the conmbined data, rather than having branching processing
    if len(_param_list) > 0:
        (
            third_operator_str,
            third_operator_params,
            _param_list,
            third_bracketed_operation,
        ) = parse_next_command(
            _param_list,
            should_memorize=should_memorize,
            should_validate=should_validate,
        )

        if third_bracketed_operation is not None:
            third_operator = third_bracketed_operation
        else:
            third_operator = get_operator(
                param_list=[second_operator_str]+second_operator_params,
                should_memorize=should_memorize,
                should_validate=should_validate,
            )
    else:
        third_operator_str = 'id'
        third_operator_params = []
        third_operator = OPERATIONS_DICT[third_operator_str]

    @docstring_format(
        str(slice_size),
        indent_text(second_operator.__doc__),
        indent_text(third_operator.__doc__),
    )
    def slice_apply_func(xx,
        # Run time optimizations with variable loopup speed
        tuple=tuple,
        second_operator=second_operator,
        third_operator=third_operator,
        slice_size=slice_size,
    ):
        """
        Slice Apply Function
        Slice Size: {}
        ----------------
        Second Operation Doc: {}
        ----------------
        Third Operation Doc: {}
        """
        dice = []
        results = []

        # some runtime optimizations
        dice_len = dice.__len__
        dice_append = dice.append
        results_extend = results.extend

        for ii in xx:
            dice_append(ii)
            if dice_len() < slice_size:
                continue
            else:
                results_extend(second_operator(tuple(dice)))
                dice = []
                dice_append = dice.append
                dice_len = dice.__len__

        return third_operator(tuple(results))

    return slice_apply_func

def get_if_else_operation(
    conditoinal_func,
    if_operation,
    else_operation=None,
    should_validate=True,
):

    _else_operation=else_operation or OPERATIONS_DICT['id']

    @docstring_format(
        indent_text(conditoinal_func.__doc__),
        indent_text(if_operation.__doc__),
        indent_text(_else_operation.__doc__),
    )
    def apply_op_if_else_compare(xx,
        # Run time optimizations with variable loopup speed
        tuple=tuple,
        len=tuple.__len__,
        enumerate=enumerate,
        if_operation=if_operation,
        _else_operation=_else_operation,
        conditoinal_func=conditoinal_func,
        should_validate=should_validate,
    ):
        """
        IF-ELSE operation wrapper
        -------------------
        Conditional func doc: {}

        -------------------
        IF operation doc: {}

        -------------------
        ELSE operation doc: {}
        """
        if_results = if_operation(xx)
        else_results = _else_operation(xx)

        if should_validate and not (len(if_results) == len(else_results) == len(xx)):
            raise Exception("\n".join([
                'Operations given within an if-else-block do not yeild results with matching sizes.',
                'Function Doc: {}'.format(apply_op_if_else_compare.__doc__),
            ]))

        return tuple(
            if_results[index] if conditoinal_func(item, index) else else_results[index]
            for index,item in enumerate(xx)
        )

    return apply_op_if_else_compare

def parse_next_command(
    param_list,
    should_memorize=False,
    should_validate=False,
):
    if not param_list:
        raise Exception("Parsing Error.")

    _param_list = list(param_list)
    cur_params = []
    bracketed_operation = None

    if param_list[0] == BRACKET_CHARS[0]:
        stack = []
        for index, item in enumerate(param_list):

            if item == BRACKET_CHARS[0]:
                stack.append(index)

            elif item == BRACKET_CHARS[1]:
                start_index = stack.pop()

                if (index - start_index) < 2:
                    raise Exception("No contents inside brackets.")

                if not stack:
                    bracketed_operation = get_operator(
                        param_list=param_list[start_index+1:index],
                        should_memorize=should_memorize,
                        should_validate=should_validate,
                    )
                    operation_str = "bracketed-operation"
                    _param_list = param_list[index+1:]
                    break

        if stack:
            raise Exception("Parsing Error. Bracket Mismatch.")

    else:
        operation_str = param_list[0]

        # parse parameters for current operation
        cur_params = list(itertools.takewhile(
            lambda xx: (
                xx not in OPERATIONS_DICT and
                xx not in CUSTOM_OPERATIONS_DICT and
                xx not in LOGIC_KEYWORDS
            ),
            _param_list[1:],
        ))
        _param_list = _param_list[len(cur_params)+1:]

    return (
        operation_str,
        cur_params,
        _param_list,
        bracketed_operation,
    )


def parse_next_conditional_syntax(
    param_list,
    should_memorize=False,
    should_validate=False,
):
    # make a shallow copy
    _param_list = list(param_list)

    # parse conditional statement
    conditoinal_func = None
    else_operation = None
    if _param_list and _param_list[0] == LOGIC_START_KEYWORD:
        full_conditional_params = list(
            itertools.takewhile(
                lambda xx: xx != LOGIC_END_KEYWORD,
                _param_list[1:],
        ))

        cur_conditional_params = list(
            itertools.takewhile(
                lambda xx: (
                    xx != LOGIC_ELSE_KEYWORD and
                    xx != LOGIC_END_KEYWORD
                ),
                _param_list[1:],
        ))

        conditoinal_func = determine_compare_func(cur_conditional_params)

        else_parameters = full_conditional_params[len(cur_conditional_params):]

        if else_parameters and else_parameters[0] == LOGIC_ELSE_KEYWORD:
            token = else_parameters[1]

            if token in ELSE_ABLE_OPERATIONS or token == BRACKET_CHARS[0]:
                else_operation = get_operator(
                    param_list=else_parameters[1:],
                    should_memorize=should_memorize,
                    should_validate=should_validate,
                )

            else:
                raise Exception('Operation cannot be in an else')


        # remove the if
        _param_list = _param_list[1+len(full_conditional_params):]

        # remove the then
        if _param_list and _param_list[0] == LOGIC_END_KEYWORD:
                _param_list = _param_list[1:]

    return (
        conditoinal_func,
        else_operation,
        _param_list
    )

def get_operator(
    param_list=[],
    should_memorize=True,
    should_validate=True,
    is_first_operation=False,
    is_nested=False,
):
    # make a shallow copy
    _param_list = list(param_list)
    _operator = None

    (
        operation_str,
        cur_params,
        _param_list,
        bracketed_operation,
    ) = parse_next_command(
        _param_list,
        should_memorize=should_memorize,
        should_validate=should_validate,
    )

    (
        conditoinal_func,
        else_operation,
        _param_list, # the current param_list after parsing though the conditional
    ) = parse_next_conditional_syntax(
        _param_list,
        should_memorize=should_memorize,
        should_validate=should_validate,
    )

    if not bracketed_operation:
        # skip these checks if we have a bracketed_operation
        if hasattr(conditoinal_func, "__call__") and operation_str not in IF_ABLE_OPERATIONS:
            raise Exception('This operation is not if-able: "{}"'.format(param_list))

        if hasattr(else_operation, "__call__") and operation_str not in ELSE_ABLE_OPERATIONS:
            raise Exception('This operation is not else-able: "{}"'.format(param_list))

    apply_nested_operation = True

    if bracketed_operation is not None:
        if conditoinal_func is None:
            _operator = bracketed_operation
        else:
            _operator = get_if_else_operation(
                conditoinal_func=conditoinal_func,
                if_operation=bracketed_operation,
                else_operation=else_operation,
                should_validate=should_validate,
            )

    elif operation_str in CUSTOM_OPERATIONS_DICT:
        # consider user defined operations before built-in one
        # so if they name a operation as one built in, we use theirs
        # instead
        _operator = custom_func_wrapper(
            CUSTOM_OPERATIONS_DICT[operation_str],
            cur_params,
            should_validate,
        )

    elif operation_str in BASIC_OPERATIONS:
        _operator = get_basic_operation(operation_str, cur_params)

    elif operation_str in IF_ABLE_OPERATIONS and operation_str in ELSE_ABLE_OPERATIONS:

        if operation_str == 'add':
            _operator = get_add_operation(cur_params)

        elif operation_str == 'scale':
            _operator = get_scale_operation(cur_params)

        elif operation_str == 'exp':
            _operator = get_exp_operation(cur_params)

        elif operation_str == 'set-to':
            _operator = get_set_to_operation(cur_params)

        elif operation_str == 'bound':
            _operator = get_bound_operation(cur_params)

        else:
            raise Exception('Error while parsing.')

        if hasattr(conditoinal_func, "__call__"):
            _operator = get_if_else_operation(
                conditoinal_func=conditoinal_func,
                if_operation=_operator,
                else_operation=else_operation,
                should_validate=should_validate,
            )

    elif operation_str == 'reroll':
        _operator = get_reroll_operation(cur_params, conditoinal_func or always_true)

    elif operation_str == 'select':
        _operator = get_select_operation(cur_params)

    elif operation_str == 'slice-apply':
        _operator = get_slice_apply_operation(
            slice_params=cur_params,
            other_param_list=_param_list,
            should_memorize=should_memorize,
            should_validate=should_validate,
        )
        apply_nested_operation = False

    else:
        raise Exception("operation string '{}' is not valid".format(operation_str))

    if apply_nested_operation and _param_list:
        # Apply a nested operation

        other_operator = get_operator(
            param_list=_param_list,
            should_memorize=should_memorize,
            should_validate=should_validate,
        )

        _operator = composed_func_wrapper(
            first_func=_operator,
            second_func=other_operator
        )

    if should_validate:
        _operator = dice_input_checker(_operator)

    if should_memorize and not is_first_operation:
        """
        The top level operation will never benifit from memorize
        since all inputs will be unique by design
        """
        _operator = memorize(_operator)

    return _operator

def save_data(counter_dict, save_file_path):
    save_dict = dict()

    for key, value in counter_dict.items():
        new_key = key
        if isinstance(new_key, int):
            new_key = [key]

        if isinstance(new_key, (list, tuple)):
            new_key = json.dumps(new_key)
        else:
            raise Exception("Unexpected key to save: {}".format(key))

        save_dict[new_key] = value

    with open(save_file_path, "w") as file_stream:
        json.dump(save_dict, file_stream)

def load_data(file_path):
    if not os.path.isfile(file_path):
        raise Exception('File path give to load is not a file.')

    with open(file_path) as file_stream:
        load_dict = json.load(file_stream)

    counter_dict = Counter()

    for key, value in load_dict.items():
        new_key = None

        try:
            new_key = tuple(json.loads(key))
        except:
            raise Exception("Key in file is not valid")
        else:
            if not all(isinstance(entry, int) for entry in new_key):
                raise Exception("Key in file is not valid")

            new_key = tuple(zip(new_key, itertools.repeat(1)))

        if not isinstance(value, int):
            raise Exception("Values given in file are not integers.")

        counter_dict[new_key] += value

    return counter_dict

def counter_dict_product(*counter_dicts):
    for items in itertools.product(*(count_dict.items() for count_dict in counter_dicts)):
        keys, values = zip(*items)
        yield tuple(itertools.chain(*keys)), prod_values(values)

def display_data(args, counter_dict):
    total = sum(counter_dict.values())

    _temp_key = list(counter_dict.keys())[0]
    num_items_in_key = len(_temp_key)

    all_keys = []
    values_has_float = False

    for key_set, count_value in counter_dict.items():
        all_keys.extend(key_set)
        values_has_float+= isinstance(count_value, float)

    num_key_digits = find_max_digits(all_keys)

    sub_key_formater = "{{key:{num_key_digits}d}}".format(
        num_key_digits=num_key_digits
    )

    key_formater = "{{key:>{num_char}s}}".format(
        num_char = sum([
            num_items_in_key * num_key_digits, # room for all the digits
            (num_items_in_key - 1) * len(","), # room for all the seperators
        ]),
    )

    num_count_digits = find_max_digits(counter_dict.values())

    if args.show_counts:
        value_formater = "{{value:{num_count_digits}{type}}}".format(
            num_count_digits=num_count_digits,
            type='d' if not values_has_float else '.{}f'.format(args.result_decimal_place),
        )
    else:
        value_formater = "{{value:{percent_formatter}}} %".format(
            percent_formatter="{}.{}f".format(
                len("100.") + args.result_decimal_place,
                args.result_decimal_place,
            ),
        )

    full_formater = "{key}: {value} {bar}"

    if args.sort == "key":
        iterater = sorted(list(counter_dict.items()))
    elif args.sort == "value":
        iterater = sorted(list(counter_dict.items()), key=lambda xx:xx[-1::-1])
    else:
        raise Exception("Unexpected sort value")

    for key, count_value in iterater:

        percent = 100 * float(count_value) / total

        key_string = key_formater.format(
            key=",".join(sub_key_formater.format(key=_key) for _key in key)
        )
        value_string = value_formater.format(
            value=count_value if args.show_counts else percent
        )

        bar_string = ""
        if args.bar_size > 0:
            bar = int(percent * args.bar_size) * args.bar_char
            bar_string = args.bar_prefix + bar

        print(full_formater.format(
            key=key_string,
            value=value_string,
            bar=bar_string,
        ))

def main():
    args = parser.parse_args()

    if args.show_args:
        print(args)

    # load dice values
    if isinstance(args.load_file_paths, (list, tuple)) and args.load_file_paths:
        dice_iterator = counter_dict_product(*(
            load_data(file_path)
            for file_path in args.load_file_paths
        ))
    else:
        dice_iterator = get_outcome_generator(args)

    if isinstance(args.custom, (list, tuple)) and args.custom:
        load_custom_files(args.custom)

    _operator = get_operator(
        # remove any entries that are empty strings
        param_list=simple_clean_params(args.apply),
        should_memorize=args.memorize_input,
        should_validate=args.should_valdiate_input,
        is_first_operation=True,
    )

    counter_dict = Counter()

    # the next few lines is the majority of the program run time for larger values
    for dice, count in dice_iterator:
        dice_pool, weight_values = zip(*dice)
        counter_dict[_operator(dice_pool)] += count * prod_values(weight_values)

    if args.save_file_path is not None:
        save_data(counter_dict, args.save_file_path)

    if args.display_output:
        display_data(args, counter_dict)

if __name__ == '__main__':
    main()
