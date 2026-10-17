from pathlib import Path
import sys

import matplotlib.pyplot as plt
import scipy.io as sio
import numpy as np
import re

from scipy.signal import find_peaks
from operator import itemgetter


# S5_Memory_Loss.py is located at:
# repository/S4 code/BE_3090_Engrams_S4/S5_Memory_Loss.py
repo_root = Path(__file__).resolve().parents[2]

session_directories = [
    repo_root / "S1 code",
    repo_root / "S2 code",
    repo_root / "S3 code",
]

for directory in session_directories:
    if not directory.is_dir():
        raise FileNotFoundError(
            f"Required code directory not found: {directory}"
        )

    sys.path.insert(0, str(directory))
from BE3090_Engrams_S3_Part2 import character_to_matrix_map
from BE_3090_Engrams_S1_part4 import vectorsim1

#this variable is dictionary containing all char, encoding pairs
matrix_map = character_to_matrix_map
#this variable stores the text sequence that we will be using in this part of the lab
characterseq1 = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec."
characterseq2 = "But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids"
characterseq3 = "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary re"
characterseq4 = "A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring which I enjoy with my whole heart. I am alone, and feel the charm of existence in this spot, which was created for the bliss of souls like mine. I am so happy, my dear friend, so absorbed in the exquisit"
characterseq5 = "CJ Stroud is a certified bum. Bro had one good rookie season and has been coasting ever since. His pocket presence vanishes under pressure, his decision-making is questionable, and he folds when the Texans need him most. At this point, calling him a franchise quarterback is just disrespectful to actual franchise quarterbacks. He's washed."
#find 10 most commonly activated neurons
def find_most_frequently_occurring_neurons(matrix, num_wanted):
    length = len(matrix[0])
    most_frequent = []
    for i in range(0,length,1):
        count = np.count_nonzero(matrix[:, i] == 1)
        neuron_num = i
        most_frequent.append((count, neuron_num))
    sorted_neurons = sorted(
    most_frequent,
    key=lambda item: item[0],
    reverse=True)
    return(sorted_neurons[:num_wanted])

    



##dict is the dictionary containing character, encoding pairs
def get_encoding_from_seq(sequence, decoder):
    missing_characters = set(sequence) - set(decoder.keys())

    if len(missing_characters) > 0:
        raise KeyError(
            f"Characters missing from decoder: {sorted(missing_characters)}"
        )

    matrices = [
        decoder[character]
        for character in sequence
    ]

    return np.vstack(matrices)

#alters encoding depending on the neuron forgotten, forgotten_n. Encoding is a 2d array
def forget_neuron(encoding, forgotten_n):
    encoding = np.array(encoding)
    encoding[:, forgotten_n] = 0
    return encoding
#we know each sequence is between 50 to 250 ms long, so can only check first 50ms.
def determine_best_char(matrix, decoder):
    matrix = np.array(matrix)
    max_sim = -1
    opt_char = ''
    for key,value in decoder.items():
        if matrix.shape[0] >= value.shape[0] and matrix.shape[1] == value.shape[1]:
            similarity = vectorsim1(matrix[:value.shape[0], :], value)
            if(similarity > max_sim):
                max_sim = similarity
                opt_char = key
    return (opt_char,max_sim)

#takes in a character sequence and the character encoding, measure accuracy of decode based on the key
#recall pct takes in decoded sequence, original sequence and returns recall %
def recall_pct(characterseq1, characterseq2):
    sequence_1_words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", characterseq1)
    sequence_2_words = re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", characterseq2)
    recalled_words = sum(s1word == s2word
        for s1word, s2word in zip(sequence_1_words, sequence_2_words))
    print(sequence_2_words)
    return(recalled_words/len(sequence_1_words))

def memory_pct(characterseq, decoder):
    encodingseq = get_encoding_from_seq(
        characterseq,
        decoder
    )
    #forget 10 neuron
    Most_frequent_neurons = find_most_frequently_occurring_neurons(encodingseq, 20)
    Most_frequent_neurons_clean = []
    
    counter = 0
    for x,y in Most_frequent_neurons:
        if(counter < 20):
            Most_frequent_neurons_clean.append(y)
        counter = counter+1
    print(Most_frequent_neurons)
    for i in Most_frequent_neurons_clean:
        encodingseq = forget_neuron(encodingseq, i)
    decoded_characters = []
    current_row = 0

    for _ in range(len(characterseq)):
        remaining_encoding = encodingseq[current_row:, :]

        best_char, _ = determine_best_char(
            remaining_encoding,
            decoder
        )

        if best_char == "":
            break

        decoded_characters.append(best_char)

        # Advance by the selected character's duration.
        current_row += decoder[best_char].shape[0]

    decoded_seq = "".join(decoded_characters)

    return recall_pct(characterseq, decoded_seq)
