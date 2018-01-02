# General Info

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

# Examples

## Aesthetic Examples

### Rolling Two D6 (and Changing the Output)
We apply the sum operation on the dice.
```
➔ python dice_distro.py -d 6 -n 2 --op-func sum
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
➔ # python dice_distro.py -d 6 -n 2 --percent-decimal-place 4 --op-func sum
➔ python dice_distro.py -d 6 -n 2 -pdp 4 --op-func sum
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
➔ python dice_distro.py -d 6 -n 2 --show-counts --op-func sum
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
➔ python dice_distro.py -d 6 -n 2 --sort value --op-func sum
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
➔ python dice_distro.py -d 6 -n 2 --bar-size 0 --op-func sum
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
➔ python dice_distro.py -d 6 -n 2 --bar-size 2 --bar-char '@#' --bar-prefix '<|' --op-func sum
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

## Functional Examples

### Distinguishable Dice
The default operation is to show the results of the dice as if the results are distinguishable.
```
➔ python dice_distro.py -d 4 -n 2
1,1:   6.25 % |============
1,2:   6.25 % |============
1,3:   6.25 % |============
1,4:   6.25 % |============
2,1:   6.25 % |============
2,2:   6.25 % |============
2,3:   6.25 % |============
2,4:   6.25 % |============
3,1:   6.25 % |============
3,2:   6.25 % |============
3,3:   6.25 % |============
3,4:   6.25 % |============
4,1:   6.25 % |============
4,2:   6.25 % |============
4,3:   6.25 % |============
4,4:   6.25 % |============
```

### Four D2 Sum in Pairs (Distinguishable Results)
```
➔ python ./dice_distro.py -d 2 -n 4 --op-func sum --op-params 2
2,2:   6.25 % |============
2,3:  12.50 % |=========================
2,4:   6.25 % |============
3,2:  12.50 % |=========================
3,3:  25.00 % |==================================================
3,4:  12.50 % |=========================
4,2:   6.25 % |============
4,3:  12.50 % |=========================
4,4:   6.25 % |============
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

### Selecting the Second Lowest Value from Four D6
Note that the select index parameter is zero-indexed,
and refers to the index of the value in the list of sorted dice roll results.
The selection index of `1` refers to the second lowest value.
```
➔ python dice_distro.py -d 6 -n 4 --op-func select --op-param 1
1:  13.19 % |==========================
2:  27.55 % |=======================================================
3:  28.01 % |========================================================
4:  20.14 % |========================================
5:   9.49 % |==================
6:   1.62 % |===
```

### Selecting the Second Highest Value from Four D6
Using the selection function uses parameters that are interpreted as python indices.
The negative selection index takes from the end of the list of sorted dice roll results.
Thus selection index `-2` is the second last element
(or second largest value) in the list of sorted dice roll results,
```
➔ python dice_distro.py -d 6 -n 4 --op-func select --op-param -2
1:   1.62 % |===
2:   9.49 % |==================
3:  20.14 % |========================================
4:  28.01 % |========================================================
5:  27.55 % |=======================================================
6:  13.19 % |==========================
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
You can give the `select` function more than one select index
but the result is a list in the order of the select indices that you gave.
In this example this is the same as excluding the lowest.
The key sorting is lexicographic.
```
➔ python dice_distro.py -d 4 -n 4 --op-func select --op-params -1 -2 -3
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
The indices have the same meaning as with `--op-func multi-select`
(and thus the same meaning as `--op-func select`),
but with an additional parameter referring to the operation
that will be applied to the selected values.
```
➔ python dice_distro.py -d 6 -n 4 --op-func select --op-params -1 -2 -3 sum
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

### Conditional Rerolling
Roll a D6, if the value is greater than 4 (the `--op-params` value), keep the value.
Otherwise reroll, repeat to a max of three rolls.
Keep the final roll, regardless of outcome.
To change the max reroll count, change the number of dice that are rolled (the `-n` parameter).
```
➔ python dice_distro.py -d 6 -n 3 --op-func conditional-reroll --op-params 4
1:   4.17 % |========
2:   4.17 % |========
3:   4.17 % |========
4:  29.17 % |==========================================================
5:  29.17 % |==========================================================
6:  29.17 % |==========================================================
```

### Conditional Rerolling with Multiple Dice
Roll two D6 and sum their values. If the value is equal to or greater than 7, keep the value.
Otherwise, reroll.
The rolls are parsed two at a time, so if you have `-n 8` will have a max of four rolls.
**Note** that its up to the user to make sure that there is enough dice.
```
➔ python dice_distro.py -d 6 -n 4  --op-func sum --op-params 2 conditional-reroll 7
 2:   1.16 % |==
 3:   2.31 % |====
 4:   3.47 % |======
 5:   4.63 % |=========
 6:   5.79 % |===========
 7:  23.61 % |===============================================
 8:  19.68 % |=======================================
 9:  15.74 % |===============================
