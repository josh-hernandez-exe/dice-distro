from __future__ import print_function

import math
import argparse
import operator
import functools
from itertools import product
from collections import Counter

operations = {
    'sum':sum,
    'min':min,
    'max':max,
    'prod':lambda xx: functools.reduce(operator.mul, xx, 1),
    'or':lambda xx: functools.reduce(operator.or_, xx, 0),
    'xor':lambda xx: functools.reduce(operator.xor, xx),
    'and':lambda xx: functools.reduce(operator.and_, xx),
    'select': None, # This will get defined later if used
    'multi-select': None, # This will get defined later if used
}

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description="\n".join([
        "This program is used to calculate the distributions of dice rolling",
        "with operations applied to results of the roll (via brute force calculations).",
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
        "The value given must be a positive integer."
        "The values on the die will start from '--die-start' and fill up the sides of the die incrementing by '--die-step'.",
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
        "This and '--die-sides' are mutually exclusive options."
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
        "The value given must be a positive integer."
        "The values on the die will start from '--die-start' and fill up the sides of the die incrementing by '--die-step'.",
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
    "--op-func",
    type=str,
    choices=sorted(operations.keys()),
    default = 'sum',
    help=" ".join([
        "The operation that will be applied to the values rolled.",
        "The operations available are both communitive and associative.",
        "The 'select' operation requires an integer parameter (use '--op-params')."
        "The 'multi-select' operation at least one integer parameter,",
        "the meaning behind the parameter is the same as 'select' (use '--op-params')."
        "Note: that bit-wise operations are available, not logical operations.",
    ]),
)

op_group.add_argument(
    "--op-params",
    nargs="*",
    default = [],
    help=" ".join([
        "Optional parameters that may be needed for '--op-func'.",
        "When '--op-func' is 'select' then the parameter is the index of the item in the sorted array."
        "Example-Select-1: '--op-func select --op-params 0' is the same as min.",
        "Example-Select-2: '--op-func select --op-params 1' returns the second lowest value.",
        "Example-Select-3: '--op-func select --op-params -1' is the same as max.",
        "Example-Select-4: '--op-func select --op-params -2' returns the second highest value.",
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
        "One percent is represented as this string repeated '--bar-size' times."
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

args = parser.parse_args()

formatter_percent = "{{value:{percent_formatter}}} %".format(
    percent_formatter = "{}.{}f".format(
        len("100.") + args.percent_decimal_place,
        args.percent_decimal_place,
    ),
)

class Memorize(object):
    def __init__(self, func):
        self.func = func
        self.cashe = dict()

    def __call__(self, iterable):
        key = frozenset(Counter(iterable).items())

        if key in self.cashe: return self.cashe[key]

        result = self.func(iterable)
        self.cashe[key] = result

        return result

def get_outcome_generator():
    if isinstance(args.multi_die_sides, (list,tuple)):
        dice = []

        if isinstance(args.multi_die_values, (list,tuple)) and len(args.multi_die_values) > 0:
            die = []
            for value in args.multi_die_values:
                die.append(value)
                if len(die) == args.multi_die_sides[len(dice)]:
                    dice.append(tuple(die))
                    die = []

            assert len(dice) == len(args.multi_die_sides), "Not enough die values were given"
            assert sum(len(item) for item in dice) == len(args.multi_die_values), "Not all die values were used"
        else:
            if isinstance(args.multi_die_start, (list,tuple)) and len(args.multi_die_start) > 0:
                assert len(args.multi_die_start) == len(args.multi_die_sides), "Multi die starts must have parallel values to multi die sides"
                start_values = args.multi_die_start
            else:
                start_values = tuple(1 for _ in args.multi_die_sides)

            if isinstance(args.multi_die_step, (list,tuple)) and len(args.multi_die_step) > 0:
                assert len(args.multi_die_step) == len(args.multi_die_step), "Multi die steps must have parallel values to multi die sides"
                step_values = args.multi_die_step
            else:
                step_values = tuple(1 for _ in args.multi_die_sides)

            for start,step,size in zip(start_values, step_values, args.multi_die_sides):
                dice.append(range(start,start+step*size, step))

        return product(*tuple(dice))
    else:
        if isinstance(args.die_sides,int) and len(args.die_values) > 0:
            raise Exception("Both die sides are given and die values are given. Only pass one")

        elif isinstance(args.die_sides,int) and args.die_sides > 0:
            values = range(args.die_start,args.die_start + args.die_step*args.die_sides, args.die_step)

        elif len(args.die_values) > 0:
            values = args.die_values

        else:
            raise Exception('Must pass in one of \'--die\' or \'--die-values\'')

        return product(values,repeat=args.num_dice)

def find_max_digits(iterable):
    if not all(isinstance(xx, (int, float)) for xx in iterable):
        raise Exception('All items in the iterable must be ints or floats.')

    max_abs = max(abs(xx) for xx in iterable)
    any_neg = any(xx < 0 for xx in iterable)

    return 1*any_neg + int(
        math.ceil(
            math.log10(max_abs)
    ))

def get_operation(operation_str):
    _operator = operations[args.op_func]

    if args.op_func == 'select':
        if len(args.op_params) != 1:
            raise Exception("The 'select' operation requires a single parameter which is the select index.")

        try:
            select_index = int(args.op_params[0])
        except:
            raise Exception("The parameter passed must be in integer")

        def select_func(xx):
            """
            this could be sped up with the quick select algorithm
            """
            return sorted(list(xx))[select_index]

        _operator = select_func

    if args.op_func == 'multi-select':
        if len(args.op_params) < 1:
            raise Exception("The 'select' operation requires at least one parameter which is the select index.")

        try:
            select_indices = tuple(int(item) for item in args.op_params)
        except:
            raise Exception("The parameters passed must be in integers")

        def select_func(xx):
            """
            this could be sped up with the quick select algorithm
            """
            sorted_list = sorted(list(xx))

            return tuple(sorted_list[ii] for ii in select_indices)

        _operator = select_func

    # return an function that cashes the results to speed up runtime at the cost of memory
    return Memorize(_operator)


def main():
    count = Counter()

    _operator = get_operation(args.op_func)

    # the next two lines is the majority of the program run time for larger values
    for item in get_outcome_generator():
        count[_operator(item)] += 1

    total = sum(count.values())

    if args.op_func == 'multi-select':
        all_keys = []
        for key_set in count:
            all_keys.extend(key_set)
        num_key_digits = find_max_digits(all_keys)

    else:
        num_key_digits = find_max_digits(count.keys())

    key_formater = "{{key:{num_key_digits}d}}".format(
        num_key_digits=num_key_digits
    )

    if args.op_func == 'multi-select':
        sub_key_formater = key_formater
        key_formater = "{{key:>{num_char}s}}".format(
            num_char=sum([
                len(args.op_params)*num_key_digits, # room for all the digits
                (len(args.op_params) - 1)*len(","), # room for all the seperators
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

        if args.op_func == 'multi-select':
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
