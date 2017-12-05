## General Info

This program was meant to be used as a command line tool.
It only uses built-in modules to calculate everything, but uses brute force calculations.
This has been tested with `Python 2.7.x` and `Python 3.5.x`,
though it should work for all versions that are `Python 3.x`.

**Note**: This tool enumerates all possible outcomes (treating the dice as distinguishable).
This gives it the flexibility to calculated different kinds of distributions with many restrictions,
but may take a while to compute when lots of dice are being rolled.
For example six D20 calculations may take quite a while to compute depending on your machine.
There is a `--simulate` flag if you don't need exact probabilistic values, but approximations are good enough for you use case.

There is a lot of explanation in the `--help` output. Which you can see using:
```
➔ python dice_distro.py --help
```

## Examples

### Rolling Two D6 (and Changing the Output)
The default operation applied is to sum all the values of what is rolled.
```
➔ python dice_distro.py -d 6 -n 2
 2:   2.78 % |=====
 3:   5.56 % |===========
 4:   8.33 % |================
 5:  11.11 % |======================
 6:  13.89 % |===========================
 7:  16.67 % |=================================
 8:  13.89 % |===========================
 9:  11.11 % |======================
10:   8.33 % |================
11:   5.56 % |===========
12:   2.78 % |=====
```

You can change the output to show a different number of decimal places (default is 2).
```
➔ # python dice_distro.py -d 6 -n 2 --percent-decimal-place 4
➔ python dice_distro.py -d 6 -n 2 -pdp 4
 2:   2.7778 % |=====
 3:   5.5556 % |===========
 4:   8.3333 % |================
 5:  11.1111 % |======================
 6:  13.8889 % |===========================
 7:  16.6667 % |=================================
 8:  13.8889 % |===========================
 9:  11.1111 % |======================
10:   8.3333 % |================
11:   5.5556 % |===========
12:   2.7778 % |=====
```

You can also change the output to show the counts.
The modules trying every combination of output, treating each die as distinguishable.
```
➔ python dice_distro.py -d 6 -n 2 --show-counts
 2: 1 |=====
 3: 2 |===========
 4: 3 |================
 5: 4 |======================
 6: 5 |===========================
 7: 6 |=================================
 8: 5 |===========================
 9: 4 |======================
10: 3 |================
11: 2 |===========
12: 1 |=====
```

You can also change the sort order.
```
➔ python dice_distro.py -d 6 -n 2 --sort value
 2:   2.78 % |=====
12:   2.78 % |=====
 3:   5.56 % |===========
11:   5.56 % |===========
 4:   8.33 % |================
10:   8.33 % |================
 5:  11.11 % |======================
 9:  11.11 % |======================
 6:  13.89 % |===========================
 8:  13.89 % |===========================
 7:  16.67 % |=================================
```

If you don't want to see the bars, you can turn them off.
```
➔ python dice_distro.py -d 6 -n 2 --bar-size 0
 2:   2.78 % 
 3:   5.56 % 
 4:   8.33 % 
 5:  11.11 % 
 6:  13.89 % 
 7:  16.67 % 
 8:  13.89 % 
 9:  11.11 % 
10:   8.33 % 
11:   5.56 % 
12:   2.78 % 
```

Or you can drastically change how the bars get rendered.
```
➔ python dice_distro.py -d 6 -n 2 --bar-size 2 --bar-char '@#' --bar-prefix '<|'
 2:   2.78 % <|@#@#@#@#@#
 3:   5.56 % <|@#@#@#@#@#@#@#@#@#@#@#
 4:   8.33 % <|@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
 5:  11.11 % <|@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
 6:  13.89 % <|@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
 7:  16.67 % <|@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
 8:  13.89 % <|@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
 9:  11.11 % <|@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
10:   8.33 % <|@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#
11:   5.56 % <|@#@#@#@#@#@#@#@#@#@#@#
12:   2.78 % <|@#@#@#@#@#
```

