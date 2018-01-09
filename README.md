# General Info

This program was meant to be used as a command line tool.
It only uses built-in modules to calculate everything, but uses brute force calculations.
This has been tested with `Python 2.7.x`, `Python 3.5.x`, and `Python 3.6.x`.
Though it should work for all versions that are `Python 3.x`.

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
➔ python dice_distro.py -d 6 -n 2 --apply sum
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
➔ # python dice_distro.py -d 6 -n 2 --percent-decimal-place 4 --apply sum
➔ python dice_distro.py -d 6 -n 2 -pdp 4 --apply sum
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
The module is trying every combination of output, treating each die as distinguishable.
```
➔ python dice_distro.py -d 6 -n 2 --show-counts --apply sum
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
➔ python dice_distro.py -d 6 -n 2 --sort value --apply sum
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
➔ python dice_distro.py -d 6 -n 2 --bar-size 0 --apply sum
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
➔ python dice_distro.py -d 6 -n 2 --bar-size 2 --bar-char '@#' --bar-prefix '<|' --apply sum
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

## Editing Die Values

### Rolling a True D10
This program by default will treat a D10 to begin at `1` and have values all the way up to `10`.
If we want the lowest value to start at `0` we can do the following.
```
➔ python dice_distro.py -d 10 -n 2 --die-start 0 --apply sum
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
➔ python dice_distro.py -d 10 -n 2 --die-start 0 --die-step 10 --apply sum
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
➔ python dice_distro.py -n 2 --die-values 0 10 100 -1000 --apply sum
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
➔ python dice_distro.py --multi-die-sides 12 8 6 --apply sum
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
➔ python dice_distro.py -d 2 -n 4 --apply sum  2
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
➔ python dice_distro.py -d 20 -n 2 --apply max
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
➔ python dice_distro.py -d 20 -n 2 --apply min
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

### Rolling D6 Shifting the Value but Bounding the Results
We roll a D6, add 2, but don't let the value exceed the values that can be possibly rolled.
```
➔ python dice_distro.py --bar-size 1 -d 6 --apply add 2 bound 1 6
3:  16.67 % |================
4:  16.67 % |================
5:  16.67 % |================
6:  50.00 % |==================================================
```

### Selecting the Second Lowest Value from Four D6
Note that the select index parameter is zero-indexed,
and refers to the index of the value in the list of sorted dice roll results.
The selection index of `1` refers to the second lowest value.
```
➔ python dice_distro.py -d 6 -n 4 --apply select 1
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
➔ python dice_distro.py -d 6 -n 4 --apply select -2
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
➔ python dice_distro.py -d 4 -n 4 --apply sort
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
➔ python dice_distro.py -d 4 -n 4 --apply select -1 -2 -3
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
The indices have the same meaning as with `--apply select`,
but with an additional parameter referring to the operation
that will be applied to the selected values.
```
➔ python dice_distro.py -d 6 -n 4 --apply select -1 -2 -3 sum
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
Roll a D6, if the value is greater than 4, keep the value.
Otherwise reroll, repeat to a max of three rolls.
Keep the final roll, regardless of outcome.
To change the max reroll count, change the number of dice that are rolled (the `-n` parameter).
```
➔ python dice_distro.py -d 6 -n 3 --apply reroll if lt 4
1:   4.17 % |========
2:   4.17 % |========
3:   4.17 % |========
4:  29.17 % |==========================================================
5:  29.17 % |==========================================================
6:  29.17 % |==========================================================
```
**Note**: Since this program enumerates the dice outcome, you need "another" die to reroll.
Since each reroll can be thought of as a new independent die roll.
The real calculation just rolls all the indpendent dice needed,
looks at the first one, if the condition is met, then keep that (regarless of the other die results).
If it didn't keep the value, it looks at the next die and apply the condition,
and repeats until there are no more dice in the pool.
A limitation to the design is that you have to predetermine the max amount of rerolls.
This program cannot indefinitely reroll conditionally.
An example condition that is *not* possible is, "Roll a D6, reroll so long as the result is 3."

