# import scipy.io as sio              
# import numpy as np                   
# from scipy.signal import find_peaks  

# FRAMES = 100      # 1 recall = 1 second = 100 frames
# STEP   = 10       # each frame = 10 ms
# THRESH = 0.6      # neuron must fire in 60% of recalls to count as real

# # Give one character's data, get back engram
# def find_engram(data):
#     T, N = data.shape                 # T = time frames, N = neurons
#     reps = T // FRAMES                # number of recalls (e.g. 10)

#     # occurance[neuron, time] = how many recalls fired at that time
#     occ = np.zeros((N, FRAMES), int)
    
#     for n in range(N):                        # each neuron
#         for r in range(reps):                 # each recall
#             block = data[r*FRAMES:(r+1)*FRAMES, n]        # this recall's signal
#             peaks, _ = find_peaks(block, height=100, distance=10)  # its firings
#             for p in set(peaks):
#                 occ[n, p] += 1                # tally firing at that time

#     # keep firings that happen consistently 
#     min_occ = int(np.ceil(THRESH * reps))     # ex, 60% of 10 = 6 recalls
#     events = []
#     for n in range(N):
#         for b in range(FRAMES):
#             if occ[n, b] >= min_occ:
#                 events.append((n + 1, (b + 1) * STEP))    # (1-indexed ID, ms)

#     events.sort(key=lambda e: e[1])           # order by time
#     return events



# #Part 1 Engram for A 
# data = sio.loadmat('session2_a_misfire_12.mat')['neuron_network_imaging']
# engram_a = find_engram(data)                  # run recipe on "a" data
# print('engram for "a" [neuron, ms]:')
# for e in engram_a:
#     print(e)


# #Part 2 All Characters
# data3d = sio.loadmat('session2_training_chars_misfire_12.mat')['neuron_network_imaging']  # (time, neuron, char)

# # read the character list, it handles one-per-line or one long string)
# text = open('char_train.txt').read().split()
# chars = ''.join(text) if len(text) > 1 else text[0]

# engram_dict = {}                              # character to its engram
# n_chars = min(data3d.shape[2], len(chars))    # stay safe if counts differ
# for k in range(n_chars):                      # each character
#     engram_dict[chars[k]] = find_engram(data3d[:, :, k])   # reuse recipe on slice k
#     print(f"trained '{chars[k]}' with {len(engram_dict[chars[k]])} events")

import matplotlib.pyplot as plt
import scipy.io as sio

from scipy.signal import find_peaks
from operator import itemgetter

data = sio.loadmat('session2_a_misfire_12.mat')  # Load in the .mat file containing neuron activity data

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




