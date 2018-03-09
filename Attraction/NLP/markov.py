# CS122 W'18: Markov models and hash tables
# Mengchen Shi

import sys
import math
import Hash_Table

HASH_CELLS = 57


class Markov:

    def __init__(self, k, s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''

        self._text = s[-k:] + s
        self._k = k
        self._S = len(set(s))
        self._table = Hash_Table.Hash_Table(HASH_CELLS, None)
        self._set_table()


    def _set_table(self):
        '''
        Set the hash table. Fill cells with k-order strings and
        k+1-order strings and their frequencies.
        '''

        length = len(self._text)-self._k

        for i in range(0, length):
            key = self._text[i : i+self._k+1]
            k_freq = self._table.lookup(key)
            if not k_freq:
                k_freq = 0
            self._table.update(key, k_freq+1)

            prefix = key[:-1]
            p_freq = self._table.lookup(prefix)
            if not p_freq:
                p_freq = 0
            self._table.update(prefix, p_freq + 1)


    def log_probability(self, s):
        '''
        Given a string(s), iterate each k-order preceding sequences in the
        string, and calculate the log probability each string. Return the sum
        of the log probabilities (log_prob_sum).
        '''

        unident = s[-self._k:] + s #unidentified string
        log_prob_sum = 0

        for i in range(0, len(s)):
            key = unident[i : i+self._k+1]
            prefix = key[:-1]
            M = self._table.lookup(key)
            if not M:
                M = 0
            N = self._table.lookup(prefix)
            if not N:
                N = 0
            log_prob_sum += math.log((M+1) / (N+self._S))


        return log_prob_sum




def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the *normalized* log probabilities of each of the speakers
    uttering that text under an "order" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    m1 = Markov(order, speech1)
    m2 = Markov(order, speech2)
    prob1 = m1.log_probability(speech3)/len(speech3)
    prob2 = m2.log_probability(speech3)/len(speech3)
    if prob1 >= prob2:
        conclusion  = 'A'
    else:
        conclusion = 'B'

    res_tuplp = (prob1, prob2, conclusion)

    return res_tuplp



def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple

    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")


if __name__ == "__main__":
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)

    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)
