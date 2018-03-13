#### CAPP30122 Project
# Ruxin Chen and Mengchen Shi 

###############################################################################
    
    # To run this, you need to install selenium package, and its Chrome driver.
    # Run $ pip install selenium
    # Installation Guideline:
    # http://selenium-python.readthedocs.io/installation.html
    # Chrome Driver Installation Guideline:
    # https://sites.google.com/a/chromium.org/chromedriver/downloads

###############################################################################

from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

class ChromeDriver():

    '''
    The ChromeDriver class is a driver of chrome browser that can
    be used to mimic and automate the operations of a webpage such
    as turn pages and click button.
    Input:
    url: the underlying url of the web driver object
    '''

    def __init__(self, url):

        '''
        Construct a driver of Chrome and direct to the given url.
        If the webdriver fails to implement the above operations,
        print "unable to set up Chrome Driver" and quit the driver. 

        '''

        self.url = url
        try:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(10)
            self.driver.set_window_size(1024,768)
            self.driver.get(self.url)
        except:
            print("Unable to set up Chrome Driver")
            self.driver.quit()

    def is_attraction(self):
        '''
        The function determines wether the current driver is generated from
        an attraction page. If it is the case, the function returns the info
        for this attraction written in html. if otherwise, the function returns
        None. 
        '''

        # tripadvisor writes the info for each attraction in its html under a 
        # script tag specified as follows, and this tag exists only in 
        # attraction page. 
        is_attraction = self.driver.find_elements_by_xpath("//script[@type = \
            'application/ld+json']")
        if is_attraction:
            return is_attraction[0]
        else:
            return None


    def click_more(self):

        '''
        The click_more method can be used to simulate click "more"
        button when we visit the review section of attraction pages
        '''

        more_xpath = "//*[contains(@onclick, 'handlers.clickExpand')]"
        # find the click more handler 
        more = self.driver.find_elements_by_xpath(more_xpath)

        # determine if the page contains reviews that needs to be expanded
        if more:
            try:
                # the webdriver is not very stable so we use print to 
                # moniter the process of our crawler function. 
                print('click')
                # the click handler function is designed to be applied to 
                # all "more" buttons on the remaining page 
                more[0].click()

            except:
                print("Wait To Click")
                # let the function wait 3 secs for the new page to completedly
                # upload 
                time.sleep(3)
                more[0].click()


    def turn_page(self):

        '''
        The turn_page method can be used to simulate the action of
        turning page of review section of attractions
        '''

        try:
            # find the turn page handler 
            next_disable = self.driver.find_elements_by_xpath(\
                "//span[@class = 'nav next ui_button primary disabled']")
        except:
            print("ERROR")

        # if the current page is not the last page for the attraction, click 
        # next button to turn page 
        if not next_disable:
            next_page = self.driver.find_elements_by_xpath("\
                //span[@class = 'nav next taLnk ui_button primary'][@onclick]")[0].click()


    def add_reviews(self, attraction_id):
        '''
        Scrape content of reviews (date, stars, title, text) and add it to the
        dictionay of the given attraction
        Inputs:
        attraction_id (dict): an attraction
        soup: a beautiful soup object
        '''

        reviews = list()
        page = 1

        while self.driver.find_elements_by_xpath("//span[@class='nav next \
            taLnk ui_button primary']"):
            try:
                self.click_more()
                time.sleep(1)
                star_list = self.driver.find_elements_by_xpath("//div[@class =\
                     'ratingInfo']")

                div_list = self.driver.find_elements_by_xpath("//div[@class \
                    = 'prw_rup prw_reviews_category_ratings_hsx']")

                for i in range(len(div_list)): 

                    div = div_list[i].find_elements_by_xpath("..//\
                        preceding-sibling::div")

                    date = div[0].text.split('\n')[0]

                    review = tuple()
                    review += date,

                    stars = int(star_list[i].find_element_by_tag_name('span'\
                        ).get_attribute('class')[-2: ])/10
                    review += stars,

                    title = div[4].text
                    review += title,

                    print(review)

                    text = div[5].text
                    review += text,

                    reviews.append(review)

            except StaleElementReferenceException:
                self.driver.quit()
                continue

            except NoSuchElementException:
                self.driver.quit()
                continue

            print("page complete: ", page)
            page += 1
            if page > 20:
                attraction_id['reviews'] = reviews
                self.driver.quit()
                print('complete 20 pages: ', attraction_id['reviews'][-1])
                break
            self.turn_page()
            time.sleep(2)

            if self.driver.find_elements_by_xpath("//span[@class \
                = 'nav next ui_button primary disabled']"):
                break










