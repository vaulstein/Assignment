#!/usr/bin/env python
import common

array_size = common.ask("Enter array size : ", answer=int, l=0)
array_input = common.ask("Enter {0} array element : ".format(array_size+2), answer=list, l=array_size+2)
counts = dict()
for i in array_input:
  counts[i] = counts.get(i, 0) + 1

for key, value in counts.items():
    if value == 2:
        print key