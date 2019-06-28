
import re
import unidecode
import numpy
import sys
import subprocess
import getopt
from nltk import ngrams
from collections import Counter
import bs4
import requests
from bs4 import BeautifulSoup as soup
import datetime as date

#
# Questao 1
#


def count_digits(numbers):
    totalnumbers = 0

    for number in numbers:
        totalnumbers = totalnumbers + len(re.findall(r"\d", str(number)))

    return totalnumbers


# print(count_digits([1, 5, 14, 2800, 1000]))

def is_palindrome(text):
    text = unidecode.unidecode(text)

    # Caso seja um conjunto de palavras
    if len(text.split()) > 1:

        # Buscar todas as palavras
        allwords = re.findall("\w+", text, re.DOTALL)

        # Buscar as palavras que estão juntas a pontos.
        pointwords = re.findall("(\w+)(?=\.|\!|\,)", text, re.DOTALL)

        if(numpy.array_equal(allwords, pointwords)):
            return True
        else:
            return False

    # Caso seja só uma palavra
    else:
        size = int(len(text) / 2)

        if(len(text) % 2 == 0):
            l, r = text[:size], text[size:]
        else:
            l, r = text[:size], text[size+1:]

        if(re.search(l, r[::-1]), re.DOTALL):
            return True
        else:
            return False


# print(is_palindrome("Olê! Maracujá, caju, caramelo."))
# print(is_palindrome("Ana"))


#
# Questão 2
#

def unix_filter():

    options, remainder = getopt.getopt(sys.argv[1:], "")

    input = open(remainder[0])
    output = sys.stdout

    text = input.read().split(" ")

    words = {key.split("/")[0]: {} for key in text}

    for i in range(len(text)):
        word = text[i].split("/")
        wordTags = words.get(word[0])
        wordTags["Occur"] = wordTags.get("Occur", 0) + 1
        wordTags[word[1]] = wordTags.get(word[1], 0) + 1

    for word in words.items():
        output.write(word[0] + " (" + str(word[1].get("Occur")) + "): ")

        for tag in word[1].items():
            if(tag[0] != "Occur"):
                output.write(tag[0] + " (" + str(tag[1]) + ") ")

        output.write("\n")


# unix_filter()

#
# Questão 3
#

def calc_trigrams():
    file = sys.argv[1]

    text = open(file).read()
    text = text.lower()
    trigrams = [text[i:i+3] for i in range(len(text)-(2))]

    occur = Counter(trigrams)
    return occur


def fix_word(word):
    occurs = calc_trigrams()

    errors = re.findall("(\w\%\w)", word)

    for error in errors:
        best = 0

        for occur in occurs.items():
            if(error[0] == occur[0][0] and error[2] == occur[0][2]):

                if(best < occur[1]):
                    correctWay = occur[0]
                    best = occur[1]

    if(correctWay):
        word = re.sub(r"\w\%\w", correctWay, word)

    return word

# print(fix_word("ser%ande"))

#
# Questão 4
#


'''
a)
Precision - Representa a proporção de coisas classificadas corretamente

Ferramenta A:

5 / 5 = 1

Ferramenta B:

20 / 20 + 10 = 0.666


Cobertura - Expressa a habilidade para encontrar instâncias relevantes

Ferramenta A:

5 / 10 = 0.5

Ferramenta B:

20 / 20 = 1


Resultado Ferramenta 1:

2 * (1 * 0.5)/(1 + 0.5) = 0.666

Resultado Ferramenta 2:

2 * (1 * 0.666)/(1 + 0.666) = 0.799

b) Devia se escolher a ferramenta B pois comparando os resultados das duas ferramentas esta apresenta um maior valor de confiabilidade

c)
'''

#
# Questao 5
#


# def g():


s = (
    [
        (
            "meu caro",
            [
                "amigo,",
                lambda x: x["nome"]
            ]
        ),
        "querido interlocutor"
    ],
    [
        "cala-te que já lá vai o tempo em que os animais falavam",
        "estou profundamente abismado com o que me dizes"
    ]
)

#
# Questao 6
#


def conselhos_da_avo(weather):
    x = date.datetime.now()
    x = x.strftime("%d ") + x.strftime("%b")
    for day in weather:
        if(day.get('date') == x):
            if(day.get('temp_min') < 15):
                print("Leva um casaco!")
            if (day.get('uv') > 7):
                print("Sai do Sol que faz mal!")


weather = [
    {
        'date': '16 Jun',
        'prev_txt': 'Céu nublado por nuvens altas',
        'temp_min': 18,
        'temp_max': 28,
        'uv': 8

    },
    {
        'date': '3 Seg',
        'prev_txt': 'Céu pouco nublado',
        'temp_min': 11,
        'temp_max': 27,
        'uv': 9

    },
    {
        'date': '4 Qua',
        'prev_txt': 'Céu limpo',
        'temp_min': 9,
        'temp_max': 31

    }


]

#conselhos_da_avo(weather)


def previsaoSemanal(distrito, concelho):

    requestLink = "https://www.ipma.pt/pt/otempo/prev.localidade.hora/#" + distrito + "&" + concelho

    response = requests.get(requestLink).content

    soup_page = soup(response, 'html.parser')

    print(soup_page)

    # ul = soup_page.find('ul', 'subnav')

    # lis = ul.find_all('li')

    # for li in lis:
    #     a = li.find('a', title="Previsão no mundo")
    #     if(a):
    #         print(a.text)
    #         print(a["href"])
    #         print(a["title"])

previsaoSemanal("Porto", "Felgueiras")