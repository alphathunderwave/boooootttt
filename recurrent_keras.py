from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM, SimpleRNN
from keras.layers.wrappers import TimeDistributed
import argparse
from RNN_utils import *

def recurrent(DATA_DIR, BATCH_SIZE = 50, LAYER_NUM = 2, SEQ_LENGTH = 50, HIDDEN_DIM = 500, GENERATE_LENGTH = 140, epochs = 20, mode = 'train', WEIGHTS = ''):
    # Creating training data
    X, y, VOCAB_SIZE, ix_to_char = load_data(DATA_DIR, SEQ_LENGTH)

    # Creating and compiling the Network
    model = Sequential()
    model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
    for i in range(LAYER_NUM - 1):
        model.add(LSTM(HIDDEN_DIM, return_sequences=True))
    model.add(TimeDistributed(Dense(VOCAB_SIZE)))
    model.add(Activation('softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

    # Generate some sample before training to know how bad it is!
    generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)

    if not WEIGHTS == '':
        print('\n load weights')
        model.load_weights(WEIGHTS)

    # Training if there is no trained weights specified
    if mode == 'train' or WEIGHTS == '':
        for i in range(epochs):
            print('\n\nEpoch: {}\n'.format(i))
            model.fit(X, y, batch_size=BATCH_SIZE, verbose=1, epochs=1)
            epochs += 1
            generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
        model.save_weights('./saved/model.hdf5')

    # Else, loading the trained weights and performing generation only
    elif WEIGHTS == '':
        # Loading the trained weights
        model.load_weights(WEIGHTS)
        generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
        print('\n\n')
    else:
        print('\n\nNothing to do!')

    return True
