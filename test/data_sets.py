import itertools

index_independent_test_value_set = [
    range(10),
    range(-10,1),
    range(-10000,10000),
]

# Every combination of six values from -10 to 9 (inclusive)
# this adds about [20 choose 6] = 38760 entries
index_dependent_test_06 = list(itertools.combinations(range(-10,10), 6))

index_dependent_test_06.extend([
    range(-12,0,2),
    range(-6,12,3),
    range(-5,13,3),
    range(-7,11,3),
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
])

# make all sets contain tuples
for key, value in list(globals().items()):
	if (
		isinstance(value, (list, tuple)) and
		all(isinstance(item, (list, tuple, range)) for item in value)
	):
		globals()[key] = tuple(tuple(item) for item in value)
