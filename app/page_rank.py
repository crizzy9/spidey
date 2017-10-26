import math
import operator


class PageRank:

    # dampening factor
    d = 0.85
    ranks = {}
    prev_perp = 0
    converge_limit = 4
    converge_counter = 0

    # p - crawled (all pages)
    # S- sink nodes
    # M(p) - inlinks of page P
    # L(q) - outlinks from page q
    def __init__(self, inlink_graph, outlink_graph):
        self.inlink_graph = inlink_graph
        self.outlink_graph = outlink_graph
        self.all_pages = self.outlink_graph.keys()

        self.corp_len = len(self.all_pages)
        self.sinks = []
        self.get_sinks()

    def calculate_page_rank(self):
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

        print("PAGE RANK RESULTS")
        rank_tuples = sorted(self.ranks.items(), key=operator.itemgetter(1))
        sorted_ranks = list(reversed(rank_tuples))
        print(sorted_ranks)
        # top_fifty = sorted_ranks[:50]
        # print("TOP 50 PAGES:")
        # print(top_fifty)

    def converged(self):
        shannon_entropy = 0
        for p in self.all_pages:
            rank = self.ranks[p]
            shannon_entropy -= rank*math.log(rank, 2)

        perplexity = 2 ** shannon_entropy
        diff = perplexity - self.prev_perp
        if diff < 1 or diff > -1:
            self.converge_counter += 1
        else:
            self.converge_counter = 0

        if self.converge_counter >= 4:
            return True
        else:
            return False

    def get_sinks(self):
        # from outlink_graph check if any page with 0 outlinks
        for doc in self.outlink_graph.keys():
            if len(self.outlink_graph[doc]) == 0:
                self.sinks.append(doc)
