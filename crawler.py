# page crawler 
import bs4
import urllib3
import csv
import string
import re
import json
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def crawl_page():

    url_prefix = 'https://www.tripadvisor.com'
    starting_url = 'https://www.tripadvisor.com/Attractions-g28926-Activities-California.html#LOCATION_LIST'
    soup = make_soup(starting_url)
    city_list = soup.find_all("div", class_="ap_navigator")
    ct_list = [city.find("a").get("href") for city in city_list[3:-1]]
    
    #page_redirector_url = url_prefix + city_list[-1].find("a").get("href")
    #soup = make_soup(page_redirector_url)

    attraction_dict = {}

    for num in range(20, 970, 50):
        url = "https://www.tripadvisor.com/Attractions-g28926-Activities-oa{}-California.html".format(num)
        soup = make_soup(url)
        geoList = soup.find_all("ul", class_="geoList")[0]
        city_list = geoList.find_all("a")

        ct_list += [city.get("href") for city in city_list]
        for ct in ct_list:
            ct_url = url_prefix + ct
            explore_city(ct_url, url_prefix, attraction_dict)


def explore_city(city_url, url_prefix, attraction_dict):

    page_soup = make_soup(city_url)
    
    # if the city has multiple pages of attractions 
    if page_soup.find('div', class_='unified pagination '): 

        while not page_soup.find_all('span', class_ ='nav next disabled'):
            add_dictionary(attraction_dict, page_soup, url_prefix)
            next_page = page_soup.find('a', class_='nav next rndBtn ui_button primary taLnk')
            print("turn page")
            if next_page:
                url = url_prefix + next_page.get('href')
                page_soup = make_soup(url)
    else:
        add_dictionary(attraction_dict, page_soup, url_prefix)



def add_dictionary(attraction_dict, page_soup, url_prefix):

    for listing in page_soup.find_all("div", class_="listing_title "):
        url = url_prefix + listing.find("a").get("href")
        print("pass")
        soup = make_soup(url)
        if soup.find('script', type='application/ld+json'):  # if it is  an attraction

            attraction_id = soup.find('script', type='application/ld+json').get_text()
            attraction_id = json.loads(attraction_id)
            name = attraction_id['name']
            if name not in attraction_dict:
                attraction_dict[name] = attraction_id



def make_soup(url):

    pm = urllib3.PoolManager()
    html = pm.urlopen(url=url, method="GET").data

    # set the crawler to sleep for 2 secs to avoid blocking 
    #time.sleep(2)
    soup = bs4.BeautifulSoup(html, "html5lib")

    return soup


def find_geolocation(attraction_dict):

    GOOGLE_MAP_API_KEY = "AIzaSyBOrt_ShtRC1-O-KFUR0S2PQ3Ir6zXMzTY"

    geo_dict = {}
    for attraction in attraction_dict:

        request = "https://maps.googleapis.com/maps/api/geocode/json?\
        address={}&key={}".format(attraction, GOOGLE_MAP_API_KEY)

        if request["status"] == "OK":
            if attraction not in geo_dict:
                geo_dict[attraction] = request['geometry']['location']

    return geo_dict



######### sentiment analysis NLP ##############























