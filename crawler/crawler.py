###### CAPP30122
# Ruxin Chen and Mengchen Shi 
###############################################################################
    
    # To run this, you need to install selenium package, and its Chrome driver.
    # Run $ pip install selenium
    # Installation Guideline:
    # http://selenium-python.readthedocs.io/installation.html
    # Chrome Driver Installation Guideline:
    # https://sites.google.com/a/chromium.org/chromedriver/downloads

###############################################################################
import bs4
import urllib3
import csv
import string
import re
import json
import time
import click

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def crawl_page(begin_page, end_page, filename):
    '''
    The function crawls the "attraction by city" page and collects 
    all information for attractions and writes into a json file. 
    The begin_page and end_page is set as parameter for our team
    to split the scraping work.  

    Input:
    begin_page, end_page(int): the page we start and end crawling 
    filename(str): the name of our output file 
    '''

    limiting_domain = 'https://www.tripadvisor.com'
    starting_url = 'https://www.tripadvisor.com/Attractions-g28926-\
        Activities-California.html#LOCATION_LIST'

    ct_list = []

    attraction_dict = {}

    for num in range(begin_page, end_page, 50):
        url = "https://www.tripadvisor.com/Attractions-g28926-\
        Activities-oa{}-California.html".format(num)
        soup = make_soup(url)
        geoList = soup.find_all("ul", class_="geoList")[0]
        city_list = geoList.find_all("a")

        ct_list += [city.get("href") for city in city_list]

    for ct in ct_list:
        ct_url = limiting_domain + ct
        explore_city(ct_url, limiting_domain, attraction_dict)

    with open(filename, 'w') as file:
        file.write(json.dumps(attraction_dict))

    return attraction_dict


def explore_city(city_url, limiting_domain, attraction_dict):
    '''
    The function visits page for each city and adds the information
    we needed for attractions to attraction_dict. 

    Inputs:
    city_url: the url for each city 
    limiting_domain: a string of url of limiting domain
    attraction_dict: 
    the dictionary that contains the info needed for each attraction

    '''

    page_soup = make_soup(city_url)

    # if the city has multiple pages of attractions
    if page_soup.find('div', class_='unified pagination '):

        while not page_soup.find_all('span', class_ ='nav next disabled'):
            add_dictionary(attraction_dict, page_soup, limiting_domain)
            next_page = page_soup.find('a', class_='nav next rndBtn ui_button\
                 primary taLnk')

            print("turn page")
            if next_page:
                url = limiting_domain + next_page.get('href')
                page_soup = make_soup(url)
    else:
        add_dictionary(attraction_dict, page_soup, limiting_domain)


def add_dictionary(attraction_dict, page_soup, limiting_domain):
    '''
    The function visits each attraction page and scrape the first 200
    reviews if the total number of reviews for that attraction is more 
    than 1000 (we think the number of reviews can reflect the level of 
    popularity for each attraction), and then add them to the attraction_dict.

    Input: 
    attraction_dict:
    the dictionary that contains the info needed for each attraction
    page_soup:
    the soup object created in explore_city function(at the city level)
    limiting_domain:
    a string of url of limiting domain

    '''

    for listing in page_soup.find_all("div", class_="listing_title "):

        name = listing.find('a').text
        if name in attraction_dict:
            continue
        else:
            review_tag = listing.find_next_sibling('div', \
                class_='listing_rating')

            if review_tag.find('a'):
                review_count = int(review_tag.find('a').text.strip(\
                    ).split()[0].replace(',',''))

                if review_count < 1000:
                    continue

                else:
                    url = limiting_domain + listing.find("a").get("href")
                    # create a driver for each attraction and expand all 
                    # the reviews
                    c = click_03.ChromeDriver(url)
                    print('new attraction')

                    is_attraction = c.is_attraction()

                    if is_attraction:
                        attraction_id = json.loads(\
                            is_attraction.get_attribute('text'))

                        attraction_dict[name] = attraction_id
                        c.add_reviews(attraction_id)
                    else:
                        c.driver.quit()
                        continue
            else:
                continue


def make_soup(url):
    '''
    The function takes a url and turns it into a soup object
    '''
    pm = urllib3.PoolManager()
    html = pm.urlopen(url=url, method="GET").data
    soup = bs4.BeautifulSoup(html, "html5lib")

    return soup