### Conditional Rerolling with Multiple Dice
Roll two D6 and sum their values. If the value is equal to or greater than 7, keep the value.
Otherwise, reroll.
The rolls are parsed two at a time, so if you have `-n 8` will have a max of four rolls.
**Note** that its up to the user to make sure that there is enough dice.
```
➔ python dice_distro.py -d 6 -n 4 --apply sum 2 reroll if lt 7
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
➔ python dice_distro.py --multi-die-sides 8 6 4 --apply reroll if lt 5 4
1:   6.25 % |============
2:   6.25 % |============
3:   6.25 % |============
4:  14.58 % |=============================
5:  20.83 % |=========================================
6:  20.83 % |=========================================
7:  12.50 % |=========================
8:  12.50 % |=========================
```

### Nested Selecting

This example rolls five D8 and applies the following instructions:
- select the four highest values (in the order highest, fourth, second, third)
- sum the values in pairs (highest and fourth is summed to one value, the second and third highest are summed)
- of the two values select the lowest
```
➔ python dice_distro.py -d 8 -n 5 --apply select -1 -4 -2 -3 sum 2 select 0
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
➔ python dice_distro.py -d 4 -n 4 --apply sum 2 sort
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

### Using `slice-apply`
The example is encompases the following instructions:
- Roll a D4
- If the value is less than 3 reroll, repeat to a max of three rolls.
- Record the value.
- Repeat the whole process two more times (distinguishable) value.
The above is the equvalent in saying:
- Roll nine independent D4
- Make groups of three:
	- For each group:
		- For each die in the group:
			- Look at the result and check if it is greater or equal to 3
			- Record the die result if it is and move to the next group
			- Otherwise continue to the next die result
- With the recorded results from each group display results
```
➔ python dice_distro.py -d 4 -n 9 --apply slice-apply 3 reroll if lt 3
1,1,1:   0.02 % |
1,1,2:   0.02 % |
1,1,3:   0.17 % |
1,1,4:   0.17 % |
1,2,1:   0.02 % |
1,2,2:   0.02 % |
1,2,3:   0.17 % |
1,2,4:   0.17 % |
1,3,1:   0.17 % |
1,3,2:   0.17 % |
1,3,3:   1.20 % |==
1,3,4:   1.20 % |==
1,4,1:   0.17 % |
1,4,2:   0.17 % |
1,4,3:   1.20 % |==
1,4,4:   1.20 % |==
2,1,1:   0.02 % |
2,1,2:   0.02 % |
2,1,3:   0.17 % |
2,1,4:   0.17 % |
2,2,1:   0.02 % |
2,2,2:   0.02 % |
2,2,3:   0.17 % |
2,2,4:   0.17 % |
2,3,1:   0.17 % |
2,3,2:   0.17 % |
2,3,3:   1.20 % |==
2,3,4:   1.20 % |==
2,4,1:   0.17 % |
2,4,2:   0.17 % |
2,4,3:   1.20 % |==
2,4,4:   1.20 % |==
3,1,1:   0.17 % |
3,1,2:   0.17 % |
3,1,3:   1.20 % |==
3,1,4:   1.20 % |==
3,2,1:   0.17 % |
3,2,2:   0.17 % |
3,2,3:   1.20 % |==
3,2,4:   1.20 % |==
3,3,1:   1.20 % |==
3,3,2:   1.20 % |==
3,3,3:   8.37 % |================
3,3,4:   8.37 % |================
3,4,1:   1.20 % |==
3,4,2:   1.20 % |==
3,4,3:   8.37 % |================
3,4,4:   8.37 % |================
4,1,1:   0.17 % |
4,1,2:   0.17 % |
4,1,3:   1.20 % |==
4,1,4:   1.20 % |==
4,2,1:   0.17 % |
4,2,2:   0.17 % |
4,2,3:   1.20 % |==
4,2,4:   1.20 % |==
4,3,1:   1.20 % |==
4,3,2:   1.20 % |==
4,3,3:   8.37 % |================
4,3,4:   8.37 % |================
4,4,1:   1.20 % |==
4,4,2:   1.20 % |==
4,4,3:   8.37 % |================
4,4,4:   8.37 % |================
```

### Two Ways to Roll Two Sets of D6, Summing Then Taking Max
```
➔ python dice_distro.py -d 6 -n 4 -pdp 4 --apply sum 2 max
 2:   0.0772 % |
 3:   0.6173 % |=
 4:   2.0833 % |====
 5:   4.9383 % |=========
 6:   9.6451 % |===================
 7:  16.6667 % |=================================
 8:  18.1327 % |====================================
 9:  17.2840 % |==================================
