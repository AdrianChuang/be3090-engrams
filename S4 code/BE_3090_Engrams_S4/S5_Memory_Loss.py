import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
import re

from scipy.signal import find_peaks
from operator import itemgetter
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "S1 code"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "S2 code"))
from BE_3090_Engrams_S1_part4 import vectorsim
#this variable is dictionary containing all char, encoding pairs
matrix_map = {}
#this variable stores the text sequence that we will be using in this part of the lab
characterseq1 = ""
characterseq2 = ""
characterseq3 = ""
characterseq4 = ""
characterseq5 = ""

##dict is the dictionary containing character, encoding pairs
def get_encoding_from_seq(sequence, dict):
    encodingseq = []
    for i in range(len(sequence)):
        if i==0:
            encodingseq = dict[sequence[i]]
        else:
            encodingseq = np.stack(encodingseq, dict[sequence[i]])

    return encodingseq

#alters encoding depending on the neuron forgotten, forgotten_n. Encoding is a 2d array
def forget_neuron(encoding, forgotten_n):
    encoding = np.array(encoding)
    encoding[:, forgotten_n] = 0
    return encoding
#we know each sequence is between 50 to 250 ms long, so can only check first 50ms.
def determine_best_char(matrix, decoder):
    matrix = np.array(matrix)
    max_sim = -1
    opt_char = ''
    for key,value in decoder.items():
        if(matrix.shape[1] >= value.shape[1]):
            similarity = vectorsim(matrix[:value.shape[1]],value)
        if(similarity > max_sim):
            max_sim = similarity
            opt_char = key
    return (opt_char,max_sim)

#takes in a character sequence and the character encoding, measure accuracy of decode based on the key
#recall pct takes in decoded sequence, original sequence and returns recall %
def recall_pct(characterseq1, characterseq2):
    sequence_1_words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", characterseq1)
    sequence_2_words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", characterseq2)
    recalled_words = sum(s1word == s2word
        for s1word, s2word in zip(sequence_1_words, sequence_2_words))
    return(recalled_words/len(sequence_2_words))
def memory_pct(characterseq, character_encoding, key):
    decoded_seq = ""


    








