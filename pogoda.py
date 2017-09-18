import csv
import re
from itertools import groupby

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
    'północny' :'N',
    'wschodni' :'E',
    'zachodni' :'W'
}

beaufort_list = [1, 5, 11, 19, 28, 38, 49, 61, 74, 88, 102, 117]

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
    pi_matrix([d.direction for d in my_data])



    #for line in lines:
    #    print(line)

    #print(len(lines))