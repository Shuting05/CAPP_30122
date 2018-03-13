### Project MIT@U
### rvw_word2vec.py
### Mengchen Shi, Ruxin Chen March 6th
### "Modified" -- Some of codes are copied from a tutorial on kaggle:
### https://www.kaggle.com/c/word2vec-nlp-tutorial#part-2-word-vectors
### Generated by installed package: gensim, nltk and logging

########################################################################

# To run this file, gensim and nltk packages should be installed
# gensim: https://radimrehurek.com/gensim/install.html
# nltk: http://www.nltk.org/install.html


# Processing reviews using gensim word2vec package and Phrases package
# Generate a word2vec model and a Phrases model

# The word2vec model can calculate similarity between
# two lists of words(see phrase_classify.py)

# The Phrase model can find all posible phrases in reviews
# that are utilized to do clustering(see phrase_classify.py)

########################################################################

import gensim
import nltk.data
import logging
import pandas as pd
import csv
import re
from nltk.corpus import stopwords
from gensim.models import Phrases
from gensim.models import word2vec

############ Input file ###############
ATTR_ATTRIBUTES_FILE = 'data/merged_attrs.json'

############ Output file ##############
PHRS_OUTFILE = 'data/gensim_phrs_noscore.csv'

############ Outout model #############
W2V_MODEL_NAME = 'data/all_reviews_context'


def go():
    '''
    Train models. Start of the document.
    '''
    all_reviews_app = load_attr_rvw()
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    sentences = []
    for review in all_reviews_app:
        sentences += review_to_sentences(review, tokenizer, True)

    word2vec_model(sentences)
    phrs_model(sentences)



def load_attr_rvw():
    '''
    Load attraction review file and extract reviews one by one for  nlp

    Return:
    all_reviews_app(list of reviews(string)): each element is one review
    '''

    df = pd.read_json(ATTR_ATTRIBUTES_FILE).transpose()
    attr_rvw = df['reviews'].apply(lambda x: [i[2]+' || '+i[3] for i in x])
    attr_rvw = attr_rvw.apply(lambda x: [i.replace('\n','') for i in x])
    attr_rvw = attr_rvw.apply(lambda x: [i.replace('Show less','') for i in x])
    attr_rvw = pd.DataFrame(attr_rvw)
    attr_rvw.reset_index(level=0, inplace=True)
    attr_rvw.columns = ['attr','reviews']


    all_reviews_app = []
    for r in attr_rvw['reviews']:
        all_reviews_app += r


    return all_reviews_app




def phrs_model(sentences):
    '''
    Generate Phrases model to find potential phrases,
    save its phrases into csv file

    Input:
    sentences(list of list of words): sentences without stop words
    '''
    model_ph = Phrases(sentences)
    #model_ph.save(PHRS_MODEL_NAME)
    gensim_phrs=model_ph.export_phrases(sentences)
    gensim_phrs = list(set(gensim_phrs))
    gensim_phrs = [g[0].decode("utf-8") for g in gensim_phrs \
                                    if g[0].split()[0]!=g[0].split()[1]]

    with open(PHRS_OUTFILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        sent = set()
        for i in gensim_phrs:
            if i not in sent:
                writer.writerow([i])
                sent |= {i}


############### Most of codes below are copied from kaggle:
# https://www.kaggle.com/c/word2vec-nlp-tutorial#part-2-word-vectors

def review_to_sentences(review, tokenizer, remove_stopwords=False ):
    '''
    Function to split a review into parsed sentences. Returns a
    list of sentences, where each sentence is a list of words

    Return:
    sentences(list of list of words(string))
    '''
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(review.strip())
    #
    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call review_to_wordlist to get a list of words
            sentences.append( review_to_wordlist( raw_sentence, \
              remove_stopwords ))
    #
    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences




def review_to_wordlist(review, remove_stopwords=False ):
    '''
    Function to convert a document to a sequence of words,
    optionally removing stop words.  Returns a list of words.
    Input:
    review(string): one review

    Return:
    words(list of strings): words in the view with stopwords removed(optional)
    '''
    review_text = re.sub("[^a-zA-Z]", " ", review)
    words = review_text.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return words




def word2vec_model(sentences):
    '''
    Generage word2vec model, save it and its csv file
    Input:
    sentences(list of list of words): sentences without stop words
    '''

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',\
        level=logging.INFO)

    num_features = 300    # Word vector dimensionality
    min_word_count = 40   # Minimum word count
    num_workers = 4       # Number of threads to run in parallel
    context = 10  #Context window size
    downsampling = 1e-3   # Downsample setting for frequent words

    #Initialize and train the model (this will take some time)
    model = word2vec.Word2Vec(sentences, workers=num_workers, \
                            size=num_features, min_count = min_word_count, \
                                window = context, sample = downsampling)
    # If you don't plan to train the model any further, calling
    # init_sims will make the model much more memory-efficient.
    model.init_sims(replace=True)

    # It can be helpful to create a meaningful model name and
    # save the model for later use. You can load it later using Word2Vec.load()
    # model_name = "all_reviews_context"
    model.save(W2V_MODEL_NAME)






