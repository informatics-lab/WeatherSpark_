#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import math

import datetime
import random

import datapoint

def wind_strength(val):
    if val < 8:
        return ' →  '
    if val < 20:
        return ' ⇉  '
    if val:
        return ' ⇶  '

def wind_dir(dir):
    """http://unicode-table.com/en/#1F865"""""
    dir = dir + 45/2
    dir = dir - 360 if dir >= 360 else dir
    cardinal = int(math.floor(dir / 45))
    week_chars = [u'\u2191', u'\u2197',u'\u2192',u'\u2198',
             u'\u2193',u'\u2199',u'\u2190',u'\u2196']
    strong_chars = [u'\u21D1', u'\u21D7',u'\u21D2',u'\u21D8',
                    u'\u21D3',u'\u21D9',u'\u21D0',u'\u21D6']

    strong_chars = [u'\u21D1', u'\u21D7',u'\u21D2',u'\u21D8',
                    u'\u21D3',u'\u21D9',u'\u21D0',u'\u21D6']

    twitter_chars = ['⬆','↗','➡','↘','⬇','↙','⬅','↖']

    #chars = week_chars if value <15 else strong_chars
    return twitter_chars[cardinal]

def get_vis(i):
    vis = [u'\u2001', u'\u2591', u'\u2592',u'\u2593']
    return vis[i]

def sigwx(code):
    clear_night = [0]
    sun = [1]
    sun_cloud = [3]
    fog = [5, 6]
    cloud = [7, 8, 9, 2] # 2 is partly cloudy at night but it looks better as cloud than a sun and cloud
    rain = range(9,22)
    thunder = [28, 29, 30]
    snow = range(22,28)

    if code in clear_night:
        return ("\\U%08x" % (127765)).decode('unicode-escape')
    if code in sun:
        return u'\u2600'
    if code in sun_cloud:
        return u'\u26c5'
    if code in fog:
        return ("\\U%08x" % (127787)).decode('unicode-escape')
    if code in cloud:
        return u'\u2601'
    if code in rain:
        return u'\u2614'
    if code in snow:
        return ("\\U%08x" % (127784)).decode('unicode-escape')
    if code in thunder:
        return u'\u26c8'
    print code

print ''.join((sigwx(i) for i in [0,1,2,3] + range(5, 31)))

def graph(vals):
    minval = min(vals)
    maxval = max(vals)
    range = (maxval - minval)
    step   = range / 7
    as_frac = lambda v: (v-minval)/range
    as_bar = lambda frac: int(round(frac * 7) + 1)
    print(map(as_frac, vals))
    print(map(as_bar,map(as_frac, vals)))
    return ''.join(map(get_8th_bar, map(as_bar,map(as_frac, vals))))


def tosub(number_str):
    result = u''
    for c in number_str:

        result += unichr(8320 + int(c)) if c is not '-' else u'\u208B'
    return result


def clock(hr):
    offset = hr - 1
    offset = offset if offset >= 0 else 11
    s = "\\U%08x" % (128336 + offset)
    c = s.decode('unicode-escape')
    return c

def get_8th_bar(val):
    return unichr(9601 + val -1) if val > 0 else u' '


def temp_bars(vals):
    pad = lambda val: ('0'+str(int(val)))[-2:]

    minval = min(vals)
    maxval = max(vals)
    range = (maxval - minval)
    middle = minval + (range / 2)
    step = range / 8
    step = 1 if step < 1 else step
    norm = lambda val: round((val-middle)/step) + 4
    graph = ''.join(map(get_8th_bar, map(int, map(norm, vals))))
    out =  tosub(pad(minval))
    out += u'\u21c5'
    out += tosub(pad(maxval))
    out += graph

    out =  tosub(pad(minval))
    out += u'\u2193'
    out += graph
    out += u'\u2191'
    out += tosub(pad(maxval))
    return out



def perc_to_bar(percent):
    a_bar = (100 / 8)
    num_bars = int(round(percent / a_bar))
    return get_8th_bar(num_bars)



def forecast():
    id, name = datapoint.rand_site()
    forecasts = []
    for forecast in datapoint.get_a_forecast(id):
        if forecast['datetime'] < datetime.datetime.now():
            continue
        forecasts.append(forecast)
        if(len(forecasts) >= 7):
            break

    print name
    print u'Time   ',
    print ''.join(clock(int(f['datetime'].hour)) for f in forecasts)

    print u'Wind  ',
    print ''.join(wind_strength(f['wind_gust']) for f in forecasts)

    print u'Wind  ',
    print ''.join(wind_dir(f['wind_dir_deg']) for f in forecasts)

    print u'Symb ',
    print ''.join(sigwx(f['type']) for f in forecasts)

    print '%Rain? ',
    print ''.join([perc_to_bar(f['prob_precip']) for f in forecasts])

    print u'Temp:',
    print temp_bars([t['temp'] for t in forecasts])


print ''.join([perc_to_bar(f) for f in [0,10,20,40,40,50,60,70,80,90,100]])
forecast()
print ''
forecast()
print ''
forecast()
print ''
forecast()
print ''
forecast()
print ''
forecast()
