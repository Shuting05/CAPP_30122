### Project MIT@U
### nlp.py
### Mengchen Shi March 5th
### "Original"

#######################################################################
# This file is the start point of the whole natural language processing,
# including rvw_word2vec.py and phrase_classify.
# Class_Phrase.py and hasg_table.py are helper files
#
# To begin, run $python3 npl.py in shell

#######################################################################

import pandas as pd
import csv
import rvw_word2vec
import phrase_classify

############## Input file ################
INPUT_FILE = 'data/merged_attrs.json'

############## Output file ###############
OUTPUT_FILE = 'data/attr_rvw.json'





def merge_rvw(reviews):
    '''
    "Stick" all reviews of one attraction togather into one string
    Input:
    reviews(list of strings): all reviews of an attraction

    Return:
    merged(string): all reviews merged
    '''
    merged = ''
    for r in reviews:
        merged = merged + ' ||| ' + r

    return merged

def reviews_cleaning():
    '''
    Load all attractions from json file (attraction and reviews)
    and clean unwanted words.

    Return:
    attr_rvw(pandas data Series): index are attraction name, values are reviews

    '''
    df = pd.read_json(INPUT_FILE).transpose()
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


    with open(OUTPUT_FILE, 'w') as file:
        file.write(attr_rvw.to_json(orient='index'))


if __name__ == "__main__":

    attr_rvw = reviews_cleaning()
    write_files(attr_rvw)
    rvw_word2vec.go()
    phrase_classify.go()


