

class Grapher:

    # class variables shared among all instances
    # curr_doc = -1
    # doc_ids = []

    def __init__(self, graph, current_url, matched_links, queue, crawled):
        self.url = current_url
        self.links = matched_links
        self.queue = queue
        self.crawled = crawled
        self.graph = graph

        self.doc_ids = []

        try:
            self.curr_doc = self.crawled.index(self.url)
        except ValueError:
            try:
                self.curr_doc = len(self.crawled) + self.queue.index(self.url)
            except:
                print("ERROR in getting curr doc")

        self.get_document_ids()

    def get_document_ids(self):
        # get index of all links from crawled and store it as doc_id
        for link in self.links:
            try:
                self.doc_ids.append(self.crawled.index(link))
            except ValueError:
                try:
                    self.doc_ids.append(len(self.crawled) + self.queue.index(link))
                except ValueError:
                    # not in queue or crawled
                    continue

    def update_graph(self):
        print("Current doc:", self.curr_doc, "\ndoc_ids:", self.doc_ids)
        for doc_id in self.doc_ids:
            if doc_id not in self.graph.keys():
                self.graph[doc_id] = [self.curr_doc]
            elif self.curr_doc not in self.graph[doc_id]:
                self.graph[doc_id].append(self.curr_doc)




