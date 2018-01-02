#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

dice_distro_file="$DIR/dice_distro.py"
test_params="--show-args"

echo "Starting Test" && \gui
    python $dice_distro_file $test_params -d 6 -n 2 && \
    python $dice_distro_file $test_params -d 6 -n 2 --show-counts && \
    python $dice_distro_file $test_params -d 6 -n 2 --sort value && \
    python $dice_distro_file $test_params -d 6 -n 2 --bar-size 0 && \
    python $dice_distro_file $test_params -d 6 -n 2 --bar-size 2 --bar-char '@#' --bar-prefix '<|' && \
    python $dice_distro_file $test_params -d 20 -n 2 --op-func max && \
    python $dice_distro_file $test_params -d 20 -n 2 --op-func min && \
    python $dice_distro_file $test_params -d 4 -n 4 --op-func set && \
    python $dice_distro_file $test_params -d 6 -n 4 --op-func select --op-param -2 && \
    python $dice_distro_file $test_params -d 6 -n 4 --op-func select --op-param 1 && \
    python $dice_distro_file $test_params -d 4 -n 4 --op-func select --op-params -1 -2 -3 && \
    python $dice_distro_file $test_params -d 4 -n 4 --op-func select --op-params -1 -2 -3 --sort value && \
    python $dice_distro_file $test_params -d 6 -n 4 --op-func select --op-params -1 -2 -3 sum && \
    python $dice_distro_file $test_params -d 8 -n 5 --op-func select --op-params -1 -2 -3 select 0 1 && \
    python $dice_distro_file $test_params -d 8 -n 5 --op-func select --op-params -1 -2 -3 select 0 1 sum && \
    python $dice_distro_file $test_params -d 8 -n 5 --op-func select --op-params -1 -2 -3 select 0 1 select 1 && \
    python $dice_distro_file $test_params -d 8 -n 5 --op-func select --op-params -1 -2 -3 select 0 1 select 1 --memorize && \
    python $dice_distro_file $test_params -d 6 -n 2 --op-func conditional-reroll --op-params 4 && \
    python $dice_distro_file $test_params -d 6 -n 4 --op-func sum --op-params 2 conditional-reroll 7 && \
    python $dice_distro_file $test_params -d 10 -n 2 --die-start 0 && \
    python $dice_distro_file $test_params -d 10 -n 2 --die-start 0 --die-step 10 && \
    python $dice_distro_file $test_params -n 2 --die-values 0 10 100 -1000 && \
    python $dice_distro_file $test_params --multi-die-sides 12 8 6 && \
    python $dice_distro_file $test_params --multi-die-sides 8 6 4 --op-func conditional-reroll --op-params 3 && \
    python $dice_distro_file $test_params --multi-die-sides 8 6 4 --op-func conditional-reroll --op-params 5 4 && \
    python $dice_distro_file $test_params --multi-die-sides 4 3 2 --multi-die-start -1 0 1 --multi-die-step 3 2 1 && \
    python $dice_distro_file $test_params --multi-die-sides 4 3 2 --multi-die-values 0 1 2 3 10 20 30 100 200 && \
    python $dice_distro_file $test_params -d 40 -n 6 --op-func max --simulate 100000
