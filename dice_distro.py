from __future__ import print_function

import argparse
import decimal
import functools
import itertools
import json
import math
import operator
import os
import random
import sys

from collections import Counter

if (2,0) <= sys.version_info < (3, 0):
    zip = itertools.izip

OPERATIONS_DICT = {
    'id':tuple,
    'sum':lambda xx: (sum(xx),),
    'min':lambda xx: (min(xx),),
    'max':lambda xx: (max(xx),),
    'set':lambda xx: tuple(sorted(xx)),
    'prod':lambda xx: (functools.reduce(operator.mul, xx, 1),),
    'bit-or':lambda xx: (functools.reduce(operator.or_, xx, 0),),
    'bit-xor':lambda xx: (functools.reduce(operator.xor, xx),),
    'bit-and':lambda xx: (functools.reduce(operator.and_, xx),),
    'shift': None, # This will get defined later if used
    'scale': None, # This will get defined later if used
    'bound': None, # This will get defined later if used
    'select': None, # This will get defined later if used
    'reroll': None, # This will get defined later if used,
    'slice-apply': None, # This will get defined later if used,
}

BASIC_OPERATIONS = set(
    key for key,value in OPERATIONS_DICT.items() if value is not None
)

# set of operations that support an if-block
IF_ABLE_OPERATIONS = set([
    'shift',
    'scale',
    'bound',
    'select',
    'reroll',
])

BASIC_COMPARE_DICT = {
    'eq':lambda aa,bb,cc=None: aa == bb,
    'gt':lambda aa,bb,cc=None: aa > bb,
    'ge':lambda aa,bb,cc=None: aa >= bb,
    'lt':lambda aa,bb,cc=None: aa < bb,
    'le':lambda aa,bb,cc=None: aa <= bb,
}

