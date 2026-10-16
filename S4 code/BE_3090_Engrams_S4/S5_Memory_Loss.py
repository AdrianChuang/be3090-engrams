import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
import re

from scipy.signal import find_peaks
from operator import itemgetter
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "S1 code"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "S2 code"))

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "S3 code")) 
from BE_3090_Engrams_S3_Part2 import character_to_matrix_map    
from BE_3090_Engrams_S1_part4 import vectorsim
#this variable is dictionary containing all char, encoding pairs
matrix_map = {}
#this variable stores the text sequence that we will be using in this part of the lab
characterseq1 = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec."
characterseq2 = "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids"
characterseq3 = "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary re"
characterseq4 = "A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring which I enjoy with my whole heart. I am alone, and feel the charm of existence in this spot, which was created for the bliss of souls like mine. I am so happy, my dear friend, so absorbed in the exquisit"
characterseq5 = "CJ Stroud is a certified bum. Bro had one good rookie season and has been coasting ever since. His pocket presence vanishes under pressure, his decision-making is questionable, and he folds when the Texans need him most. At this point, calling him a franchise quarterback is just disrespectful to actual franchise quarterbacks. He's washed."

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

def memory_pct(characterseq, dict):
    encodingseq = get_encoding_from_seq(characterseq, dict)
    decoded_seq = ""

    for i in range(len(characterseq)):
        char_matrix = encodingseq[i]
        best_char, _ = determine_best_char(char_matrix, dict)
        decoded_seq += best_char

    return recall_pct(characterseq, decoded_seq)


    








