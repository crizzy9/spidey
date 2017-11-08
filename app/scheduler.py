import threading
from queue import Queue

from app.spider import Spider

from app.general import *


class Scheduler:

    queue = Queue()
    DIR_NAME = "data"
    QUEUE_FILE = DIR_NAME + '/queue.txt'

    def __init__(self, seed, keyword):
        self.seed = seed
        self.keyword = keyword
        self.domain_name = get_domain_name(self.seed)
        self.style = 'bfs'

    # method to initialize the spider and the style
    def init_spider(self, style):
        self.style = style
        Spider(Scheduler.DIR_NAME, self.seed, self.domain_name, self.keyword, self.style)

    @staticmethod
    def create_spider():
        t = threading.Thread(target=Scheduler.work)
        t.daemon = True
        t.start()

    # the method executed by the thread
    @staticmethod
    def work():
        while True:
            url = Scheduler.queue.get()
            Spider.crawl_page_bfs(url)
            Scheduler.queue.task_done()

    # mutual recursion between crawl and create jobs
    def create_jobs(self):
        for link in file_to_arr(Scheduler.QUEUE_FILE):
            Scheduler.queue.put(link)
        Scheduler.queue.join()
        self.crawl()

    # mutual recursion between crawl and create jobs
    def crawl(self):
        queued_links = file_to_arr(Scheduler.QUEUE_FILE)
        if len(queued_links) > 0:
            print(str(len(queued_links)) + " links in the queue")
            self.create_jobs()
