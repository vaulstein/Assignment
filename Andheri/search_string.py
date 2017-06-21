#!/usr/bin/env python
import common

input_string = common.ask("Enter input string:", answer=common.str_compat)
search_string = common.ask("Enter search string:", answer=common.str_compat)
location = common.ask("Enter location to search from:", answer=int, l=-1)

def find(s, sub, index):
    trun_s = s[index:]
    for i, _ in enumerate(trun_s):
        if trun_s.startswith(sub, i):
            return i+index
    return -1

print(find(input_string, search_string, location))

