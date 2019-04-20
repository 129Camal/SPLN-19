#!/usr/local/bin/python3.7
import nltk
from nltk.corpus import stopwords

#nltk.download('stopwords')

text = open("text.txt").read()
stop = set(stopwords.words('english'))
sentences = nltk.sent_tokenize(text)

for sentence in sentences:
    #filteredWords = []

    words = nltk.word_tokenize(sentence)
    # for w in words:
    #     if w not in stop:
    #         filteredWords.append(w)

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
            print("Location: "+str(t.leaves()))
        if t.label() == "ORGANIZATION":
            print("Company: "+str(t.leaves()))
            
    #print(list(tree.subtrees()))

    flag = 0
    product = ""
    price = ""
    for subtree in tree.subtrees():
        if subtree.label() == "Price": 
            #print("Price: "+str(subtree.leaves()))
            price = str(subtree.leaves())
            flag = 1
        if subtree.label() == "Product": 
            #print("Product: "+str(subtree.leaves()))
            product = str(subtree.leaves())
        if flag == 1:
            print("Product: " + product +"\nPrice: " + price)
            flag = 0