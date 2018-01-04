from __future__ import print_function

import sys
import math
import argparse
import operator
import functools
import random
import itertools
import decimal
from collections import Counter

if (2,0) <= sys.version_info < (3, 0):
    zip = itertools.izip

operations_dict = {
    'id':tuple,
    'sum':lambda xx: (sum(xx),),
    'min':lambda xx: (min(xx),),
    'max':lambda xx: (max(xx),),
    'set':lambda xx: tuple(sorted(xx)),
    'prod':lambda xx: functools.reduce(operator.mul, xx, 1),
    'bit-or':lambda xx: functools.reduce(operator.or_, xx, 0),
    'bit-xor':lambda xx: functools.reduce(operator.xor, xx),
    'bit-and':lambda xx: functools.reduce(operator.and_, xx),
    'shift': None, # This will get defined later if used
    'scale': None, # This will get defined later if used
    'bound': None, # This will get defined later if used
    'select': None, # This will get defined later if used
    'reroll': None, # This will get defined later if used,
    'slice-apply': None, # This will get defined later if used,
}

basic_operations = set(
    key for key,value in operations_dict.items() if value is not None
)

# set of operations that support an if-block
ifable = set([
    'shift',
    'scale',
    'bound',
    'select',
    'reroll',
])

basic_compare_dict = {
    'eq':lambda aa,bb,cc=None: aa == bb,
    'neq': lambda aa,bb,cc=None: aa != bb,
    'gt':lambda aa,bb,cc=None: aa > bb,
    'ge':lambda aa,bb,cc=None: aa >= bb,
    'lt':lambda aa,bb,cc=None: aa < bb,
    'le':lambda aa,bb,cc=None: aa <= bb,
}

compare_modifiers = set([
    'mod',
])

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description="\n".join([
        "This program is used to calculate the distributions of",
        "dice rolling (using brute force enumeration) with operations",
        "applied to results of the roll (via brute force calculations).",
    ]),
)

parser.add_argument(
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
    type=int,
    default=1,
    help="Number of dice simulated",
)

single_type_group_side_option = single_type_group.add_mutually_exclusive_group()

