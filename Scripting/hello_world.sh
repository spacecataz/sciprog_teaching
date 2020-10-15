#!/bin/bash

for a in ${BASH_ARGV[*]}
do
    echo -e "$a"
done

echo -e 'Hello World'

ls *.py | grep sciprog
