import math
import operator
from app.general import *


class PageRank:

    # dampening factor
    d = 0.85
    ranks = {}
    converge_limit = 4
    converge_counter = 0
    perplexities = []
    total_rounds = 0

    def __init__(self, dir_name, inlink_graph, outlink_graph):
        self.inlink_graph = inlink_graph
        self.outlink_graph = outlink_graph
        self.all_pages = self.outlink_graph.keys()
        self.page_rank_file = os.path.join(dir_name, 'pagerank.txt')
        self.perplexity_file = os.path.join(dir_name, 'perplexity.txt')

        self.corp_len = len(self.all_pages)
        self.sinks = []
        self.get_sinks()

    def calculate_page_rank(self):
        print("GRAPHS:")
        print(self.inlink_graph)
        print(self.outlink_graph)
        if self.inlink_graph == {} or self.outlink_graph == {}:
            print("Graph is empty!!!")
            return
        for page in self.all_pages:
            self.ranks[page] = 1/self.corp_len
        while not self.converged():
            sink_rank = 0
            for s in self.sinks:
                if s in self.ranks:
                    sink_rank += self.ranks[s]
            for p in self.all_pages:
                self.ranks[p] = (1 - self.d)/self.corp_len + self.d * sink_rank/self.corp_len
                for q in self.inlink_graph[p]:
                    self.ranks[p] += self.d*self.ranks[q]/len(self.outlink_graph[q])

        print("PAGE RANK CALCULATED IN:", self.page_rank_file)
        # sorting the page rank values
        rank_tuples = sorted(self.ranks.items(), key=operator.itemgetter(1))
        sorted_ranks = list(reversed(rank_tuples))

        # storing page rank in file
        arr_to_file(sorted_ranks, self.page_rank_file)

        # storing perplexities
        arr_to_file(self.perplexities, self.perplexity_file)

    def converged(self):
        self.total_rounds += 1
        shannon_entropy = 0
        for p in self.all_pages:
            rank = self.ranks[p]
            shannon_entropy -= rank*math.log(rank, 2)

        perplexity = 2 ** shannon_entropy
        self.perplexities.append(perplexity)

        if len(self.perplexities) > 3:
            for i in range(len(self.perplexities) - self.converge_limit, len(self.perplexities)):
                pp = 0
                if i != 0:
                    pp = self.perplexities[i - 1]
                p = self.perplexities[i]
                if 1 > p-pp > -1:
                    self.converge_counter += 1
                else:
                    self.converge_counter = 0

        if self.converge_counter >= self.converge_limit:
            return True
        else:
            return False

    def get_sinks(self):
        for doc in self.outlink_graph.keys():
            if len(self.outlink_graph[doc]) == 0:
                self.sinks.append(doc)


