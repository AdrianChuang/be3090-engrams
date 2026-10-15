import scipy.io as sio               
import numpy as np                  
from scipy.signal import find_peaks   
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "S1 code"))
from BE_3090_Engrams_S1_part4 import vectorsim
import math
np.set_printoptions(threshold=sys.maxsize, linewidth=sys.maxsize)

#discover how long one recall could potentially be (range min, max)
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

#this determines whether a particular "guess" for the period
#actually is correct (high similarity score between periods)
def find_period(data, test_np):
    print(data.shape[0])
    fraction = 1/test_np #test_np/(data.shape[0])
    first_period = data[:int(fraction*len(data))]
    
    second_period = data[int(fraction*len(data)):int(2*fraction*len(data))]
    
    j = vectorsim(first_period, second_period)
    print(j)
    if(j > 0.9):
        
        return 1
    else:
        return 0


#now test our methods on the data!

from operator import itemgetter
data = sio.loadmat('session2_b_variable_length_12.mat')  # Load in the .mat file containing neuron activity data for letter b with unknown period

activity = data['neuron_network_imaging'][0][0] # Extract the neuron activity data from the loaded .mat file

min_np, max_np = id_pot_periods(len(activity))

print(min_np)
print(max_np)
#iterate through all potential periods
for i in range(min_np, max_np + 1, 1):
    if(len(activity) % i == 0):
        val = find_period(activity, i)
        if(val == 1):
            print(i)
print(-1)
