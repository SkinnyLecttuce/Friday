import re
import random
import numpy as np
from tensorflow.keras.layers import Input, LSTM, Dense,GRU,RNN
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model

class Seq2Seq():
    def __init__(self):
        self.q = ''
        self.a = ''
        self.training_model = 0
        self.decoder_input = 0
        self.decoder_model = 0
        self.decoder_lstm = 0
        self.reverse_target_features_dict=0
        self.dense_layer = 0
        self.encoder_model =0
        self.max_decoder_seq_length = 0
        self.target_features_dict = 0
        self.num_decoder_tokens = 0
        self.decoder_dense = 0
        self.input_features_dict = 0
        self.num_decoder_tokens = 0
        self.max_encoder_seq_length = 0

    def load_file(self):
        f = open("data/movie_lines.txt","r")
        fr = f.readlines()
        q = []
        a = []
        i = 0
        ii = 0
        for t in fr:
            tt=t.split("+++$+++")
            if(i%2 == 0):
                tt = tt[4].split('\n')
                tt = tt[0].split(' ')
                text = ''
                ttt = []
                for stuff in tt:
                    if(stuff == ''):
                        pass
                    else:
                        text = text+stuff + ' '
                    ii = ii + 1

                q.append(text)
                text = ''

            else:
                tt = tt[4].split('\n')
                tt = tt[0].split(' ')
                text = ''
                ttt = []
                for stuff in tt:
                    if(stuff == ''):
                        pass
                    else:
                        text = text+stuff+' '
                    ii = ii+1


                a.append(text)
                text = ''

            if(i == 3001):
                break
            i = i+1
        f.close()

        f2 = open("data/bot_unk_q.txt","+a")
        print("QA:",q,a)
        for m in q:
            f2.writelines('\n')
            f2.writelines(m)

        f2.close()
        f3 = open("data/bot_unk_a.txt","+a")
        for mm in a:
            f3.writelines('\n')
            f3.writelines(mm)
        f3.close()


    def define_data_path(self,q,a):
        self.q = q
        self.a = a

    def train(self,hist_model):
        data_path = self.q
        data_path2 = self.a
        with open(data_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('\n')
            with open(data_path2, 'r', encoding='utf-8') as f:
                lines2 = f.read().split('\n')
        print(lines,lines2)
        lines = [re.sub(r"\[\w+\]", 'hi', line) for line in lines]
        lines = [" ".join(re.findall(r"\w+", line)) for line in lines]
        lines2 = [re.sub(r"\[\w+\]", '', line) for line in lines2]
        lines2 = [" ".join(re.findall(r"\w+", line)) for line in lines2]


        # grouping lines by response pair
        pairs = list(zip(lines, lines2))
        # random.shuffle(pairs)

        input_docs = []
        target_docs = []
        input_tokens = []
        target_tokens = []
        for line in pairs:
            input_doc, target_doc = line[0], line[1]
            # Appending each input sentence to input_docs
            input_docs.append(input_doc)
            # Splitting words from punctuation
            target_doc = " ".join(re.findall(r"[\w']+|[^\s\w]", target_doc))
            # Redefine target_doc below and append it to target_docs
            target_doc = '<START> ' + target_doc + ' <END>'
            target_docs.append(target_doc)

            print(target_doc)
            # Now we split up each sentence into words and add each unique word to our vocabulary set
            for token in re.findall(r"[\w']+|[^\s\w]", input_doc):
                if token not in input_tokens:
                    input_tokens.append(token)
            for token in target_doc.split():
                if token not in target_tokens:
                    target_tokens.append(token)
                    input_tokens = sorted(list(input_tokens))
        target_tokens = sorted(list(target_tokens))
        num_encoder_tokens = len(input_tokens)
        num_decoder_tokens = len(target_tokens)

        self.num_decoder_tokens = num_decoder_tokens
        self.num_encoder_tokens = num_encoder_tokens

        input_features_dict = dict([(token, i) for i, token in enumerate(input_tokens)])
        target_features_dict = dict([(token, i) for i, token in enumerate(target_tokens)])
        self.target_features_dict = target_features_dict
        self.input_features_dict = input_features_dict
        reverse_input_features_dict = dict((i, token) for token, i in self.input_features_dict.items())
        reverse_target_features_dict = dict((i, token) for token, i in self.target_features_dict.items())
        self.reverse_target_features_dict = reverse_target_features_dict
        max_encoder_seq_length = max([len(re.findall(r"[\w']+|[^\s\w]", input_doc))+15 for input_doc in input_docs])
        max_decoder_seq_length = max([len(re.findall(r"[\w']+|[^\s\w]", target_doc))+15 for target_doc in target_docs])
        self.max_decoder_seq_length = max_decoder_seq_length
        self.max_encoder_seq_length = max_encoder_seq_length
        encoder_input_data = np.zeros((len(input_docs), max_encoder_seq_length, num_encoder_tokens),dtype='float32')
        decoder_input_data = np.zeros((len(input_docs), max_decoder_seq_length, num_decoder_tokens),dtype='float32')
        decoder_target_data = np.zeros((len(input_docs), max_decoder_seq_length, num_decoder_tokens),dtype='float32')
        for line, (input_doc, target_doc) in enumerate(zip(input_docs, target_docs)):
            for timestep, token in enumerate(re.findall(r"[\w']+|[^\s\w]", input_doc)):
                encoder_input_data[line, timestep, self.input_features_dict[token]] = 1.
            for timestep, token in enumerate(target_doc.split()):
                decoder_input_data[line, timestep, target_features_dict[token]] = 1.
                if timestep > 0:
                    decoder_target_data[line, timestep - 1, target_features_dict[token]] = 1.

        dimensionality = 258
        batch_size = 15
        epochs = 1900

        #Encoder
        encoder_inputs = Input(shape=(None, num_encoder_tokens))

        encoder_lstm = LSTM(dimensionality, return_state=True)
        encoder_outputs, state_hidden, state_cell = encoder_lstm(encoder_inputs)
        encoder_states = [state_hidden, state_cell]#Decoder
        decoder_inputs = Input(shape=(None, num_decoder_tokens))
        self.decoder_inputs = decoder_inputs
        decoder_lstm = LSTM(dimensionality, return_sequences=True, return_state=True)
        self.decoder_lstm = decoder_lstm
        decoder_outputs, decoder_state_hidden, decoder_state_cell = decoder_lstm(decoder_inputs, initial_state=encoder_states)
        decoder_dense = Dense(num_decoder_tokens, activation='softmax')
        self.decoder_dense = decoder_dense
        decoder_outputs = decoder_dense(decoder_outputs)
        #from tensorflow.keras.optimizers import Adamax
        #from tensorflow.keras.activations import tanh
        training_model = Model([encoder_inputs, decoder_inputs], decoder_outputs)#Compiling
        training_model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'], sample_weight_mode='temporal')#Training
        training_model.fit([encoder_input_data, decoder_input_data], decoder_target_data, batch_size=batch_size,epochs = epochs)
        training_model.save(hist_model)
        self.training_model = training_model

    def load_model(self,hist_model):
        training_model = load_model(hist_model)
        encoder_inputs = training_model.input[0]
        encoder_outputs, state_h_enc, state_c_enc = training_model.layers[2].output
        encoder_states = [state_h_enc, state_c_enc]
        encoder_model = Model(encoder_inputs, encoder_states)
        self.encoder_model = encoder_model

        latent_dim = 258
        decoder_state_input_hidden = Input(shape=(latent_dim,))
        decoder_state_input_cell = Input(shape=(latent_dim,))
        decoder_states_inputs = [decoder_state_input_hidden, decoder_state_input_cell]

        decoder_outputs, state_hidden, state_cell = self.decoder_lstm(self.decoder_inputs, initial_state=decoder_states_inputs)
        decoder_states = [state_hidden, state_cell]
        decoder_outputs = self.decoder_dense(decoder_outputs)
        decoder_model = Model([self.decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)
        self.decoder_model = decoder_model


    def decode_response(self,test_input):
        # Getting the output states to pass into the decoder
        states_value = self.encoder_model.predict(test_input)
        # Generating empty target sequence of length 1
        target_seq = np.zeros((1, 1, self.num_decoder_tokens))
        # Setting the first token of target sequence with the start token
        target_seq[0, 0, self.target_features_dict['<START>']] = 1.

        # A variable to store our response word by word
        decoded_sentence = ''

        stop_condition = False
        while not stop_condition:
            output_tokens, hidden_state, cell_state =self.decoder_model.predict(
                [target_seq] + states_value)  # Choosing the one with highest probability
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            sampled_token = self.reverse_target_features_dict[sampled_token_index]
            decoded_sentence += " " + sampled_token  # Stop if hit max length or found the stop token
            if (sampled_token == '<END>' or len(decoded_sentence) > self.max_decoder_seq_length):
                stop_condition = True  # Update the target sequence
            target_seq = np.zeros((1, 1, self.num_decoder_tokens))
            target_seq[0, 0, sampled_token_index] = 1.
            # Update states
            states_value = [hidden_state, cell_state]
        return decoded_sentence

    def generate(self, reply):
        reply = self.generate_response(reply) + "\n"
        return reply

    def string_to_matrix(self, user_input):
        tokens = re.findall(r"[\w']+|[^\s\w]", user_input)
        user_input_matrix = np.zeros(
            (1, self.max_encoder_seq_length, self.num_encoder_tokens),
            dtype='float32')
        for timestep, token in enumerate(tokens):
            if token in self.input_features_dict:
                user_input_matrix[0, timestep, self.input_features_dict[token]] = 1.
        return user_input_matrix

    # Method that will create a response using seq2seq model we built
    def generate_response(self, user_input):
        input_matrix = self.string_to_matrix(user_input)
        chatbot_response = self.decode_response(input_matrix)
        # Remove <START> and <END> tokens from chatbot_response
        chatbot_response = chatbot_response.replace("<START>", '')
        chatbot_response = chatbot_response.replace("<END>", '')
        return chatbot_response  # Method to check for exit commands

'''
t = ''
chatbot = Seq2Seq()
#chatbot.load_file()

chatbot.define_data_path("data/bot_test_punk_q.txt","data/bot_test_punk_a.txt")

chatbot.train('model_history/responsepunk_model.h5')

while True:
    chatbot.load_model('model_history/responsepunk_model.h5')
    i = input("Chat:")
    #i = i.split(' ')
    #i = m.lemma(i)
    #i = m.stop(i)

    #text = ''
    #for t in i:
    #   text = text+t+' '

    text = i

    r=chatbot.generate(text)
    for rr in r.split(" "):
        t = t+rr+' '
    print("Reply:",t.upper())
    t = ''
'''
#fridays all codes