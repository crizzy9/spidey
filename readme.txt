THINGS REQUIRED:

1) install python 3.5
2) install pyCharm
3) install pip3 if not already installed with python3
4) install beautifulsoup4



DESIGN CHOICES and CODE EXPLANATION:

parser.py
The options to chose casefolding and punctuation hadling is given in the main.py file
the options can be accessed using
# parser.case_folding = False
# parser.handle_punctuation = False
The parser gets all the p tags from the html content that was downloaded
The parser then takes out all the span tags from it to remove all the formulas in the document
The parser has a regex which is designed to remove all kinds of PUNCTUATIONS and REFERENCES and FOREIGN CHARACTERS
The regex also keeps the important punctuations intact such as '$' '%' '.' ',' in case of numbers
and preserves the - in case of letters

indexer.py
This parsed content is then fed to the indexer
The indexer takes the documents and creats all 3 indexes and their tf/df tables and stores them in the data directory
The indexer sorts the terms and inverted list by the number of documents a term appears in and the inverted lists are
sorted by the document frequency


CRAWLER ARCHITECTURE:

- Firstly main.py will be executed and a scheduler object is created in it
- The scheduler object is passed the style in which the crawling needs to be done bfs/dfs
- The scheduler creates a Spider instance and starts crawling
- The spider.py file contains the core logic of the crawler
- The page_rank.py file takes in the inlink and outlink graph and is independent of the crawler
- link_finder.py contains the core link scrapping logic of the crawler
- general.py contains all the small helper functions needed in the crawler
- parser.py takes all the crawled documents and parses them and stores them again
- indexer.py takes all the parsed documents and creates unigram, bigram and trigram index from it
- The crawler could generate 5 files in the data directory which includes
    - bfs_crawled.txt     :  list of all links crawled in bfs crawler
    - dfs_crawled.txt.    :  list of all links crawled in dfs crawler
    - queue.txt      : list of all the links in the queue(bfs) or the stack(dfs)
    - inlinks.pickle    : the inlink graph stored in a pickle format for compression
    - outlinks.pickle  : the outlink graph stored in a pickle format for compression
    - pagerank.txt     : page rank of all the crawled urls in order
    - index_uni/bi/trigram.txt    : all three indexes
    - tf/df_table.txt : td/df table for all 3 indexes
    - token.txt   : number of tokens in each document
- After crawling a document it is stored in the documents directory, named as a number


HOW TO RUN THE PROGRAM:

1) run the main.py file
2) input the seed url
3) input the keyword for focused crawling/ no keyword for normal crawling