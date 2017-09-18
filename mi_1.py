import numpy as np
import itertools

from actual_alg import alg

states = ['H', 'C']
observations = ['S', 'M', 'L']

#a = np.matrix('0.7 0.3; 0.4 0.6')

a = {
    'H': { 'H': 0.7, 'C': 0.3},
    'C': { 'H': 0.4, 'C': 0.6}
}
#b = np.matrix('0.1 0.4 0.5; 0.7 0.2 0.1')
b = {
    'H': { 'S': 0.1, 'M': 0.4, 'L': 0.5},
    'C': { 'S': 0.7, 'M': 0.2, 'L': 0.1}
}

#p = np.array([0.6, 0.4])
p = {
    'H': 0.6,
    'C': 0.4
}

def as_observation(col):
    return [observations[i] for i in col]

def as_states(col):
    return [states[i] for i in col]

#o = np.array([0, 1, 0, 2])
#o = ['S', 'M', 'S', 'L']




#       S       M       L
# H     0.1     0.4     0.5
# C     0.7     0.2     0.1
#



def calc(sequence: list):
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

o = as_observation([0, 1, 0, 2])

N = len(p) #liczba stanow
M = len(next(iter(b.values()))) #liczba obserwacji
T = len(o)

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
    sequence = as_states(sequence)
    seq_states.append(sequence)
    v = calc(sequence)
    std.append(v)
    #print("{0} -> {1:.6f}".format(sequence, calc(sequence)))

norm = normalize(std)

state_prob = np.zeros((N, T))
for t in range(T):
    for i in range(len(seq)):
        #print ('row:{0}, col:{1} val:{2}'.format(t, seq[i][t], std[i]))
        state_prob[seq[i][t], t] += std[i]

    #print ([v for k, v in state_dict.items()])
for t in range(T):
    state_prob[:, t] = normalize(state_prob[:, t])

best = max(std)

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
    print("{0} -> {1:.6f} = {2:.6f} {3}{4}".format(seq_states[i], std[i], norm[i], best_str, best_state_str))

#print (best_state)


print (state_prob)

alg(states, observations, p, a, b, o)



#print(calc([0, 0, 1, 1]))