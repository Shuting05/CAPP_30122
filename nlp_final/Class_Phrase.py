### Project MIT@U
### Class Phrase
### Mengchen Shi Mar. 4th
### "Origin" --- inspired by CAPP 30122 PA5

########################################################################

# This document builds a class to find the frequences of
# given phrases in all the reviews of an attraction

########################################################################

import hash_table as ht
import string
import csv
import pandas as pd


HASH_CELLS = 57


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


