import scipy.io as sio               
import numpy as np                  
from scipy.signal import find_peaks   

STEP   = 10       # each frame 10 ms
THRESH = 0.6      # neuron must fire in 60% of recalls 

#discover how long one recall is
def id_pot_periods(datalength): 
    #given length of overall sequence in ms,
    #and min/max possible sequence length, set
    #return an arr of all possible sequence lengths. 
    #Use this code for find_period to identify potential periods to test. 
    min = 50
    max = 250
    max_np = math.floor(datalength/min) #max possible number of periods (to nearest int)
    min_np = math.ceil(datalength/max) #max possible number of periods (to nearest int)
    return(min_np, max_np) #return min and max number of periods


def find_period(data, lo=50, hi=250):
    pop = data.sum(axis=1).astype(float)   # total activity of all neurons per frame
    pop = pop - pop.mean()                 # center around zero
    best_L, best_score = lo, -1
    for L in range(lo, hi + 1):            # try every possible recall length
        score = np.sum(pop[:-L] * pop[L:]) # how well signal matches itself shifted by L
        if score > best_score:
            best_score, best_L = score, L  # keep the length that matches best
    return best_L                          # the discovered recall length



