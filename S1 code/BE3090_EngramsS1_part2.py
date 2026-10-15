import matplotlib.pyplot as plt
import scipy.io as sio

from scipy.signal import find_peaks
from operator import itemgetter

data = sio.loadmat('session1_a_12.mat')  # Load in the .mat file containing neuron activity data

activity = data['neuron_network_imaging'] # Extract the neuron activity data from the loaded .mat file

#print(activity.shape)
#print(activity.dtype)
#print(activity[:5, :5])

"""Visualize Neuron activity of one neuron over time"""
#plt.plot(activity[:,49])
#plt.xlabel('Time (frames)')
#plt.ylabel('Activity')
#plt.show()

peaks = [] # Initialize an empty list to store peak indices for each neuron

for neuron in range(activity.shape[1]):        #Loop through each neuron and find peaks, addding the indices of the peaks to the peaks list
    peakindices,_ = find_peaks(activity[:, neuron], height = 100, distance = 10)
    peaks.append(peakindices)

Neuronactivationtuples = []
i = 1
for neuron in range(len(peaks)):
    for element in peaks[neuron]:
        Neuronactivationtuples.append((i,(element + 1) * 10)) # multiply by 10 to convert to milliseconds, 1 is added to element to convert from 0-indexing to 1-indexing (first time point is 10 ms, not 0 ms)
    i = i+1
Neuronactivationtuples.sort(key = itemgetter(1))
print(Neuronactivationtuples)
print(len(Neuronactivationtuples))

codes_A = [] # a list of lists (containing tuples) containing the 10 iterations of A
for i in range(1000, 11000, 1000): #This iterates through neuronactivationtuples and blocks it into 1000 ms segments
    temparr = []
    
    for tuple in Neuronactivationtuples:
        if(i - 1000 < tuple[1] <= i):
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
        if((neurons[0], neurons[1]+i*1000) in codes_A[i]):
            print("ok")
            instances = instances + 1
        elif((neurons[0], neurons[1]+i*1000 - 10) in codes_A[i]):
            instances = instances + 1
        elif((neurons[0], neurons[1]+i*1000 - 20) in codes_A[i]):
            instances = instances + 1
        elif((neurons[0], neurons[1]+i*1000 - 30) in codes_A[i]):
            instances = instances + 1
        elif((neurons[0], neurons[1]+i*1000 + 10) in codes_A[i]):
            instances = instances + 1
        elif((neurons[0], neurons[1]+i*1000 + 20) in codes_A[i]):
            instances = instances + 1
        elif((neurons[0], neurons[1]+i*1000 + 30) in codes_A[i]):
            instances = instances + 1
    if(instances >= 5):
        denoised_neurons.append((neurons[0], neurons[1], instances))
        print("hello")
print(denoised_neurons)

"""Raster plot of neuron activity for letter a"""
#plt.figure(figsize=(12, 8))

#for neuron in range(activity.shape[1]):
    #plt.vlines(peaks[neuron], neuron, neuron + 0.8)

#plt.xlabel('Time (frames)')
#plt.ylabel('Neuron Index')
#plt.show()


