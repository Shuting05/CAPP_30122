import pandas as pd
import csv

def begin(filename):
    attr_rvw = reviews_cleaning(filename)
    write_files(attr_rvw)

    return attr_rvw


def merge_rvw(reviews):
    '''
    "Stick" all reviews of one attraction togather into one string
    '''
    merged = ''
    for r in reviews:
        merged = merged + ' ||| ' + r
    return merged

def reviews_cleaning(filename):
    '''
    Load all attractions from json file (attraction and reviews)
    and clean unwanted words.
    Inputs:

    Return:
    filename： string

    Output:
    attr_rvw(pandas data Series): index are attraction name, values are reviews

    '''
    df = pd.read_json(filename).transpose()
    #attr_rvw = df['reviews'].apply(lambda x: [i[3] for i in x])
    attr_rvw = df['reviews'].apply(lambda x: [i[2]+' || '+i[3] for i in x])
    attr_rvw = attr_rvw.apply(lambda x: [i.replace('\n','') for i in x])
    attr_rvw = attr_rvw.apply(lambda x: [i.replace('Show less','') for i in x])
    attr_rvw = attr_rvw.apply(lambda x: merge_rvw(x))
    # pandas Series, index are attraction names

    return attr_rvw

def write_files(attr_rvw):
    '''
    Write a csv file with two columns(name, reviews);
    wirte a .txt file with all reviews from all attractions
    '''
    #attr_rvw = reviews_cleaning(filename)
    f = open('attr_rvw.txt', 'w')
    attr_rvw.apply(lambda x: f.write(x))
    f.close()

    '''
    with open('attr_rvw.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(attr_rvw)):
            writer.writerow([attr_rvw.index[i], attr_rvw[i]])
    '''

    with open('attr_rvw.json', 'w') as file:
        file.write(attr_rvw.to_json(orient='index'))





