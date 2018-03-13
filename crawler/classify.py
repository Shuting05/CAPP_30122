#### CAPP30122 Project 
# Ruxin Chen 
import json
import pandas as pd 
import csv

'''
def clean_review():

    with open('reviews.json', 'r') as file:
        reviews = json.load(file)

    cleaned = {}
    for att, info in reviews.items():
        review = '||'.join([ (r[-2]+". " +r[-1]) for r in info['reviews']])
        cleaned[att] = review 

    return cleaned
'''

def classify(f, category):
    '''
    The function takes a dictionary f and a pandas data frame 'category' to
    write a csv file that records the category that the attraction belons to
    according to the classification of its phrases and the associated the most
    frequently occoured phrases 

    Input:
    f: the dictionary that maps the attraction to its phrases we summarized 
    from its reviews and the associated number of occurance. e.g.:
    {"Golden Gate Bridge" : ['must see', 24]}, where the phrase 'must see' 
    is mentioned 24 times in the 200 reviews we scraped for Golden Gate 
    Bridge.
    category: 
    the pandas data frame. For each row, the first column of the df is the 
    category that we manually categorized after browsing all the 400+ groups 
    of phrases, and the remaining columns are the phrases that we define to 
    belongs to that category. 

    The csv file we write, the first column is the name of attraction, the 
    second column is all the categories the attraction belongs to, the third 
    column is a tuple whose first item is category and second item is the 
    most frequently occurred phrase that belongs to this category for this 
    attraction. 

    '''
    d = {}
    data = {}

    for att in f:
        data[att] = {}
        data[att]['category'] = []
        data[att]['tags'] = []

        for i, row in category.iterrows():
            word_set = set()
            key_words = [j for j in row if type(j) != float][1:]

            for word in key_words:
                if word in f[att]:
                    word_set.add(word)

                    if row[0] not in d:
                        d[row[0]] = set()
                    d[row[0]].add(att)
                    if row[0] not in data[att]['category']:
                        data[att]['category'].append(row[0])

            if word_set:
                tag = find_max_tags(f, att, word_set)
                data[att]['tags'].append((row[0], tag))


    with open('reviews1.csv', 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        row = ['attraction', 'category', 'tags']
        writer.writerow(row)
        for att, info in data.items():
            row = [att]
            row += [v for k,v in info.items()]
            writer.writerow(row)

    #with open('classify.csv', 'w', newline='') as csvfile:
    #    writer = csv.writer(csvfile, delimiter=',')
    #    for category, att_set in d.items():
    #        row = [category]
    #        row += [att for att in att_set]
    #        writer.writerow(row)
    

def find_max_tags(f, attr, word_set):
    ''' 
    The function takes the dictionary f, the attration, attr, and
    a word_set and returns the more frequently occurred phrase in
    the word_set.
    Input:
    f: a dictionary, see the definition in the classify function
    attr: string,
    word_set: a set of phrases 
    Returns:
    max_tag: string 
    '''

    max_num = 0

    for tag in word_set:
        num = f[attr][tag]
        if num > max_num:
            max_tag = tag

    return max_tag


if __name__ == "__main__":

'''
##############################################################################
I changed the data structure of the file 'attr_rvw.json' for comvenience  

    with open('attr_rvw.json', 'r') as file:
        d = json.load(file)

    f = {}   

    for i, v in f.items():
        if i not in f:
            f[i] = {}
        for j in v:
            if j[0] not in f[i]:
                f[i][j[0]] = j[1]

    with open('attr_match_phrs.json', 'w') as file:
        file.write(json.dumps(f))

##############################################################################
'''

    with open('attr_match_phrs.json', 'r') as file:
        f = json.load(file)

    category = pd.read_csv('category.csv', header = None)








        


