#### CAPP30122 Project 
# Ruxin Chen 
import bs4
import urllib3
import csv
import string
import re
import json
import math
import googlemaps 


class Factory():

    def __init__(self, jsonfile1):

        # set the attraction dictionary to be private ?
        self.data = self.create_from_file(jsonfile1)

    def create_from_file(self, jsonfile1):
        ''' output a list of attraction objects '''
        instance = dict()

        with open(jsonfile1, 'r') as file1:
            dictionary = json.load(file1)


        for attr, info in dictionary.items():
            attraction = Attraction(info)
            instance[attr] = attraction

        return instance

class Attraction():

    def __init__(self, dictionary):

        for k, v in dictionary.items():

            self.label = k
            #print(self.label)
            if "formatted_address" in v:
                self.address = v["formatted_address"]
            if "rating" in v: 
                self.rating = v["rating"]
            if "types" in v:
                self.type = v["types"]
            self.place_id = v["place_id"]
            self.location = v["geometry"]["location"]
            self.lat = self.location["lat"]
            self.lng = self.location["lng"]
            if "reviews" in v:
                self.reviews = v["reviews"]


    def theo_distance(self, other):  
        '''
        This is a theoretical/shortest distcence /could also send request to google map and get a
        a more realistic distance between the two spots. 
        '''

        R = 6371 # radius of the earth in km

        dlat = math.radians(other.lat - self.lat)
        dlng = math.radians(other.lng - self.lng)

        #print(dlat, dlng)

        haversine = math.sin(dlat/2) * math.sin(dlat/2) + \
        math.cos(math.radians(self.lat)) * math.cos(math.radians(other.lat)) *\
        math.sin(dlng/2) * math.sin(dlng/2)

        c = 2 * math.atan2(math.sqrt(haversine), math.sqrt(1 - haversine))
        distance = R * c 

        return distance

    def distance(self, other):
        # API key: AIzaSyBUsRf8MjvyiH6OujTYg6cvfy98Zc8snP0

        API_KEY = "AIzaSyBUsRf8MjvyiH6OujTYg6cvfy98Zc8snP0"
        gmaps = googlemaps.Client(key=API_KEY)

        try:
            request = gmaps.distance_matrix(origins= (self.lat,self.lng), \
                destinations=(other.lat,other.lng), mode = "driving")
            if request["status"] == "OK":
                return (request["rows"][0]['elements'][0]['distance']['value'])/1000
        except:
            print("Request failed, using straight line distance:", self.label, other.label)
            return self.theo_distance(other)


def find_shortest_dist(current, attraction_set, shortest_path):

    shortest_dist = math.inf
    for attr in attraction_set:
        dist = current.distance(attr) 
        if dist < shortest_dist:
            shortest_dist = dist
            shortest = attr
    shortest_path += shortest_path

    return shortest, shortest_path


def find_shortest_path(current_spot, attraction_set, \
    unvisited_set = None, order = None, shortest_path = 0):
    
    if unvisited_set is None:
        destination = find_shortest_dist(current, attraction_set, shortest_path)[0]
        unvisited_set = attraction_set.remove(destination)
        current = current_spot

    if order is None:
        order = []

    if not unvisited_set:
        return order, shortest_path
    else:
        shortest, shortest_path = find_shortest_dist(current, unvisited_set, shortest_path)
        unvisited_set.remove(shortest)
        order += [current]
        current = shortest
        find_shortest_path(current, destination, attraction_set, unvisited_set, order, shortest_path)









































