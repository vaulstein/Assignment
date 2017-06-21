#!/usr/bin/env python
import common

def split_list(a_list):
    a_list = [int(a) for a in a_list]
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

array_size = common.ask("Enter array size : ", answer=int, l=0)
array_input = common.ask("Enter {0} array element : ".format(array_size), answer=list, l=array_size)
if array_size % 2 == 0:
    first, second = split_list(array_input)
    decreasing = True
    for i, a in enumerate(first):
        if i < len(first) - 1:
            if a <= first[i+1]:
                decreasing = False
    increasing = True
    for i, b in enumerate(second):
        if i < len(second) - 1:
            if b >= second[i+1]:
                increasing = False
    if decreasing and increasing:
        print('Yes')
    else:
        print('No')
else:
    print('No')
