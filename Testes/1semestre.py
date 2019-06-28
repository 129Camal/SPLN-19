#!/usr/local/bin/python3.7

import sys
import re
import fileinput
import getopt

# Questão 1


def maxdeff(numbers):
    min = numbers[0]
    max = 0

    for i in range(len(numbers)):
        if numbers[i] < min:
            min = numbers[i]

        if numbers[i] > max:
            max = numbers[i]

    print(str(max - min))

# numbers = [1,1,3,5,2]
# maxdeff(numbers)


def count_char_occur(text):
    caracteres = {}

    text = text.lower()

    for i in range(len(text)):
        caracteres[text[i]] = caracteres.get(text[i], 0) + 1

    print(str(caracteres))

#count_char_occur("TESTE DE SPLN")

# Questão 2


def unixFilter():
    opts, args = getopt.getopt(sys.argv[1], "r")

    text = open(args).read()

    text = re.sub(r"\n(?!\n)", r" ", text)

    sys.stdout.write(text)

# Questão 3


def fix_sent_start(text):
    print(text)

    search = re.search(r"^([A-Z]+)", text)
    if(search):
        text = re.sub(search.group(), search.group().lower(), text)
    
    print(text)

#fix_sent_start("OLA, estas BEM?")

# Questão 4
