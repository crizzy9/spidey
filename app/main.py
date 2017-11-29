import time
import os
import pprint

from app.scheduler import Scheduler
from app.page_rank import PageRank
from app.spider import Spider
from app.indexer import Indexer
from app.parser import Parser
from app.BM25 import BM25

print("WEB CRAWLER STARTING...")

print("Enter the seed url: ")
# seed = input()
seed = "https://en.wikipedia.org/wiki/Tropical_cyclone"

print("Enter the keyword or just leave it empty:")
# keyword = input()
# keyword = "rain"
keyword = ""


# starting the timer
start_time = time.time()

scheduler = Scheduler(seed, keyword)


# BFS CRAWL

scheduler.init_spider("bfs")
scheduler.create_spider()
scheduler.crawl()


# updating the graphs for bfs
Spider.update_graph()

# calculating pagerank for bfs

pageRank = PageRank(Spider.dir_name, Spider.inlink_graph, Spider.outlink_graph)
pageRank.calculate_page_rank()


# parsing stuff
parser = Parser(Spider.crawled_titles)

# options for text transformation
# parser.case_folding = False
# parser.handle_punctuation = False

print("Parsing documents...")
parser.parse_documents()
print("All documents successfully parsed")


# indexing stuff
indexer = Indexer(Spider.crawled_titles)

print("Creating index...")
indexer.create_index()
indexer.create_bi_gram_index()
indexer.create_tri_gram_index()
print("Index created in data/index_unigrams.txt data/index_bigrams.txt data/index_trigrams.txt")


# pp = pprint.PrettyPrinter(indent=4)
#
# bm25 = BM25(Spider.crawled_titles, indexer.get_index())
# print("Enter queries")
# queries = ["hurricane isabel damage", "forecast models", "green energy canada", "heavy rains", "hurricane music lyrics", "accumulated snow", "snow accumulation", "massive blizzards blizzard", "new york city subway"]
# bm25.calculate_scores(queries)
# print("SCORES")
# scores = bm25.get_sorted_scores()
# pp.pprint(scores)



# execution complete
print("*****************************\nExecution time:")
print("--- %s seconds ---" % (time.time() - start_time))
