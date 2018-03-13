###### CAPP30122
# Mengchen Shi

###############################################################################

    # To run this, you need to install selenium package, and its Chrome driver.
    # Run $ pip install selenium
    # Installation Guideline:
    # http://selenium-python.readthedocs.io/installation.html
    # Chrome Driver Installation Guideline:
    # https://sites.google.com/a/chromium.org/chromedriver/downloads

    # This crawler visits all attractions in given attraction_file,
    # scrapes their reviews and other attibutes, and save a json file for each
    # attraction once finishing one attraction to avoid interruption.
    # The printing indicates where the crawler is interrupted, so that
    # we can continue crawling from the fail attraction.

    # To begin, run the follwoing code in shell:
    # $python3 crawl_one_attraction.py attraction_url.csv 0


###############################################################################

import csv
import json
import click
import sys



def crawl_attr(attraction_file, begin_num):
    '''
    crawler attributes and reviews of attractions in the given file
    Inputs:
    attraction_file: name of a csv file
    begin_num: the number of attraction to crawl
    '''

    attr_name = []
    url = []
    with open(attraction_file) as csvfile:
        reader = csv.reader(csvfile)
        i = 0
        for row in reader:
            if i >= begin_num:
                attr_name.append(row[0])
                url.append(row[1])
            i += 1

    for i in range(begin_num, len(url)):
        name = attr_name[i]
        print(name, i)
        c = click.ChromeDriver(url[i])
        is_attraction = c.is_attraction()
        attr = json.loads(is_attraction.get_attribute('text'))
        c.add_reviews(attr)
        #print(len(attr['reviews']))
        attr_dict = {}
        attr_dict[name] = attr
        with open('{}.json'.format(name), 'w') as file:
            file.write(json.dumps(attr_dict))

if __name__ == "__main__":
    attraction_file_name = sys.argv[1]
    begin_num = int(sys.argv[2])
    crawl_attr(attraction_file_name, begin_num)
