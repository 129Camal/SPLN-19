from bs4 import BeautifulSoup as BS
import requests
import sys


urlBase = "https://www.lexico.com/en/definition/"

response = requests.get(urlBase).content

soup = BS(response, 'html.parser')

word_types = soup.findAll('section', 'gramb')

for word_type in word_types:
    instance = word_type.find('h3', 'ps pos')
    print(instance.span.text)

    ul = word_type.find('ul', 'semb')
    lis = ul.findAll('li')
    
    allmeaning = []
    for li in lis:
        div = li.find('div', 'trg')
        
        if(div):
            p = div.find('p')
            if(p):
                span = p.find('span', 'ind')
                print("-> " + span.text)
                allmeaning.append(span.text)

    print(" ;".join(allmeaning))
        