10:  11.81 % |=======================
11:   7.87 % |===============
12:   3.94 % |=======
```

### Conditional Rerolling with Different Dice
Instructions:
- Roll D8
- If 5 or greater, keep the value and terminate execution, otherwise disregard the value and roll a D6.
- If 4 or greater, keep the value and terminate execution, otherwise disregard the value and roll a D4.
- Keep the final value (if you got this far)
```
➔ python dice_distro.py --multi-die-sides 8 6 4 --op-func conditional-reroll --op-params 5 4
1:   6.25 % |============
2:   6.25 % |============
3:   6.25 % |============
4:  14.58 % |=============================
5:  20.83 % |=========================================
6:  20.83 % |=========================================
7:  12.50 % |=========================
8:  12.50 % |=========================
```

### Rolling a True D10
This program by default will treat a D10 to begin at `1` and have values all the way up to `10`.
If we want the lowest value to start at `0` we can do the following.
```
➔ python dice_distro.py -d 10 -n 2 --die-start 0 --op-func sum
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
➔ python dice_distro.py -d 10 -n 2 --die-start 0 --die-step 10 --op-func sum
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
➔ python dice_distro.py -n 2 --die-values 0 10 100 -1000 --op-func sum
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
➔ python dice_distro.py --multi-die-sides 12 8 6 --op-func sum
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
➔ python dice_distro.py --multi-die-sides 4 3 2 --multi-die-start -2 0 1 --multi-die-step 3 2 1
-2, 0, 1:   4.17 % |========
-2, 0, 2:   4.17 % |========
-2, 2, 1:   4.17 % |========
-2, 2, 2:   4.17 % |========
-2, 4, 1:   4.17 % |========
-2, 4, 2:   4.17 % |========
 1, 0, 1:   4.17 % |========
 1, 0, 2:   4.17 % |========
 1, 2, 1:   4.17 % |========
 1, 2, 2:   4.17 % |========
 1, 4, 1:   4.17 % |========
 1, 4, 2:   4.17 % |========
 4, 0, 1:   4.17 % |========
 4, 0, 2:   4.17 % |========
 4, 2, 1:   4.17 % |========
 4, 2, 2:   4.17 % |========
 4, 4, 1:   4.17 % |========
 4, 4, 2:   4.17 % |========
 7, 0, 1:   4.17 % |========
 7, 0, 2:   4.17 % |========
 7, 2, 1:   4.17 % |========
 7, 2, 2:   4.17 % |========
 7, 4, 1:   4.17 % |========
 7, 4, 2:   4.17 % |========
```

### Roll Multiple Types of Dice with Specific Values

- One D4 with values from 0 to 3.
- One D3 with values of 10, 20, and 30.
- One D2 with values of 100 and 200.
```
➔ python dice_distro.py --multi-die-sides 4 3 2 --multi-die-values 0 1 2 3 10 20 30 100 200
  0, 10,100:   4.17 % |========
  0, 10,200:   4.17 % |========
  0, 20,100:   4.17 % |========
  0, 20,200:   4.17 % |========
  0, 30,100:   4.17 % |========
  0, 30,200:   4.17 % |========
  1, 10,100:   4.17 % |========
  1, 10,200:   4.17 % |========
  1, 20,100:   4.17 % |========
  1, 20,200:   4.17 % |========
  1, 30,100:   4.17 % |========
  1, 30,200:   4.17 % |========
  2, 10,100:   4.17 % |========
  2, 10,200:   4.17 % |========
  2, 20,100:   4.17 % |========
  2, 20,200:   4.17 % |========
  2, 30,100:   4.17 % |========
  2, 30,200:   4.17 % |========
  3, 10,100:   4.17 % |========
  3, 10,200:   4.17 % |========
  3, 20,100:   4.17 % |========
  3, 20,200:   4.17 % |========
  3, 30,100:   4.17 % |========
  3, 30,200:   4.17 % |========