10:  14.5833 % |=============================
11:  10.4938 % |====================
12:   5.4784 % |==========
```
```
➔ python dice_distro.py -d 6 -n 4 -pdp 4 --apply slice-apply 2 sum max
 2:   0.0772 % |
 3:   0.6173 % |=
 4:   2.0833 % |====
 5:   4.9383 % |=========
 6:   9.6451 % |===================
 7:  16.6667 % |=================================
 8:  18.1327 % |====================================
 9:  17.2840 % |==================================
10:  14.5833 % |=============================
11:  10.4938 % |====================
12:   5.4784 % |==========
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
    -n 2 --apply sum
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
**Note** that after you create the distribution for the weight die you want, you can save the distribution.
After which you can load up and speed up future calculations using your weighted die.

### Advance Conditionals on Operations that Preserve Result size
Operations that that only change a single die value can be applied conditinoally.
These operations are `add`, `scale`, `bound`, `select`, `reroll`.
In this example we:
- Roll two D6
- For the first die, if it is an even number, subtract 10
- For the second die, if it is equivalent to 1 mod 3, add 100
```
➔ python dice_distro.py -d 4 -n 2 --apply add -10 100 if mod 2 3 eq 0 1
  -8,   2:   6.25 % |============
  -8,   3:   6.25 % |============
  -8, 101:   6.25 % |============
  -8, 104:   6.25 % |============
  -6,   2:   6.25 % |============
  -6,   3:   6.25 % |============
  -6, 101:   6.25 % |============
  -6, 104:   6.25 % |============
   1,   2:   6.25 % |============
   1,   3:   6.25 % |============
   1, 101:   6.25 % |============
   1, 104:   6.25 % |============
   3,   2:   6.25 % |============
   3,   3:   6.25 % |============
   3, 101:   6.25 % |============
   3, 104:   6.25 % |============
```
You can even use boolean logic operations (`not`, `and`, `or`) and even nest them as well.
Due to issues with bash, the bracket char cannot be `(` or `)`,
but instead are `[` and `]`.
```
➔ python dice_distro.py -d 10 --apply add 100 if eq 1 or not [ ge 2 and le 3 ] and [ gt 5 and lt 8  ]
  2:  10.00 % |====================
  3:  10.00 % |====================
  4:  10.00 % |====================
  5:  10.00 % |====================
  8:  10.00 % |====================
  9:  10.00 % |====================
 10:  10.00 % |====================
101:  10.00 % |====================
106:  10.00 % |====================
107:  10.00 % |====================
```
There is an `else` keyword as well. Note that `reroll` cannot be used with `else`.
```
➔ python dice_distro.py -d 10 -n 1 --apply add 100 if mod 5 eq 2 else add 10 if mod 2 eq 1 else scale -2
 -20:  10.00 % |====================
 -16:  10.00 % |====================
 -12:  10.00 % |====================
  -8:  10.00 % |====================
  11:  10.00 % |====================
  13:  10.00 % |====================
  15:  10.00 % |====================
  19:  10.00 % |====================
 102:  10.00 % |====================
 107:  10.00 % |====================
```
And you can combine that all with positional parameters as well:
```
➔ python dice_distro.py -d 4 -n 2 --apply add 10 100  if mod 2 3 eq 0 1 else scale 2 3 if mod 3 2 eq 1 0 else set-to 0
  0,  0:   6.25 % |============
  0,  6:   6.25 % |============
  0,101:   6.25 % |============
  0,104:   6.25 % |============
  2,  0:   6.25 % |============
  2,  6:   6.25 % |============
  2,101:   6.25 % |============
  2,104:   6.25 % |============
 12,  0:   6.25 % |============
 12,  6:   6.25 % |============
 12,101:   6.25 % |============
 12,104:   6.25 % |============
 14,  0:   6.25 % |============
 14,  6:   6.25 % |============
 14,101:   6.25 % |============
 14,104:   6.25 % |============
```

