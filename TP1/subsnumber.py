#!/usr/bin/python3.7

import sys, re
from num2words import num2words

file = sys.argv[1]

for line in open(file).readlines():
    line = re.sub(r"(\d+)", lambda x : num2words(int(x.group()), lang='pt'), line)
    print(line)
