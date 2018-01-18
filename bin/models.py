#!/usr/bin/env python
"""
coding=utf-8

Code Template

"""
import keras
import numpy
from keras import Model
from keras.layers import Embedding, Dense, LSTM, Conv1D, MaxPooling1D, Flatten, Bidirectional
from keras.optimizers import Adam, RMSprop

import lib


def cnn_embedding(X, y):

    # Create Input layer
    # Input: Input length
    if len(X.shape) >= 2:
        model_input_length = int(X.shape[1])
    else:
        model_input_length = 1

    # Create Embedding layer
    # Embedding: Embedding input dimensionality is the same as the number of classes in the input data set
    embedding_input_dim = max(len(lib.legal_characters()), numpy.max(X)) + 1

    # Embedding: Embedding output dimensionality is determined by heuristic
    embedding_output_dim = int(min((embedding_input_dim + 1) / 2, 50))

    # Input: Use a smaller datatype, if possible. This explicit typing is necessary due to the OHE layer.
    if embedding_input_dim < 250:
        dtype = 'uint8'
    else:
        dtype = 'int32'

    # Create output layer
    # Output: Output shape
    if len(y.shape) >= 2:
        softmax_output_dim = y.shape[1]
    else:
        softmax_output_dim = 1

    sequence_input = keras.Input(shape=(model_input_length,), dtype=dtype, name='char_input')

    embedding_layer = Embedding(input_dim=embedding_input_dim,
                                output_dim=embedding_output_dim,
                                input_length=model_input_length,
                                trainable=True,
                                name='char_embedding')

    output_layer = Dense(units=softmax_output_dim, activation='sigmoid')

    x = sequence_input
    x = embedding_layer(x)
    x = Conv1D(32, 10, activation='relu')(x)
    x = Conv1D(32, 10, activation='relu')(x)
    x = MaxPooling1D(3)(x)
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)
    x = output_layer(x)

    optimizer = Adam()
    bool_model = Model(sequence_input, x)
    bool_model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])

    return bool_model

def lstm_embedding(X, y):
    # Create Input layer
    # Input: Input length
    if len(X.shape) >= 2:
        model_input_length = int(X.shape[1])
    else:
        model_input_length = 1

    # Create Embedding layer
    # Embedding: Embedding input dimensionality is the same as the number of classes in the input data set
    embedding_input_dim = max(len(lib.legal_characters()), numpy.max(X)) + 1

    # Embedding: Embedding output dimensionality is determined by heuristic
    embedding_output_dim = int(min((embedding_input_dim + 1) / 2, 50))

    # Input: Use a smaller datatype, if possible. This explicit typing is necessary due to the OHE layer.
    if embedding_input_dim < 250:
        dtype = 'uint8'
    else:
        dtype = 'int32'

    # Create output layer
    # Output: Output shape
    if len(y.shape) >= 2:
        softmax_output_dim = y.shape[1]
    else:
        softmax_output_dim = 1

    sequence_input = keras.Input(shape=(model_input_length,), dtype=dtype, name='sigmoid')

    embedding_layer = Embedding(input_dim=embedding_input_dim,
                                output_dim=embedding_output_dim,
                                input_length=model_input_length,
                                trainable=True,
                                name='char_embedding')

    output_layer = Dense(units=softmax_output_dim, activation='sigmoid')

    x = sequence_input
    x = embedding_layer(x)
    x = LSTM(256)(x)
    x = output_layer(x)

    optimizer = RMSprop(lr=.001)
    bool_model = Model(sequence_input, x)
    bool_model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])

    return bool_model

def bi_lstm_embedding(X, y):
    # Create Input layer
    # Input: Input length
    if len(X.shape) >= 2:
        model_input_length = int(X.shape[1])
    else:
        model_input_length = 1

    # Create Embedding layer
    # Embedding: Embedding input dimensionality is the same as the number of classes in the input data set
    embedding_input_dim = max(len(lib.legal_characters()), numpy.max(X)) + 1

    # Embedding: Embedding output dimensionality is determined by heuristic
    embedding_output_dim = int(min((embedding_input_dim + 1) / 2, 50))

    # Input: Use a smaller datatype, if possible. This explicit typing is necessary due to the OHE layer.
    if embedding_input_dim < 250:
        dtype = 'uint8'
    else:
        dtype = 'int32'

    # Create output layer
    # Output: Output shape
    if len(y.shape) >= 2:
        softmax_output_dim = y.shape[1]
    else:
        softmax_output_dim = 1

    sequence_input = keras.Input(shape=(model_input_length,), dtype=dtype, name='sigmoid')

    embedding_layer = Embedding(input_dim=embedding_input_dim,
                                output_dim=embedding_output_dim,
                                input_length=model_input_length,
                                trainable=True,
                                name='char_embedding')

    output_layer = Dense(units=softmax_output_dim, activation='sigmoid')

    x = sequence_input
    x = embedding_layer(x)
    x = Bidirectional(LSTM(128))(x)
    x = output_layer(x)

    optimizer = RMSprop(lr=.001)
    bool_model = Model(sequence_input, x)
    bool_model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])

    return bool_model

def cnn_lstm_embedding(X, y):
    # Create Input layer
    # Input: Input length
    if len(X.shape) >= 2:
        model_input_length = int(X.shape[1])
    else:
        model_input_length = 1

    # Create Embedding layer
    # Embedding: Embedding input dimensionality is the same as the number of classes in the input data set
    embedding_input_dim = max(len(lib.legal_characters()), numpy.max(X)) + 1

    # Embedding: Embedding output dimensionality is determined by heuristic
    embedding_output_dim = int(min((embedding_input_dim + 1) / 2, 50))

    # Input: Use a smaller datatype, if possible. This explicit typing is necessary due to the OHE layer.
    if embedding_input_dim < 250:
        dtype = 'uint8'
    else:
        dtype = 'int32'

    # Create output layer
    # Output: Output shape
    if len(y.shape) >= 2:
        softmax_output_dim = y.shape[1]
    else:
        softmax_output_dim = 1

    sequence_input = keras.Input(shape=(model_input_length,), dtype=dtype, name='char_input')

    embedding_layer = Embedding(input_dim=embedding_input_dim,
                                output_dim=embedding_output_dim,
                                input_length=model_input_length,
                                trainable=True,
                                name='char_embedding')

    output_layer = Dense(units=softmax_output_dim, activation='sigmoid')

    x = sequence_input
    x = embedding_layer(x)
    x = Conv1D(32, 10, padding='valid', activation='relu')(x)
    x = Conv1D(32, 10, padding='valid', activation='relu')(x)
    x = MaxPooling1D(3)(x)
    x = LSTM(256)(x)
    x = output_layer(x)

    optimizer = RMSprop(lr=.001)
    bool_model = Model(sequence_input, x)
    bool_model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['acc'])

    return bool_model