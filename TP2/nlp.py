#!/usr/local/bin/python3.7
import nltk
from owlready2 import *

#nltk.download('stopwords')
#nltk.download('words')
#nltk.download('maxent_ne_chunker')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

text = open("text.txt").read()

sentences = nltk.sent_tokenize(text)

products = []
prices = []
locations = []
j = 0 
h = 0

for sentence in sentences:
    words = nltk.word_tokenize(sentence)

    tags = nltk.pos_tag(words)
    
    #Company: {<NNP>+<NN>?}
    chunkGram = r"""Product: {<NN.*>+<IN>}
                             {<NN.*>+<V.*>}
                    Price: {<\$><CD>}"""
    chunkParser = nltk.RegexpParser(chunkGram)
    tree = chunkParser.parse(tags)

    namedEnt = nltk.ne_chunk(tags)
    for t in namedEnt.subtrees():
        if t.label() == "GPE":
            locations.append(t.leaves())
        if t.label() == "ORGANIZATION":
            company = (t.leaves())[0][0]

    flag = 0
    for subtree in tree.subtrees():
        if subtree.label() == "Price": 
            price = subtree.leaves()
            flag = 1

        if subtree.label() == "Product": 
            product = subtree.leaves()
        
        if flag == 1:
            products.append(product)
            prices.append(price)
            flag = 0

for product in products:
    for i in range(len(product)):
        if(i != (len(product)-1)):
            products[j] = (product[i][0], prices[j][1][0])
            j += 1

for location in locations:
    for i in range(len(location)):
        location[i] = location[i][0]
    locations[h] = "_".join(location)
    h += 1

# OwlReady2 

ontology = get_ontology("http://spln.di.uminho.pt/ontology")

with ontology:
    class Company(Thing):
        pass
    class Product(Thing):
        pass
    class Location(Thing):
        pass
    class has_product(ObjectProperty):
        domain = [Company]
        range  = [Product]
    class has_location(ObjectProperty):
        domain = [Company]
        range  = [Location]
    class has_cost(DataProperty, FunctionalProperty):
        domain = [Product]
        range  = [float]

my_company = Company(company)

for location in locations:
    my_company.has_location.append(Location(location))

for product in products:
    produto = Product(product[0])
    produto.has_cost = float(product[1])

    my_company.has_product.append(produto)

ontology.save(file = "walmart.rdf", format = "rdfxml")

# print("Products: " + str(products))
# print("Locations: " + str(locations))
# print("Company: " + str(company) + "\n\n\n")
# print("\nEmpresa: " + str(Company.instances()))
# print("Produtos: " + str(Product.instances()))
# for i in Product.instances():
#     print("Custo do produto " + str(i) +": " + str(i.has_cost))
# print("Locais: " + str(Location.instances()))
# print("Localizações da Empresa: " + str(list(ontology.has_location.get_relations())))
# print("Produtos da Empresa: " + str(list(ontology.has_product.get_relations())))