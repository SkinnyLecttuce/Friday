import os
import bert
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from official import nlp
from official.nlp import bert
import official.nlp.bert.tokenization
import spacy

class NLP():
    def __init__(self):
        self.bert_voc = 'uncased_L-12_H-768_A-12'
        self.tokenizer = bert.tokenization.FullTokenizer(vocab_file=os.path.join(self.bert_voc, 'vocab.txt'),
                                                         do_lower_case=True)

    def sentence_split(self,query):
        breaks = ['and','but',',','then','because','then']

        clear = []

        for b in breaks:
            try:
                if(b in query):
                    qs = query.split(b)
                    clear.append(qs)
            except:
                pass
        print("CLEAR:",clear)
        return clear

    def tokens(self,text):
        tokens = self.tokenizer.tokenize(text)
        return tokens

    def lemma(self,tok):
        l = []
        lems = ''
        for t in tok:
            lems = lems+t+' '

        nlp = spacy.load("en_core_web_sm")
        docs = nlp(lems)
        for d in docs:
            l.append(d.lemma_)
        i = 0
        ll = []
        for ls in l:
            if(ls == '-PRON-'):
                ll.append(tok[i])
            else:
                ll.append(ls)
            i = i+1

        return ll

    def Normalize_entities(self,POS,label_arr):
        nlp = spacy.load('en_core_web_sm')
        sents = nlp("Zeus and Tony Stark are scientists")
        i=[ee for ee in sents.ents if ee.label_ == 'PERSON']
        print(i)

    def stop(self,lemms):
        w = set(['in','a','an','the','that','this','those','he','she','it','they','we','ours','could','should','also','and','or','you','!','.',':','them','so','need','at','to'])
        s = [ww for ww in lemms if not ww in w]
        return s

'''
a = NLP()
t = a.tokens("This is a sample text")
l = a.lemma(t)
s = a.stop(l)
print(s)
print(a.Normalize_entities(['ACT','NNP','NNP','NNP','NNP'],['buy','vito','pizza','lola','tots']))
'''
