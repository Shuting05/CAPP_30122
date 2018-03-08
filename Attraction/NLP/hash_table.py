# CS122 W'18: Markov models and hash tables
# Mengchen Shi


TOO_FULL = 0.5
GROWTH_RATIO = 2


class Hash_Table:

    def __init__(self, cells, defval):
        '''
        Construct a new hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        self.cells = cells
        self.defval = defval
        self.table = [defval] * cells
        self.nfull = 0


    def _hash_val(self, key):
        '''
        Calculate the hash value of the key using standard hash value fomula
        '''

        hval = 0
        for k in key:
            hval = (hval * 37 + ord(k)) % self.cells

        return hval


    def _find_next(self, hval, key):
        '''
        Find the next slot that is empty (default value) or has the same key
         as given

        Return the index of the found slot
        '''
        index = hval
        while self.table[index] != self.defval:
            if self.table[index][0] == key:
                return index
            else:
                index = (index + 1) % self.cells

        return index



    def _rehashing(self):
        '''
        Rehash the table. Increase the size of the table and
        rebuild an empty table. Recalculate the hash value of the former elements
        and fill them into the new table.
        '''

        self.cells = self.cells * GROWTH_RATIO
        ex_table = self.table
        self.table = [self.defval] * self.cells

        for c in ex_table:
            if c != self.defval:
                hval = self._hash_val(c[0])
                index = self._find_next(hval, c[0])

                self.table[index] = c



    def lookup(self, key):
        '''
        Retrieve the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''

        hval = self._hash_val(key)
        index = self._find_next(hval, key)
        if self.table[index] == self.defval:
            return self.defval

        return self.table[index][1]



    def update(self, key, val):
        '''
        Change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table,  insert it with
        value "val".
        '''
        hval = self._hash_val(key)
        index = self._find_next(hval, key)
        self.table[index] = (key, val)
        self.nfull += 1

        if self.nfull / self.cells > TOO_FULL:
            self._rehashing()

