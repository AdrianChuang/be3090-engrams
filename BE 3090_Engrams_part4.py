import numpy as np
def similarity_score(engram, sequence):
    # engram/sequence: neuron IDs in firing order
    matches = 0
    for i in range(len(engram)):                     # compare position by position
        if engram[i] == sequence[i]:
            matches += 1                             # same neuron in same slot
    return matches / len(engram)                     # fraction of positions that match
    
#example
a_engram = [187, 75, 74, 38, 19]
new = [187, 75, 74, 38, 1]        
print(similarity_score(a_engram, new))   

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
        return(min(a,b,c))
print(levenshsim("cat", "cap"))

def rawDataDenoiser(raw_data):
    for i in range (raw_data):
        for j in range(raw_data[0]):
            if(raw_data[i][j] < 50):
                raw_data[i][j] = 0

def cosineSim(orig, comp):
    orig1 = np.array(orig)
    comp1 = np.array(comp)
    
    res = np.sum(orig1 * comp1)/(np.linalg.norm(orig1) * np.linalg.norm(comp1))
    return res

arr1 = ([1,2,3],
    [4,5,6],
    [7,8,9])
arr2 = ([59,2,16],
    [42,67,420],
    [714,4,92])
print(cosineSim(arr1, arr2))
