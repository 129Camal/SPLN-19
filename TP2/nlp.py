#!/usr/local/bin/python3.7
import nltk
from owlready2 import *

# Pacotes do nltk para fazer download

#nltk.download('stopwords')
#nltk.download('words')
#nltk.download('maxent_ne_chunker')
#nltk.download('averaged_perceptron_tagger')

# Abrir ontologia
ontology = get_ontology("http://spln.di.uminho.pt/ontology")

# Especificar Classes, ObjectProperties e DataProperties
with ontology:
    class Company(Thing):
        pass
    class Product(Thing):
        pass
    class Location(Thing):
        pass

    class is_product_of(ObjectProperty):
        domain = [Product]
        range  = [Company]
    
    class is_location_of(ObjectProperty):
        domain = [Location]
        range  = [Company]
    
    class has_product(ObjectProperty):
        domain = [Company]
        range  = [Product]
        inverse_property = is_product_of

    class has_location(ObjectProperty):
        domain = [Company]
        range  = [Location]
        inverse_property = is_location_of

    class has_cost(DataProperty, FunctionalProperty):
        domain = [Product]
        range  = [float]

# Abrir ficheiro com o texto
text = open("text.txt").read()

products = []
prices = []
my_company = ""
indexProduct = 1

# Função que associa produtos e preços a uma determinada empresa na ontologia
def addProducts():
    global indexProduct
    j = 0
    
    for product in products:
        aux = []
        for i in range(len(product)-1):
            aux.append(product[i][0])
        aux.append(str(indexProduct))
        x = "_".join(aux)

        obj = Product(x)
        obj.has_cost = float(prices[j][1][0])
        my_company.has_product.append(obj)
        indexProduct += 1
        j += 1
    
    del products[:]
    del prices[:]


# Divisão por frases
sentences = nltk.sent_tokenize(text)

#Percorrer cada frase procurando entidades ou fazendo chunks para descobrir determinadas coisas como produtos ou preços. 
for sentence in sentences:

    # Divisão por palavras
    words = nltk.word_tokenize(sentence)

    # Tags de discurso
    tags = nltk.pos_tag(words)
    
    
    #Chunks
    #Company: {<NNP>+<NN>?}
    chunkGram = r"""Product: {<NN.*>+<IN>}
                             {<NN.*>+<V.*>}
                    Price: {<\$><CD>}"""
    chunkParser = nltk.RegexpParser(chunkGram)
    tree = chunkParser.parse(tags)

    #Entidades
    namedEnt = nltk.ne_chunk(tags)
    
    for t in namedEnt.subtrees():
        #Encontrar localizações
        if t.label() == "GPE":
            location = t.leaves()
            for i in range(len(location)):
                location[i] = location[i][0]
            local = "_".join(location)

            my_company.has_location.append(Location(local))        
                
        #Encontrar empresas
        if t.label() == "ORGANIZATION" or t.label() == "PERSON":
            company = (t.leaves())[0][0]
            if(not ontology.company):
                if(len(products)):
                    addProducts()
                my_company = Company(company)

    # Tratamento de dados sobre os chunks encontrados de preços e produtos            
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

# Inserir na ontologia os produtos e preços da ultima empresa encontrada
addProducts()

# Guardar a ontologia 
ontology.save(file = "onto.rdf", format = "rdfxml")

# print("Company: " + company)
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