#### CAPP30122 Project 
# Ruxin Chen 

from selenium import webdriver
import time 
from selenium.webdriver.support.ui import Select 

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


    def click_more(self):

        '''
        The click_more method can be used to simulate click "more"
        button when we visit the review section of attraction pages 
        '''

        more_xpath = "//*[contains(@onclick, 'handlers.clickExpand')]"
        more = self.driver.find_elements_by_xpath(more_xpath)
        if more: 
            try:
                more[0].click()
            except:
                print("Unable To Click")


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

        reviews = set()

        #star_list = soup.find_all('div',class_='ratingInfo')
        #div_list = soup.find_all('div', class_='prw_rup prw_reviews_category_ratings_hsx')
        #tilte_list = soup.find_all('span', class_='noQuotes')
        #date_list = soup.find_all('span', class_='')

        while self.driver.find_elements_by_xpath("//span[@class='nav next taLnk ui_button primary']"):

            self.click_more()
            time.sleep(1)
            star_list = self.driver.find_elements_by_xpath("//div[@class = 'ratingInfo']")
            div_list = self.driver.find_elements_by_xpath("//p[@class = 'partial_entry']")
            title_list = self.driver.find_elements_by_class_name("noQuotes")
            date_list = self.driver.find_elements_by_xpath("//span[@class='ratingDate relativeDate'][@title ='']")
            date_list = [date_list[i].text for i in range(len(date_list))]
            for i in range(len(date_list)): # There are 10 review per page

                date = date_list[i]
                print(date)
                if date[-4:] == "2016":
                    break

                review = tuple()
                review += date,
                print("pass")
                print(len(star_list))
    
                stars = int(star_list[i].find_element_by_tag_name('span').get_attribute('class')[-2: ])/10
                review += stars,
   
                title = title_list[i].text
                review += title,
                print(review)
    
                text = div_list[i].text
                review += text,
                reviews |= {review}
                #time.sleep(0.5)

            self.turn_page()
            print("turn page")
            time.sleep(0.5)
    
            if self.driver.find_elements_by_xpath("//span[@class \
                = 'nav next ui_button primary disabled']"):
                break 
           

        attraction_id['reviews'] = reviews
        #self.driver.quit()








