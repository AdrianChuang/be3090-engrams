import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

from scipy.signal import find_peaks
from operator import itemgetter
data = sio.loadmat('prelab_session2_training_chars.mat')  # Load in the .mat file containing neuron activity data

activity_old = data['neuron_network_imaging'] # Extract the neuron activity data from the loaded .mat file

activity = np.ascontiguousarray(np.moveaxis(activity_old, 2, 0))

      #'''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~    '''

with open("char_train.txt", "r") as file:
    traincharsequence = file.read()  # Read the contents of the text file into a string variable:



#print(activity.shape)
#print(activity.dtype)
#print(activity[:5, :5])
def getsequence(arr_peaks):
     # takes in a list of tuples of (arr of peak indices for the character, the character)

    Neuronactivationtuples = arr_peaks
    

    codes_A = [] # a list of lists (containing tuples) containing the 10 iterations of A
    for i in range(1000, 11000, 1000): #This iterates through neuronactivationtuples and blocks it into 1000 ms segments
        temparr = []
        
        for tuple in Neuronactivationtuples:
            if(i - 1000 < tuple[1]*10 <= i):
                temparr.append(tuple)
        codes_A.append(temparr)
        # while(count < len(Neuronactivationtuples)):
        #     if(Neuronactivationtuples[count][1] < i - 1000):
        #         temparr.append(Neuronactivationtuples[count])
        #         count = count+1
        # codes_A.append(temparr) # adds this sequence of A engram to codes_A

    #now we have to determine which neuron firings are repeated across all codes
    
    denoised_neurons = []
    for neurons in codes_A[0]:
        instances = 1
        for i in range (1,10,1):
            if((neurons[0], neurons[1]+i*100) in codes_A[i]):
                instances = instances + 1
            elif((neurons[0], neurons[1]+i*100 - 1) in codes_A[i]):
                instances = instances + 1
            elif((neurons[0], neurons[1]+i*100 - 2) in codes_A[i]):
                instances = instances + 1
            elif((neurons[0], neurons[1]+i*100 - 3) in codes_A[i]):
                instances = instances + 1
            elif((neurons[0], neurons[1]+i*100 + 1) in codes_A[i]):
                instances = instances + 1
            elif((neurons[0], neurons[1]+i*100 + 2) in codes_A[i]):
                instances = instances + 1
            elif((neurons[0], neurons[1]+i*100 + 3) in codes_A[i]):
                instances = instances + 1
        if(instances >= 5):
            denoised_neurons.append((neurons[0], neurons[1], instances))
        
    return((denoised_neurons))





"""Raster plot of neuron activity for letter a"""
#plt.figure(figsize=(12, 8))

#for neuron in range(activity.shape[1]):
    #plt.vlines(peaks[neuron], neuron, neuron + 0.8)

#plt.xlabel('Time (frames)')
#plt.ylabel('Neuron Index')
#plt.show()




"""Visualize Neuron activity of one neuron over time"""
#plt.plot(activity[:,49])
#plt.xlabel('Time (frames)')
#plt.ylabel('Activity')
#plt.show()

codes = []

for letters in activity:
    peaks = [] # Initialize an empty list to store peak indices for each neuron

    for neuron in range(letters.shape[1]):        #Loop through each neuron and find peaks, addding the indices of the peaks to the peaks list
        peakindices,_ = find_peaks(letters[:, neuron], height = 100, distance = 3)
        peaks.append(peakindices)

    Neuronactivationtuples = []
    i = 1
    for neuron in range(len(peaks)):
        for element in peaks[neuron]:
            Neuronactivationtuples.append((i,element))
        i = i+1
    Neuronactivationtuples.sort(key = itemgetter(1))
    codes.append(Neuronactivationtuples)
# determine numeric code sequence from+

training_set_key = []




for i in range (len(codes)):
        training_set_key.append((codes[i], traincharsequence[i]))

letter_code_pairs = []
for i in range (len(training_set_key)):
        #print(training_set_key[i][1])
        #print(getsequence(training_set_key[i][0]))
        letter_code_pairs.append((training_set_key[i][1], getsequence(training_set_key[i][0])))

print(letter_code_pairs[0])

stripped_code_pairs =[] # create a list of tuples containing (letter, neuron list in firing order)
for char, seq in letter_code_pairs:
    temp_list = []
    for triple in seq:
        temp_list.append(triple[0])
    stripped_code_pairs.append((char, temp_list))
    

prelab_session2_sequence = sio.loadmat('prelab_session2_sequence.mat')
sequence_to_analyze = prelab_session2_sequence['neuron_network_imaging'] #load in sequence of string we are trying to predict

sequence_peaks = []
for neuron in range(sequence_to_analyze.shape[1]):  # Loop through each neuron and add list of peaks to sequence_peaks
    peakindices,_ = find_peaks(sequence_to_analyze[:, neuron], height = 100, distance = 3)
    sequence_peaks.append(peakindices)
print(len(sequence_peaks))

sequence_activation_tuples = []
neuron_counter = 0
for neuron in sequence_peaks: #convert sequence peaks into tuples with neuron, peak time
    neuron_counter+=1
    for peak in neuron:
        sequence_activation_tuples.append((neuron_counter, peak))
    sequence_activation_tuples.sort(key = itemgetter(1))

separated_by_time_neuron_list =[]
print(sequence_to_analyze.shape[0])
for i in range(100, sequence_to_analyze.shape[0], 100): # Loop through time windows of 100 frames. creating a list of neurons that fired within each time window
    temp_list = []
    for tup in sequence_activation_tuples:
        if tup[1] < i and tup[1] >= i - 100:
            temp_list.append(tup[0])
    separated_by_time_neuron_list.append(temp_list)

print(separated_by_time_neuron_list[0])

from BE_3090_Engrams_part4 import levenshsim
print(stripped_code_pairs[0])
print(levenshsim('asjdhkqebdkqhbwdkhqg', 'ifhuetuwtguydegwtduydt'))
prediction = ''
for letter_sequence in separated_by_time_neuron_list:  # Loop through each time window's neuron firing sequence to predict the corresponding letter
    best_match = ''
    best_score = float('inf')
    
    for letter, neuron_list in stripped_code_pairs:
        score = levenshsim(letter_sequence, neuron_list)
        print(score)
        if score < best_score:
            best_score = score
            best_match = letter
    prediction += best_match
print(prediction)






