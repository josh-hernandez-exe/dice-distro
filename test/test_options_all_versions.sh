#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

test_file="$DIR/test_options.sh"

# NOTE: python2 and python3 are alias
#       for the default python sub-version (2.x or 3.x)
#       on that machine.
version_list="
    2
    2.7
    3
    3.0
    3.1
    3.2
    3.3
    3.4
    3.5
    3.6
"

is_missing_versions=0
tested_versions=""
missing_versions=""

for num in $version_list; do
    which "python$num" > /dev/null 2>&1
    if [[ $? -eq 0 ]]; then
        $test_file $num
        test_status=$?
        if [[ $test_status -ne 0 ]]; then
            exit $test_status
        fi
        tested_versions="$tested_versions $num"
    else
        missing_versions="$missing_versions $num"
        is_missing_versions=1
    fi
done


if [[ $is_missing_versions -eq 1 ]]; then
    echo ""
    echo "The following python versions are not available on this machine:"
    for num in $missing_versions; do
        echo "python$num"
    done
fi

if [[ $tested_versions == "" ]]; then
    echo ""
    echo "No tests have been run."
    exit 1
else
    echo ""
    echo "The following versions of python have been tested:"
    for num in $tested_versions; do
        echo "python$num"
    done
fi

echo ""
echo "All testing with available python versions completed with a successful status code."

exit 0
