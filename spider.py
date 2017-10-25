from urllib.request import urlopen
from link_finder import LinkFinder
from general import *


class Spider:

    # Class variables (shared among all instances)
    dir_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    keyword = ''
    depth = 0
    prev_depth_len = 0
    counter = 0
    only_storage = False
    limit = 1000

    # remove redundant variables like counter and use crawled length

    queue = []
    crawled = []

    def __init__(self, dir_name, base_url, domain_name, keyword):
        Spider.dir_name = dir_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = os.path.join(Spider.dir_name, 'queue.txt')
        Spider.crawled_file = os.path.join(Spider.dir_name, 'crawled.txt')
        Spider.keyword = keyword

        self.boot()

        self.crawl_page('Init crawl: ', Spider.base_url)

    @staticmethod
    def boot():
        create_dir(Spider.dir_name)
        create_data_files(Spider.dir_name, Spider.base_url)
        Spider.queue = file_to_arr(Spider.queue_file)
        Spider.crawled = file_to_arr(Spider.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print('Queue: ' + str(len(Spider.queue)) + ' | Crawled: ' + str(len(Spider.crawled)))
            print("Crawling:", page_url)
            # print(thread_name + ' crawling ' + page_url)

            matched_links = Spider.gather_links(page_url)

            if Spider.counter == Spider.prev_depth_len:
                Spider.depth += 1
                Spider.counter = 0
                Spider.prev_depth_len = len(Spider.queue)
                # this means that the crawler has started crawling this depth
                # or the other way around?
                # get depth properly
                print("Now crawling Depth " + str(Spider.depth) + "\nGetting Depth " + str(Spider.depth + 1) + " links"
                      + "\nDepth " + str(Spider.depth - 1) + ": had " + str(Spider.prev_depth_len) + " links")

            if page_url not in Spider.queue:
                Spider.queue.append(page_url)

            total_length = len(Spider.crawled) + len(Spider.queue)
            if total_length + len(matched_links) <= Spider.limit and Spider.depth <= 6:
                Spider.add_links_to_queue(matched_links, total_length)
            else:
                Spider.only_storage = True
                Spider.add_links_to_queue(matched_links, total_length)
                # could add less links in queue if duplicates are there at the end of the matched links and dont reach limit
                # and not all 1000 documents getting stored.. so exit only after that is done

            Spider.queue.remove(page_url)
            if page_url not in Spider.crawled:
                Spider.crawled.append(page_url)
            Spider.update_files()
        Spider.counter += 1

    @staticmethod
    def gather_links(page_url):
        html = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html; charset=UTF-8':
                html = response.read()
            finder = LinkFinder(Spider.base_url, page_url, Spider.domain_name, len(Spider.crawled))
            finder.scrape_links(html, Spider.keyword, Spider.only_storage)
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
            if total < Spider.limit:
                Spider.queue.append(url)
                total += 1
            else:
                break

    @staticmethod
    def update_files():
        arr_to_file(Spider.queue, Spider.queue_file)
        arr_to_file(Spider.crawled, Spider.crawled_file)
