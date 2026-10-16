from pathlib import Path
import sys

import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
import re

from scipy.signal import find_peaks
from operator import itemgetter


# S5_Memory_Loss.py is located at:
# repository/S4 code/BE_3090_Engrams_S4/S5_Memory_Loss.py
repo_root = Path(__file__).resolve().parents[2]

session_directories = [
    repo_root / "S1 code",
    repo_root / "S2 code",
    repo_root / "S3 code",
]

for directory in session_directories:
    if not directory.is_dir():
        raise FileNotFoundError(
            f"Required code directory not found: {directory}"
        )

    sys.path.insert(0, str(directory))
from BE3090_Engrams_S3_Part2 import character_to_matrix_map
from BE_3090_Engrams_S1_part4 import vectorsim1

#this variable is dictionary containing all char, encoding pairs
matrix_map = character_to_matrix_map
#this variable stores the text sequence that we will be using in this part of the lab
characterseq1 = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec."
characterseq2 = "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids"
characterseq3 = "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary re"
characterseq4 = "A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring which I enjoy with my whole heart. I am alone, and feel the charm of existence in this spot, which was created for the bliss of souls like mine. I am so happy, my dear friend, so absorbed in the exquisit"
characterseq5 = "CJ Stroud is a certified bum. Bro had one good rookie season and has been coasting ever since. His pocket presence vanishes under pressure, his decision-making is questionable, and he folds when the Texans need him most. At this point, calling him a franchise quarterback is just disrespectful to actual franchise quarterbacks. He's washed."
#find 10 most commonly activated neurons
def find_most_frequently_occurring_neurons(matrix, num_wanted):
    length = len(matrix[0])
    most_frequent = []
    for i in range(0,length,1):
        count = np.count_nonzero(matrix[:, i] == 1)
        neuron_num = i
        most_frequent.append((count, neuron_num))
    sorted_neurons = sorted(
    most_frequent,
    key=lambda item: item[0],
    reverse=True)
    return(sorted_neurons[:num_wanted])

    



##dict is the dictionary containing character, encoding pairs
def get_encoding_from_seq(sequence, decoder):
    missing_characters = set(sequence) - set(decoder.keys())

    if len(missing_characters) > 0:
        raise KeyError(
            f"Characters missing from decoder: {sorted(missing_characters)}"
        )

    matrices = [
        decoder[character]
        for character in sequence
    ]

    return np.vstack(matrices)

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
        if matrix.shape[0] >= value.shape[0] and matrix.shape[1] == value.shape[1]:
            similarity = vectorsim1(matrix[:value.shape[0], :], value)
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
    print(sequence_2_words)
    return(recalled_words/len(sequence_1_words))

def memory_pct(characterseq, decoder):
    encodingseq = get_encoding_from_seq(
        characterseq,
        decoder
    )
    #forget 10 neuron
    Most_frequent_neurons = find_most_frequently_occurring_neurons(encodingseq, 20)
    Most_frequent_neurons_clean = []
    
    counter = 0
    for x,y in Most_frequent_neurons:
        if(counter < 20):
            Most_frequent_neurons_clean.append(y)
        counter = counter+1
    print(Most_frequent_neurons)
    for i in Most_frequent_neurons_clean:
        encodingseq = forget_neuron(encodingseq, i)
    decoded_characters = []
    current_row = 0

    for _ in range(len(characterseq)):
        remaining_encoding = encodingseq[current_row:, :]

        best_char, similarity = determine_best_char(
            remaining_encoding,
            decoder
        )

        if best_char == "":
            break

        decoded_characters.append(best_char)

        # Advance by the selected character's duration.
        current_row += decoder[best_char].shape[0]

    decoded_seq = "".join(decoded_characters)

    return recall_pct(characterseq, decoded_seq)
print("hello")
print(memory_pct(characterseq1, matrix_map))
print(memory_pct(characterseq2, matrix_map))
print(memory_pct(characterseq3, matrix_map))
print(memory_pct(characterseq4, matrix_map))
print(memory_pct(characterseq5, matrix_map))






