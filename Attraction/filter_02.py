###### CAPP30122
# Ruxin Chen
import bs4
import urllib3
import csv
import string
import re
import json
import time
import click

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def crawl_page():

    limiting_domain = 'https://www.tripadvisor.com'
    starting_url = 'https://www.tripadvisor.com/Attractions-g28926-Activities-California.html#LOCATION_LIST'

    soup = make_soup(starting_url)
    city_list = soup.find_all("div", class_="ap_navigator")
    ct_list = [city.find("a").get("href") for city in city_list[3:-1]]

    #ct_list = [] # DELETE IT!!!!!

    attraction_dict = {}

    for num in range(20, 970, 50):
    #for num in range(920, 970, 50):
        url = "https://www.tripadvisor.com/Attractions-g28926-Activities-oa{}-California.html".format(num)
        #print(url)
        soup = make_soup(url)
        geoList = soup.find_all("ul", class_="geoList")[0]
        city_list = geoList.find_all("a")

        ct_list += [city.get("href") for city in city_list]

    for ct in ct_list:
        ct_url = limiting_domain + ct
        #print(ct_url)
        explore_city(ct_url, limiting_domain, attraction_dict)

    with open('url_review_num.json', 'w') as file:
            file.write(json.dumps(attraction_dict))

    return attraction_dict



def explore_city(city_url, limiting_domain, attraction_dict):

    page_soup = make_soup(city_url)


    # if the city has multiple pages of attractions
    if page_soup.find('div', class_='unified pagination '):

        while not page_soup.find_all('span', class_ ='nav next disabled'):
            add_dictionary(attraction_dict, page_soup, limiting_domain, city_url)
            next_page = page_soup.find('a', class_='nav next rndBtn ui_button primary taLnk')

            if next_page:
                url = limiting_domain + next_page.get('href')
                page_soup = make_soup(url)
    else:
        add_dictionary(attraction_dict, page_soup, limiting_domain, city_url)



def add_dictionary(attraction_dict, page_soup, limiting_domain, city_url):
    count = 0

    for listing in page_soup.find_all("div", class_="listing_title "): # city level

        name = listing.find('a').text
        if name in attraction_dict:
            continue
        else:
            review_tag = listing.find_next_sibling('div', class_='listing_rating')

            if review_tag.find('a'):
                review_count = int(review_tag.find('a').text.strip().split()[0].replace(',',''))

                #if review_count < 1000:
                    #continue
                #else:
                url = limiting_domain + listing.find("a").get("href")
                print((name, url, review_count))
                attraction_dict[name] = (url, review_count)



def make_soup(url):

    pm = urllib3.PoolManager()
    html = pm.urlopen(url=url, method="GET").data

    # set the crawler to sleep for 2 secs to avoid blocking
    # time.sleep(2)
    soup = bs4.BeautifulSoup(html, "html5lib")

    return soup












