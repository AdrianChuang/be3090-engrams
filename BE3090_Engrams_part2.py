import matplotlib.pyplot as plt
import scipy.io as sio

from scipy.signal import find_peaks

data = sio.loadmat('session1.mat')  # Load in the .mat file containing neuron activity data

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

plt.figure(figsize=(12, 8))

for neuron in range(activity.shape[1]):
    plt.vlines(peaks[neuron], neuron, neuron + 0.8)

plt.xlabel('Time (frames)')
plt.ylabel('Neuron Index')
plt.show()