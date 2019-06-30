from bs4 import BeautifulSoup as BS
import requests
import sys


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
                # Get Meaning
                p = div.find('p')
                if(p):
                    span = p.find('span', 'ind')
                    allmeaning.append(span.text)

                    # Get Synonyms
                    sysn = div.find('div', 'synonyms')
                    if(sysn):
                        strong = sysn.find('strong', 'syn')
                        exg = sysn.find('span', 'syn')
                        allsyn.append(strong.text + exg.text)
                    else:
                        allsyn.append("Doesn`t have synonyms")


        if(len(allmeaning) > 0):
            x = " || ".join(allmeaning)
            print("Meaning -> " + x)
        
        if(len(allsyn) > 0):
            x = " || ".join(allsyn)
            print("Sys -> " + x)

getMeaning('cold', 'noun')
        