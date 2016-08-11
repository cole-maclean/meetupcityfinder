from math import radians, cos, sin, asin, sqrt
import json
import configparser
import googlemaps
import time
import geohash
import os
import fasteners

config = configparser.ConfigParser()
config.read("secrets.ini")
API_key = config['google']['google_API']
gmaps = googlemaps.Client(key=API_key)


def load_pop_dict():
    with open('populations.json', 'r') as f:
        p_dict = json.load(f)
    return p_dict

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
#reverse lon/lat positions of a GPS tuple
def reverse_GPS(GPS):
    return [GPS[1],GPS[0]]


def get_geohash_directions(gh_A,gh_B):
    try:
        with open("google_directions_cache.json","r") as f:
            google_directions_cache = json.load(f)
    except ValueError:
        GPS_A = geohash.decode(gh_A)
        GPS_B = geohash.decode(gh_B) 
        directions_result = gmaps.directions(GPS_A,
                                             GPS_B,
                                             mode="driving")
        connection_data =({'distance':directions_result[0]['legs'][0]['distance']['value'],
                           'steps':len(directions_result[0]['legs'][0]['steps'])})
        time.sleep(1)
        print ("failed cache read")
        return connection_data
    sorted_hashes = sorted([gh_A,gh_B])
    connection_key = sorted_hashes[0] + sorted_hashes[1]
    if connection_key in list(google_directions_cache.keys()):
        connection_data = google_directions_cache[connection_key]
    else:
        GPS_A = geohash.decode(gh_A)
        GPS_B = geohash.decode(gh_B) 
        directions_result = gmaps.directions(GPS_A,
                                             GPS_B,
                                             mode="driving")
        connection_data =({'distance':directions_result[0]['legs'][0]['distance']['value'],
                           'steps':len(directions_result[0]['legs'][0]['steps'])})
        google_directions_cache[connection_key] = connection_data
        with open("google_directions_cache.json","w") as f:
                json.dump(google_directions_cache,f)
        time.sleep(1)
    return connection_data

def gh_expansion(seed_gh,exp_iters):
    expansion_ghs = {0:[seed_gh]}
    ghs = []
    for i in range(1,exp_iters+1):
        expansion_ghs[i] = []
        for gh in expansion_ghs[i-1]:
            expansion_ghs[i] = expansion_ghs[i] + geohash.expand(gh)
            ghs = ghs + geohash.expand(gh)
    return list(set(ghs))

def get_close_ghs(src_hash,lookup_hash_list,gh_precision,exp_iterations,max_haversine):
    exp_src_hash = gh_expansion(src_hash[0:gh_precision],exp_iterations)
    if max_haversine == -1:
        return [gh for gh in lookup_hash_list if gh[0:gh_precision] in exp_src_hash]
    else:
        return [gh for gh in lookup_hash_list
                    if gh[0:gh_precision] in exp_src_hash
                    and haversine(*reverse_GPS(geohash.decode(src_hash)),*reverse_GPS(geohash.decode(gh))) <= max_haversine]

def get_gh_city(gh):
    with open("google_geocity_cache.json","r") as f:
            google_geocity_cache = json.load(f)
    if gh in list(google_geocity_cache.keys()):
         city = google_geocity_cache[gh]
    else:
        location = gmaps.reverse_geocode(geohash.decode(gh))
        city = location[0]["formatted_address"].split(",")[1]
        time.sleep(1)
        google_geocity_cache[gh] = city
        with open("google_geocity_cache.json","w") as f:
                json.dump(google_geocity_cache,f)
        time.sleep(1)
    return city

def get_address_gps(address):
    address_geocode = gmaps.geocode(address)
    return address_geocode