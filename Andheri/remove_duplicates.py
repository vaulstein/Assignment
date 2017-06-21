#!/usr/bin/env python
import common

array_size = common.ask("Enter array size : ", answer=int, l=0)
array_input = common.ask("Enter {0} array element : ".format(array_size), answer=list, l=array_size)
print("Original array is : {0}".format(" ".join(array_input)))
print("New array is : {0}".format(" ".join(list(set(array_input)))))

# Test Cases
# Input 1: Integers, strings, -ve numbers, 0
# Input 2: matching size entered, non-matching values, strings/numbers allowed as no criteria
# specified in question
