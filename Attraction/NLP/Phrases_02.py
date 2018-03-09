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
        #self._table = ht.Hash_Table(HASH_CELLS, None)
        self._table = {}
        self._text_len = self._set_table()



    def _set_table(self):
        nopunc = [char for char in self._text if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        nopunc = nopunc.split()
        #for ki in range(self._k):
        for i in range(len(nopunc)-self._k+1):
            key = nopunc[i]
            for j in range(1, self._k):
                key = key + ' ' + nopunc[i+j]
                #k_freq = self._table.lookup(key)
                if key not in self._table:
                    self._table[key] = 0
                else:
                    self._table[key] += 1
                #if not k_freq:
                    #k_freq = 0
                #self._table.update(key, k_freq+1)

        return len(nopunc)
        #return len(self._table)

    def set_target_table(self, phrs):

        #tgt_table = ht.Hash_Table(HASH_CELLS, None)
        tgt_table = {}
        for ph in phrs:
            print(ph)
            print(tgt_table)
            print(ph in self._table)
            if ph in self._table:
                tgt_table[ph] += 1
            else:
                tgt_table[ph] = 0
            #freq = self._table.lookup(ph)
            #if not freq:
                #freq = 0
            #tgt_table.update(ph, freq/self._text_len)
            #tgt_table.update(ph, freq)

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

    attr_rvw = pd.read_json('attr_rvw.json',typ='series')

    tables = {}
    for i in range(len(attr_rvw)):
        P = Phrases(max_len, attr_rvw[i])
        tgt_table = P.set_target_table(flt_phrs['phrase'])
        tgt_table = [p for p in tgt_table if p and p[1]>0.0]
        tgt_table = sorted(tgt_table, key=lambda t: t[1], reverse=True)
        tables[attr_rvw.index[i]] = tgt_table

    return tables

