import itertools
import operator

import numpy as np


def as_observation(col, observations):
    return [observations[i] for i in col]

def as_states(col, states):
    return [states[i] for i in col]

def calc(sequence: list, p, a, b, o):
    my = np.array(sequence)
    sum = 1
    for i in range(my.size):
        ai = p[my[i]] if i is 0 else a[my[i - 1]][my[i]]
        bi = b[my[i]][o[i]]
        sum *= ai * bi
    return sum

def normalize(iter):
    s = sum(iter)
    if s == 0.0:
        raise Exception('cannot normalalize sum is 0')
    return [v / s for v in iter]

def alg(states, observations, p, a, b, o, log=True):
    N = len(p)  # liczba stanow
    M = len(next(iter(b.values())))  # liczba obserwacji
    T = len(o)
    if log:
        print(a)
        print(b)
        print(p)
        print(o)

        print(N)
        print(M)
        print(T)

    if (N != len(states) or M != len(observations)):
        raise Exception('bad')

    seq = []
    seq_states = []
    std = []

    for sequence in itertools.product(range(N), repeat=T):
        seq.append(sequence)
        sequence = as_states(sequence, states)
        seq_states.append(sequence)
        v = calc(sequence, p, a, b, o)
        std.append(v)
        # print("{0} -> {1:.6f}".format(sequence, calc(sequence)))

    norm = normalize(std)

    state_prob = np.zeros((N, T))
    for t in range(T):
        for i in range(len(seq)):
            # print ('row:{0}, col:{1} val:{2}'.format(t, seq[i][t], std[i]))
            state_prob[seq[i][t], t] += std[i]

            # print ([v for k, v in state_dict.items()])
    for t in range(T):
        state_prob[:, t] = normalize(state_prob[:, t])

    #best = max(std)
    best_i, best = max(enumerate(std), key=operator.itemgetter(1))

    best_state = []
    for t in range(T):
        best_s = None
        for s in range(N):
            if best_s is None or state_prob[s, t] > state_prob[best_s, t]:
                best_s = s
        best_state.append(best_s)

    for i in range(len(seq)):
        best_str = '<-- best ' if std[i] is best else ''
        best_state_str = '<-- best state ' if list(seq[i]) == best_state else ''
        if log:
            print("{0} -> {1:.6f} = {2:.6f} {3}{4}".format(seq_states[i], std[i], norm[i], best_str, best_state_str))

    # print (best_state)

    if log:
        print(state_prob)

    return as_states(seq[best_i], states), as_states(best_state, states)