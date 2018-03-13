#### CAPP30122 Project 
# Ruxin Chen 
###############################################################################
    
    # To run this, you need to get a google map api key and install googlemaps 
    # Run $ pip install -U googlemaps in terminal 
    # Reference page:
    # https://github.com/googlemaps/google-maps-services-python

###############################################################################
import googlemaps 
import json
import time

def find_attributes(jsonfile, start, end, GOOGLE_API_KEY, request_rate=50):

    '''
    The find_attributions function takes a GOOGLE map api key to send request 
    for the infomation of attractions stored in the jsonfile and write an output
    jsonfile of the responses from google.

    Input:
    jsonfile: a dictionary 
    start, end(int): there are 10000+ attractions in total so we set the
    start and end parameter to split the request workload in our team. 
    GOOGLE_API_KEY : the required key to request from google api 
    reqeust_rate: the max per sec request rate set by google 

    '''
    # GOOGLE_API_KEY = "AIzaSyBOrt_ShtRC1-O-KFUR0S2PQ3Ir6zXMzTY"

    with open(jsonfile, 'r') as file:
        attraction_dict = json.load(file)

    lst = [attraction for attraction in attraction_dict]
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

    new_dictionary = {}
    failed_request = {}

    for attraction in lst[start:end]:
        query = attraction.replace(" ", "+")

        # sleep to avoiding exceeding the request rate 
        request_per_second = 1.0/request_rate
        time.sleep(request_per_second)

        try: 
            request = gmaps.places(query=query)
            pass 
        except:
            print("Request Failed:", query, fail)
            failed_request[attraction] = None
            continue 

        if request["status"] == "OK":
            new_dictionary[attraction] = request["results"][0]
        else:
            new_dictionary[attraction] = None 

    with open("attraction_{}_{}.json".format(start, end), "w") as file:
        file.write(json.dumps(new_dictionary))

    if failed_request:
        with open("failed_{}_{}.txt".format(start, end), "w") as file:
            file.write(json.dumps(failed_request))


##############################################################################
# Auxiliary functions: merge_file() and merge(f)
# The two functions are used to merge and process the data we collected 
# For simplicity, we only upload the final file "Attractions.json" and 
# "review.json" in our data folder 
##############################################################################


def merge_file(file1, file2, file3):
    '''
    The function combines the files we obtained in find_attributes 
    function and write a json file named "Attractions.json" 

    '''
    with open(file1, 'r') as file:
        f1 = json.load(file)

    with open(file2, 'r') as file:
        f2 = json.load(file)

    with open(file3, 'r') as file:
        f3 = json.load(file)

    f1.update(f2)
    f1.update(f3)

    with open("Attractions.json", "w") as file:
        file.write(json.dumps(f1))


def merge(f):
    '''
    The function merges the review data we collected in to one file 
    '''
    f = pd.read_csv('att.csv', header = None)

    total = {}

    for i in range(f.shape[0]):

        with open("reviews_dta/{}.json".format(f.iloc[i, 0]), 'r') as file:
            f1 = json.load(file)

        total.update(f1)

    with open("review.json", "w") as file:
        file.write(json.dumps(total))







