### Project MIT@U
### Class Phrase
### Mengchen Shi Mar. 4th
### "Modified" --- learn from CAPP 30122 PA5

########################################################################

# This document builds a class to find the frequences of
# given phrases in all the reviews of an attraction

########################################################################

import hash_table as ht
import string
import csv
import pandas as pd


HASH_CELLS = 57
#PHRS_FILE = 'AutoPhrase_multi-words.txt'
#ATTR_RVW_FILE = 'attr_rvw.json'

class Phrases:

    def __init__(self, k, s, name):
        '''
        Constructor
        '''
        self._k = k #the biggest number of words in target phrase
        self._text = s.lower()
        self._table = ht.Hash_Table(HASH_CELLS, None)
        self._text_len = self._set_table()
        self._name = set([n.lower() for n in name.split()])
        self._cities = set(['santa monica', 'san francisco', 'san diego', 'los angeles', 'santa barbara'])
        #self._tgt_table = ht.Hash_Table(HASH_CELLS, None)
        #self._table_len = self._set_table()
        #self._set_tgt_table()
        #self._words = set(s.split())


    def _set_table(self):
        '''
        Set the hash table. Keys are all phrases (t-words string
         where t>=2 and t<=self._k) in given string(self._text,
         values are frequence of times phrases appear in self._text
        '''
        nopunc = [char for char in self._text if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        nopunc = nopunc.split()
        #for ki in range(self._k):
        for i in range(len(nopunc)-self._k+1):
            key = nopunc[i]
            for j in range(1, self._k):
                key = key + ' ' + nopunc[i+j]
                k_freq = self._table.lookup(key)
                if not k_freq:
                    k_freq = 0
                self._table.update(key, k_freq+1)

        #return len(nopunc)
        #return len(self._table)

    def set_target_table(self, phrs):
        '''
        Input:
        phrs(list): phrases to look up in self_table

        Return:
        tgt_table: hash table object,
        its attribute 'table' contains looked up phrases in with frequences
        '''

        tgt_table = ht.Hash_Table(HASH_CELLS, None)

        for ph in phrs:
            if set(ph.split()).intersection(self._name):
                continue
            if ph in self._cities:
                continue
            freq = self._table.lookup(ph)
            if not freq:
                freq = 0
            #tgt_table.update(ph, freq/self._text_len)
            tgt_table.update(ph, freq)

        return tgt_table

'''
def go():
    with open(PHRS_FILE,'r') as f:
        content = f.readlines()
    content = [x.split('\t') for x in content]
    phrs = pd.DataFrame(content, columns=['prob','phrase'])
    phrs['phrase'] = phrs['phrase'].apply(lambda x: x.replace('\n',''))
    phrs['prob'] = phrs['prob'].apply(lambda x: float(x))
    flt_phrs = phrs[phrs['prob']>=0.5] #filtered phrases

    max_len = max(flt_phrs['phrase'].apply(lambda x: len(x.split())))
    print(max_len)
    '''
'''
    with open(attr_rvw_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        count = 0
        tables = {}
        for row in reader:
            if count <=19:
                P = Phrases(max_len, row[1])
                tgt_table = P.set_target_table(flt_phrs['phrase']).table
                tgt_table = [p for p in tgt_table if p and p[1]>0.0]
                tgt_table = sorted(tgt_table, key=lambda t: t[1], reverse=True)
                tables[row[0]] = tgt_table
                count += 1
            else:
                break
'''

    #with open('attr_rvw.json') as csvfile:


    #return tables
'''
clustering = AgglomerativeClustering(linkage='ward', n_clusters=10)
pred = clustering.fit_predict(X)
flt_phrs['phrase'].iloc[[i for i in range(len(pred)) if pred[i]==3]]
'''