single_type_group_side_option.add_argument(
    "--die-sides","-d",
    type=int,
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
    type=int,
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
    help=" ".join([
        ""
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
    type=int,
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
Value Die Options
========================================================================================
"""
value_group = parser.add_argument_group(
    'Value Options',
    'Options related to displaying calculated information',
)

value_group.add_argument(
    "--percent-decimal-place","-pdp",
    type=int,
    default = 2,
    help="The number of digits that will be displayed after the decimal place.",
)

value_group.add_argument(
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
    type=int,
    default = None,
    help=" ".join([
        "The number of simulated dice rols that will occur.",
        "If this option is not provided, then enumerating all outcomes will take place.",
    ]),
)


args = parser.parse_args()

formatter_percent = "{{value:{percent_formatter}}} %".format(
    percent_formatter = "{}.{}f".format(
        len("100.") + args.percent_decimal_place,
        args.percent_decimal_place,
    ),
)

def always_true(*args, **kwargs):
    return True

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

def get_dice():
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
    return zip(*tuple(itertools.starmap(
            random.choice, itertools.repeat((die,), num_iterations)
        )
        for die in dice
    ))

def get_outcome_generator():
    dice = get_dice()

    if not isinstance(args.simulate_num_iterations, int):
        return itertools.product(*dice)

    elif args.simulate_num_iterations > 0:
        return get_outcome_simulator(dice,args.simulate_num_iterations)
    else:
        raise Exception('The number of simulation iterations must be a positive integer')


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

        if comparison_str in basic_compare_dict:
            return basic_compare_dict[comparison_str]
        elif comparison_str == 'mod':
            try:
                mod_values = tuple(int(item) for item in itertools.takewhile(
                    lambda xx: xx not in basic_compare_dict and xx not in compare_modifiers,
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
        _operator = operations_dict[operation_str]

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

def get_reroll_if_operation(param_list, comparison_func):
    if len(param_list) > 0:
        raise Exception("Reroll doesn't take any parameters")

    @docstring_format(
        param_list=str(param_list),
        conditional_info=comparison_func.__doc__,
    )
    def reroll_if_func(xx):
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

    return reroll_if_func

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
    second_operator_params = list(itertools.takewhile(lambda xx: xx not in operations_dict, other_param_list[1:]))
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
        if operation_str in ifable:
            conditional_params = list(itertools.takewhile(lambda xx: xx != 'then', param_list[1:]))
            param_list = param_list[1+len(conditional_params):]

            if len(param_list) > 0 and param_list[0] == 'then':
                param_list = param_list[1:]
        else:
            raise Exception('This operation is not if-able.')

    conditoinal_func = determine_compare_func(conditional_params)

    cur_params = list(itertools.takewhile(lambda xx: xx not in operations_dict, param_list))
    apply_nested_operation = True

    param_list = param_list[len(cur_params):]

    if operation_str in basic_operations:
        _operator = get_basic_operation(operation_str, cur_params)

    elif operation_str == 'shift':
        _operator = get_shift_operation(cur_params, conditoinal_func)

    elif operation_str == 'scale':
        _operator = get_scale_operation(cur_params, conditoinal_func)

    elif operation_str == 'bound':
        _operator = get_bound_operation(cur_params, conditoinal_func)

    elif operation_str == 'select':
        _operator = get_select_operation(cur_params)

    elif operation_str == 'reroll':
        _operator = get_reroll_if_operation(cur_params, conditoinal_func)

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

def main():
    count = Counter()

    if args.show_args:
        print(args)

    _operator = get_operator(args.apply[0], args.apply[1:], args.memorize)

    # the next two lines is the majority of the program run time for larger values
    for item in get_outcome_generator():
        count[_operator(item)] += 1

    total = sum(count.values())

    _temp_key = list(count.keys())[0]
    is_key_array_like = isinstance(_temp_key, (tuple,list))
    num_items_in_key = 1*(not is_key_array_like) or len(_temp_key)

    if is_key_array_like:
        all_keys = []
        for key_set in count:
            all_keys.extend(key_set)
        num_key_digits = find_max_digits(all_keys)

    else:
        num_key_digits = find_max_digits(count.keys())

    key_formater = "{{key:{num_key_digits}d}}".format(
        num_key_digits=num_key_digits
    )

    if is_key_array_like:
        sub_key_formater = key_formater
        key_formater = "{{key:>{num_char}s}}".format(
            num_char=sum([
                num_items_in_key*num_key_digits, # room for all the digits
                (num_items_in_key - 1)*len(","), # room for all the seperators
            ]),
        )

    num_count_digits = find_max_digits(count.values())

    formatter_count = "{{value:{num_count_digits}d}}".format(
        num_count_digits=num_count_digits,
    )

    full_formater = "{key}: {value} {bar}"

    if args.sort == "key":
        iterater = sorted(list(count.items()))
    elif args.sort == "value":
        iterater = sorted(list(count.items()), key=lambda xx:xx[-1::-1])
    else:
        raise Exception("Unexpected sort value")

    for key,count_value in iterater:

        percent = 100 * float(count_value) / total

        key_string = ""
        value_string = ""
        bar_string = ""

        if is_key_array_like:
            key_string = key_formater.format(
                key=",".join(sub_key_formater.format(key=_key) for _key in key)
            )
        else:
            key_string = key_formater.format(key=key)

        if args.show_counts:
            value_string = formatter_count.format(value=count_value)
        else:
            value_string = formatter_percent.format(value=percent)

        if args.bar_size > 0:
            bar = int(percent * args.bar_size) * args.bar_char
            bar_string = args.bar_prefix + bar

        print(full_formater.format(
            key=key_string,
            value=value_string,
            bar=bar_string,
        ))

    return count

if __name__ == '__main__':
    main()
