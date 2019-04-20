#!/usr/local/bin/python3.7

import nltk
#nltk.download('words')
#nltk.download('maxent_ne_chunker')
# nltk.download('mac_morpho')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

from nltk.corpus import state_union
import sys

f = open('out.txt', 'w')
sys.stdout = f
text = open('../harry_phoenix.en.txt').read()

sentences = nltk.sent_tokenize(text)

def process_content():
    try:
        for i in sentences:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            
            namedEnt = nltk.ne_chunk(tagged, binary=True)
            namedEnt.draw()
            # chunkGram = r"""Names: {<NNP>+}"""
   
            # chunkParser = nltk.RegexpParser(chunkGram)
            # chunked = chunkParser.parse(tagged)

            # print(chunked)
            # chunked.draw()
    except Exception as e:
        print(str(e))

process_content()