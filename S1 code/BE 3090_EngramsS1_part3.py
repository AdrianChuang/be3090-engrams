import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np

from scipy.signal import find_peaks
from operator import itemgetter
data = sio.loadmat('session2_b_variable_length_12.mat')  # Load in the .mat file containing neuron activity data
print(data.keys())
activity = data['neuron_network_imaging'] # Extract the neuron activity data from the loaded .mat file
print(activity)
print(activity.shape)      #'''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~    '''

with open("char_train.txt", "r") as file:
    traincharsequence = file.read()  # Read the contents of the text file into a string variable:
print(traincharsequence)


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
    print(len(denoised_neurons))
    return(str(denoised_neurons))





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
print(activity[1].shape)
print("hello")
print("end of test")
codes = []
print(len(activity))
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
print(len(codes))
for i in range (len(codes)):
        training_set_key.append((traincharsequence[i], codes[i]))

#for l in range (len(training_set_key)):
print(training_set_key[0][0]) #prints out char in place (l, 0)
print(getsequence(training_set_key[0][1])) #prints out sequence from arr in place (l, 1)
