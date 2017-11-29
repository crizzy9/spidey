import os
import pprint
from app.BM25 import BM25

DOCUMENTS_DIR = '../documents'


docs = [d.replace('.txt', '') for d in os.listdir(DOCUMENTS_DIR)]


pp = pprint.PrettyPrinter(indent=4)

bm25 = BM25(docs, '../data/index_unigram.txt')
# print("Enter queries")
# queries = {1: "hurricane isabel damage", 2: "forecast models", 3: "green energy canada", 4: "heavy rains", 5: "hurricane music lyrics", 6: "accumulated snow", 7: "snow accumulation", 8: "massive blizzards blizzard", 9: "new york city subway"}
bm25.calculate_scores()
print("DONE")
# scores = bm25.get_sorted_scores()
# pp.pprint(scores)