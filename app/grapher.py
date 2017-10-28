

class Grapher:

    # class variables shared among all instances

    def __init__(self, curr_title, matched_titles, inlinks, outlinks):
        self.curr = curr_title
        self.titles = matched_titles
        self.inlink_graph = inlinks
        self.outlink_graph = outlinks

    def update_outlink_graph(self):
        self.outlink_graph[self.curr] = self.titles

    def update_inlink_graph(self):
        for title in self.titles:
            if title not in self.inlink_graph.keys():
                self.inlink_graph[title] = [self.curr]
            elif self.curr not in self.inlink_graph[title]:
                self.inlink_graph[title].append(self.curr)





