from urllib.request import urlopen

from app.general import *
from app.link_finder import LinkFinder

from app.grapher import Grapher


class Spider:

    # Class variables (shared among all instances)
    dir_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    bfs_crawled_file = ''
    dfs_crawled_file = ''
    inlinks_file = ''
    outlinks_file = ''
    keyword = ''
    style = 'bfs'
    depth = 0
    max_depth = 6
    prev_depth_len = 0
    counter = 0
    limit = 1000
    inlink_graph = {}
    outlink_graph = {}

    # remove redundant variables
    queue = []
    crawled = []

    def __init__(self, dir_name, base_url, domain_name, keyword, style):
        Spider.dir_name = dir_name
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue_file = os.path.join(Spider.dir_name, 'queue.txt')
        Spider.bfs_crawled_file = os.path.join(Spider.dir_name, 'bfs_crawled.txt')
        Spider.dfs_crawled_file = os.path.join(Spider.dir_name, 'dfs_crawled.txt')
        Spider.inlinks_file = os.path.join(Spider.dir_name, 'inlinks.pickle')
        Spider.outlinks_file = os.path.join(Spider.dir_name, 'outlinks.pickle')
        Spider.keyword = keyword
        Spider.style = style
        self.dep = 0

        self.boot()

    def boot(self):
        create_dir(Spider.dir_name)
        create_data_files(Spider.dir_name, Spider.base_url)
        Spider.queue = file_to_arr(Spider.queue_file)

        Spider.inlink_graph = file_to_dict(Spider.inlinks_file)
        Spider.outlink_graph = file_to_dict(Spider.outlinks_file)

        #initializing vars which are different for bfs and dfs
        Spider.depth = 0
        Spider.prev_depth_len = 0
        Spider.counter = 0

        if Spider.style == 'bfs':
            Spider.crawled = file_to_arr(Spider.bfs_crawled_file)
            self.crawl_page_bfs(Spider.base_url)
        else:
            Spider.crawled = file_to_arr(Spider.bfs_crawled_file)
            self.crawl_page_dfs(Spider.base_url)


    @staticmethod
    def crawl_page_bfs(page_url):
        if page_url not in Spider.crawled:

            print("Crawling:", page_url)
            matched_links = Spider.gather_links(page_url)
            print("Found:", len(matched_links), " links")

            Spider.manage_depth()

            if page_url not in Spider.queue:
                Spider.queue.append(page_url)

            Spider.add_links_to_queue(matched_links)

            # create graph now
            Spider.add_to_graph(page_url, matched_links)

            Spider.queue.remove(page_url)
            Spider.crawled.append(page_url)
            Spider.update_files()

            print('Queue: ' + str(len(Spider.queue)) + ' | Crawled: ' + str(len(Spider.crawled)))

        Spider.counter += 1

    def crawl_page_dfs(self, page_url):



        if page_url not in Spider.crawled:
            if self.dep < Spider.max_depth or len(Spider.crawled) >= Spider.limit:
                self.dep += 1
                print("CRAWLING depth", self.dep)
            else:
                return
            print("Crawling:", page_url)
            matched_links = Spider.gather_links(page_url)
            print("Found:", len(matched_links), " links")
            # adding to crawled links
            Spider.crawled.append(page_url)
            # update crawled file
            arr_to_file(Spider.crawled, Spider.dfs_crawled_file)

            for link in matched_links:
                print("Crawled:", str(len(Spider.crawled)), "Depth:", self.dep)
                self.crawl_page_dfs(link)



    @staticmethod
    def manage_depth():
        # depth logic
        if Spider.counter == Spider.prev_depth_len:
            Spider.depth += 1
            Spider.counter = 0
            Spider.prev_depth_len = len(Spider.queue)
            # get depth properly
            print("Now crawling Depth " + str(Spider.depth) + "\nGetting Depth " + str(Spider.depth + 1) + " links"
                  + "\nDepth " + str(Spider.depth - 1) + ": had " + str(Spider.prev_depth_len) + " links")

    @staticmethod
    def gather_links(page_url):
        html = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html; charset=UTF-8':
                html = response.read()
            finder = LinkFinder(Spider.base_url, page_url, Spider.domain_name, len(Spider.crawled))
            finder.scrape_links(html, Spider.keyword)
        except:
            print('Error: could not crawl page', page_url)
            return []

        links = finder.page_links()
        return links

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url in Spider.queue:
                continue
            if url in Spider.crawled:
                continue
            if Spider.domain_name not in url:
                continue
            # logic for 1000 urls and 6 depth
            if len(Spider.queue) + len(Spider.crawled) < Spider.limit and Spider.depth <= Spider.max_depth:
                Spider.queue.append(url)
            else:
                break

    @staticmethod
    def add_to_graph(current_url, matched_links):
        grapher = Grapher(current_url, matched_links, Spider.queue, Spider.crawled, Spider.inlink_graph, Spider.outlink_graph)
        # could just save outlink graph right now and generate inlink graph later
        # check for efficiency later
        grapher.update_outlink_graph()
        grapher.update_inlink_graph()

    @staticmethod
    def update_files():
        # check execution time after removing this
        # if possible update these after execution finished to reduce execution time
        arr_to_file(Spider.queue, Spider.queue_file)
        # updating bfs crawl file
        arr_to_file(Spider.crawled, Spider.bfs_crawled_file)
        dict_to_file(Spider.inlink_graph, Spider.inlinks_file)
        dict_to_file(Spider.outlink_graph, Spider.outlinks_file)
