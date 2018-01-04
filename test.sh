#!/bin/bash

python_exe="python$1"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

dice_distro_file="$DIR/dice_distro.py"
test_params="--show-args"

echo "Starting Test" && \
    $python_exe $dice_distro_file $test_params --help && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sum && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply min && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply max && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply set && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply prod && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-or && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-xor && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-and && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply sum  2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply shift 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply shift 2 -1 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-ceil 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-floor 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-truncate 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-half-up 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-half-down 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply scale 0.5 0.333 prod && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply bound 3 4 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bound 2 5 3 4 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply shift 2 bound 1 6 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply shift if mod 2 3 eq 0 1 then 10 100 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply select 1 && \
    $python_exe $dice_distro_file $test_params -d 4 -n 4 --apply select -1 -2 -3 && \
    $python_exe $dice_distro_file $test_params -d 4 -n 4 --apply select -1 -2 -3 --sort value && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply select -1 -2 -3 sum && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -2 -3 select 0 1 && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -2 -3 select 0 1 sum && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -2 -3 select 0 1 select 1 && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -4 -2 -3 sum 2 select 0 && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -2 -3 select 0 1 select 1 --memorize && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply reroll if lt 4 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply sum 2 reroll if lt 7 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply slice-apply 2 sum max && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply reroll if mod 2 eq 1 && \
    $python_exe $dice_distro_file $test_params -d 10 -n 2 --die-start 0 && \
    $python_exe $dice_distro_file $test_params -d 10 -n 2 --die-start 0 --die-step 10 && \
    $python_exe $dice_distro_file $test_params -n 2 --die-values 0 10 100 -1000 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 12 8 6 --apply sum && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 8 6 4 --apply reroll if lt 3 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 8 6 4 --apply reroll if lt 5 4 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 4 3 2 --multi-die-start -1 0 1 --multi-die-step 3 2 1 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 4 3 2 --multi-die-values 0 1 2 3 10 20 30 100 200 && \
    # the following two tests are related
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --save /tmp/2d6.json && \
    $python_exe $dice_distro_file $test_params --load /tmp/2d6.json /tmp/2d6.json --apply sum && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sum --show-counts && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sum --sort value && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sum --bar-size 0 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sum --bar-size 2 --bar-char '@#' --bar-prefix '<|' && \
    $python_exe $dice_distro_file $test_params -d 40 -n 6 --apply max --simulate 100000
