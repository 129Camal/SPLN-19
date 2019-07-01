from bs4 import BeautifulSoup as BS
import requests
import sys
import re
import getopt
import os

#
# Funtion to get the meaning of the word with certain semantic meaning
#
def getMeaning(word, semantic_meaning):

    urlBase = "https://www.lexico.com/en/definition/" + word

    response = requests.get(urlBase).content

    soup = BS(response, 'html.parser')

    word_types = soup.findAll('section', 'gramb')

    for word_type in word_types:
        instance = word_type.find('h3', 'ps pos')

        if(semantic_meaning != instance.span.text):
            continue

        ul = word_type.find('ul', 'semb')
        lis = ul.findAll('li')

        allmeaning = []
        allsyn = []
        for li in lis:
            div = li.find('div', 'trg')

            if(div):
                p = div.find('p')

                if(p):
                    span = p.find('span', 'ind')
                    if(span):
                        allmeaning.append(span.text)

                    # Get Synonyms
                    sysn = div.find('div', 'synonyms')
                    if(sysn):
                        strong = sysn.find('strong', 'syn')
                        exg = sysn.find('span', 'syn')

                        if(not exg):
                            allsyn.append(strong.text)
                        else:
                            allsyn.append(strong.text + exg.text)
                    else:
                        allsyn.append("Doesn`t have synonyms")

        if(len(allmeaning) > 0):
            x = " || ".join(allmeaning)
            print("\t\t\t<prop type=\"meaning\">" +
                  x + "</prop>")
        
        if(len(allsyn) > 0):
            x = " || ".join(allsyn)
            print("\t\t\t<prop type=\"synonyms\">" +
                  x + "</prop>")


# -------------------------------- BEGIN ----------------------------------- #

# All languages available
languages = [('german', 'de'), ('french', 'fr'), ('spanish', 'es'),
             ('chinese', 'ch'), ('russian', 'ru'), ('portuguese', 'pt'), ('italian', 'it'), ('polish', 'pl')]

# See what words and what languages the user wants
opts, args = getopt.getopt(sys.argv[1:], '', ['to='])

# Filter the languages that user wants
languages = list(filter(lambda x: x[1] in opts[0][1], languages))

# End the script if we not have languages or words to translate
if(len(languages) <= 0 or len(args) <= 0):
    print("Please enter the corret inputs!")
    sys.exit()

notFound = 0
for userWord in args:
    types = {}

    for language in languages:
        urlBase = "https://www.linguee.com/english-" + \
            language[0] + "/search?query=" + userWord

        response = requests.get(urlBase).content

        soup = BS(response, 'html.parser')

        dictionary = soup.find('div', id="dictionary")
        
        if(not dictionary):
            notFound = 1
            print(userWord + ": we don't find any translation for that!")
            break
        
        exact = dictionary.find('div', 'exact')
        lemma = exact.findAll('div', 'lemma')

        for lem in lemma:
            word = lem.find('span', 'tag_lemma')
            tag_wordtype = word.find('span', 'tag_wordtype')

            word_type = tag_wordtype.text
            if(not types.get(word_type)):
                types[word_type] = []

            translation = lem.find('span', 'tag_trans')
            types[word_type].append((language[1], translation.a.text))

    f = open('english_' + userWord + '2all.tmx', 'w')
    sys.stdout = f

    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
          "<tmx version=\"1.4\">", 
          "\t<header adminlang=\"en\"",
          "\t\tdatatype=\"tbx\"",
          "\t\to-tmf=\"unknown\"",
          "\t\tsegtype=\"block\"",
          "\t\tsrclang=\"en\"/>",
          "\t<body>",
          sep="\n")

    i = 0

    for word_type in types.items():
        print("\t\t<tu tuid=\"" + str(i+1) + "\">",
              "\t\t\t<prop type=\"word_type\">" + word_type[0] +
              "</prop>", sep="\n")

        getMeaning(userWord, word_type[0])

        print("\t\t\t<tuv xml:lang=\"en\">",
              "\t\t\t\t<seg>" + userWord + "</seg>",
              "\t\t\t</tuv>",
              sep="\n")

        for translation in word_type[1]:
            print("\t\t\t<tuv xml:lang=\"" + translation[0] + "\">",
                  "\t\t\t\t<seg>" + translation[1] + "</seg>",
                  "\t\t\t</tuv>",
                  sep="\n")
        i = i + 1
        print("\t\t</tu>")

    print("\t</body>",
          "</tmx>",
          sep="\n")

    if(notFound == 1):
        os.remove('english_' + userWord + '2all.tmx')
        notFound = 0
