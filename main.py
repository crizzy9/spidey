import threading
from multiprocessing import Process
import time

from queue import Queue
from spider import Spider
from general import *


seed = "https://en.wikipedia.org/wiki/Tropical_cyclone"
# keyword = "rain"
# keyword = ""
# domain_name = get_domain_name(seed)

DIR_NAME = "data"
QUEUE_FILE = DIR_NAME + '/queue.txt'
CRAWLED_FILE = DIR_NAME + '/crawled.txt'

NUMBER_OF_THREADS = 8

queue = Queue()


def create_spider():
    t = threading.Thread(target=work)
    t.daemon = True
    t.start()


# Create spider threads, will die when main exits
def create_spiders():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# def create_spiders():
#     for _ in range(NUMBER_OF_THREADS):
#         p = Process(target=work)
#         p.start()
#         p.join()


def work():
    # print("#Inside work outside loop")
    while True:
        # print("#Inside work while loop")
        url = queue.get()
        # Spider.crawl_page(url)
        Spider.crawl_page(threading.current_thread().name, url)
        queue.task_done()
        # print("#Exiting work while loop")


# this is depth wise so it will be displayed on each depth?
def create_jobs():
    # print("#Creating jobs")
    for link in file_to_arr(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()


def crawl():
    # print("#Inside crawl()")
    queued_links = file_to_arr(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + " links in the queue")
        create_jobs()


print("WEB CRAWLER STARTING...")
print("Enter the seed url: ")
#seed = input()
print("Enter the keyword or just leave it empty:")
keyword = input()
domain_name = get_domain_name(seed)

# starting the timer
start_time = time.time()

# Set the variables for the spider
Spider(DIR_NAME, seed, domain_name, keyword)

# without any threading
# work()

# for 1 thread only no for loop
# creating a spider which will crawl recursively
create_spider()

# for multithreaded crawler
# create_spiders()

crawl()

print("*****************************\nExecution time:")
print("--- %s seconds ---" % (time.time() - start_time))
