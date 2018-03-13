### Project MIT@U
### phrases_classify.py
### Mengchen Shi Mar 10th
### "Original"

#######################################################################

# Semi-manually clustering(classifying) phrases
# We tried K-means and AgglomerativeClustering, but drew bad results
# Instead, we clustering phrases by merging phrases with
# high similarity together, repeat the process until no more merge can be done
# We generated 4891 phrases to 453 clusters (clusters have overlaps).
# Then we manually pick  meaningful clusters, merge some of them,
# and get 41 categories eventually

#######################################################################

import Class_Phrase
from gensim.models import word2vec
import pandas as pd
import csv
import json



################### load model #################
W2V_MODEL_NAME = 'all_reviews_context'


################### Input files ################
PHRS_INFILE = 'gensim_phrs_noscore.csv'
ATTR_RVW_FILE = 'attr_rvw.json'

################### Output files ###############
ATTR_MATCH_PHRS= 'attr_match_phrs.csv'
MERGE_SIMILAR_PHRS = 'phrs_merge.csv'


################### constant value
SIMILARITY = 0.9


def go():
    '''
    Start from here
    '''
    w2v_model = word2vec.Word2Vec.load(W2V_MODEL_NAME)
    #phrs_model = Phrases.load(PHRS_MODEL_NAME)
    gensim_phrs = pd.read_csv(PHRS_INFILE, names=['ph'])['ph'].tolist()

    tables = attr_match_phrs(gensim_phrs)
    phrs_similar = select_similarity(gensim_phrs, w2v_model)
    phrs_similar_merge = merge_similar_phrs(phrs_similar)



def attr_match_phrs(gensim_phrs):
    '''
    Match each attraction with all phrases that appear in its reviews

    Input:
    gensim_phrs: list of phrases

    Return:
    tables: dictionary of attractions(keys) and their matched phrases(values)
    '''
    attr_rvw = pd.read_json(ATTR_RVW_FILE,typ='series')
    tables = {}
    max_len=max([len(c.split()) for c in gensim_phrs])

    with open(ATTR_MATCH_PHRS,'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(len(attr_rvw)):
            P = Class_Phrase.Phrases(max_len, attr_rvw[i], attr_rvw.index[i])
            tgt_table = P.set_target_table(gensim_phrs).table
            tgt_table = [p for p in tgt_table if p and p[1]>0.0]
            tgt_table = sorted(tgt_table, key=lambda t: t[1], reverse=True)
            tables[attr_rvw.index[i]] = tgt_table
            writer.writerow([attr_rvw.index[i], tgt_table])

    return tables



def select_similarity(gensim_phrs, model):
    '''
    For each phrase, find similar phrases greater than given SIMILARITY

    Input:
    gensim_phrs: list of phrases
    model: a word2vec model trained by all reviews

    Return:
    phrs_similar: dictionary of phrases(keys) and their similar phrases(values)
    '''

    phrs_similar = {}
    for i in range(0, len(gensim_phrs)):
        phrs_similar[gensim_phrs[i]]=set()
        print(i)
        for j in range(0, len(gensim_phrs)):
            if i!=j:
                try:
                    if model.n_similarity(gensim_phrs[i].split(),\
                                        gensim_phrs[j].split()) >= SIMILARITY:
                        phrs_similar[gensim_phrs[i]] |= set([gensim_phrs[j]])
                except:
                    continue

    return phrs_similar




def merge_similar_phrs(phrs_similar):
    '''
    Merge similar phrase groups until no more merge can be done,
    and write result to a csv file

    Input:
    phrs_similar: dictionary of phrases(keys) and their similar phrases(values)
    '''
    phrs_similar_merge = {}
    while len(phrs_similar) > len(phrs_similar_merge):
        if phrs_similar_merge:
            phrs_similar = phrs_similar_merge
        clstd = set()
        phrs_similar_merge = {}
        for k, v in phrs_similar.items():
            if v:
                if k not in clstd:
                    clstd|= {k}
                    phrs_similar_merge[k] = set(v)
                    for vi in v:
                        clstd |= {vi}
                        if vi in phrs_similar:
                            phrs_similar_merge[k] |= set(phrs_similar[vi])


    with open(MERGE_SIMILAR_PHRS, 'w',newline='') as csvfile:
        writer = csv.writer(csvfile)
        for k, v in phrs_similar_merge.items():
            writer.writerow([k]+list(v))

    return phrs_similar_merge



