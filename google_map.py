import googlemaps 
import json

def find_attributes(jsonfile, start, end, GOOGLE_API_KEY):

    with open(jsonfile, 'r') as file:
        attraction_dict = json.load(file)

    lst = [attraction for attraction in attraction_dict]

    # GOOGLE_API_KEY = "AIzaSyBOrt_ShtRC1-O-KFUR0S2PQ3Ir6zXMzTY"
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

    new_dictionary = {}

    for attraction in lst[start:end]:
        query = attraction.replace(" ", "+")
        request = gmaps.places(query=query)

        if request["status"] == "OK":
            new_dictionary[attraction] = request["results"]
        else:
            new_dictionary[attraction] = None 

    with open("attraction_{}_{}.json".format(start, end), "w") as file:
        file.write(json.dumps(attraction_dict))
