#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import os
import random
import urllib2

import datetime

KEY = os.environ['DATAPOINT_KEY']
EXETER = 351414
EDINBURGH = 3166
GET_ALL_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/all?res=3hourly&key=" + KEY
GET_SITE_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/%s?res=3hourly&key=" + KEY
GET_SITE_DATA = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key=" + KEY

SITES = []

if os.environ.has_key('HTTP_PROXY'):
    proxy = urllib2.ProxyHandler({'http': os.environ['HTTP_PROXY']})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)


PARAM_INDEXES = {
    "uv":0,
    "temp":1,
    "wind_speed":2,
    "precip_prob":3,
    "humidity":4,
    "wind_gust":5
}

direction_to_deg = {
    'N':0,
    'NNE':22.5,
    'NE':45,
    'ENE':67.5,
    'E':90,
    'ESE':112.5,
    'SE':135,
    'SSE':157.5,
    'S':180,
    'SSW':202.5,
    'SW':225,
    'WSW':247.5,
    'W':270,
    'WNW':292.5,
    'NW':315,
    'NNW':337.5
}

def get_sites():
    global SITES
    cache_file = 'sites.json'

    if len(SITES) > 0:
        return SITES

    if not os.path.exists(cache_file):
        req = urllib2.Request(url=(GET_SITE_DATA))
        res = urllib2.urlopen(req)
        with open(cache_file, 'w') as fp:
            fp.write(res.read())

    with open(cache_file) as fp:
        data = json.load(fp)
        SITES = {site['id']:site_name(site) for site in data['Locations']['Location']}

    return SITES

def site_name(site):
    max_len = len('Hamilton (South Lana')
    name = ''
    if (site.has_key('unitaryAuthArea')):
        name = "%s (%s)" % (site['name'], site['unitaryAuthArea'])
    else:
        name = site['name']
    if len(name) > max_len:
        name = name[:(max_len - 3)] + '...'
    return name

def rand_site():
    sites = get_sites()
    id = random.choice(sites.keys())
    return (id, sites[id])

def get_a_forecast(site):
    req = urllib2.Request(url=(GET_SITE_URL % site))
    res = urllib2.urlopen(req)
    data = json.load(res)
    forecasts = []
    for period in data['SiteRep']['DV']['Location']['Period']:
        basedt = datetime.datetime.strptime(period['value'][:-1]+'UTC', "%Y-%m-%d%Z")
        for rep in period['Rep']:
            mins = int(rep['$'])
            valid_time = basedt + datetime.timedelta(minutes=mins)
            forecast = {
                'wind_dir':rep['D'],
                'wind_speed':float(rep['S']),
                'temp':float(rep['T']),
                'type':int(rep['W']),
                'datetime': valid_time,
                'wind_dir_deg':direction_to_deg[rep['D']],
                'prob_precip': float(rep['Pp']),
                'wind_gust':float(rep['G'])
            }
            forecasts.append(forecast)
    return forecasts

def feels_like_temp_training_set():
    X, Y = [], []
    print ("Grabbing 3 hourly weather forecast from Met Office datapoint")
    req = urllib2.Request(url=GET_ALL_URL)
    res = urllib2.urlopen(req)
    data = json.load(res)

    # Grab all the numeric weather parameters to make our feature vector x and put in to the collection X
    # Grab the feels like temp and stick it in our collection Y, this is what we are aiming to guess.
    for i, loc in enumerate(data['SiteRep']['DV']['Location']):
        for period in loc['Period']:
            for rep in period['Rep']:
                X.append([
                    float(rep['U']),
                    float(rep['T']),
                    float(rep['S']),
                    float(rep['Pp']),
                    float(rep['H']),
                    float(rep['G'])
                ])
                Y.append(float(rep['F']))

    return X, Y
