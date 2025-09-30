import tensorflow_datasets as tfds
tfds.disable_progress_bar()
import tensorflow as tf
import numpy as np
import ai_nlp as nlps

from keras.preprocessing.sequence import pad_sequences
import tensorflow_hub as hub

import os
from official.nlp import bert

from tensorflow.keras.models import load_model
import official.nlp.bert.tokenization


from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, Flatten, Dense, Embedding, LSTM, Dropout, Bidirectional,GlobalAveragePooling1D

class Recognizer():
    def __init__(self):
        self.bert_voc = 'uncased_L-12_H-768_A-12'
        self.tokenizer = bert.tokenization.FullTokenizer(vocab_file=os.path.join(self.bert_voc, 'vocab.txt'), do_lower_case=True)

    def encode_sentence(self,s):
        tokens = list(self.tokenizer.tokenize(s))
        tokens = tokens
        token_ids = self.tokenizer.convert_tokens_to_ids(tokens)
        return self.tokenizer.convert_tokens_to_ids(tokens)

    def create_x_y(self,file):
        idz = []
        f = open(file, "r").readlines()
        import numpy as np
        intents = []
        strings = []
        f = open(file, "r").readlines()
        for fs in f:
            text = fs.split('+++$+++')
            fs = text[0]
            tok = nlps.NLP().tokens(fs)
            lems = nlps.NLP().lemma(tok)
            #stops = nlps.NLP().stop(lems)
            strings.append(lems)
            fs = text[-1]
            for tt in fs:
                try:
                    intents.append(int(tt))
                except:
                    pass


        for sent in strings:
            ids = self.tokenizer.convert_tokens_to_ids(sent)
            idz.append(ids)

        return [idz,intents]

    def pad(self, x):
        padded_sentences = []
        xx = 20 - len(x)
        for xs in x:
            padded_sentences.append(xs)

        for xs in range(0, xx):
            padded_sentences.append(0)

        return padded_sentences

    def Model_exec(self,file,file2):
        x_y = self.create_x_y(file)
        x = x_y[0]
        y = x_y[1]
        padded_x = []
        for xs in x:
            padded_x.append(self.pad(xs))

        print(y,padded_x)
        intent_model = self.Model(padded_x,y,file2)

        return [intent_model]

    def Model(self,x,y,file):
        x = np.array(x)
        y = np.array(y)

        print("XY:",len(x),len(y))
        print(x)
        print(y)
        y_key = set(y)
        num_cat = len(y_key)

        # print("X:",x,x.shape)
        # print("Y:",y,y.shape)
        # print("INP:",inp,inp.shape)

        e = 160 - (15 * (num_cat + 1))
        e = 200
        #print("EPOCHS:", e, num_cat)

        over_fitting = ((num_cat + 1) / 10) / 2
        #print("DIM:", x.ndim, y.ndim)

        model = Sequential()

        model.add(Embedding(30523, (num_cat+1), input_length=20))
        # model.add(LSTM(256, dropout=over_fitting, recurrent_dropout=over_fitting))
        model.add(Conv1D(256, (num_cat+1), activation='relu'))
        model.add(GlobalAveragePooling1D())
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(over_fitting))
        model.add(Dense((num_cat+1), activation='softmax'))
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        model.fit(x, y, epochs=e)
        model.save(file)

        model = load_model(file)
        print("Model:", model)
        return model

    def Intent_to_str(self,intent,intent_data_type):
        tasks_or_social = {1:'Social',2:'Task'}
        tasks = {1:'Book_Flight',2:'Rate_Book',3:'Play_Music',4:'Book_Hotel',5:'Launch_App',6:'What_If'}
        social = {1:'About_You',2:'Romantic'}
        if(intent_data_type == 'Task'):
            print('Tasking')
            return tasks[intent]

        elif(intent_data_type == 'Social'):
            print('Socialing')
            return social[intent]

        if(intent_data_type == 'Task_Social'):
            return tasks_or_social[intent]

    def Predict(self,model,test_x):
        i = 0
        ii = 0
        ppp = []
        intents = []

        text_tok = test_x.split(" ")
        text_lemma = nlps.NLP().lemma(text_tok)
        text_stop = nlps.NLP().stop(text_lemma)

        text = ''
        for tok in text_stop:
            text = text+tok+' '

        print('Filtered :',text)
        test_x_encoded = self.encode_sentence(text)
        test_x_padded = np.array([self.pad(test_x_encoded)])

        print(test_x_padded)

        pp = model.predict(test_x_padded)

        print("REAL:", pp, max(pp[0]))

        ppp = []
        i = 0

        pp = pp[0]
        ppp=np.array(pp)
        print("np_array_ppp:",ppp)
        v_argmax = np.argmax(ppp)
        intent = ''
        print("arg:", v_argmax)
        intent = v_argmax

        return intent
'''
a = Recognizer()
x_y = a.Model_exec('data/bot_social.txt','model_history/intent_detect2.h5')
while(True):
    inp = input(':')
    p = a.Predict(x_y[0],inp)
    arg = a.Intent_to_str(p,'Social')
    print(arg)
'''
