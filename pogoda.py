import csv
import re
from collections import OrderedDict
from itertools import groupby

from actual_alg import alg

pattern = re.compile('\s+')


filename = "./pogoda.csv"

columns_with_text = [0, 1, 2, 3, 4, 5]
columns_with_boolean = []
columns_with_numbers = []

def as_item(index, item):
    if index in columns_with_numbers:
        return item
    elif index in columns_with_text:
        return "'{0}'".format(item)
    elif index in columns_with_boolean:
        if item == 'tak':
            return 'True'
        elif item == 'nie':
            return 'False'
        else:
            return "null"
    return None

month_map = {
    'sty': 0,
    'lut': 1,
    'mar': 2,
    'kwi': 3,
    'maj': 4,
    'cze': 5,
    'lip': 6,
    'sie': 7,
    'wrz': 8,
    'paź': 9,
    'lis': 10,
    'gru': 11,
}

direction_map = {
    'połud.-wsch.': 'S-E',
    'połud.-zach.': 'S-W',
    'południowy' :'S',
    'północ.-wsch.': 'N-E',
    'północ.-zach.': 'N-W',
    'północny': 'N',
    'wschodni': 'E',
    'zachodni': 'W'
}

beaufort_list = [1, 5, 11, 19, 28, 38, 49, 61, 74, 88, 102, 117]

beaufort_map = {
    0: 'Calm',
    1: 'Light air',
    2: 'Light breeze',
    3: 'Gentle breeze',
    4: 'Moderate breeze',
    5: 'Fresh breeze',
    6: 'Strong breeze',
}

def as_beaufort(value):
    return len([x for x in beaufort_list if value > x])

#print(as_beaufort(0))
#print(as_beaufort(0.5))
#print(as_beaufort(1))
#print(as_beaufort(1.5))
#print(as_beaufort(4.5))
#print(as_beaufort(5))
#print(as_beaufort(5.1))
#print(as_beaufort(6.5))

start_year = 2015

class data:
    def __init__(self, date, weather, temperature, pressure, wind, rain):
        self.raw_wind = wind
        self.raw_rain = rain
        self.raw_pressure = pressure
        self.raw_temperature = temperature
        self.raw_weather = weather
        self.raw_date = date

        self.day, self.month, self.year = self._parse_date(date)
        self.speed, self.direction, self.beaufort = self._parse_wind(wind)
        self.beaufort_str = beaufort_map[self.beaufort]

    def _parse_date(self, raw: str):
        split = raw.split(',')
        day_of_week = split[0]
        raw2 = split[1]
        raw2 = raw2.lstrip()
        split2 = raw2.split(' ')
        day = int(split2[0])
        month_raw = split2[1]
        month = month_map[month_raw]
        global start_year
        if month == 1 and day == 1:
            start_year += 1
        year = start_year
        return day, month, year

    def _parse_wind(self, raw: str):
        split = raw.split(',')
        speed_raw = split[0]
        direction_raw = split[1]
        speed = float(speed_raw.replace('km/h', '').replace("'", ''))
        direction = direction_raw.replace("'", '').strip()
        beaufort = as_beaufort(speed)
        return speed, direction_map[direction], beaufort


def analyze(foo):
    grouped = groupby(sorted(foo))
    for key, group in grouped:
        print('{0}: {1}'.format(key, len(list(group))))
    #uniq = sorted(set(foo))
    #for l in uniq:
    #    print(l)
    print('all: ' + str(len(foo)))

def pi_matrix(foo):
    ret = {}
    grouped = groupby(sorted(foo))
    for key, group in grouped:
        ret[key] = len(list(group)) / len(foo)
    return ret

def pi_raw(foo):
    ret = {}
    grouped = groupby(sorted(foo))
    for key, group in grouped:
        ret[key] = len(list(group))
    return ret

def init_dict(dim1, dim2):
    ret = OrderedDict()
    for d in dim1:
        ret[d] = OrderedDict()
        for d2 in dim2:
            ret[d][d2] = 0
    return ret

def a_matrix(col: list, states: list):
    ret = init_dict(states, states)

    for i in range(1, len(col)):
        s1 = col[i - 1]
        s2 = col[i]
        ret[s1][s2] += 1

    return ret

