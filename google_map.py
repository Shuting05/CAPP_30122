import googlemaps 
import json
import sched, time

def find_attributes(jsonfile, start, end, GOOGLE_API_KEY, request_rate=50):

    # GOOGLE_API_KEY = "AIzaSyBOrt_ShtRC1-O-KFUR0S2PQ3Ir6zXMzTY"

    with open(jsonfile, 'r') as file:
        attraction_dict = json.load(file)

    lst = [attraction for attraction in attraction_dict]


    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

    new_dictionary = {}
    failed_request = set()
    fail = 0

    for attraction in lst[start:end]:
        query = attraction.replace(" ", "+")

        # sleep to avoiding exceeding the request rate 
        request_per_second = 1.0/request_rate
        time.sleep(request_per_second)

        try: 
            request = gmaps.places(query=query)
            pass 
        except:
            fail += 1
            print("Request Failed:", query, fail)
            failed_request.add(query)
            continue 

        if request["status"] == "OK":
            new_dictionary[attraction] = request["results"][0]
        else:
            new_dictionary[attraction] = None 


    with open("attraction_{}_{}.json".format(start, end), "w") as file:
        file.write(json.dumps(new_dictionary))

    if failed_request:
        with open("failed_{}_{}.json".format(start, end), "w") as file:
            file.write(json.dumps(dict(failed_request)))

 

'''
scheduler = sched.scheduler(time.time, time.sleep)

def send_request(query, GOOGLE_API_KEY):

    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

    request = gmaps.places(query=query)

    return request


def new_timed_request(request_per_second):

    period = 1.0/ request_per_second
    scheduler.enter(period, send_request, )
'''



