#!/usr/local/bin/python3.7

import sys, re
import xml.etree.ElementTree as ET

file = sys.argv[1]

#Abrir o ficheiro de escrita
f = open('xml.xml', 'w')
sys.stdout = f

i = 0

#Abrir o ficheiro e ler o conteudo do ficheiro
openedfile = open(file).readlines()
nlinhas = len(openedfile)

while i < nlinhas:
    #tratar de captar a abertura do ficheiro
    match = re.search(r"(\w+)\: ?\{", openedfile[i])
    if match:
        beginning = ET.Element(match.group(1))
        i+= 1
        #encontrar os atributos da variavel de abertura do ficheiro
        while i < nlinhas:
            atr = re.search(r"\'\_(.*)\'( )*\:( )*\'(.*)\'\,", openedfile[i])
            if(atr):
                beginning.set(atr.group(1), atr.group(4))
                i += 1
            else:
                break
        
        #encontrar os filhos que pertencem à tag de abertura e os filhos desses filhos 
        while i < nlinhas:
            #encontrar o nome da tag
            match = re.search(r"(\w+)\: ?\{", openedfile[i])
            i += 1

            if(match):    
                item = ET.SubElement(beginning, match.group(1))
                
                while i < nlinhas:
                    #encontrar atributos relacionados à tag
                    atr = re.search(r"\'\_(.*)\'( )*\:( )*\'(.*)\'\,", openedfile[i])
                    #encontrar content relacionado com a tag
                    content = re.search(r"\'\_\_CONTENT\'( )*\:( )*\'(.*)\'\,?", openedfile[i])
                    #encontrar um lista, que é filha de uma tag
                    matchList = re.search(r"(\w+)\: ?\[", openedfile[i])
                    #encontrar outra tag que é filha de uma tag
                    match = re.search(r"(\w+)\: ?\{", openedfile[i])

                    if(atr):
                        #adicionar atributo
                        item.set(atr.group(1), atr.group(4))
                        i += 1
                    else:
                        if(content):
                            #adicionar content
                            item.text = content.group(3)
                            i += 1 
                        else:
                            if(matchList):
                                #adicionar tag de lista como filho
                                item = ET.SubElement(item, matchList.group(1))
                                i+=2
                            else:
                                if(match):
                                    #adicionar nova tag como tag filho
                                    item = ET.SubElement(item, match.group(1))
                                    i += 1
                                else:
                                    break
    else:        
        i+=1

# print dos resultados
mydata = ET.tostring(beginning)  
print(mydata) 
