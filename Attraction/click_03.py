#### CAPP30122 Project
# Ruxin Chen

from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

class ChromeDriver():

    '''
    The ChromeDriver class is a driver of chrome browser that can
    be used to mimic and automate the operations of a webpage such
    as turn pages and click button.
    Input:
    url: the underlying url of the web driver object
    '''

    def __init__(self, url):

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
        is_attraction = self.driver.find_elements_by_xpath("//script[@type = 'application/ld+json']")
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
        more = self.driver.find_elements_by_xpath(more_xpath)
        if more:
            try:
                print('click')
                more[0].click()
            except:
                print("wait To Click")
                time.sleep(3)
                more[0].click()


    def turn_page(self):

        '''
        The turn_page method can be used to simulate the action of
        turning page of review section of attractions
        '''

        try:
            next_disable = self.driver.find_elements_by_xpath(\
                "//span[@class = 'nav next ui_button primary disabled']")
        except:
            print("ERROR")

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
        while self.driver.find_elements_by_xpath("//span[@class='nav next taLnk ui_button primary']"):
            try:
                self.click_more()
                time.sleep(1)
                star_list = self.driver.find_elements_by_xpath("//div[@class = 'ratingInfo']")

                div_list = self.driver.find_elements_by_xpath("//div[@class = 'prw_rup prw_reviews_category_ratings_hsx']")

                for i in range(len(div_list)): # There are 10 review per page

                    #date = date_list[i]
                    div = div_list[i].find_elements_by_xpath("..//preceding-sibling::div")

                    date = div[0].text.split('\n')[0]
                    #%print(date)
                    '''
                    if date[-4:] == "2016":
                        attraction_id['reviews'] = reviews
                        self.driver.quit()
                        return
                    '''

                    review = tuple()
                    review += date,

                    stars = int(star_list[i].find_element_by_tag_name('span').get_attribute('class')[-2: ])/10
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
            self.turn_page()
            time.sleep(2)
            page += 1

            if self.driver.find_elements_by_xpath("//span[@class \
                = 'nav next ui_button primary disabled']"):
                break
            if page > 20:
                attraction_id['reviews'] = reviews
                self.driver.quit()
                print('complete 20 pages: ', attraction_id['reviews'][-1])
                break


        #attraction_id['reviews'] = reviews
        #return attraction_id
        #self.driver.quit()