### Optimization Using Saving/Loading Output
You can use the `--save <file_name>` flag to save the data to a file.
Then use it later for other calculations.
You can use the `--no-output` to not render any output.
```
➔ python dice_distro.py -d 6 --no-output --save /tmp/1d6.json
➔ python dice_distro.py -d 8 --no-output --save /tmp/1d8.json
```
You can then load the data using `--load <file_names>`.
If you supply more than one file name, the distributions are **multiplied**.
```
➔ python dice_distro.py --load /tmp/1d6.json /tmp/1d8.json --apply sum
 2:   2.08 % |====
 3:   4.17 % |========
 4:   6.25 % |============
 5:   8.33 % |================
 6:  10.42 % |====================
 7:  12.50 % |=========================
 8:  12.50 % |=========================
 9:  12.50 % |=========================
10:  10.42 % |====================
11:   8.33 % |================
12:   6.25 % |============
13:   4.17 % |========
14:   2.08 % |====
```
This makes calculating some larger dice pools to be easier.
For example, calculating the distribution for eight D20.
The normal example will take a very long time to run:
```
➔ # do not run, this will take a very long time
➔ python dice_distro.py -d 20 -n 8  --apply sum --show-counts
```
While the example using file save runs much faster:
```
➔ python dice_distro.py -d 20 -n 2 --apply sum --save /tmp/sum-2d20.json --no-output
➔ python dice_distro.py --load /tmp/sum-2d20.json /tmp/sum-2d20.json --apply sum --save /tmp/sum-4d20.json --no-output
➔ python dice_distro.py --load /tmp/sum-4d20.json /tmp/sum-4d20.json --apply sum --show-counts
```
**Note** that this only applies if you can break down your problem into a product of smaller distributions.

# Custom Operations
If you are trying to do something very complicated,
and you feel that the tools given are restrictive
you can make your very own custom operations.
Make a python file, and write a function.

The function signature should be:
- First parameter is a tuple of order ints (the dice roll)
- Parameters passed in from `--apply`
	- Note that your parameters should **NOT** be any function name or logical keyword
		- The parser will assume it is not a parameter
The return value should be any of:
- An `int`
- A `list` or `tuple` where all the entries are `int`

Lets say that the following is saved in `/tmp/custom_funcs.py`:
```python
# Functions you want to use should not begin with `_`
# nor should they be any other keyword
def myadd(dice,*args):
	# do stuff
	if len(args) > 0:
		print(args)
	return [value + 2 for value in dice]
```
Then to invoke your custom function you can run:
```
➔ python dice_distro.py -d 6 -n 1 --custom /tmp/custom_funcs.py --apply myadd
3:  16.67 % |=================================
4:  16.67 % |=================================
5:  16.67 % |=================================
6:  16.67 % |=================================
7:  16.67 % |=================================
8:  16.67 % |=================================
```
And if you were passing parameters:
```
➔ python dice_distro.py -d 6 -n 1 --custom /tmp/custom_funcs.py --apply myadd 1 2 hi 3
('1', '2', 'hi', '3')
('1', '2', 'hi', '3')
('1', '2', 'hi', '3')
('1', '2', 'hi', '3')
('1', '2', 'hi', '3')
('1', '2', 'hi', '3')
3:  16.67 % |=================================
4:  16.67 % |=================================
5:  16.67 % |=================================
6:  16.67 % |=================================
7:  16.67 % |=================================
8:  16.67 % |=================================
```
This should allow you all the flexablity required to do anything else that isn't implemented.

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
➔ python dice_distro.py -d 30 -n 10 -pdp 3 --apply select -1 -2 sum --simulate 100000
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

If I find time in the future, I plan to (in no specific order):
- Add parallelization the work so that options with a large enumeration set can be computed faster
    - also allowing larger numbers of simulated dice throws.
    - there are current issues with pickeling the operation function applied to the dice roll
- Expand the unit tests
	- Logic parser needs to be tested more thoroughly.
