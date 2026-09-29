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
print(levenshsim(a_engram, new))