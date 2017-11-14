import os
from app.general import index_to_str_file


class Indexer:

    data_directory = 'data'
    index = {}
    index_file_name = 'index_unigram.txt'
    index_bi_gram = {}
    bigram_file_name = 'index_bigrams.txt'
    index_tri_gram = {}
    trigram_file_name = 'index_trigrams.txt'
    frequencies = {}

    def __init__(self, crawled):
        self.crawled = crawled

    def create_index(self):
        for doc in self.crawled:
            file_name = os.path.join('documents', doc)
            with open(file_name, 'r') as f:
                words = f.read().split(' ')
                words = list(filter(None, words))
                for unstriped_word in words:
                    word = unstriped_word.strip()
                    if word not in self.index.keys():
                        self.index[word] = [[doc, 1]]
                    else:
                        found = False
                        for i in self.index[word]:
                            if i[0] == doc:
                                i[1] += 1
                                found = True
                                break
                        if not found:
                            self.index[word].append([doc, 1])

        # self.store_index(self.index, self.index_file_name)
        index_to_str_file(self.index, os.path.join(self.data_directory, self.index_file_name))

    def create_bi_gram_index(self):
        for doc in self.crawled:
            file_name = os.path.join('documents', doc)
            with open(file_name, 'r') as f:
                words = f.read().split(' ')
                words = list(filter(None, words))
                # creating list of 2 grams
                two_grams = []
                for i in range(len(words) - 1):
                    two_grams.append(words[i].strip() + ' ' + words[i+1].strip())

                for word in two_grams:
                    if word not in self.index_bi_gram.keys():
                        self.index_bi_gram[word] = [[doc, 1]]
                    else:
                        found = False
                        for i in self.index_bi_gram[word]:
                            if i[0] == doc:
                                i[1] += 1
                                found = True
                                break
                        if not found:
                            self.index_bi_gram[word].append([doc, 1])

        # self.store_index(self.index_bi_gram, self.bigram_file_name)
        index_to_str_file(self.index_bi_gram, os.path.join(self.data_directory, self.bigram_file_name))

    def create_tri_gram_index(self):
        for doc in self.crawled:
            file_name = os.path.join('documents', doc)
            with open(file_name, 'r') as f:
                words = f.read().split(' ')
                words = list(filter(None, words))
                # creating list of 3 grams
                two_grams = []
                for i in range(len(words) - 2):
                    two_grams.append(words[i].strip() + ' ' + words[i + 1].strip() + ' ' + words[i + 2].strip())

                for word in two_grams:
                    if word not in self.index_tri_gram.keys():
                        self.index_tri_gram[word] = [[doc, 1]]
                    else:
                        found = False
                        for i in self.index_tri_gram[word]:
                            if i[0] == doc:
                                i[1] += 1
                                found = True
                                break
                        if not found:
                            self.index_tri_gram[word].append([doc, 1])

        # self.store_index(self.index_tri_gram, self.trigram_file_name)
        index_to_str_file(self.index_tri_gram, os.path.join(self.data_directory, self.trigram_file_name))

    def get_index(self):
        return self.index

    def get_bi_gram_index(self):
        return self.index_bi_gram

    def get_tri_gram_index(self):
        return self.index_tri_gram

    # to store index which is sorted by length of inverted list and inverted list is sorted by term frequency
    def store_index(self, index, file_name):
        with open(os.path.join(self.data_directory, file_name), 'w') as f:
            for k in sorted(index, key=lambda k: len(index[k]), reverse=True):
                inverted_list = sorted(index[k], key=lambda m: m[1], reverse=True)
                f.write(k + ':' + str(inverted_list) + '\n')