def a_sum(a):
    s = 0
    for k, v in a.items():
        for k2, v2 in v.items():
            s += v2
    #print(s)
    return s

def check_a_sum(a, e):
    s = a_sum(a)
    #print (s)
    assert (abs(s - e) <= 0.000001)

def normalize_a(a):
    s = a_sum(a)
    for k, v in a.items():
        for k2, v2 in v.items():
            a[k][k2] /= s

def b_matrix(col, states, observations):
    ret = init_dict(states, observations)

    for beaufort, direction in col:
        ret[direction][beaufort] += 1
        #pass

    return ret

separator = """\t"""

def print_a(a, col1, col2):
    print (separator + separator.join([s1 for s1 in col2]))
    for s1 in col1:
        string = s1
        for s2 in col2:
            string += '{1}{0}'.format(a[s1][s2], separator)
        print(string)

def print_pi(p, col1):
    print(separator.join([s1 for s1 in col1]))
    print(separator.join([str(p[s1]) for s1 in col1]))

def print_2_elem(col: list):
    print(', '.join(col))

with open(filename) as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    csvfile.seek(0)
    reader = csv.reader(csvfile, dialect)

    #skip header
    next(reader)

    lines = []
    my_data = []

    for line in reader:
        items = [as_item(index, item) for index, item in enumerate(line) if as_item(index, item) is not None]
        items = [pattern.sub(' ', item) for item in items]
        lines.append('  ,({0})'.format(', '.join(items)))
        my_data.append(data(items[0], items[1], items[2], items[3], items[4], items[5]))


    #analyze(['{0} {1}'.format(d.beaufort, d.direction) for d in my_data])
    p = pi_matrix([d.direction for d in my_data])



    states = [k for k, v in p.items()]
    states_ordered = ['N', 'N-E', 'E', 'S-E', 'S', 'S-W', 'W', 'N-W']

    #p = {s: 1 / len(states) for s in states}

    observations = [ beaufort_map[i] for i in sorted(set([d.beaufort for d in my_data]))]
    print(states)
    print(observations)

    a = a_matrix([d.direction for d in my_data], states)
    #print (sum([v for k, v in p.items()]))

    check_a_sum(a, 730)
    print_a(a, states_ordered, states_ordered)

    normalize_a(a)
    check_a_sum(a, 1)

    b = b_matrix([(d.beaufort_str, d.direction) for d in my_data], states, observations)

    check_a_sum(b, 731)

    print_a(b, states_ordered, observations)
    normalize_a(b)
    check_a_sum(b, 1)

    print_pi(pi_raw([d.direction for d in my_data]), states_ordered)


    print(p)
    print(a)
    print(b)

    t1 = [16.25, 29.75, 26.5, 33]
    t2 = [21, 16.25, 13.25]
    t3 = [4.5, 18.75, 15.75]
    t4 = [13, 17.75, 19.75]
    t5 = [10, 16, 12.25, 9]
    t6 = [10, 16]
    o = [beaufort_map[as_beaufort(i)] for i in t6]
    #o = [observations[i] for i in [2, 3, 1, 3]]

    stats = { True: 0, False: 0}
    for i in range(1, len(my_data)):
        d = my_data[i - 1]
        d2 = my_data[i]
        if d.year == 2017 and d.month == 6:
        #if True:
            o = [d.beaufort_str, d2.beaufort_str]

            best, best_state = alg(states, observations, p, a, b, o, False)

            correct = [d.direction, d2.direction]
            if True:
            #if (correct == best or correct == best_state):
            #if (best != ['W', 'W'] or best_state != ['W', 'W']):
                #print(o)
                print('{0} {1} {2}'.format(d.day, d.month, d.year))
                #print(['{0} {1}'.format(d.beaufort, d.beaufort_str), '{0} {1}'.format(d2.beaufort, d2.beaufort_str)])

                print(['{0} {1}, {2} {3}'.format(d.beaufort, d.beaufort_str, d2.beaufort, d2.beaufort_str)])

                print_2_elem(correct)
                print_2_elem(best)
                print_2_elem(best_state)
                #print(correct)
                #print(best)
                #print(best_state)

                stats[True] += 1
            else:
                stats[False] += 1
    print (stats)

    #analyze([d.beaufort for d in my_data])


    #for line in lines:
    #    print(line)

    #print(len(lines))