import csv
import json
import click_03



def crawl_attr(attraction_file, begin_num):
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

    for i in range(begin_num, len(url)):
        name = attr_name[i]
        print(name)
        c = click_03.ChromeDriver(url[i])
        is_attraction = c.is_attraction()
        attr = json.loads(is_attraction.get_attribute('text'))
        c.add_reviews(attr)
        print(len(attr['reviews']))
        attr_dict = {}
        attr_dict[name] = attr
        with open('{}.json'.format(name), 'w') as file:
            file.write(json.dumps(attr_dict))


