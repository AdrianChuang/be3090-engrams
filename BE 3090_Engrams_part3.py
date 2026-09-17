import matplotlib.pyplot as plt
import scipy.io as sio

from scipy.signal import find_peaks
from operator import itemgetter
data = sio.loadmat('session1_training_chars_12.mat')  # Load in the .mat file containing neuron activity data
print(data.keys())
activity = data['neuron_network_imaging'] # Extract the neuron activity data from the loaded .mat file
traincharsequence = '''0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[]^_`{|}~  '''
print(len(traincharsequence))
#print(activity.shape)
#print(activity.dtype)
#print(activity[:5, :5])

"""Visualize Neuron activity of one neuron over time"""
#plt.plot(activity[:,49])
#plt.xlabel('Time (frames)')
#plt.ylabel('Activity')
#plt.show()
print(activity)
print("hello")
print("end of test")
codes = []

for letters in activity:
    peaks = []
    print(letters.shape[1]) # Initialize an empty list to store peak indices for each neuron
    for neuron in range(letters.shape[1]):        #Loop through each neuron and find peaks, addding the indices of the peaks to the peaks list
        peakindices,_ = find_peaks(letters[:, neuron], height = 100, distance = 10)
        peaks.append(peakindices)

    Neuronactivationtuples = []
    i = 1
    for neuron in range(len(peaks)):
        for element in peaks[neuron]:
            Neuronactivationtuples.append((i,element))
        i = i+1
    Neuronactivationtuples.sort(key = itemgetter(1))
    codes.append(Neuronactivationtuples)
    #print(Neuronactivationtuples)
# determine numeric code sequence from+

training_set_key = []
print(len(codes))
for i in range (len(codes)):
        training_set_key.append((codes[i], traincharsequence[i]))
print(training_set_key)    







"""Raster plot of neuron activity for letter a"""
#plt.figure(figsize=(12, 8))

#for neuron in range(activity.shape[1]):
    #plt.vlines(peaks[neuron], neuron, neuron + 0.8)

#plt.xlabel('Time (frames)')
#plt.ylabel('Neuron Index')
#plt.show()


