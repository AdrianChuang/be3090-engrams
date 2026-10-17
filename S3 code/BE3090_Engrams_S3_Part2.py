import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

from scipy.signal import find_peaks
from operator import itemgetter
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "S1 code"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "S2 code"))
from BE_3090_Engrams_S1_part4 import vectorsim
from BE_3090_Engrams_S2_part3_4 import id_pot_periods
from BE_3090_Engrams_S2_part3_4 import find_period

import math

data = sio.loadmat('session3_training_chars_12.mat')  # Load in the .mat file containing neuron activity data

activity_old = data['neuron_network_imaging'] # Extract the neuron activity data from the loaded .mat file


activity = [np.ascontiguousarray(cell[0]) for cell in activity_old]

period_map = {} #Map from character index to period
     
with open("char_train.txt", "r") as file:
    traincharsequence = file.read()  # Read the contents of the text file into a string variable:


def get_correct_period(activity_matrix):
    min_np, max_np = id_pot_periods(len(activity_matrix))
    L = len(activity_matrix)
    scores = {i: find_period(activity_matrix, i) for i in range(min_np, max_np + 1) if L % i == 0}
    best = max(scores.values())
    return L // max(i for i, s in scores.items() if s >= 0.9 * best)

def getsequence(character_index, NAT, character_raw_matrix_length, period):
     # takes in a list of tuples of (neuron number, time))
     # What get sequence takes in is in the format: (95, np.int64(292))

    Neuronactivationtuples = NAT # gets the list of tuples of (neuron number, time)

    print(period)
    codes_A = [] # a list of lists (containing tuples) containing the 10 iterations of A
    #find the correct length segments
    
    #This iterates through neuronactivationtuples and blocks it into the correct length segments

    for i in range(period, character_raw_matrix_length +period, period): 
        temparr = []
        
        for tuple in Neuronactivationtuples:
            if(i - period < tuple[1] <= i):
                temparr.append(tuple)
        codes_A.append(temparr)
        # while(count < len(Neuronactivationtuples)):
        #     if(Neuronactivationtuples[count][1] < i - 1000):
        #         temparr.append(Neuronactivationtuples[count])
        #         count = count+1
        # codes_A.append(temparr) # adds this sequence of A engram to codes_A

    #now we have to determine which neuron firings are repeated across all codes
    #print(codes_A)
    denoised_neurons = []
    # for neurons in codes_A[0]:
    #     instances = 1
    #     for i in range (1,10,1):
    #         if((neurons[0], neurons[1]+i*100) in codes_A[i]):
    #             instances = instances + 1
    #         elif((neurons[0], neurons[1]+i*100 - 1) in codes_A[i]):
    #             instances = instances + 1
    #         elif((neurons[0], neurons[1]+i*100 - 2) in codes_A[i]):
    #             instances = instances + 1
    #         elif((neurons[0], neurons[1]+i*100 - 3) in codes_A[i]):
    #             instances = instances + 1
    #         elif((neurons[0], neurons[1]+i*100 + 1) in codes_A[i]):
    #             instances = instances + 1
    #         elif((neurons[0], neurons[1]+i*100 + 2) in codes_A[i]):
    #             instances = instances + 1
    #         elif((neurons[0], neurons[1]+i*100 + 3) in codes_A[i]):
    #             instances = instances + 1
    #     if(instances >= 5):
    #         denoised_neurons.append((neurons[0], neurons[1], instances))
    # print(len(denoised_neurons))
    dict_neuron_tuples = {}
    for i in codes_A:
        for j in i:
                mod = j[1]%period
                
                
                
                

                if((j[0],mod) in dict_neuron_tuples):
                    currentVal = dict_neuron_tuples.get((j[0],mod))
                    dict_neuron_tuples.update({(j[0],mod): currentVal+1})
                # elif((j[0],mod+10) in dict_neuron_tuples):
                #     curval = dict_neuron_tuples.get((j[0],mod+10))
                #     dict_neuron_tuples.update({(j[0],mod+10): curval+1})
                # elif((j[0],mod+20) in dict_neuron_tuples):
                #     curval = dict_neuron_tuples.get((j[0],mod+20))
                #     dict_neuron_tuples.update({(j[0],mod+20): curval+1})
                # elif((j[0],mod+30) in dict_neuron_tuples):
                #     curval = dict_neuron_tuples.get((j[0],mod+30))
                #     dict_neuron_tuples.update({(j[0],mod+30): curval+1})
                # elif((j[0],mod-10) in dict_neuron_tuples):
                #     curval = dict_neuron_tuples.get((j[0],mod-10))
                #     dict_neuron_tuples.update({(j[0],mod-10): curval+1})
                # elif((j[0],mod-20) in dict_neuron_tuples):
                #     curval = dict_neuron_tuples.get((j[0],mod-20))
                #     dict_neuron_tuples.update({(j[0],mod-20): curval+1})
                # elif((j[0],mod-30) in dict_neuron_tuples):
                #     curval = dict_neuron_tuples.get((j[0],mod-30))
                #     dict_neuron_tuples.update({(j[0],mod-30): curval+1})
                else:
                    dict_neuron_tuples.setdefault((j[0],mod),1)
    for key,value in dict_neuron_tuples.items():
        if(value >= math.ceil(character_raw_matrix_length/period*0.6)):
            denoised_neurons.append((key, value))

    return(denoised_neurons)






