from urllib.request import urlopen
import pickle
from link_finder import LinkFinder
from grapher import Grapher
from general import *


class Spider:

    # Class variables (shared among all instances)
    dir_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    graph_file = ''
    keyword = ''
    depth = 0
    prev_depth_len = 0
    counter = 0
    only_storage = False
    limit = 50
    graph = {}

    # remove redundant variables like counter and use crawled length

    queue = []
    crawled = []

    def __init__(self, dir_name, base_url, domain_name, keyword):
        Spider.dir_name = dir_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = os.path.join(Spider.dir_name, 'queue.txt')
        Spider.crawled_file = os.path.join(Spider.dir_name, 'crawled.txt')
        Spider.graph_file = os.path.join(Spider.dir_name, 'graph.pickle')
        Spider.keyword = keyword

        self.boot()

        self.crawl_page('Init crawl: ', Spider.base_url)

    @staticmethod
    def boot():
        create_dir(Spider.dir_name)
        create_data_files(Spider.dir_name, Spider.base_url)
        Spider.queue = file_to_arr(Spider.queue_file)
        Spider.crawled = file_to_arr(Spider.crawled_file)

        if os.path.isfile(Spider.graph_file):
            print("Loading graph file...")
            if os.path.getsize(Spider.graph_file) > 0:
                with open(Spider.graph_file, "rb") as handle:
                    Spider.graph = pickle.load(handle)
        else:
            print("Creating graph file...")
            f = open(Spider.graph_file, "wb+")
            f.close()

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:

            matched_links = Spider.gather_links(page_url)
            print("Crawling:", page_url, "\nFound:", len(matched_links))
            # print(thread_name + ' crawling ' + page_url)

            # depth logic
            if Spider.counter == Spider.prev_depth_len:
                Spider.depth += 1
                Spider.counter = 0
                Spider.prev_depth_len = len(Spider.queue)
                # get depth properly
                print("Now crawling Depth " + str(Spider.depth) + "\nGetting Depth " + str(Spider.depth + 1) + " links"
                      + "\nDepth " + str(Spider.depth - 1) + ": had " + str(Spider.prev_depth_len) + " links")

            if page_url not in Spider.queue:
                Spider.queue.append(page_url)

            # remove total length
            total_length = len(Spider.crawled) + len(Spider.queue)

            Spider.add_links_to_queue(matched_links, total_length)

            # create graph now
            Spider.add_to_graph(page_url, matched_links)

            # if total_length + len(matched_links) <= Spider.limit and Spider.depth <= 6:
            #     Spider.add_links_to_queue(matched_links, total_length)
            # else:
            #     Spider.only_storage = True
            #     Spider.add_links_to_queue(matched_links, total_length)

            Spider.queue.remove(page_url)
            if page_url not in Spider.crawled:
                Spider.crawled.append(page_url)
            Spider.update_files()

            print('Queue: ' + str(len(Spider.queue)) + ' | Crawled: ' + str(len(Spider.crawled)))

        Spider.counter += 1

    @staticmethod
    def gather_links(page_url):
        html = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html; charset=UTF-8':
                html = response.read()
            finder = LinkFinder(Spider.base_url, page_url, Spider.domain_name, len(Spider.crawled))
            finder.scrape_links(html, Spider.keyword)
        except :
            print('Error: could not crawl page', page_url)
            return []

        links = finder.page_links()
        return links

    @staticmethod
    def add_links_to_queue(links, total):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            # logic for 1000 urls and 6 depth
            if total < Spider.limit and Spider.depth <= 6:
                Spider.queue.append(url)
                total += 1
            else:
                break

    @staticmethod
    def add_to_graph(current_url, matched_links):
        grapher = Grapher(Spider.graph, current_url, matched_links, Spider.queue, Spider.crawled)
        grapher.update_graph()

    @staticmethod
    def update_files():
        arr_to_file(Spider.queue, Spider.queue_file)
        arr_to_file(Spider.crawled, Spider.crawled_file)
        with open(Spider.graph_file, "wb") as handle:
            pickle.dump(Spider.graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
