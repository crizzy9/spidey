import threading
from queue import Queue

from app.spider import Spider

from app.general import *


class Scheduler:

    # NUMBER_OF_THREADS = 8
    queue = Queue()
    DIR_NAME = "data"
    QUEUE_FILE = DIR_NAME + '/queue.txt'

    def __init__(self, seed, keyword):
        self.seed = seed
        self.keyword = keyword
        self.domain_name = get_domain_name(self.seed)
        self.style = 'bfs'

    def init_spider(self, style):
        self.style = style
        Spider(Scheduler.DIR_NAME, self.seed, self.domain_name, self.keyword, self.style)

    @staticmethod
    def create_spider():
        t = threading.Thread(target=Scheduler.work)
        t.daemon = True
        t.start()

    @staticmethod
    def work():
        while True:
            url = Scheduler.queue.get()
            Spider.crawl_page_bfs(url)
            # Spider.crawl_page(threading.current_thread().name, url)
            Scheduler.queue.task_done()

    def create_jobs(self):
        # will run depth wise?
        for link in file_to_arr(Scheduler.QUEUE_FILE):
            Scheduler.queue.put(link)
        Scheduler.queue.join()
        self.crawl()

    def crawl(self):
        queued_links = file_to_arr(Scheduler.QUEUE_FILE)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + " links in the queue")
            self.create_jobs()
