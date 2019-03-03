#!/usr/local/bin/python3.7

import sys, re
from num2words import num2words

file = sys.argv[1]

f = open('out.txt', 'w')
sys.stdout = f

#abrir o ficheiro e ler o conteudo
text = open(file).read()

#Captar os números ordinais e traduzir dando cast para inteiro
text = re.sub(r"(\d+)(\º|\ª)", lambda x : num2words(int(x.group(1)), to='ordinal', lang='pt'), text)

#Captar os números decimais que usam , e substituir por .
text = re.sub(r"(\d+)\,(\d+)", r"\1.\2", text)

#Captar os números decimais que possuem . e traduzir dando cast para float
text = re.sub(r"(\d+)\.(\d+)", lambda x : num2words(float(x.group()), lang='pt'), text)

#Substituir o simbolo % pela tradução verbal
text = re.sub(r"\%", " por cento", text)

#Captar os número inteiros e traduzir dando cast para inteiro
text = re.sub(r"(\d+)", lambda x : num2words(int(x.group()), lang='pt'), text)

#Dar print para o ficheiro
print(text)


#for line in open(file).readlines():
#    line = re.sub(r"(\d+)(\º|\ª)", lambda x : num2words(int(x.group(1)), to='ordinal', lang='pt'), line)
#    line = re.sub(r"(\d+)\,(\d+)", r"\1.\2", line)
#    line = re.sub(r"(\d+)\.(\d+)", lambda x : num2words(float(x.group()), lang='pt'), line)
#    line = re.sub(r"\%", "por cento", line)
#    line = re.sub(r"(\d+)", lambda x : num2words(int(x.group()), lang='pt'), line)
#    print(line)
