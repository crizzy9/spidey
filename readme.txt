Things required:

1) install python 3.5
2) install pyCharm
3) install pip3 if not already installed with python3
4) install beautifulsoup4

Crawler Architecture

- Firstly main.py will be executed and a scheduler object is created in it
- The scheduler object is passed the style in which the crawling needs to be done bfs/dfs
- The scheduler creates a Spider instance and starts crawling
- The spider.py file contains the core logic of the crawler
- The page_rank.py file takes in the inlink and outlink graph and is independent of the crawler
- link_finder.py contains the core link scrapping logic of the crawler
- general.py contains all the small helper functions needed in the crawler
- The crawler could generate 5 files in the data directory which includes
    - bfs_crawled.txt     :  list of all links crawled in bfs crawler
    - dfs_crawled.txt.    :  list of all links crawled in dfs crawler
    - queue.txt      : list of all the links in the queue(bfs) or the stack(dfs)
    - inlinks.pickle    : the inlink graph stored in a pickle format for compression
    - outlinks.pickle  : the outlink graph stored in a pickle format for compression
    - pagerank.txt     : page rank of all the crawled urls in order
- After crawling a document it is stored in the documents directory, named as a number

The source code for the PageRank implementation is in page_rank.py
I am using mutual recursion to do bfs crawling the logic for which you can view in Scheduler.py
For the dfs crawler I have used the stack method the logic for which is inside Spider.py

To run the program:

1) run the main.py file
2) input the seed url
3) input the keyword for focused crawling/ no keyword for normal crawling