### Advantage (Rolling Two D20 Taking Max)
```
➔ python dice_distro.py -d 20 -n 2 --op-func max
 1:   0.25 % |
 2:   0.75 % |=
 3:   1.25 % |==
 4:   1.75 % |===
 5:   2.25 % |====
 6:   2.75 % |=====
 7:   3.25 % |======
 8:   3.75 % |=======
 9:   4.25 % |========
10:   4.75 % |=========
11:   5.25 % |==========
12:   5.75 % |===========
13:   6.25 % |============
14:   6.75 % |=============
15:   7.25 % |==============
16:   7.75 % |===============
17:   8.25 % |================
18:   8.75 % |=================
19:   9.25 % |==================
20:   9.75 % |===================
```

### Disadvantage (Rolling Two D20 Taking Min)
```
➔ python dice_distro.py -d 20 -n 2 --op-func min
 1:   9.75 % |===================
 2:   9.25 % |==================
 3:   8.75 % |=================
 4:   8.25 % |================
 5:   7.75 % |===============
 6:   7.25 % |==============
 7:   6.75 % |=============
 8:   6.25 % |============
 9:   5.75 % |===========
10:   5.25 % |==========
11:   4.75 % |=========
12:   4.25 % |========
13:   3.75 % |=======
14:   3.25 % |======
15:   2.75 % |=====
16:   2.25 % |====
17:   1.75 % |===
18:   1.25 % |==
19:   0.75 % |=
20:   0.25 % |
```

### Selecting the Second Highest Value from Four D6
```
➔ python dice_distro.py -d 6 -n 4 --op-func select --op-param -2
1:   1.62 % |===
2:   9.49 % |==================
3:  20.14 % |========================================
4:  28.01 % |========================================================
5:  27.55 % |=======================================================
6:  13.19 % |==========================
```

### Selecting the Second Lowest Value from Four D6
Note that the select index parameter is zero-indexed.
```
➔ python dice_distro.py -d 6 -n 4 --op-func select --op-param 1
1:  13.19 % |==========================
2:  27.55 % |=======================================================
3:  28.01 % |========================================================
4:  20.14 % |========================================
5:   9.49 % |==================
6:   1.62 % |===
```

### Rolling Four D4 (Indistinguishable)
The possible outcomes treating the dice as indistinguishable.
```
➔ python dice_distro.py -d 4 -n 4 --op-func set
1,1,1,1:   0.39 % |
1,1,1,2:   1.56 % |===
1,1,1,3:   1.56 % |===
1,1,1,4:   1.56 % |===
1,1,2,2:   2.34 % |====
1,1,2,3:   4.69 % |=========
1,1,2,4:   4.69 % |=========
1,1,3,3:   2.34 % |====
1,1,3,4:   4.69 % |=========
1,1,4,4:   2.34 % |====
1,2,2,2:   1.56 % |===
1,2,2,3:   4.69 % |=========
1,2,2,4:   4.69 % |=========
1,2,3,3:   4.69 % |=========
1,2,3,4:   9.38 % |==================
1,2,4,4:   4.69 % |=========
1,3,3,3:   1.56 % |===
1,3,3,4:   4.69 % |=========
1,3,4,4:   4.69 % |=========
1,4,4,4:   1.56 % |===
2,2,2,2:   0.39 % |
2,2,2,3:   1.56 % |===
2,2,2,4:   1.56 % |===
2,2,3,3:   2.34 % |====
2,2,3,4:   4.69 % |=========
2,2,4,4:   2.34 % |====
2,3,3,3:   1.56 % |===
2,3,3,4:   4.69 % |=========
2,3,4,4:   4.69 % |=========
2,4,4,4:   1.56 % |===
3,3,3,3:   0.39 % |
3,3,3,4:   1.56 % |===
3,3,4,4:   2.34 % |====
3,4,4,4:   1.56 % |===
4,4,4,4:   0.39 % |
```

### Selecting the Three Highest Values from Four D4
The same as excluding the lowest.
The key sorting is lexicographic.
```
➔ python dice_distro.py -d 4 -n 4 --op-func multi-select --op-params -1 -2 -3
1,1,1:   0.39 % |
2,1,1:   1.56 % |===
2,2,1:   2.34 % |====
2,2,2:   1.95 % |===
3,1,1:   1.56 % |===
3,2,1:   4.69 % |=========
3,2,2:   6.25 % |============
3,3,1:   2.34 % |====
3,3,2:   7.03 % |==============
3,3,3:   3.52 % |=======
4,1,1:   1.56 % |===
4,2,1:   4.69 % |=========
4,2,2:   6.25 % |============
4,3,1:   4.69 % |=========
4,3,2:  14.06 % |============================
4,3,3:  10.94 % |=====================
4,4,1:   2.34 % |====
4,4,2:   7.03 % |==============
4,4,3:  11.72 % |=======================
4,4,4:   5.08 % |==========
```

