import time

from app.scheduler import Scheduler
from app.page_rank import PageRank
from app.spider import Spider


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


# dfs crawl

# scheduler.init_spider("dfs")


# calculating pagerank for dfs

# pageRank = PageRank(Spider.dir_name, Spider.inlink_graph, Spider.outlink_graph)
# pageRank.calculate_page_rank()

# execution complete
print("*****************************\nExecution time:")
print("--- %s seconds ---" % (time.time() - start_time))