print("hello")
print(memory_pct(characterseq1, matrix_map))
print(memory_pct(characterseq2, matrix_map))
print(memory_pct(characterseq3, matrix_map))
print(memory_pct(characterseq4, matrix_map))
print(memory_pct(characterseq5, matrix_map))









import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t as t_dist

# ---------- fast decoder (same cosine score as vectorsim1, but much quicker) ----------
def build_template_info(decoder):
    """Store each template as (length, event rows, event cols, event count)."""
    info = {}
    for ch, M in decoder.items():
        rows, cols = np.nonzero(M)
        info[ch] = (M.shape[0], rows, cols, rows.size)
    return info

def decode_fast(stream, info):
    n_time = stream.shape[0]
    cum = np.concatenate(([0], np.cumsum(stream.sum(axis=1))))   # events up to each row
    lengths = [v[0] for v in info.values()]
    typical_len, min_len = int(np.median(lengths)), min(lengths)
    pos, out = 0, []
    while pos < n_time:
        best_ch, best_sim, best_len = None, 0.0, typical_len
        for ch, (L, rows, cols, n_events) in info.items():
            if pos + L > n_time or n_events == 0:
                continue
            n_window = cum[pos + L] - cum[pos]
            if n_window == 0:
                continue
            overlap = stream[pos + rows, cols].sum()
            sim = overlap / np.sqrt(n_events * n_window)   # cosine for 0/1 matrices
            if sim > best_sim:
                best_ch, best_sim, best_len = ch, sim, L
        if best_ch is None:                  # nothing matched this window
            if n_time - pos < min_len:
                break
            out.append('?')                  # failed letter, skip a typical length
            pos += typical_len
        else:
            out.append(best_ch)
            pos += best_len
    return ''.join(out)

# ---------- recall efficiency: fully recalled words / total words in the original ----------
WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
def word_recall(original, decoded):
    words = list(WORD.finditer(original))
    ok = sum(decoded[m.start():m.end()] == m.group() for m in words)
    return ok / len(words)

# ---------- experiment ----------
passages = [characterseq1, characterseq2, characterseq3, characterseq4, characterseq5]
info = build_template_info(matrix_map)
n_neurons = next(iter(matrix_map.values())).shape[1]

fractions = [0, .05, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]     # coarse grid
levels = sorted({int(round(f * n_neurons)) for f in fractions})   # neurons removed
n_trials = 5
rng = np.random.default_rng(0)

results = np.zeros((len(levels), len(passages), n_trials))
for p, seq in enumerate(passages):
    clean = get_encoding_from_seq(seq, matrix_map)
    for trial in range(n_trials):
        order = rng.permutation(n_neurons)        # one random removal order per trial
        for li, k in enumerate(levels):
            damaged = clean.copy()
            damaged[:, order[:k]] = 0             # remove the first k neurons in that order
            results[li, p, trial] = word_recall(seq, decode_fast(damaged, info))
    print(f"passage {p + 1} done")

# ---------- average and confidence interval across passages ----------
per_passage = results.mean(axis=2)                # (levels, passages), averaged over trials
mean_curve = per_passage.mean(axis=1)
sd = per_passage.std(axis=1, ddof=1)
n_p = len(passages)
half_width = t_dist.ppf(0.975, n_p - 1) * sd / np.sqrt(n_p)

# ---------- plot ----------
plt.figure(figsize=(9, 6))
for p in range(n_p):
    plt.plot(levels, per_passage[:, p], color='gray', alpha=0.35, lw=1, marker='o', ms=3)
plt.plot(levels, mean_curve, 'k-o', lw=2, label='Mean across passages')
plt.fill_between(levels,
                 np.clip(mean_curve - half_width, 0, 1),
                 np.clip(mean_curve + half_width, 0, 1),
                 alpha=0.25, label=f'95% CI of the mean (t, df={n_p - 1})')
plt.xlabel('Neurons removed')
plt.ylabel('Recall efficiency (fully recalled words / total words)')
plt.ylim(-0.02, 1.02)
plt.legend()
plt.tight_layout()
plt.show()

# ---------- neurons lost before half the words are gone ----------
below = np.where(mean_curve < 0.5)[0]
if below.size and below[0] > 0:
    i = below[0]
    x0, x1, y0, y1 = levels[i - 1], levels[i], mean_curve[i - 1], mean_curve[i]
    print("Approx. neurons removed at 50% recall:", round(x0 + (0.5 - y0) * (x1 - x0) / (y1 - y0)))



