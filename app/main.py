import time
import operator

from app.scheduler import Scheduler
from app.page_rank import PageRank
from app.spider import Spider
from app.general import *


print("WEB CRAWLER STARTING...")

print("Enter the seed url: ")
# seed = input()
seed = "https://en.wikipedia.org/wiki/Tropical_cyclone"

print("Enter the keyword or just leave it empty:")
keyword = input()
# keyword = "rain"


# starting the timer
start_time = time.time()

scheduler = Scheduler(seed, keyword)

# print("BFS CRAWL: ")

# bfs crawl
# scheduler.init_spider("bfs")

# scheduler.create_spider()

# scheduler.crawl()
# Spider.update_graph()
# dict_to_str_file(Spider.inlink_graph, 'hw2_task1/G1.txt')


# pageRank = PageRank(Spider.dir_name, Spider.inlink_graph, Spider.outlink_graph)

# pageRank.calculate_page_rank()

print("DFS CRAWL: ")

# dfs crawl
scheduler.init_spider("dfs")
pageRank = PageRank(Spider.dir_name, Spider.inlink_graph, Spider.outlink_graph)
pageRank.calculate_page_rank()

# execution complete
print("*****************************\nExecution time:")
print("--- %s seconds ---" % (time.time() - start_time))

zero_inlink_pages = []
zero_outlink_pages = []


for key in Spider.outlink_graph.keys():
    if len(Spider.outlink_graph[key]) == 0:
        zero_outlink_pages.append(key)

for key in Spider.inlink_graph.keys():
    if len(Spider.inlink_graph[key]) == 0:
        zero_inlink_pages.append(key)

print("ZERO INLINK PAGES:", len(zero_inlink_pages))
print(zero_inlink_pages)

print("ZERO OUTLINK PAGES:", len(zero_outlink_pages))
print(zero_outlink_pages)


graph2 = {}
for key in Spider.inlink_graph.keys():
    graph2[key] = len(Spider.inlink_graph[key])


inlink_tuples = list(reversed(sorted(graph2.items(), key=operator.itemgetter(1))))

print("TOP 10 INLINKS:")
print(inlink_tuples[:10])