### Selecting the Three Highest Values from Four D6 and Summing
```
➔ python dice_distro.py -d 6 -n 4 --op-func multi-select-apply --op-params -1 -2 -3 sum
 3:   0.08 % |
 4:   0.31 % |
 5:   0.77 % |=
 6:   1.62 % |===
 7:   2.93 % |=====
 8:   4.78 % |=========
 9:   7.02 % |==============
10:   9.41 % |==================
11:  11.42 % |======================
12:  12.89 % |=========================
13:  13.27 % |==========================
14:  12.35 % |========================
15:  10.11 % |====================
16:   7.25 % |==============
17:   4.17 % |========
18:   1.62 % |===
```

### Rolling a True D10
This program by default will treat a D10 to begin at `1` and have values all the way up to `10`.
If we want the lowest value to start at `0` we can do the following.
```
➔ python dice_distro.py -d 10 -n 2 --die-start 0
 0:   1.00 % |==
 1:   2.00 % |====
 2:   3.00 % |======
 3:   4.00 % |========
 4:   5.00 % |==========
 5:   6.00 % |============
 6:   7.00 % |==============
 7:   8.00 % |================
 8:   9.00 % |==================
 9:  10.00 % |====================
10:   9.00 % |==================
11:   8.00 % |================
12:   7.00 % |==============
13:   6.00 % |============
14:   5.00 % |==========
15:   4.00 % |========
16:   3.00 % |======
17:   2.00 % |====
18:   1.00 % |==
```

Or other type of D10 (some refer to as a D100, but does not have 100 sides)
```
➔ python dice_distro.py -d 10 -n 2 --die-start 0 --die-step 10
  0:   1.00 % |==
 10:   2.00 % |====
 20:   3.00 % |======
 30:   4.00 % |========
 40:   5.00 % |==========
 50:   6.00 % |============
 60:   7.00 % |==============
 70:   8.00 % |================
 80:   9.00 % |==================
 90:  10.00 % |====================
100:   9.00 % |==================
110:   8.00 % |================
120:   7.00 % |==============
130:   6.00 % |============
140:   5.00 % |==========
150:   4.00 % |========
160:   3.00 % |======
170:   2.00 % |====
180:   1.00 % |==
```

### Rolling Custom Values
You can manually set the values on the sides of the die.
```
➔ python dice_distro.py -n 2 --die-values 0 10 100 -1000
-2000:   6.25 % |============
-1000:  12.50 % |=========================
 -990:  12.50 % |=========================
 -900:  12.50 % |=========================
    0:   6.25 % |============
   10:  12.50 % |=========================
   20:   6.25 % |============
  100:  12.50 % |=========================
  110:  12.50 % |=========================
  200:   6.25 % |============
```

### Rolling a D12 D8 and D6
```
➔ python dice_distro.py --multi-die-sides 12 8 6
 3:   0.17 % |
 4:   0.52 % |=
 5:   1.04 % |==
 6:   1.74 % |===
 7:   2.60 % |=====
 8:   3.65 % |=======
 9:   4.69 % |=========
10:   5.73 % |===========
11:   6.60 % |=============
12:   7.29 % |==============
13:   7.81 % |===============
14:   8.16 % |================
15:   8.16 % |================
16:   7.81 % |===============
17:   7.29 % |==============
18:   6.60 % |=============
19:   5.73 % |===========
20:   4.69 % |=========
21:   3.65 % |=======
22:   2.60 % |=====
23:   1.74 % |===
24:   1.04 % |==
25:   0.52 % |=
26:   0.17 % |
```

### Roll Multiple Types of Dice with Non-Default Values
When rolling multiple types of die, the default start and step will be `1`.
This can be changed with `--multi-die-start` and `--multi-die-step`.
Both flags are optional, but when using one, the values you pass are in parallel with the values given
in relation to `--multi-die-sides`.
```
➔ python dice_distro.py --multi-die-sides 4 3 2 --multi-die-start -1 0 1 --multi-die-step 3 2 1
 0:   4.17 % |========
 1:   4.17 % |========
 2:   4.17 % |========
 3:   8.33 % |================
 4:   8.33 % |================
 5:   8.33 % |================
 6:   8.33 % |================
 7:   8.33 % |================
 8:   8.33 % |================
 9:   8.33 % |================
10:   8.33 % |================
11:   8.33 % |================
12:   4.17 % |========
13:   4.17 % |========
14:   4.17 % |========
```

