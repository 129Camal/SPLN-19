#!/usr/local/bin/python3.7

import xml.etree.ElementTree as ET
import sys 

file = sys.argv[1]

tree = ET.parse(file)
root = tree.getroot()
count = 1

#itera sobre os filhos dos filhos do root imprimindo as suas tags identadas
def parseChilds(parent, count):
    for child in parent:
        print(('\t'* count)+'-->',child.tag)
        children = child.getchildren()
        if(children):
            parseChilds(children, count+1)

#imprime tag do elemento root
print(root.tag)
#itera sobre os filhos do root imprimindo as suas tags
for child in root:
    print('-->', child.tag)
    children = child.getchildren()
    if(children):
        parseChilds(children, count)
