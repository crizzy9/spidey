Things required:

1) install python 3.5
2) install pyCharm
3) install pip3 if not already installed with python3
4) install beautifulsoup4

Explaination:

I have implemented a crawler in python which uses multithreading to create multiple crawlers(spiders)
and keeps calling them until there are there are no links in the queue.txt file which gets created once the crawler
starts. The crawler creates one more file crawled.txt which will store all the urls that have been crawled.
This information is stored inside the data directory. After crawling the documents the the downloaded documents are
stored inside the documents directory.

I couldn't complete my multithreaded implementation in time due to collision/duplicate issues so
DO NOT USE MORE THAN 1 THREAD TO IMPLEMENT THIS PROGRAM.


######## check
I have implemented the code in such a way that state of the execution is stored once it is stopped
and resumes at the same position once it is run again



To run the program:

1) run the main.py file
2) input the seed url
3) input the keyword and for focused crawling and no keyword for normal crawling