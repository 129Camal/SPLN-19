from bs4 import BeautifulSoup as BS
import requests
import sys
import re


def getMeaning(word, semantic_meaning):
    urlBase = "https://www.lexico.com/en/definition/cold"

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
        for li in lis:
            div = li.find('div', 'trg')

            if(div):
                p = div.find('p')
                if(p):
                    span = p.find('span', 'ind')
                    allmeaning.append(span.text)
        
        if(len(allmeaning) > 0):
            x = ";".join(allmeaning)
            print("\t\t\t<prop type=\"meaning\">" +
                  x + "</prop>")


languages = [('german', 'de'), ('french', 'fr'), ('spanish', 'es'),
             ('chinese', 'ch'), ('russian', 'ru'), ('portuguese', 'pt'), ('italian', 'it'), ('polish', 'pl')]

types = {}

for language in languages:
    urlBase = "https://www.linguee.com/english-" + \
        language[0] + "/search?query=cold"

    response = requests.get(urlBase).content

    soup = BS(response, 'html.parser')

    dictionary = soup.find('div', id="dictionary")
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

f = open('english2all.tmx', 'w')
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

    getMeaning("cold", word_type[0])

    print("\t\t\t<tuv xml:lang=\"en\">",
          "\t\t\t\t<seg>cold</seg>",
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

# for language in languages:

#     urlBase = "https://www.linguee.com/english-" + language + "/search?query=cold"

#     response = requests.get(urlBase).content

#     soup = BS(response, 'html.parser')

#     dictionary = soup.find('div', id="dictionary")
#     exact = dictionary.find('div', 'exact')
#     lemma = exact.findAll('div', 'lemma')

#     for lem in lemma:
#         words = lem.findAll('span', 'tag_lemma')
#         translations = lem.findAll('span', 'tag_trans')

#         for word in words:

#             if("cold" == word.a.text):

#                 audio = word.find('a', 'audio')
#                 word_type = word.find('span', 'tag_wordtype')

#                 audio = re.search(r"\"PT_PT(\w|\d|\/|\-)+\"", audio['onclick'])
#                 # print(audio.group())
# print("\t\t<tu tuid=\"" + str(i+1) + "\">",
#       "\t\t\t<prop type=\"word_type\"> " + word_type.text +
#       " </prop>", "\t\t\t<tuv xml:lang=\"en\">",
#       "\t\t\t\t<seg> " + word.a.text + " </seg>",
#       "\t\t\t</tuv>",
#       sep="\n")
# i = i + 1
#                 for translation in translations:
#                     print("\t\t\t<tuv xml:lang=\"" + language+"\">",
#                           "\t\t\t\t<seg> " + translation.a.text + " </seg>",
#                           "\t\t\t</tuv>",
#                           sep="\n")
#                     break

#         print("\t\t</tu>")

# print("\t</body>",
#       "</tmx>",
#       sep="\n")
