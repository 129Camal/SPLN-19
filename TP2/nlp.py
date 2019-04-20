#!/usr/local/bin/python3.7
import nltk
from nltk.corpus import stopwords

#nltk.download('stopwords')
#nltk.download('words')
#nltk.download('maxent_ne_chunker')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

text = open("text.txt").read()
stop = set(stopwords.words('english'))
sentences = nltk.sent_tokenize(text)

products = []
prices = []
locations = []

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
j = 0
for product in products:
    for i in range(len(product)):
        if(i != (len(product)-1)):
            products[j] = (product[i][0], prices[j][1][0])
            j += 1

j = 0
for location in locations:
    for i in range(len(location)):
        location[i] = location[i][0]
    locations[j] = " ".join(location)
    j += 1
    

print("Products: " + str(products))
print("Locations: " + str(locations))
print("Company: " + str(company))
