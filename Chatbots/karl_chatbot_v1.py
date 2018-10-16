# -*- coding: utf-8 -*-
"""
Created on Sun Aug  5 23:55:43 2018

Karl V1 - Uses a LSTM-style RNN trained on The Communist Manifesto, and 
The Romance of Lust

Generates a sort of text predicting chatbot-esque neural network using 
Alice in Wonderland and other books as training data.

This script requires all training data (texts) to be in one folder. The
script iterates through the folder and reads all texts.

The training text used here and many other books can be found on:
    www.gutenberg.com
    
Most of this code is copied/modified from the book Deep Learning With Keras.

@author: Administrator
"""

from __future__ import print_function
import os
from keras.layers import Dense, Activation
#from keras.layers.recurrent import SimpleRNN
from keras.layers.recurrent import LSTM
from keras.models import Sequential
#from keras.utils.visualize_util import plot
import numpy as np

# Setting directory to read in text files
textDirectory = "C:/Users/Administrator/Dropbox/Python/deep_learning/book_texts/subset_books"
dirList = os.listdir(textDirectory)

# Opening text and formatting it in "text" variable
text = str()
for filename in dirList:
    fin = open(textDirectory + '/' + filename, 'rb')
    lines = []
    for line in fin:
        line = line.strip().lower()
        line = line.decode("ascii", "ignore")
        if len(line) == 0:
            continue
        lines.append(line)
    fin.close()
    oneBookText = " ".join(lines)
    text = text + oneBookText

# Creating lookup tables for the 42 unique characters that appear in the text
chars = set([c for c in text])
nb_chars = len(chars)
char2index = dict((c, i) for i, c in enumerate(chars))
index2char = dict((i, c) for i, c in enumerate(chars))

# Creating input and label texts
SEQLEN = 40 # Important hyperparameter??
STEP = 1
input_chars = []
label_chars = []
for i in range(0, len(text) - SEQLEN, STEP):
    input_chars.append(text[i:i + SEQLEN])
    label_chars.append(text[i + SEQLEN])
    
# Vectorizing input and label texts. This has to do with one-hot enconding;
    # I don't really understand this yet
X = np.zeros((len(input_chars), SEQLEN, nb_chars), dtype=np.bool)
y = np.zeros((len(input_chars), nb_chars), dtype=np.bool)
for i, input_char in enumerate(input_chars):
    for j, ch in enumerate(input_char):
        X[i, j, char2index[ch]] = 1
    y[i, char2index[label_chars[i]]] = 1
    
# Creating and compiling model

HIDDEN_SIZE = 128*4 # This is an important hyperparameter
BATCH_SIZE = HIDDEN_SIZE
NUM_ITERATIONS = 20
NUM_EPOCHS_PER_ITERATION = 2
NUM_PREDS_PER_EPOCH = 300
model = Sequential()
model.add(LSTM(HIDDEN_SIZE, return_sequences=False, # Return sequence is 
                    # false if we are building around using characters instead of words
                    input_shape=(SEQLEN, nb_chars),
                    unroll=True)) # Improves performance on TensorFlow backend
model.add(Dense(nb_chars))
model.add(Activation("softmax"))

model.compile(loss="categorical_crossentropy", optimizer="rmsprop")


# Training model

for iteration in range(NUM_ITERATIONS):
    print("=" * 50)
    print("Iteration #: %d" % (iteration))
    model.fit(X, y, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS_PER_ITERATION)
    test_idx = np.random.randint(len(input_chars))
    test_chars = input_chars[test_idx]
    print("Generating from seed: %s\n" % (test_chars))
    print(test_chars, end="")
    for i in range(NUM_PREDS_PER_EPOCH):
        Xtest = np.zeros((1, SEQLEN, nb_chars))
        for i, ch in enumerate(test_chars):
            Xtest[0, i, char2index[ch]] = 1
        pred = model.predict(Xtest, verbose=0)[0]
        ypred = index2char[np.argmax(pred)]
        print(ypred, end="")
        # move forward with test_chars + ypred
        test_chars = test_chars[1:] + ypred
print()

#%% Give the bot an input, see how it finishes it


def ask():
    rawInput = input('Say something at least '+ str(SEQLEN) + ' characters long: ')
    
    # Format input the same way as up top
    textInput = rawInput.strip().lower()
    
    # Strip the input down to the correct size for the model
    finalInput = textInput[0:SEQLEN]
    
    input_chars = finalInput
    
    # Copying code from up top
    test_chars = input_chars
    print("Generating from seed: %s\n" % (test_chars))
    print(test_chars, end="")
    for i in range(NUM_PREDS_PER_EPOCH): # Could change this to change length of output
        Xtest = np.zeros((1, SEQLEN, nb_chars))
        for i, ch in enumerate(test_chars):
            Xtest[0, i, char2index[ch]] = 1
        pred = model.predict(Xtest, verbose=0)[0]
        ypred = index2char[np.argmax(pred)]
        print(ypred, end="")
        # move forward with test_chars + ypred
        test_chars = test_chars[1:] + ypred
