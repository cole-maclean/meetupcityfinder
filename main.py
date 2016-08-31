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

#load top 250 cities list by population
city_country_list = []
with open('cities.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        city_country_list.append(', '.join([row[1],row[2]]))

def get_meetup_data():   

    with open('group_list.json', 'r') as infile:
        group_list = json.load(infile) #load group list from data cache
    with open('meetup_data.json', 'r') as infile:
        city_topic_data = json.load(infile) #load topic data from data cache

    groups_per_page = 200 #max results per page from meetup.com api

    for j,city_country in enumerate(city_country_list): #enumerate over each city in city list to use a centroids for meetup.com API requests
        print(str(round(j/len(city_country_list)*100,1)) + " percent complete")
        print("city " + str(j))
        geo = gmaps.geocode(city_country) #get GPS coords from city using gmaps API
        lat = geo[0]['geometry']['location']["lat"]
        lon = geo[0]['geometry']['location']["lng"]
        groups = client.GetGroups(lat=lat, lon=lon,radius=300)
        time.sleep(1)
        pages = int(groups.meta['total_count']/groups_per_page) #get total pages needed to iterate over total request dataset
        print(groups.meta['total_count'])
        for i in range(0,pages + 1):
            print("page " + str(i) + "/" + str(pages))
            groups = client.GetGroups(lat=lat, lon=lon,radius=300,fields=['topics'],pages=groups_per_page,offset=i)
            time.sleep(1)
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
                                key = topic_name + "-" + city #data is uniquely keyed on topic and city
                                if key in city_topic_data.keys(): #if topic-city key exists in dict, then add new groups membership to existing memebers in topic-city key
                                    members = city_topic_data[key]["members"]
                                    city_topic_data[key] = {"topic":topic_name,
                                                             "city":city,
                                                             "members": members + group["members"],
                                                             "lat":group["lat"],
                                                             "lon":group["lon"]}
                                else: #else initialize unique city-topic key with current groups members
                                    city_topic_data[key] = {"topic":topic_name,
                                                             "city":city,
                                                             "members": group["members"],
                                                             "lat":group["lat"],
                                                             "lon":group["lon"]}
                        except KeyError as e:
                                print(e)
        with open('group_list.json', 'w') as outfile:
            json.dump(group_list, outfile)
        with open('meetup_data.json', 'w') as outfile:
            json.dump(city_topic_data, outfile)

    

def filter_grouped_topic_data():
    min_members = 100
    with open('meetup_data.json', 'r') as infile:
        data = json.load(infile)
    topic_data = sorted([data[record_key] for record_key in data.keys()], key=lambda k: k['members'],reverse=True)
    filtered_data = [datum for datum in topic_data if datum["members"] >= min_members]

    with open('grouped_topic_data.json', 'w') as outfile:
        json.dump(filtered_data, outfile)

#get_meetup_data()
filter_grouped_topic_data()