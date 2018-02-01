#!/bin/bash

python_exe="python$1"

CUR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT_DIR="$( cd "$( dirname $CUR_DIR )" && pwd )"

dice_distro_file="$PROJECT_ROOT_DIR/dice_distro.py"
test_params_with_output="--show-args"
test_params="$test_params_with_output --no-output"

echo "Starting Test with $python_exe" && \
    # Test help render
    $python_exe $dice_distro_file $test_params --help && \
    # Run unit tests
    $python_exe -m unittest discover --start-directory $CUR_DIR && \
    # Test basic operations
    $python_exe $dice_distro_file $test_params -d 6 -n 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sum && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply min && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply max && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sort && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply prod && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-or && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-xor && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-and && \
    # Test basic operations with parameters
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sum 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply min 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply max 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply sort 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply prod 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-or 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-xor 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bit-and 2 && \
    # Test add
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply add 2 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply add 2 -1 && \
    # Test scale operations with all the different rounding options
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-ceil 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-floor 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-truncate 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-half-up 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply scale r-half-down 0.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply scale 0.5 0.333 prod && \
    # Test set-to
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply set-to 1 && \
    # Test exp
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp r-ceil 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp r-floor 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp r-truncate 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp r-half-up 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp r-half-down 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply exp 2.5 3 prod && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp as-base r-ceil 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp as-base r-floor 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp as-base r-truncate 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp as-base r-half-up 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply exp as-base r-half-down 2.5 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply exp as-base 2.5 3 prod && \
    # Test bound
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply bound 3 4 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply bound 2 5 3 4 && \
    # Test chained operation with bound
    $python_exe $dice_distro_file $test_params -d 6 -n 1 --apply add 2 bound 1 6 && \
    # Test Select operation
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply select 1 && \
    $python_exe $dice_distro_file $test_params -d 4 -n 4 --apply select -1 -2 -3 && \
    $python_exe $dice_distro_file $test_params -d 4 -n 4 --apply select -1 -2 -3 --sort value && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply select -1 -2 -3 sum && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -2 -3 select 0 1 && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -2 -3 select 0 1 sum && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -2 -3 select 0 1 select 1 && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -4 -2 -3 sum 2 select 0 && \
    $python_exe $dice_distro_file $test_params -d 8 -n 5 --apply select -1 -2 -3 select 0 1 select 1 --memorize-input && \
    # Test slice-apply
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply slice-apply 2 sum max && \
    # Test if-block
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply add 10 100 if mod 2 3 eq 0 1 && \
    # Test if-else block
    $python_exe $dice_distro_file $test_params -d 10 -n 1 --apply add 100 if mod 5 eq 2 else add 10 if mod 2 eq 1 else scale 0 && \
    $python_exe $dice_distro_file $test_params -d 10 -n 2 --apply add 100 if mod 5 eq 2 else add 10 if mod 2 eq 1 else scale 0 then sum && \
    # Test complex if-block with nested boolean logic
    $python_exe $dice_distro_file $test_params -d 10 --apply add 100 if eq 1 or not [ ge 2 and le 3 ] and [ gt 5 and lt 8 ] && \
    $python_exe $dice_distro_file $test_params -d 10 --apply [ add 2 scale 2 ] if mod 3 eq 1 else scale -1 add -1 && \
    # Test Reroll
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --apply reroll if lt 4 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply sum 2 reroll if lt 7 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 4 --apply reroll if mod 2 eq 1 && \
    # # Test Memorize
    $python_exe $dice_distro_file $test_params --memorize-input -d 6 -n 4 --apply sum 2 sum && \
    $python_exe $dice_distro_file $test_params --memorize-input -d 6 -n 4 --apply slice-apply 2 sum sum && \
    $python_exe $dice_distro_file $test_params --memorize-input -d 6 -n 4 --apply select -1 -2 sum && \
    $python_exe $dice_distro_file $test_params --memorize-input -d 6 -n 4 --apply sort sum && \
    # # Test Custom Functions
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --custom "$CUR_DIR/mock_custom_func.py" --apply custom_sum && \
    # Test custom single die type options
    $python_exe $dice_distro_file $test_params -d 10 -n 2 --die-start 0 && \
    $python_exe $dice_distro_file $test_params -d 10 -n 2 --die-start 0 --die-step 10 && \
    $python_exe $dice_distro_file $test_params -n 2 --die-values 0 10 100 -1000 && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --die-weights 6 5 4 3 2 1 --apply sum && \
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --die-weights 6.1 5.2 4.3 3.4 2.5 1.6 --apply sum && \
    # Test custom multi-die type options
    $python_exe $dice_distro_file $test_params --multi-die-sides 12 8 6 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 4 3 2 --multi-die-start -1 0 1 --multi-die-step 3 2 1 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 4 3 2 --multi-die-values 0 1 2 3 10 20 30 100 200 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 2 3 4 --multi-die-weights 1 2 3 4 5 6 7 8 9 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 2 3 4 --multi-die-values 9 8 7 6 5 4 3 2 1 --multi-die-weights 1 2 3 4 5 6 7 8 9 && \
    $python_exe $dice_distro_file $test_params --multi-die-sides 2 3 4 --multi-die-values 9 8 7 6 5 4 3 2 1 --multi-die-weights 1.9 2.8 3.7 4.6 5.5 6.4 7.3 8.2 9.1 && \
    # Test file save and load with distrobution product
    $python_exe $dice_distro_file $test_params -d 6 -n 2 --save /tmp/2d6.json && \
    $python_exe $dice_distro_file $test_params --load /tmp/2d6.json /tmp/2d6.json --apply sum && \
    # Test simulate (with different dice generation options)
    $python_exe $dice_distro_file $test_params --simulate 10000 -d 6 -n 2 && \
    $python_exe $dice_distro_file $test_params --simulate 10000 -d 10 -n 2 --die-start 0 --die-step 10 && \
    $python_exe $dice_distro_file $test_params --simulate 10000 -n 2 --die-values 0 10 100 -1000 && \
    $python_exe $dice_distro_file $test_params --simulate 10000 -d 6 -n 2 --die-weights 6 5 4 3 2 1 --apply sum && \
    $python_exe $dice_distro_file $test_params --simulate 10000 -d 6 -n 2 --die-weights 6.1 5.2 4.3 3.4 2.5 1.6 --apply sum && \
    $python_exe $dice_distro_file $test_params --simulate 10000 --multi-die-sides 12 8 6 && \
    $python_exe $dice_distro_file $test_params --simulate 10000 --multi-die-sides 4 3 2 --multi-die-start -1 0 1 --multi-die-step 3 2 1 && \
    $python_exe $dice_distro_file $test_params --simulate 10000 --multi-die-sides 4 3 2 --multi-die-values 0 1 2 3 10 20 30 100 200 && \
    $python_exe $dice_distro_file $test_params --simulate 10000 --multi-die-sides 2 3 4 --multi-die-weights 1 2 3 4 5 6 7 8 9 && \
    $python_exe $dice_distro_file $test_params --simulate 10000 --multi-die-sides 2 3 4 --multi-die-values 9 8 7 6 5 4 3 2 1 --multi-die-weights 1 2 3 4 5 6 7 8 9 && \
    $python_exe $dice_distro_file $test_params --simulate 10000 --multi-die-sides 2 3 4 --multi-die-values 9 8 7 6 5 4 3 2 1 --multi-die-weights 1.9 2.8 3.7 4.6 5.5 6.4 7.3 8.2 9.1 && \
    # Test display options
    $python_exe $dice_distro_file $test_params_with_output -d 6 -n 2 && \
    $python_exe $dice_distro_file $test_params_with_output -d 6 -n 2 --apply sum --show-counts && \
    $python_exe $dice_distro_file $test_params_with_output -d 6 -n 2 --apply sum --sort value && \
    $python_exe $dice_distro_file $test_params_with_output -d 6 -n 2 --apply sum --bar-size 0 && \
    $python_exe $dice_distro_file $test_params_with_output -d 6 -n 2 --apply sum --bar-size 2 --bar-char '@#' --bar-prefix '<|' && \
    echo "End of Test with $python_exe"