```

### Nested Selecting

This example rolls five D8 and applies the following instructions:
- select the four highest values (in the order highest, fourth, second, third)
- sum the values in pairs (highest and fourth is summed to one value, the second and third highest are summed)
- of the two values select the lowest
```
➔ python dice_distro.py -d 8 -n 5 --op-func select --op-params -1 -4 -2 -3 sum 2 select 0
 2:   0.11 % |
 3:   0.43 % |
 4:   1.48 % |==
 5:   2.93 % |=====
 6:   5.45 % |==========
 7:   8.24 % |================
 8:  12.01 % |========================
 9:  15.62 % |===============================
10:  17.14 % |==================================
11:  14.65 % |=============================
12:  10.94 % |=====================
13:   6.59 % |=============
14:   3.31 % |======
15:   0.98 % |=
16:   0.11 % |
```

### The Sum of Two Independent Sets of Two D4
We roll four D4 group them into 2 pairs.
Then sum their values, and treat the results as indistinguishable.
```
➔ python dice_distro.py -d 4 -n 4 --op-func sum --op-params 2 set
2,2:   0.39 % |
2,3:   1.56 % |===
2,4:   2.34 % |====
2,5:   3.12 % |======
2,6:   2.34 % |====
2,7:   1.56 % |===
2,8:   0.78 % |=
3,3:   1.56 % |===
3,4:   4.69 % |=========
3,5:   6.25 % |============
3,6:   4.69 % |=========
3,7:   3.12 % |======
3,8:   1.56 % |===
4,4:   3.52 % |=======
4,5:   9.38 % |==================
4,6:   7.03 % |==============
4,7:   4.69 % |=========
4,8:   2.34 % |====
5,5:   6.25 % |============
5,6:   9.38 % |==================
5,7:   6.25 % |============
5,8:   3.12 % |======
6,6:   3.52 % |=======
6,7:   4.69 % |=========
6,8:   2.34 % |====
7,7:   1.56 % |===
7,8:   1.56 % |===
8,8:   0.39 % |
```

### Weighted Dice
Since this program uses enumeration to calculate the distribution,
weighted dice can't simply be added with a parameter with weights.
To work around that, you must make a custom die with repeated values on the faces.

The following example shows a weighted D6.
```
➔ python dice_distro.py --die-values \
    1 1 1 1 1 1 \
    2 2 2 2 2 \
    3 3 3 3 \
    4 4 4 \
    5 5 \
    6
1:  28.57 % |=========================================================
2:  23.81 % |===============================================
3:  19.05 % |======================================
4:  14.29 % |============================
5:   9.52 % |===================
6:   4.76 % |=========
```

The following example shows two the above weighted D6 then summing the values.
```
➔ python dice_distro.py --die-values \
    1 1 1 1 1 1 \
    2 2 2 2 2 \
    3 3 3 3 \
    4 4 4 \
    5 5 \
    6 \
    -n 2 --op-func sum
 2:   8.16 % |================
 3:  13.61 % |===========================
 4:  16.55 % |=================================
 5:  17.23 % |==================================
 6:  15.87 % |===============================
 7:  12.70 % |=========================
 8:   7.94 % |===============
 9:   4.54 % |=========
10:   2.27 % |====
11:   0.91 % |=
12:   0.23 % |
```

# Simulating Dice Rolls

If the enumeration of all outcomes takes too long, you can choose to simulate the dice rolls.
This allows you get an idea for what the distribution looks like without have to wait for computation time
of full enumeration.

**NOTE:** This will only provide an approximation of the results,
and the numbers can be slightly different each time (can be reduced with a large iteration count).
To get exact values, do not use simulated dice rolls.

An example of simulating 100000 rolls of ten D30, taking the two largest values and summing them.
Ten D30's has `30^10` or `5.904900e+14` distinct outcomes if you treat each die as distinguishable.
Enumerating all the outcomes would take quite a while.
```
➔ python dice_distro.py -d 30 -n 10 -pdp 3 --op-func select --op-params -1 -2 sum --simulate 100000
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

# Future Plans

If I find time in the future, I plan to parallelize the work so that options with a large enumeration set can be computed faster,
as well as allowing larger numbers of simulated dice throws.