class CustomFormatter(argparse.HelpFormatter):
    """
    Utilized code from:
        - https://github.com/bewest/argparse/blob/master/argparse.py
            class RawDescriptionHelpFormatter(HelpFormatter)
            class ArgumentDefaultsHelpFormatter(HelpFormatter)
            RawTextHelpFormatter._split_lines
        - https://bitbucket.org/ruamel/std.argparse/src/cd5e8c944c5793fa9fa16c3af0080ea31f2c6710/__init__.py?at=default&fileviewer=file-view-default

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

def parse_int(compare_func, type_string):
    if not hasattr(compare_func,'__call__'):
        raise Exception('A function must be passed to parse_int.')

    def parse_int_compare(value):
        ivalue = int(value)
        if not compare_func(ivalue):
            raise argparse.ArgumentTypeError("{} is an invalid {} int value".format(value,type_string))
        return ivalue

    return parse_int_compare

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
    'Single Die Type Options',
    'Use these flags when wanting to roll a specific die type.',
)

single_type_group.add_argument(
    "--num-dice","-n",
    type=parse_int(lambda xx: xx > 0, 'positive'),
    default=1,
    help="Number of dice simulated",
)

single_type_group_side_option = single_type_group.add_mutually_exclusive_group()

single_type_group_side_option.add_argument(
    "--die-sides","-d",
    type=parse_int(lambda xx: xx > 0, 'positive'),
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
    default=1,
    help=" ".join([
        "If using '--die-sides' this defines the lowest value of the die.",
        "This option is ignored if '--die-sides' is not used.",

    ]),
)

single_type_group.add_argument(
    "--die-step",
    type=int,
    default=1,
    help=" ".join([
        "If using '--die-sides' this defines the increments between values on the sides of the die.",
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

"""
========================================================================================
Multi Die Options
========================================================================================
"""
multi_type_group = parser.add_argument_group(
    'Multi Die Type Options',
    'Use these flags when wanting to roll multiple types of dies at once.',
)

multi_type_group.add_argument(
    "--multi-die-sides",
    type=parse_int(lambda xx: xx > 0, 'positive'),
    nargs="+",
    help=" ".join([
        "Number of sides the dice simulated should have.",
        "The value given must be a positive integer.",
        "The values on the die will start from '--die-start' and fill up the sides of the die",
        "incrementing by '--die-step'.",
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
        "If using '--die-sides' this defines the increments between values on the sides of the die.",
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

"""
========================================================================================
Operation Options
========================================================================================
"""
op_group = parser.add_argument_group(
    'Operation Options',
    'Options how to deal with the result of rolls of the dice.',
)

op_group.add_argument(
    "--apply",
    type=str,
    nargs="*",
    default = ['id'],
    help="\n".join([
        "D|"
        # Intro block
        "The operation that will be applied to the values rolled.",
        "Operations can be chained, but it is up to the user to make",
        "sure that the outputs of one are correct inputs for the other.",
        # Explain if-block synatx
        "Some operations can be applied conditionally, denoted by an",
        "if-block between the operation string and its parameters.",
        "The 'then' keyword can be used to denote the end",
        "of the conditional statement",
        "if more operation or parameters are needed.",
        "Example Syntax:",
        "'--apply op1 if cond1... then params1... then op2 if cond2... then params2...'",
        "Note that if the last operation does not need parameters",
        "but has an if-block, the final 'then' is not needed.",
        # End of into block
        # Define id operation
        "The 'id' operation refers to the identity operation, which will",
        "leave the input unchanged.",
        # Define math operations operation
        "The following operations:",
        "'sum', 'min', 'max', 'set', 'prod', 'bit-or', 'bit-xor', 'bit-and',",
        "apply their assosiated operation to all the dice.",
        "An optional parameter can be given for a block-size, for block-wise application.",
        "If the a block-size parameter is used, the results will be treated",
        "as distinguishable dice.",
        # Define set operation
        "The 'set' enumerates the results, treating the dice is indistiguishable.",
        # Define shift operation
        "The 'shift' operation will add a static value to all results",
        "(you can specify the value per die).",
        # Define bound operation
        "The 'bound' operation will keep the values within specified upper and",
        "lower bound (can be spcified per die).",
        # Define reroll operation
        "The 'reroll' will assume ordered dice rolls.",
        "To be useful, 'reroll' should be given an if block,",
        "otherwise, the die is always rerolled and the final roll will just be used.",
        # Define slice-apply operation
        "The 'slice-apply' will take an block-size parameter to split the current",
        "dice pool into blocks.",
        "The immideate subsequent operation is applied to each block independently.",
        "Operations applied after the immideate subsequent one will be applied to the",
        "whole dice pool again (unless 'slice-apply' is used again).",
        # Define select operation
        "The 'select' operation requires at least one integer parameter.",
        "This parameter is the index of the item in the sorted array.",
        "Example-Select-1: '--apply select  0' is the same as min.",
        "Example-Select-2: '--apply select  1' returns the second lowest value.",
        "Example-Select-3: '--apply select -1' is the same as max.",
        "Example-Select-4: '--apply select -2' returns the second highest value.",
    ]),
)

op_group.add_argument(
    "--bracket-chars",
    type=str,
    nargs=2,
    default=['[',']'],
    help=" ".join([
        "You can redfine what the delimiter for brackets are.",
        "You must give two values, for the left brackets, then the right."
    ]),
)

op_group.add_argument(
    "--memorize",
    action='store_true',
    help=" ".join([
        "An option for cashing results.",
        "This will hash the results of a roll, and save the result.",
        "This speeds up some calculations, but adds overhead since you",
        "must calculate the hash of the input.",
    ]),
)

"""
========================================================================================
Bar Options
========================================================================================
"""
bar_group = parser.add_argument_group(
    'Bar Options',
    'Options related to the bar rendering',
)

bar_group.add_argument(
    "--bar-size",
    type=parse_int(lambda xx: xx >= 0, 'non-negative'),
    default = 2,
    help=" ".join([
        "The approximate number of '--bar-char'(s) that count as 1 percent.",
        "If '--bar-size' is set to zero, then no bars will be displayed.",
    ]),
)

bar_group.add_argument(
    "--bar-char",
    type=str,
    default = "=",
    help=" ".join([
        "The fill string used for the bar charts.",
        "One percent is represented as this string repeated '--bar-size' times.",
    ]),
)

bar_group.add_argument(
    "--bar-prefix",
    type=str,
    default = "|",
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
    'Display Output Options',
    'Options related to displaying calculated information',
)

display_output_group.add_argument(
    "--sort",
    type=str,
    choices=["key","value"],
    default = 'key',
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
    "--percent-decimal-place","-pdp",
    type=parse_int(lambda xx: xx > 0, 'positive'),
    default = 2,
    help="The number of digits that will be displayed after the decimal place.",
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
    'Simulate Options',
    ' '.join([
        'Options related to simulating the dice rolls rather than enumerating all the outcomes.',
        'Useful if the compute time of calculating all the outcomes takes too long.',
        'This will only provide an approximation of the results.',
    ]),
)

simulate_group.add_argument(
    '--simulate',
    dest='simulate_num_iterations',
    type=parse_int(lambda xx: xx > 0, 'positive'),
    default = None,
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
    'Save/Load Options',
    ' '.join([
        'Options related to saving data and loading data'
    ]),
)

file_save_load_options.add_argument(
    '--load',
    dest='load_file_paths',
    type=str,
    nargs="*",
    default = None,
    help=" ".join([
        "The file path of where you want the data loaded from.",
        "NOTE: If this parameter is used, all dice generation parameters will be ignored.",
    ]),
)


file_save_load_options.add_argument(
    '--save',
    dest='save_file_path',
    type=str,
    default = None,
    help=" ".join([
        "The file path of where you want the data saved.",
    ]),
)


ARGS = parser.parse_args()


BRACKET_CHARS = ARGS.bracket_chars
BRACKET_SET = set(BRACKET_CHARS)

BOOLEAN_LOGIC_OPERATOR_ORDER = ['not', 'and', 'or']
BOOLEAN_LOGIC_OPERATORS = set(BOOLEAN_LOGIC_OPERATOR_ORDER)

COMPARE_KEYWORDS_SET = set.union(
    set([
        'mod',
    ]),
    set(BASIC_COMPARE_DICT.keys()),
    BOOLEAN_LOGIC_OPERATORS,
)

if any(char in COMPARE_KEYWORDS_SET for char in BRACKET_CHARS):
    raise Exception('The bracket chars you set cannot be an existing keyword.')


def always_true(*args, **kwargs):
    return True

def apply_not(func):
    def not_func(*args, **kwargs):
        return not func(*args, **kwargs)
    return not_func

def apply_and(*funcs):
    def and_func(*args, **kwargs):
        return all(func(*args, **kwargs) for func in funcs)
    return and_func

def apply_or(*funcs):
    def or_func(*args, **kwargs):
        return any(func(*args, **kwargs) for func in funcs)
    return or_func

def docstring_format(*sub,**kwargs):
    def decorator(func):
        func.__doc__ = func.__doc__.format(*sub,**kwargs)
        return func
    return decorator

def dice_input_checker(func):
    @functools.wraps(func)
    def wrapper(xx):
        if not isinstance(xx, (list, tuple)):
            raise Exception('Input of operation is not an instance of `list` or `tuple`. Given: {}'.format(str(xx)))

        if not all(isinstance(item, int) for item in xx):
            raise Exception('Entries in the list/tuple are not integers. Given: {}'.format(str(xx)))

        return func(xx)

    return wrapper

def memorize(func):
    cashe = dict()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (tuple(args),frozenset(kwargs.items()))

        if key in cashe: return cashe[key]

        result = func(*args, **kwargs)
        cashe[key] = result

        return result

    return wrapper

def get_dice(args):
    if isinstance(args.multi_die_sides, (list,tuple)):
        dice = []

        if isinstance(args.multi_die_values, (list,tuple)) and len(args.multi_die_values) > 0:
            die = []
            for value in args.multi_die_values:
                die.append(value)
                if len(die) == args.multi_die_sides[len(dice)]:
                    dice.append(tuple(die))
                    die = []

            if len(dice) != len(args.multi_die_sides):
                raise Exception("Not enough die values were given")

            if sum(len(item) for item in dice) != len(args.multi_die_values):
                raise Exception("Not all die values were used")

        else:
            if isinstance(args.multi_die_start, (list,tuple)) and len(args.multi_die_start) > 0:
                if len(args.multi_die_start) != len(args.multi_die_sides):
                    raise Exception("Multi die starts must have parallel values to multi die sides")

                start_values = args.multi_die_start
            else:
                start_values = tuple(1 for _ in args.multi_die_sides)

            if isinstance(args.multi_die_step, (list,tuple)) and len(args.multi_die_step) > 0:
                if len(args.multi_die_step) != len(args.multi_die_step):
                    raise Exception("Multi die steps must have parallel values to multi die sides")

                step_values = args.multi_die_step
            else:
                step_values = tuple(1 for _ in args.multi_die_sides)

            for start,step,size in zip(start_values, step_values, args.multi_die_sides):
                dice.append(range(start,start+step*size, step))

        return tuple(dice)
    else:
        if isinstance(args.die_sides,int) and len(args.die_values) > 0:
            raise Exception("Both die sides are given and die values are given. Only pass one")

        elif isinstance(args.die_sides,int) and args.die_sides > 0:
            values = range(args.die_start,args.die_start + args.die_step*args.die_sides, args.die_step)

        elif len(args.die_values) > 0:
            values = args.die_values

        else:
            raise Exception('Must pass in one of \'--die\' or \'--die-values\'')

        return tuple(values for _ in range(args.num_dice))

def get_outcome_simulator(dice, num_iterations):
    """
    Return an iterator that randomly selects dice a fixed number of times
    """
    return zip(*tuple(itertools.starmap(
            random.choice, itertools.repeat((die,), num_iterations)
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
        iterator = get_outcome_simulator(dice,args.simulate_num_iterations)
    else:
        raise Exception('The number of simulation iterations must be a positive integer')

    # an iterator that yields (dice_outcome, count)
    return zip(iterator, itertools.repeat(1))


def find_max_digits(iterable):
    if not all(isinstance(xx, (int, float)) for xx in iterable):
        raise Exception('All items in the iterable must be ints or floats.')

    max_abs = max(abs(xx) for xx in iterable)
    any_neg = any(xx < 0 for xx in iterable)

    return 1*any_neg + int(
        math.ceil(
            math.log10(max_abs)
    ))

def determine_compare_func(param_list):
    if len(param_list) == 0: return always_true

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

    left_len = len(BRACKET_CHARS[0])
    left_len = len(BRACKET_CHARS[1])
    for item in param_list:
        did_parse = False
        for bracket in BRACKET_CHARS:
            if item.startswith(bracket):
                _add_group()
                param_groups_1.append(bracket)
                if len(item) > len(bracket): _var['group'].append(item[len(bracket):])
                did_parse = True
            elif item.endswith(bracket):
                _add_group()
                param_groups_1.append(bracket)
                if len(item) > len(bracket): _var['group'].append(item[:-len(bracket)])
                did_parse = True

        if did_parse:
            # we parsed so continue on to the next item
            continue
        elif item in BOOLEAN_LOGIC_OPERATORS:
            _add_group()
            param_groups_1.append(item)

        else:
            _var['group'].append(item)

    _add_group()

    # turn parameters into functions
    param_group_funcs = [
        determine_compare_func_helper(item) if isinstance(item,(list,tuple)) else item
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
    for index,item in enumerate(logic_param_groups):
        if item == BRACKET_CHARS[0]:
            stack.append(index)
        elif item == BRACKET_CHARS[1]:
            open_index = stack.pop()
            if len(stack) == 0:
                # found matching close bracket to first opening bracket
                param_groups_2.append(logic_param_groups[open_index+1:index])
        elif len(stack) == 0:
            param_groups_2.append(item)

    """
    Example state after loop:
    [ func_a, 'or', func_b, 'and', 'not', [ func_c, 'or', '[', func_d, 'and', func_e, ']' ] ]
    Note how the last entry is an actual list now with contents that can be
    recursively sent to  '_parse_param_logic' for parsing.
    Also notice that inside any list entry, there is NOT another list
    if there are brackets, the recursive call will take of that.
    """

    if len(stack) > 0:
        raise Exception('Parsing Error of if-block')

    # we recursively parse anything in brackets
    param_groups_3 = []
    while len(param_groups_2) > 0:
        item = param_groups_2.pop(0)

        if isinstance(item,(list,tuple)):
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
                new_func = operator_apply(left_func,right_func)

                param_groups_3[index-1] = new_func
                del param_groups_3[index+1]
                del param_groups_3[index]

    if len(param_groups_3) > 1 or not hasattr(param_groups_3[0], '__call__'):
        raise Exception('Parsing Error of if-block')

    return param_groups_3[0]

def determine_compare_func_helper(param_list):
    if len(param_list) == 0: return always_true

    _vars = {
        'param_list': list(param_list),
    }

    def _determine_compare_func():
        """
        This function edits the passed parameter list in place
        """
        if len(_vars['param_list']) == 0:
            raise Exception('Not enough arguments given to determine comparision function for conditional.')

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
                return lambda aa,bb,cc=None: other_comparison(aa % mod_values[0], bb)
            else:
                return lambda aa,bb,cc=None: other_comparison(aa % mod_values[cc], bb)
        else:
            raise Exception('Comparison string invalid')

    compare_func_helper = _determine_compare_func()

    try:
        compare_values = tuple(int(item) for item in _vars['param_list'])
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    if len(compare_values) == 0:
        raise Exception('No compare values where given.')

    @docstring_format(
        param_list=str(param_list),
    )
    def compare_func(value, index):
        """
        Compare Func
        params: {param_list}
        """
        if len(compare_values) == 1:
            return compare_func_helper(value, compare_values[0], index)
        elif len(compare_values) > 1:
            return compare_func_helper(value, compare_values[index], index)

    return compare_func

def get_basic_operation(operation_str, param_list = []):
    """
    The following operations are basic and normally do not need parameters
    The only parameter these can take is one for dice parsing which will result in
    an array like result.
    """

    if len(param_list) == 0:
        _operator = OPERATIONS_DICT[operation_str]

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

def get_shift_operation(param_list, conditoinal_func):
    if len(param_list) < 1:
        raise Exception("The 'shift' operation requires at least one parameter to determine shift value.")

    only_one_param = len(param_list) == 1

    try:
        shift_values = tuple(int(item) for item in param_list)
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    @docstring_format(
        shift_values=str(shift_values),
    )
    def shift_func(xx):
        """
        Shift Function
        Shift Values: {shift_values}
        """
        if only_one_param:
            iterable = zip(
                xx,
                itertools.repeat(shift_values[0],len(xx)),
            )
        else:
            iterable = zip(xx, shift_values)

        return tuple(
            item+shift if conditoinal_func(item,index) else item
            for index, (item,shift) in enumerate(iterable)
        )

    return shift_func

def get_scale_operation(param_list, conditoinal_func):
    if len(param_list) < 1:
        raise Exception("The 'scale' operation requires at least one parameter to determine shift value.")

    round_option_dict = {
        'r-ceil': lambda xx: math.ceil(xx),
        'r-floor': lambda xx: math.floor(xx),
        'r-truncate': lambda xx: int(xx),
        'r-half-up': lambda xx: decimal.Decimal(xx).quantize(decimal.Decimal('1'),rounding=decimal.ROUND_HALF_UP),
        'r-half-down': lambda xx: decimal.Decimal(xx).quantize(decimal.Decimal('1'),rounding=decimal.ROUND_HALF_DOWN),
    }

    param_list_copy = list(param_list)

    # set default value
    round_options = 'r-truncate'
    if param_list_copy[0] in round_option_dict:
        round_options = param_list_copy.pop(0)

    round_func = round_option_dict[round_options]
    scale_operation = lambda aa,bb: int(round_func(aa*bb))

    only_one_param = len(param_list_copy) == 1

    try:
        scale_values = tuple(float(item) for item in param_list_copy)
    except:
        raise Exception("The parameter(s) passed must be in float(s)")

    @docstring_format(
        scale_values=str(scale_values),
    )
    def scale_func(xx):
        """
        Shift Function
        Shift Values: {scale_values}
        """
        if only_one_param:
            iterable = zip(
                xx,
                itertools.repeat(scale_values[0],len(xx)),
            )
        else:
            iterable = zip(xx, scale_values)

        return tuple(
            scale_operation(item,scale_factor) if conditoinal_func(item,index) else item
            for index,(item,scale_factor) in enumerate(iterable)
        )

    return scale_func

def get_bound_operation(param_list, conditoinal_func):
    if len(param_list) < 2:
        raise Exception("The 'bound' operation requires at least two parameters to determine min/max bounds.")

    if len(param_list) % 2 != 0:
        raise Exception("The 'bound' operation requires parameters in pairs to determine min/max bounds.")

    only_one_pair = len(param_list) == 2

    try:
        temp_value = tuple(int(item) for item in param_list)
    except:
        raise Exception("The parameters passed must be in integers")
    else:
        lower_bounds = temp_value[0::2]
        upper_bounds = temp_value[1::2]

    if len(lower_bounds) != len(upper_bounds):
        raise Exception("Error during parsing parameters for 'bound', miss match on lower and upper bound sizes")

    for low,high in zip(lower_bounds,upper_bounds):
        if low > high:
            raise Exception('Lower bound is larger than upper bound.')

    def bound_value_func(item, upper, lower):
        if item <= lower: return lower
        elif item >= upper: return upper
        else: return item

    @docstring_format(
        lower_bounds=str(lower_bounds),
        upper_bounds=str(upper_bounds),
    )
    def bound_func(xx):
        """
        Bound Function
        Lower Bounds: {lower_bounds}
        Upper Bounds: {upper_bounds}
        """
        results = []

        if only_one_pair:
            iterable = zip(
                xx,
                itertools.repeat(lower_bounds[0],len(xx)),
                itertools.repeat(upper_bounds[0],len(xx)),
            )
        else:
            iterable = zip(xx, lower_bounds, upper_bounds)

        return tuple(
            bound_value_func(item, upper, lower) if conditoinal_func(item,index) else item
            for index,(item,lower,upper) in enumerate(iterable)
        )

    return bound_func

def get_reroll_operation(param_list, comparison_func):
    if len(param_list) > 0:
        raise Exception("Reroll doesn't take any parameters")

    @docstring_format(
        param_list=str(param_list),
        conditional_info=comparison_func.__doc__,
    )
    def reroll_func(xx):
        """
        Reroll If Contitional Function
        Conditional: {conditional_info}
        """
        for index,item in enumerate(xx):
            if index + 1 == len(xx):
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
        raise Exception("The 'select' operation requires at least one parameter which is the select index.")

    try:
        select_indices = tuple(int(item) for item in param_list)
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    @docstring_format(
        select_indices=str(select_indices),
    )
    def multi_select_func(xx):
        """
        Multi Select Function
        Select Indices: {select_indices}
        """
        sorted_list = sorted(list(xx))

        return tuple(sorted_list[ii] for ii in select_indices)

    return multi_select_func

def get_slice_apply_operation(slice_params, other_param_list, should_memorize = False):
    if len(slice_params) != 1:
        raise Exception("The 'slice-apply' operation requires the first parameter to slice size.")

    try:
        slice_size = int(slice_params[0])
    except:
        raise Exception("The parameter(s) passed must be in integer(s)")

    if len(other_param_list) == 0:
        raise Exception("The 'slice-apply' operation requires extra parameters for another operation.")

    # only grab info for the second function
    # since it is this function that will be split off
    second_operator_str = other_param_list[0]
    second_operator_params = list(itertools.takewhile(lambda xx: xx not in OPERATIONS_DICT, other_param_list[1:]))
    second_operator = get_operator(
        second_operator_str,
        param_list = second_operator_params,
        should_memorize = should_memorize,
    )

    # third operation is needed to be considered so that each subsequent
    # operation acts on the conmbined data, rather than having branching processing
    num_params_related_to_second = len(second_operator_params) + 1
    if num_params_related_to_second < len(other_param_list):
        # there is a third operation
        third_operator_str = other_param_list[num_params_related_to_second]
        third_operator_params = other_param_list[num_params_related_to_second+1:]
        third_operator = get_operator(
            third_operator_str,
            param_list = third_operator_params,
            should_memorize = should_memorize,
        )
    else:
        third_operator_str = 'id'
        third_operator_params = []
        third_operator = get_operator(third_operator_str)

    @docstring_format(
        slice_size=str(slice_size),
        second_operator_str=second_operator_str,
        second_operator_params=str(second_operator_params),
        third_operator_str=third_operator_str,
        third_operator_params=str(third_operator_params),
    )
    def slice_apply_func(xx):
        """
        Slice Apply Function
        Slice Size: {slice_size}
        Second Operation: {second_operator_str}
        Second Operation Parameters: {second_operator_params}
        Third Operation: {third_operator_str}
        Third Operation Parameters: {third_operator_params}
        """
        dice = []
        results = []
        for ii in xx:
            dice.append(ii)
            if len(dice) < slice_size:
                continue
            else:
                results.extend(second_operator(dice))
                dice = []

        return third_operator(tuple(results))

    return slice_apply_func

def get_operator(operation_str, param_list = [], should_memorize = True):
    orignal_params = list(param_list)

    conditional_params = []
    if len(param_list) > 0 and param_list[0] == 'if':
        if operation_str in IF_ABLE_OPERATIONS:
            conditional_params = list(itertools.takewhile(lambda xx: xx != 'then', param_list[1:]))
            param_list = param_list[1+len(conditional_params):]

            if len(param_list) > 0 and param_list[0] == 'then':
                param_list = param_list[1:]
        else:
            raise Exception('This operation is not if-able.')

    conditoinal_func = determine_compare_func(conditional_params)

    cur_params = list(itertools.takewhile(lambda xx: xx not in OPERATIONS_DICT, param_list))
    apply_nested_operation = True

    param_list = param_list[len(cur_params):]

    if operation_str in BASIC_OPERATIONS:
        _operator = get_basic_operation(operation_str, cur_params)

    elif operation_str == 'shift':
        _operator = get_shift_operation(cur_params, conditoinal_func)

    elif operation_str == 'scale':
        _operator = get_scale_operation(cur_params, conditoinal_func)

    elif operation_str == 'bound':
        _operator = get_bound_operation(cur_params, conditoinal_func)

    elif operation_str == 'reroll':
        _operator = get_reroll_operation(cur_params, conditoinal_func)

    elif operation_str == 'select':
        _operator = get_select_operation(cur_params)

    elif operation_str == 'slice-apply':
        _operator = get_slice_apply_operation(cur_params, param_list, should_memorize)
        apply_nested_operation = False

    else:
        raise Exception("operation string '{}' is not valid".format(operation_str))

    if apply_nested_operation and len(param_list):
        # Apply a nested operation

        other_operator_str = param_list[0]
        other_operator_params = param_list[1:]

        other_operator = get_operator(
            other_operator_str,
            param_list = other_operator_params,
            should_memorize = should_memorize,
        )

        _first_operation = _operator

        @docstring_format(
            first_operation_str=operation_str,
            first_operation_params=str(cur_params),
            other_operator_str=other_operator_str,
            other_operator_params=str(other_operator_params),
        )
        def composite_operation(xx):
            """
            First Operation: {first_operation_str}
            First Operation Parameters: {first_operation_params}
            Other Operation: {other_operator_str}
            Other Operation Parameters: {other_operator_params}
            """
            return other_operator(_first_operation(xx))

        _operator = composite_operation

    _operator = dice_input_checker(_operator)

    if should_memorize:
        # return an function that cashes the results to speed up runtime at the cost of memory
        _operator = memorize(_operator)

    return dice_input_checker(_operator)

def save_data(counter_dict, save_file_path):
    save_dict = dict()

    for key,value in counter_dict.items():
        new_key = None
        if isinstance(key,(list,tuple)):
            new_key = json.dumps(key)
        elif isinstance(key,int):
            new_key = key
        else:
            raise Exception("Unexpected key to save: {}".format(key))

        save_dict[new_key] = value

    with open(save_file_path, "w") as file_stream:
        json.dump(save_dict, file_stream)

def load_data(file_path):
    counter_dict = Counter()

    if not os.path.isfile(file_path):
        raise Exception('File path give to load is not a file.')

    with open(file_path) as file_stream:
        load_dict = json.load(file_stream)

    for key,value in load_dict.items():
        new_key = None
        try:
            new_key = tuple(json.loads(key))
        except:
            # key is not a list
            try:
                new_key = int(key)
            except:
                raise Exception("Key in file is not valid")

        if not isinstance(value, int):
            raise Exception("Values given in file are not integers.")


        counter_dict[new_key] = value

    return counter_dict

def counter_dict_product(*args):
    for items in itertools.product(*tuple(count_dict.items() for count_dict in args)):
        full_key = []
        full_value = 1

        for key, value in items:
            if isinstance(key, (tuple,list)):
                full_key.extend(key)
            elif isinstance(key, int):
                full_key.append(key)

            full_value*=value

        yield tuple(full_key),full_value

def display_data(args,counter_dict):
    total = sum(counter_dict.values())

    _temp_key = list(counter_dict.keys())[0]
    num_items_in_key = len(_temp_key)

    all_keys = []
    for key_set in counter_dict:
        all_keys.extend(key_set)
    num_key_digits = find_max_digits(all_keys)

    sub_key_formater = "{{key:{num_key_digits}d}}".format(
        num_key_digits=num_key_digits
    )

    key_formater = "{{key:>{num_char}s}}".format(
        num_char=sum([
            num_items_in_key*num_key_digits, # room for all the digits
            (num_items_in_key - 1)*len(","), # room for all the seperators
        ]),
    )

    num_count_digits = find_max_digits(counter_dict.values())

    if args.show_counts:
        value_formater = "{{value:{num_count_digits}d}}".format(
            num_count_digits=num_count_digits,
        )
    else:
        value_formater = "{{value:{percent_formatter}}} %".format(
            percent_formatter = "{}.{}f".format(
                len("100.") + ARGS.percent_decimal_place,
                ARGS.percent_decimal_place,
            ),
        )

    full_formater = "{key}: {value} {bar}"

    if args.sort == "key":
        iterater = sorted(list(counter_dict.items()))
    elif args.sort == "value":
        iterater = sorted(list(counter_dict.items()), key=lambda xx:xx[-1::-1])
    else:
        raise Exception("Unexpected sort value")

    for key,count_value in iterater:

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
    counter_dict = Counter()

    if ARGS.show_args:
        print(ARGS)

    if isinstance(ARGS.load_file_paths, (list,tuple)) and len(ARGS.load_file_paths) > 0:
        iterator = counter_dict_product(*tuple(
            load_data(file_path)
            for file_path in ARGS.load_file_paths
        ))
    else:
        iterator = get_outcome_generator(ARGS)

    _operator = get_operator(ARGS.apply[0], ARGS.apply[1:], ARGS.memorize)

    # the next two lines is the majority of the program run time for larger values
    for item,count in iterator:
        counter_dict[_operator(item)] += count

    if ARGS.save_file_path is not None:
        save_data(counter_dict, ARGS.save_file_path)

    if ARGS.display_output:
        display_data(ARGS,counter_dict)

if __name__ == '__main__':
    main()
