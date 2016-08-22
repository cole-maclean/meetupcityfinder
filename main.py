import os
import configparser
import meetup.api
import csv
import googlemaps
import time
import json
import geohash
import pandas as pd
from collections import defaultdict, Counter
os.chdir("C:/Users/macle/Desktop/Data Journalism/meetup city finder")

config = configparser.ConfigParser()
config.read('secrets.ini')

meetup_api_key = config.get('meetup', 'api_key')
gmaps_api_key = config.get('google', 'api_key')

gmaps = googlemaps.Client(key=gmaps_api_key)

client = meetup.api.Client(meetup_api_key)

city_country_list = []
with open('cities.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        city_country_list.append(', '.join([row[1],row[2]]))

def get_meetup_data():   

    group_list = []
    groups_per_page = 200
    city_topic_data = {}

    for j,city_country in enumerate(city_country_list):
        print("city index = " + str(j))
        geo = gmaps.geocode(city_country)
        lat = geo[0]['geometry']['location']["lat"]
        lon = geo[0]['geometry']['location']["lng"]
        groups = client.GetGroups(lat=lat, lon=lon,radius=300)
        time.sleep(1)
        pages = int(groups.meta['total_count']/groups_per_page)
        print(groups.meta['total_count'])
        for i in range(0,pages + 1):
            print("page " + str(i))
            groups = client.GetGroups(lat=lat, lon=lon,radius=300,fields=['topics'],pages=groups_per_page,offset=i)
            time.sleep(1.5)
            if "results" in groups.__dict__.keys():
                for group in groups.results:
                    if group["id"] not in group_list:
                        group_list.append(group["id"])
                        if "state" in group.keys():
                            state = group["state"]
                            city = group["city"] + "," + state + "," + group["country"]
                        else:
                            state = "00"
                            city = group["city"] + "," + group["country"]
                        try:
                            for topic in group["topics"]:
                                topic_name = topic["name"].lower()
                                key = topic_name + "-" + city
                                if key in city_topic_data.keys():
                                    members = city_topic_data[key]["members"]
                                    city_topic_data[key] = {"topic":topic_name,
                                                             "city":city,
                                                             "members": members + group["members"],
                                                             "lat":group["lat"],
                                                             "lon":group["lon"]}
                                else:
                                    city_topic_data[key] = {"topic":topic_name,
                                                             "city":city,
                                                             "members": group["members"],
                                                             "lat":group["lat"],
                                                             "lon":group["lon"]}

                        except KeyError as e:
                                print(e)
    topic_data = sorted([city_topic_data[record_key] for record_key in city_topic_data.keys()], key=lambda k: k['members'],reverse=True)

    with open('meetup_data.json', 'w') as outfile:
        json.dump(topic_data, outfile)

def filter_grouped_topic_data():
    min_members = 110
    with open('meetup_data.json', 'r') as infile:
        data = json.load(infile)
    filtered_data = [datum for datum in data if datum["members"] >= min_members]

    with open('grouped_topic_data.json', 'w') as outfile:
        json.dump(filtered_data, outfile)

get_meetup_data()
filter_grouped_topic_data()