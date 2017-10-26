

class Grapher:

    # class variables shared among all instances

    def __init__(self, current_url, matched_links, queue, crawled, inlinks, outlinks):
        self.url = current_url
        self.links = matched_links
        self.queue = queue
        self.crawled = crawled
        self.inlink_graph = inlinks
        self.outlink_graph = outlinks
        self.doc_ids = []

        self.curr_doc = self.get_document_id(self.url)
        self.get_document_ids()

    def get_document_ids(self):
        # get index of all links from crawled and store it as doc_id
        for link in self.links:
            doc = self.get_document_id(link)
            if doc != -1:
                self.doc_ids.append(doc)
            else:
                continue

    def get_document_id(self, link):
        try:
            return self.crawled.index(link)
        except ValueError:
            try:
                return len(self.crawled) + self.queue.index(link)
            except ValueError:
                # not in queue or crawled so ignore
                return -1

    def update_outlink_graph(self):
        self.outlink_graph[self.curr_doc] = self.doc_ids

    def update_inlink_graph(self):
        for doc_id in self.doc_ids:
            if doc_id not in self.inlink_graph.keys():
                self.inlink_graph[doc_id] = [self.curr_doc]
            elif self.curr_doc not in self.inlink_graph[doc_id]:
                self.inlink_graph[doc_id].append(self.curr_doc)




