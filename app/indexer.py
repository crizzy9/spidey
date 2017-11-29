import os
from app.general import index_to_str_file
from operator import itemgetter


class Indexer:

    data_directory = '../data'
    documents_directory = '../documents'
    index = {}
    index_file_name = 'index_unigram.txt'
    tf_unigram_file_name = 'unigram_tf_table.txt'
    df_unigram_file_name = 'unigram_df_table.txt'
    index_bi_gram = {}
    bigram_file_name = 'index_bigrams.txt'
    tf_bigram_file_name = 'bigram_tf_table.txt'
    df_bigram_file_name = 'bigram_df_table.txt'
    index_tri_gram = {}
    trigram_file_name = 'index_trigrams.txt'
    tf_trigram_file_name = 'trigram_tf_table.txt'
    df_trigram_file_name = 'trigram_df_table.txt'
    token_freq = {}

    def __init__(self, crawled):
        self.crawled = crawled

    def create_index(self):
        for doc in self.crawled:
            file_name = os.path.join(self.documents_directory, doc + '.txt')
            with open(file_name, 'r') as f:
                words = f.read().split(' ')
                words = list(filter(None, words))
                tokens = []
                for unstriped_word in words:
                    word = unstriped_word.strip().replace("\n", "")
                    if word not in tokens:
                        tokens.append(word)
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
                self.token_freq[doc] = len(tokens)

        with open(os.path.join(self.data_directory, 'tokens.txt'), 'w') as f:
            f.write("Doc\t\t\t\tNumber of tokens\n")
            for t in self.token_freq.keys():
                f.write(str(t) + "\t\t" + str(self.token_freq[t]) + "\n")

        self.store_index(self.index, self.index_file_name)
        # index_to_str_file(self.index, os.path.join(self.data_directory, self.index_file_name))
        self.generate_tf_table(self.index, self.tf_unigram_file_name)
        self.generate_df_table(self.index, self.df_unigram_file_name)

    def create_bi_gram_index(self):
        for doc in self.crawled:
            file_name = os.path.join(self.documents_directory, doc + '.txt')
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

        self.store_index(self.index_bi_gram, self.bigram_file_name)
        # index_to_str_file(self.index_bi_gram, os.path.join(self.data_directory, self.bigram_file_name))
        self.generate_tf_table(self.index_bi_gram, self.tf_bigram_file_name)
        self.generate_df_table(self.index_bi_gram, self.df_bigram_file_name)

    def create_tri_gram_index(self):
        for doc in self.crawled:
            file_name = os.path.join(self.documents_directory, doc + '.txt')
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

        self.store_index(self.index_tri_gram, self.trigram_file_name)
        # index_to_str_file(self.index_tri_gram, os.path.join(self.data_directory, self.trigram_file_name))
        self.generate_tf_table(self.index_tri_gram, self.tf_trigram_file_name)
        self.generate_df_table(self.index_tri_gram, self.df_trigram_file_name)

    def get_index(self):
        return self.index

    def get_bi_gram_index(self):
        return self.index_bi_gram

    def get_tri_gram_index(self):
        return self.index_tri_gram

    def generate_tf_table(self, index, file_name):
        tf = {}
        for term in index.keys():
            count = 0
            for tup in index[term]:
                count += tup[1]
            tf[term] = count
        with open(os.path.join(self.data_directory,file_name), 'w') as f:
            # [[t, tf[t]] for t in sorted(tf, key=tf.get, reverse=True)]
            f.write("Term\tFrequency\n")
            for t in sorted(tf, key=tf.get, reverse=True):
                f.write(str(t) + "\t\t" + str(tf[t]) + "\n")

    def generate_df_table(self, index, file_name):
        df = []
        for term in index.keys():
            ids = []
            count = 0
            for tup in index[term]:
                ids.append(tup[0])
                count += 1
            df.append([term, ids, count])
        with open(os.path.join(self.data_directory,file_name), 'w') as f:
            f.write("Term\t\t\t\tDocID\t\t\t\tDoc_Frequency\n")
            for t in sorted(df, key=itemgetter(0)):
                f.write(str(t[0]) + "\t\t" + str(t[1]) + "\t\t\t" + str(t[2]) + "\n")


    # to store index which is sorted by length of inverted list and inverted list is sorted by term frequency
    def store_index(self, index, file_name):
        with open(os.path.join(self.data_directory, file_name), 'w') as f:
            for k in sorted(index, key=lambda k: len(index[k]), reverse=True):
                inverted_list = sorted(index[k], key=lambda m: m[1], reverse=True)
                f.write(k + ':' + str(inverted_list) + '\n')