"""Raster plot of neuron activity for letter a"""
#plt.figure(figsize=(12, 8))

#for neuron in range(activity.shape[1]):
    #plt.vlines(peaks[neuron], neuron, neuron + 0.8)

#plt.xlabel('Time (frames)')
#plt.ylabel('Neuron Index')
#plt.show()





#Codes represent an array of arrays
codes = []

#iterates through all 2D arrays, each 2D array representing a character
for letters in activity:
    peaks = [] # Initialize an empty list to store peak indices for each neuron

    for neuron in range(letters.shape[1]):        #Loop through each neuron (1-200) and find peaks, addding the indices of the peaks to the peaks list
        peakindices,_ = find_peaks(letters[:, neuron], height = 100, distance = 10) #finds the peaks for the particular neuron, and stores this in an array
        peaks.append(peakindices) #appends the array of indices peakindices for the particular neuron

    Neuronactivationtuples = [] #A list of tuples in the format ((95, np.int64(292))), where the first element is the neuron number and the second element is the time at which a peak for that neuron occurs (in centiseconds)
    i = 1 #the number of the neuron in the tuple, from 1 - 200
    for neuron in range(len(peaks)): #iterates through peaks using nested loops to extract all peaks for each neuron and put in tuple with (neuron, peaktime) format
        for element in peaks[neuron]:
            Neuronactivationtuples.append((i,element))
        i = i+1
    Neuronactivationtuples.sort(key = itemgetter(1)) #sort this list of tuples by time of the peak
    codes.append(Neuronactivationtuples)
# determine numeric code sequence from+

training_set_key = []
for i in range (len(codes)):
        training_set_key.append((traincharsequence[i], codes[i]))


#------- Populate period_map with the correct period for each character in the training set -------#
for i in range(len(activity)):
    period_map[i] = get_correct_period(activity[i])

#for l in range (len(training_set_key)):
#print(training_set_key[0][1])
#print(training_set_key[0][0]) #prints out char in place (l, 0)
print(getsequence(0, training_set_key[0][1], activity[0].shape[0], period_map[0]))
 #prints out sequence from arr in place (l, 1)


#---------- Dictionary Building ----------#
#This dictionary will map each character to its corresponding binary.

character_to_matrix_map = {}

for i in range(len(training_set_key)):
    character = training_set_key[i][0]
    neuron_activation_tuples = training_set_key[i][1]
    character_raw_matrix_length = activity[i].shape[0]
    period = period_map[i]

    n_neurons = activity[i].shape[1]

    sequence = getsequence(i, neuron_activation_tuples, character_raw_matrix_length, period)
    
    M = np.zeros((period, n_neurons), dtype=int)   # rows = time bins in one recall, cols = neurons
    for ((neuron, t), count) in sequence:
        M[t, neuron - 1] = 1                       # neuron - 1 because you numbered neurons from 1

    character_to_matrix_map[character] = M
    
