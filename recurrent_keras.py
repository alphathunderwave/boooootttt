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
from keras.models import load_model


def recurrent(mode='train', MODEL = '',WEIGHTS = ''):

    DATA_DIR = 'database.txt'
    BATCH_SIZE = 50
    LAYER_NUM = 2
    SEQ_LENGTH = 50
    HIDDEN_DIM = 500
    GENERATE_LENGTH = 140


    epochs = 180


    # Creating training data
    X, y, VOCAB_SIZE, ix_to_char = load_data(DATA_DIR, SEQ_LENGTH)

    if not MODEL == '':
        print('load model')
        model = load_model(MODEL)
    else:
        print('new model')
        model = Sequential()
        # Creating and compiling the Network
        model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
        for i in range(LAYER_NUM - 1):
            model.add(LSTM(HIDDEN_DIM, return_sequences=True))
        model.add(TimeDistributed(Dense(VOCAB_SIZE)))
        model.add(Activation('softmax'))
        model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

    # Generate some sample before training to know how bad it is!
    generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)


    # Training if there is no trained weights specified
    if mode == 'train' or WEIGHTS == '':
        for i in range(epochs):
            print('\n\nEpoch: {}\n'.format(i))
            model.fit(X, y, batch_size=BATCH_SIZE, verbose=1, epochs=1)
            epochs += 1
            generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
        model.save('./saved/model.hdf5')
        model.save_weights('./saved/weights.hdf5')

    # Else, loading the trained weights and performing generation only
    elif not WEIGHTS == '':
        # Loading the trained weights
        model.load_weights(WEIGHTS)
        generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
        print('\n\n')
    else:
        print('\n\nNothing to do!')

    return True

recurrent(mode = 'train', MODEL = './saved/model.hdf5')
