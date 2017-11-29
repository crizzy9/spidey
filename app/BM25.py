import ast
import math
from collections import Counter

class BM25:

    k1 = 1.2
    b = 0.75
    k2 = 100
    DOCUMENTS_DIR = '../documents/'
    DATA_DIR = '../data/'

    def __init__(self, docs, index_file):
        self.docs = docs
        self.index_file = index_file
        self.index = self.get_index_from_file()
        self.scores = {}
        self.k = {}
        self.calc_k()

    def calculate_scores(self):
        # since no relevance information is given
        R = 0
        ri = 0
        queries = self.get_queries_from_file()
        for query in queries.values():
            terms = query.strip().split(' ')
            qtfs = dict(Counter(terms))
            for term in terms:
                N = len(self.docs)
                ni = len(self.index[term])
                fp = math.log(((ri + 0.5) / (R - ri + 0.5))/((ni - ri + 0.5) / (N - ni - R - ri + 0.5)))
                lp = ((self.k2 + 1) * qtfs[term])/(self.k2 + qtfs[term])
                for entry in self.index[term]:
                    doc = entry[0]
                    tf = entry[1]
                    mp = ((self.k1 + 1) * tf)/(self.k[doc] + tf)
                    score = fp * mp * lp
                    if query not in self.scores.keys():
                        self.scores[query] = [[doc, score]]
                    else:
                        found = False
                        for i in self.scores[query]:
                            if i[0] == doc:
                                i[1] += score
                                found = True
                                break
                        if not found:
                            self.scores[query].append([doc, score])
        self.store_scores(queries)

    def calc_k(self):
        doc_lens = {}
        tot_len = 0
        for doc in self.docs:
            with open(self.DOCUMENTS_DIR + doc + '.txt', 'r+') as f:
                doc_lens[doc] = len(f.read().split(' '))
                tot_len += doc_lens[doc]

        avg_len = tot_len/len(self.docs)

        for doc, dlen in doc_lens.items():
            self.k[doc] = self.k1 * ((1-self.b) + self.b * dlen/avg_len)

    def get_sorted_scores(self):
        sorted_scores = {}
        for k in self.scores:
            sorted_scores[k] = sorted(self.scores[k], key=lambda m: m[1], reverse=True)
        return sorted_scores

    def store_scores(self, queries):
        system_name = 'Okapi_BM25_NoStem_NoStop'
        sorted_scores = self.get_sorted_scores()
        with open(self.DATA_DIR + 'scores.txt', 'w') as file:
            file.write("query_id Q0 doc_id rank BM25_score system_name\n")
            for i in range(1, len(queries)+1):
                curr_scores = sorted_scores[queries[i]]
                for j in range(len(curr_scores)):
                    if j+1 <= 100:
                        file.write(str(i) + ' Q0 ' + curr_scores[j][0] + ' ' + str(j+1) + ' ' + str(curr_scores[j][1]) + ' ' + system_name + '\n')
                file.write('\n')

    def get_index_from_file(self):
        with open(self.index_file, 'r+') as f:
            data = f.read().split('\n')
            dic = {}
            for line in data:
                if line == '':
                    continue
                l = line.split(":", 1)
                key = l[0]
                inverted_list = ast.literal_eval(l[1].strip())
                dic[key] = inverted_list
        return dic

    def get_queries_from_file(self):
        query_file = 'queries.txt'
        queries = {}
        with open(self.DATA_DIR + query_file, 'r') as f:
            qs = f.read().split('\n')
            count = 0
            for q in qs:
                if q == '':
                    continue
                count += 1
                queries[count] = q
        return queries

