import hash_table as ht
import string
import csv
import rvw_cleaning as rc
import pandas as pd

HASH_CELLS = 57
phrs_file = 'AutoPhrase_multi-words.txt'
attr_rvw_file = 'attr_rvw.csv'

class Phrases:

    def __init__(self, k, s):
        self._k = k #the biggest number of words in target phrase
        self._text = s.lower()
        self._table = ht.Hash_Table(HASH_CELLS, None)
        self._text_len = self._set_table()
        #self._tgt_table = ht.Hash_Table(HASH_CELLS, None)
        #self._table_len = self._set_table()
        #self._set_tgt_table()
        #self._words = set(s.split())


    def _set_table(self):
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

        return len(nopunc)
        #return len(self._table)

    def set_target_table(self, phrs):

        tgt_table = ht.Hash_Table(HASH_CELLS, None)
        for ph in phrs:
            freq = self._table.lookup(ph)
            if not freq:
                freq = 0
            #tgt_table.update(ph, freq/self._text_len)
            tgt_table.update(ph, freq)

        return tgt_table


def go():
    with open(phrs_file,'r') as f:
        content = f.readlines()
    content = [x.split('\t') for x in content]
    phrs = pd.DataFrame(content, columns=['prob','phrase'])
    phrs['phrase'] = phrs['phrase'].apply(lambda x: x.replace('\n',''))
    phrs['prob'] = phrs['prob'].apply(lambda x: float(x))
    flt_phrs = phrs[phrs['prob']>=0.5] #filtered phrases

    max_len = max(flt_phrs['phrase'].apply(lambda x: len(x.split())))
    print(max_len)
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
    attr_rvw = pd.read_json('attr_rvw.json',typ='series')
    #attr_rvw  = rc.reviews_cleaning('merge.json')
    tables = {}
    for i in range(len(attr_rvw)):
        P = Phrases(max_len, attr_rvw[i])
        tgt_table = P.set_target_table(flt_phrs['phrase']).table
        tgt_table = [p for p in tgt_table if p and p[1]>0.0]
        tgt_table = sorted(tgt_table, key=lambda t: t[1], reverse=True)
        tables[attr_rvw.index[i]] = tgt_table

    return tables

