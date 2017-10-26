import time

from app.scheduler import Scheduler
from app.page_rank import PageRank
from app.spider import Spider


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

# bfs crawl
scheduler.init_spider("bfs")
# creating a spider which will crawl recursively
scheduler.create_spider()
# goes into recursive loop and gets out when queue is empty
scheduler.crawl()

# dfs crawl
# scheduler.init_spider("dfs")


#calculate Page Rank
pageRank = PageRank(Spider.inlink_graph, Spider.outlink_graph)
pageRank.calculate_page_rank()




# execution complete
print("*****************************\nExecution time:")
print("--- %s seconds ---" % (time.time() - start_time))
