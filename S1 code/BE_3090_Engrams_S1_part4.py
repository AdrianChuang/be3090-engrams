import numpy as np
import scipy.io as sio
import numpy as np

from scipy.signal import find_peaks
"""def similarity_score(engram, sequence):
    # engram/sequence: neuron IDs in firing order
    matches = 0
    for i in range(len(engram)):                     # compare position by position
        if engram[i] == sequence[i]:
            matches += 1                             # same neuron in same slot
    return matches / len(engram)                     # fraction of positions that match
    
#example
a_engram = [187, 75, 74, 38, 19]
new = [187, 75, 74, 38, 1]        
   

def levenshsim(engram, sequence):
    #engram - known sequence of neurons in a particular letter firing
    #sequence - unknown sequence of neurons in a particular letter firing
    if(min(len(engram), len(sequence)) == 0):
        return(max(len(engram), len(sequence)))
    else:
        a = levenshsim(engram[0:len(engram) - 1], sequence) + 1
        b = levenshsim(engram, sequence[0:len(sequence) - 1]) + 1
        c = levenshsim(engram[0:len(engram) - 1], sequence[0:len(sequence) - 1])
        if(engram[-1] != sequence[-1]):
            c = c+1
        return(min(a,b,c)) """


def vectorsim(matrix1, matrix2):
    vector1 = np.array(matrix1)
    vector2 = np.array(matrix2)
    #empty arrays for binary arrays later
    vector1bin = np.zeros((len(vector1),len(vector1[0])))
    vector2bin = np.zeros((len(vector1),len(vector1[0])))
    #find peaks
    ###########
    #array that will store all the coordinate pairs (time, neuron) that are peaks
    vector1peaks = []
    #first identify all the peaks per neuron
    for neuron in range(len(vector1[0])):        #Loop through each neuron and find peaks, addding the indices of the peaks to the peaks list
        peakindices,_ = find_peaks(vector1.T[neuron], height = 100, distance = 10)
        for indices in peakindices:
            vector1peaks.append((indices, neuron))
    vector2peaks = []
    for neuron in range(len(vector2[0])):
        peakindices,_ = find_peaks(vector2.T[neuron], height = 100, distance = 10)
        for indices in peakindices:
            vector2peaks.append((indices, neuron))
    #convert first 2d matrix to binary
    for index, neuron in vector1peaks:
        vector1bin[index][neuron] = 1
    
    #convert second 2d matrix to binary            
    for index, neuron in vector2peaks:
        vector2bin[index][neuron] = 1

    numerator = np.sum(vector1bin * vector2bin)
    
    
    denom = np.linalg.norm(vector1bin) * np.linalg.norm(vector2bin)
    
    
    if(denom == 0):
        return 0
    else:
        return numerator/denom
    
                