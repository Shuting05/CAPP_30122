import csv
import json
import click_03



def crawl_attr(attraction_file):
    '''
    crawler attributes and reviews of attractions in the given file
    Inputs:
    attraction_file: name of a csv file
    '''

    attr_name = []
    url = []
    with open(attraction_file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            attr_name.append(row[0])
            url.append(row[1])

    for i in range(len(url)):
        c = click_03.ChromeDriver(url[i])
        is_attraction = c.is_attraction()
        attr = json.loads(is_attraction.get_attribute('text'))
        c.add_reviews(attr)
        attr_dict = {}
        attr_dict[attr_name[i]] = attr
        with open('{}.json'.format(attr_name[i]), 'w') as file:
            file.write(json.dumps(attr_dict))


