#!/usr/local/bin/python3.7

from owlready2 import *

#onto = get_ontology("http://spln.di.uminho.pt/2019")

onto = get_ontology("http://www.lesfleursdunormal.fr/static/_downloads/pizza_onto.owl").load()

print(list(onto.classes()))