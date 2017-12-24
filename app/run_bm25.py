import os
from app.BM25 import BM25


print("Enter FULL path to UNIGRAM INDEX file: ")
indexPath = input()
print("Enter FULL path to DOCUMENTS folder with .txt documents: ")
docsPath = input()
print("Enter FULL path to QUERIES file: ")
queriesPath = input()
print("Enter FULL path where to save SCORES file:")
scoresFile = input()

print("Working on it...")

docs = [d.replace('.txt', '') for d in os.listdir(docsPath)]

bm25 = BM25(docs, docsPath, indexPath, queriesPath, scoresFile)
bm25.calculate_scores()
print("DONE")


# /Users/exmachina/Northeastern/classes/IR/Assignments/spidey/data/index_unigram.txt
# /Users/exmachina/Northeastern/classes/IR/Assignments/spidey/documents
# /Users/exmachina/Northeastern/classes/IR/Assignments/spidey/data/queries.txt
# /Users/exmachina/Northeastern/classes/IR/Assignments/spidey/data/scores.txt
