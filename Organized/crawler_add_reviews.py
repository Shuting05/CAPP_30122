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

    attraction_dict = {}

    for num in range(20, 970, 50):
        url = "https://www.tripadvisor.com/Attractions-g28926-Activities-oa{}-California.html".format(num)
        soup = make_soup(url)
        geoList = soup.find_all("ul", class_="geoList")[0]
        city_list = geoList.find_all("a")

        ct_list += [city.get("href") for city in city_list]
        for ct in ct_list:
            ct_url = limiting_domain + ct
            explore_city(ct_url, limiting_domain, attraction_dict)

    return attraction_dict


def explore_city(city_url, limiting_domain, attraction_dict):

    page_soup = make_soup(city_url)

    # if the city has multiple pages of attractions
    if page_soup.find('div', class_='unified pagination '):

        while not page_soup.find_all('span', class_ ='nav next disabled'):
            add_dictionary(attraction_dict, page_soup, limiting_domain)
            next_page = page_soup.find('a', class_='nav next rndBtn ui_button primary taLnk')
            print("turn page")
            if next_page:
                url = limiting_domain + next_page.get('href')
                page_soup = make_soup(url)
    else:
        add_dictionary(attraction_dict, page_soup, limiting_domain)



def add_dictionary(attraction_dict, page_soup, limiting_domain):

    for listing in page_soup.find_all("div", class_="listing_title "): # city level

        url = limiting_domain + listing.find("a").get("href")

        # create a driver for each attraction and expand all the reviews
        driver = click.ChromeDriver(url)
        driver.click_more()
        # create a new soup from the webpage after expanding the reviews
        #url = driver.current_url
        #soup = make_soup(url)

        #if soup.find('script', type='application/ld+json'):  # if it is  an attraction            
        #    attraction_id = soup.find('script', type='application/ld+json').get_text()
        #    attraction_id = json.loads(attraction_id)
        #    name = attraction_id['name']
        #    if name not in attraction_dict:
        #        attraction_dict[name] = attraction_id
        #        add_reviews(attraction_id, driver)

        is_attraction = driver.find_element_by_xpath("//script[@type = 'application/ld+json']"\
            ).get_attribute('text')
        if is_attraction:
            attraction_id = json.loads(is_attraction)
            name = attraction_id['name']
            if name not in attraction_dict:
                attraction_dict[name] = attraction_id
                driver.add_reviews(attraction_id)


def make_soup(url):

    pm = urllib3.PoolManager()
    html = pm.urlopen(url=url, method="GET").data

    # set the crawler to sleep for 2 secs to avoid blocking
    # time.sleep(2)
    soup = bs4.BeautifulSoup(html, "html5lib")

    return soup



def add_reviews(attraction_id, soup):
    '''
    Scrape content of reviews (date, stars, title, text) and add it to the
    dictionay of the given attraction

    Inputs:
    attraction_id (dict): an attraction
    soup: a beautiful soup object
    '''

    reviews = set()

    #star_list = soup.find_all('div',class_='ratingInfo')
    #div_list = soup.find_all('div', class_='prw_rup prw_reviews_category_ratings_hsx')
    #tilte_list = soup.find_all('span', class_='noQuotes')
    #date_list = soup.find_all('span', class_='')

    while driver.find_elements_by_xpath("//span[@class='nav next taLnk ui_button primary']"):

        star_list = driver.find_elements_by_class_name("ratingInfo")
        div_list = driver.find_elements_by_xpath("//p[@class = 'partial_entry']")
        title_list = driver.find_elements_by_class_name("noQuotes")
        date_list = driver.find_elements_by_xpath("//span[@class='ratingDate relativeDate']")
        date_list = [date_list[i].get_attribute("title") for i in range(0, len(date_list), 2)]
 
        for i in range(date_list): # There are 10 review per page

            if date[-4:] == "2016":
                break
                review = tuple()
                review += date,

                stars = int(star_list[i].find_element_by_tag_name('span').get_attribute(\
                    'class')[1][-2: ]) / 10
                review += stars,

                title = tilte_list[i].text
                review += title,

                text = div_list[i].text
                review += text,

        if driver.find_elements_by_xpath("//span[@class \
            = 'nav next ui_button primary disabled']"):
            break 
        driver.turn_page()
           
        reviews |= {review}
        attraction_id['reviews'] = reviews


'''
def embed_map():
  <iframe src= "https://www.google.com/maps/embed/v1/directions?\
  key={}&origin={}&destination={}\
  &mode={}".format(API_key,origin,destination, "driving")
'''










