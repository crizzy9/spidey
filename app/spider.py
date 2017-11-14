import time
from urllib.request import urlopen

from app.general import *
from app.link_finder import LinkFinder


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
    prev_request_time = 0

    curr_page_title = ''
    page_titles = []

    queue = []
    crawled = []
    crawled_titles = []

    def __init__(self, dir_name, base_url, domain_name, keyword, style):
        Spider.dir_name = dir_name
        Spider.base_url = base_url.strip()
        Spider.domain_name = domain_name.strip()
        Spider.queue_file = os.path.join(Spider.dir_name, 'queue.txt')
        Spider.bfs_crawled_file = os.path.join(Spider.dir_name, 'bfs_crawled.txt')
        Spider.dfs_crawled_file = os.path.join(Spider.dir_name, 'dfs_crawled.txt')
        Spider.inlinks_file = os.path.join(Spider.dir_name, 'inlinks.pickle')
        Spider.outlinks_file = os.path.join(Spider.dir_name, 'outlinks.pickle')
        Spider.keyword = keyword
        Spider.style = style

        self.boot()

    def boot(self):
        create_dir(Spider.dir_name)
        create_data_files(Spider.dir_name, Spider.base_url)
        Spider.queue = file_to_arr(Spider.queue_file)

        Spider.inlink_graph = file_to_dict(Spider.inlinks_file)
        Spider.outlink_graph = file_to_dict(Spider.outlinks_file)

        # initializing vars which are different for bfs and dfs
        Spider.depth = 0
        Spider.prev_depth_len = 0
        Spider.counter = 0

        if Spider.style == 'bfs':
            Spider.crawled = file_to_arr(Spider.bfs_crawled_file)
            self.crawl_page_bfs(Spider.base_url)
        else:
            Spider.crawled = file_to_arr(Spider.bfs_crawled_file)
            self.crawl_pages_dfs()


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

            # doing graph stuff
            url_title = get_url_title(page_url)
            if url_title not in Spider.outlink_graph.keys():
                Spider.outlink_graph[url_title] = get_titles_for_urls(matched_links)

            Spider.queue.remove(page_url)
            Spider.crawled.append(page_url)
            Spider.update_files()
            print('Queue: ' + str(len(Spider.queue)) + ' | Crawled: ' + str(len(Spider.crawled)))

        Spider.counter += 1

    @staticmethod
    def crawl_pages_dfs():

        while Spider.queue:
            # queue acts as a stack
            url = Spider.queue.pop()

            if url in Spider.crawled:
                continue

            if len(Spider.crawled) >= Spider.limit:
                break

            print("Crawling:", url)
            matched_links = Spider.gather_links(url)
            print("Found:", len(matched_links), " links")

            # doing graph stuff
            url_title = get_url_title(url)
            if url_title not in Spider.outlink_graph.keys():
                Spider.outlink_graph[url_title] = get_titles_for_urls(matched_links)

            if Spider.depth < Spider.max_depth:
                Spider.depth += 1
                for link in reversed(matched_links):
                    Spider.queue.append(link)
            else:
                Spider.depth -= 1

            print("Reached depth: ", Spider.depth)
            # adding to crawled links
            Spider.crawled.append(url)
            print('Crawled: ' + str(len(Spider.crawled)))

        Spider.queue = []
        Spider.update_graph()
        Spider.update_files()

    @staticmethod
    def manage_depth():
        # depth logic for bfs
        if Spider.counter == Spider.prev_depth_len:
            Spider.depth += 1
            Spider.counter = 0
            Spider.prev_depth_len = len(Spider.queue)
            print("Now crawling Depth " + str(Spider.depth) + "\nGetting Depth " + str(Spider.depth + 1) + " links"
                  + "\nDepth " + str(Spider.depth - 1) + ": had " + str(Spider.prev_depth_len) + " links")

    @staticmethod
    def gather_links(page_url):
        html = ''
        # delaying requests so they are at-least 1 sec apart
        request_time = time.time()
        diff = request_time - Spider.prev_request_time
        if diff < 1:
            print("Waiting for sometime before next request...", diff)
            time.sleep(1) # - diff
        Spider.prev_request_time = request_time
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html; charset=UTF-8':
                html = response.read()
            finder = LinkFinder(Spider.base_url, page_url, Spider.domain_name, len(Spider.crawled))
            finder.scrape_links(html, Spider.keyword)
            Spider.curr_page_title = finder.get_current_page_title()
            Spider.page_titles = finder.page_titles()
        except:
            print('Error: could not crawl page', page_url)
            return []

        links = finder.page_links()
        return links

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if url.lower() in [u.lower() for u in Spider.queue]:
                continue
            if url.lower() in [u.lower() for u in Spider.crawled]:
                continue
            if Spider.domain_name.lower() not in url.lower():
                continue
            # logic for 1000 urls and 6 depth
            if len(Spider.queue) + len(Spider.crawled) < Spider.limit and Spider.depth <= Spider.max_depth:
                Spider.queue.append(url)
            else:
                break

    @staticmethod
    def update_graph():
        # putting only titles in crawled titles for making graph
        Spider.crawled_titles = get_titles_for_urls(Spider.crawled)

        # change outlink graph to only include the links that have been crawled
        # only keep the links that are in the crawled list
        for key in Spider.outlink_graph.keys():
            if key not in Spider.crawled_titles:
                del Spider.outlink_graph[key]
                continue
            new_titles = []
            for title in Spider.outlink_graph[key]:
                if title in Spider.crawled_titles and title != key:
                    new_titles.append(title)
            Spider.outlink_graph[key] = new_titles

        # create inlink graph
        for key in Spider.outlink_graph.keys():
            for title in Spider.outlink_graph[key]:
                if title not in Spider.inlink_graph.keys():
                    Spider.inlink_graph[title] = [key]
                elif key not in Spider.inlink_graph[title]:
                    Spider.inlink_graph[title].append(key)
            if key not in Spider.inlink_graph.keys():
                Spider.inlink_graph[key] = []

    # updates the queue, crawled and graph files
    @staticmethod
    def update_files():
        arr_to_file(Spider.queue, Spider.queue_file)
        if Spider.style == 'bfs':
            # updating bfs crawl file
            arr_to_file(Spider.crawled, Spider.bfs_crawled_file)
        else:
            # updating dfs crawl file
            arr_to_file(Spider.crawled, Spider.dfs_crawled_file)
        dict_to_file(Spider.inlink_graph, Spider.inlinks_file)
        dict_to_file(Spider.outlink_graph, Spider.outlinks_file)
