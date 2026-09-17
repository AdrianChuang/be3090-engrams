def similarity_score(engram, sequence):
    # engram/sequence: neuron IDs in firing order
    matches = 0
    for i in range(len(engram)):                     # compare position by position
        if engram[i] == sequence[i]:
            matches += 1                             # same neuron in same slot
    return matches / len(engram)                     # fraction of positions that match
    
#example
a_engram = [187, 75, 74, 38, 19]
new = [187, 75, 74, 38, 19]        
print(similarity_score(a_engram, new))   