### Roll Multiple Types of Dice with Specific Values

- One D4 with values from 0 to 3.
- One D3 with values of 10, 20, and 30.
- One D2 with values of 100 and 200.
```
➔ python dice_distro.py --multi-die-sides 4 3 2 --multi-die-values 0 1 2 3 10 20 30 100 200
110:   4.17 % |========
111:   4.17 % |========
112:   4.17 % |========
113:   4.17 % |========
120:   4.17 % |========
121:   4.17 % |========
122:   4.17 % |========
123:   4.17 % |========
130:   4.17 % |========
131:   4.17 % |========
132:   4.17 % |========
133:   4.17 % |========
210:   4.17 % |========
211:   4.17 % |========
212:   4.17 % |========
213:   4.17 % |========
220:   4.17 % |========
221:   4.17 % |========
222:   4.17 % |========
223:   4.17 % |========
230:   4.17 % |========
231:   4.17 % |========
232:   4.17 % |========
233:   4.17 % |========
```

### Nested Selecting

This example rolls five D8 (with 1 as the lowest value) and applies the following instructions:
- select the three highest values
- of the selected values, select the two lowest values
- sum the remaining values
```
➔ python dice_distro.py -d 8 -n 5 --op-func multi-select-apply --op-params -1 -2 -3 multi-select-apply 0 1 sum
 2:   0.11 % |
 3:   0.40 % |
 4:   1.39 % |==
 5:   2.62 % |=====
 6:   4.81 % |=========
 7:   6.87 % |=============
 8:   9.63 % |===================
 9:  11.47 % |======================
10:  13.32 % |==========================
11:  13.28 % |==========================
12:  12.77 % |=========================
13:  10.19 % |====================
14:   7.65 % |===============
15:   3.88 % |=======
16:   1.61 % |===
```

### Simulating Dice Rolls

If the enumeration of all outcomes takes too long, you can choose to simulate the dice rolls.
This allows you get an idea for what the distribution looks like without have to wait for computation time
of full enumeration.

**NOTE:** This will only provide an approximation of the results,
and the numbers can be slightly different each time (can be reduced with a large iteration count).
To get exact values, do not use simulated dice rolls.

An example of simulating 100000 rolls of ten D30, taking the two largest values and summing them.
Ten D30's has `30^10` or `5.904900e+14` distinct outcomes if you treat each die as distingishable.
Enumerating all the outcomes would take quite a while.
```
➔ python dice_distro.py -d 30 -n 10 -pdp 3 --op-func multi-select-apply --op-params -1 -2 sum --simulate 100000
20:   0.001 % |
21:   0.003 % |
22:   0.007 % |
23:   0.001 % |
24:   0.007 % |
25:   0.004 % |
26:   0.010 % |
27:   0.014 % |
28:   0.029 % |
29:   0.037 % |
30:   0.049 % |
31:   0.060 % |
32:   0.091 % |
33:   0.114 % |
34:   0.138 % |
35:   0.204 % |
36:   0.263 % |
37:   0.345 % |
38:   0.418 % |
39:   0.518 % |=
40:   0.739 % |=
41:   0.932 % |=
42:   1.071 % |==
43:   1.311 % |==
44:   1.593 % |===
45:   1.968 % |===
46:   2.451 % |====
47:   2.928 % |=====
48:   3.533 % |=======
49:   4.100 % |========
50:   5.001 % |==========
51:   5.596 % |===========
52:   6.471 % |============
53:   7.232 % |==============
54:   7.738 % |===============
55:   8.374 % |================
56:   8.803 % |=================
57:   8.860 % |=================
58:   8.228 % |================
59:   6.662 % |=============
60:   4.096 % |========
```

## Future Plans

If I find time in the future, I plan to parallalize the work so that options with a large enumeration set can be computed faster,
as well as allowing larger numbers of simulated dice throws.
