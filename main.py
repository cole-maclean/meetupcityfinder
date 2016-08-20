import os
import configparser
import meetup.api
import csv
import googlemaps
import time
import json
import geohash
import pandas as pd

config = configparser.ConfigParser()
config.read('secrets.ini')

meetup_api_key = config.get('meetup', 'api_key')
gmaps_api_key = config.get('google', 'api_key')

gmaps = googlemaps.Client(key=gmaps_api_key)

client = meetup.api.Client(meetup_api_key)

def build_grouped_topic_data():
    grouped_topic_data = []

    with open('meetup_data.json', 'r') as infile:
        meetup_data = json.load(infile)
        
    min_members = 100
    topic_count = len(meetup_data.keys())
    print(topic_count)
    perc_done = 0
    for i,topic in enumerate(list(meetup_data.keys())):
        if round(i/topic_count,2) != perc_done:
            perc_done = round(i/topic_count,2)
            print(str(perc_done) + "% done")
        else:
            perc_done = round(i/topic_count,2)
        topic_data = [data for data in meetup_data[topic] if data["members"] >= min_members]
        if topic_data:
            df = pd.DataFrame.from_dict(topic_data)
            grouped_data = df.groupby(by=['city','state','country'])['members'].sum()
            for indx,total_members in grouped_data.iteritems():
                    if indx[1] == "00":
                        city = indx[0] + "," + indx[2]
                    else:
                        city = indx[0] + "," + indx[1] + "," + indx[2]
                    with open('city_gps_cache.json', 'r') as infile:
                        city_gps_data = json.load(infile)
                    if city in city_gps_data.keys():
                        lat = city_gps_data[city][0]
                        lon = city_gps_data[city][1]
                    else:
                        geo = gmaps.geocode(city)
                        try:
                            lat = geo[0]['geometry']['location']["lat"]
                            lon = geo[0]['geometry']['location']["lng"]
                        except IndexError:
                            lat = 0
                            lon = 0
                        city_gps_data[city] = [lat,lon]
                        with open('city_gps_cache.json', 'w') as outfile:
                            json.dump(city_gps_data, outfile)
                    grouped_topic_data.append({"topic":topic,
                                               "city":city,
                                               "members":int(total_members),
                                               "lat":lat,
                                               "lon":lon})
    grouped_topic_data =sorted(grouped_topic_data, key=lambda k: k['members'],reverse=True)

    with open('grouped_topic_data.json', 'w') as outfile:
        json.dump(grouped_topic_data, outfile)

def test_build_topic_data():
    grouped_topic_data = []

    with open('meetup_data.json', 'r') as infile:
        meetup_data = json.load(infile)

    min_members = 100
    topic = 'social'
    topic_data = [data for data in meetup_data[topic] if data["members"] >= min_members]
    if topic_data:
        df = pd.DataFrame.from_dict(topic_data)
        grouped_data = df.groupby(by=['city','state','country'])['members'].sum()
        for indx,total_members in grouped_data.iteritems():
                if indx[1] == "00":
                    city = indx[0] + "," + indx[2]
                else:
                    city = indx[0] + "," + indx[1] + "," + indx[2]
                with open('city_gps_cache.json', 'r') as infile:
                    city_gps_data = json.load(infile)
                if city in city_gps_data.keys():
                    lat = city_gps_data[city][0]
                    lon = city_gps_data[city][1]
                else:
                    geo = gmaps.geocode(city)
                    try:
                        lat = geo[0]['geometry']['location']["lat"]
                        lon = geo[0]['geometry']['location']["lng"]
                    except IndexError:
                        lat = 0
                        lon = 0
                    city_gps_data[city] = [lat,lon]
                    with open('city_gps_cache.json', 'w') as outfile:
                        json.dump(city_gps_data, outfile)
                grouped_topic_data.append({"topic":topic,
                                           "city":city,
                                           "members":int(total_members),
                                           "lat":lat,
                                           "lon":lon})
    grouped_topic_data =sorted(grouped_topic_data, key=lambda k: k['members'],reverse=True)

    with open('grouped_topic_data.json', 'w') as outfile:
        json.dump(grouped_topic_data, outfile)

build_grouped_topic_data()