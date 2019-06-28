#imports
from bs4 import BeautifulSoup as BS
import requests
import subprocess
from build_utils import build_profile

# 
def getHTML(word):
  #
  urlBase = "https://dicionario.priberam.org/"
  #
  composedURL = urlBase + word

  #response = requests.get(composedURL).content
  response = subprocess.check_output(['curl',composedURL])
  #
  soup = BS(response)
  return soup

#
def getFromSoup(soup):
  # find elements using CSS selector
  #resultados = soup.select('#resultados .def')
  #
  resultados = soup.find('div',id='resultados')
  #
  data = resultados.find_all('span','def')
  #
  return data


#
def elem_extr_func(original_word,data,result_objts):
  #
  resultObjects = result_objts
  #
  defs = resultObjects['significados']
  #
  defs[original_word] = [word.text for word in data]
  #
  result_objts = resultObjects




#
def build_priberam_profile(words):
  #
  obj = {'significados':{}}
  #
  priberam_profile = build_profile(words,getHTML,getFromSoup,obj,elem_extr_func)
  #
  return priberam_profile

#
words = ['banana','Ezequiel','João','balão']
priberam_profile = build_priberam_profile(words)
