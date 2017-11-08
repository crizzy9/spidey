import re
from bs4 import BeautifulSoup as soup
from app.general import *


class Transformer:

    # give options
    case_folding = True
    handle_punctuation = True
    # should be a plain text string
    transformed_content = ""

    # regex to remove punctuation
    punc_regex = re.compile(r'([!"#&\'()*+/:;<=>?@\\^_`{|}~])|([.,$])(?![0-9])|(?<![0-9])(%)|(\[[0-9]*])|[^\x00-\x7F]*')

    def __init__(self, count, page_title, page_url, page_soup):
        self.count = count
        self.title = page_title
        self.url = page_url
        # soup object
        self.page_soup = page_soup

    def convert_to_plain_text(self):
        all_p_tags = self.page_soup.find("div", {"id": "bodyContent"}).find_all("p")
        for p in all_p_tags:
            # remove all span tags inside p tag
            [span.extract() for span in p('span')]
            # p.translate(str.maketrans('', '', '!"#$&\'()*+/:;<=>?@[\\]^_`{|}~'))
            # could use translate also but wont work with numbers in between
            self.transformed_content += re.sub(self.punc_regex, '', p.getText().lower())
            # self.transformed_content += p.getText().lower()

    def store_document(self):
        store_document(self.count, self.title, self.url, self.transformed_content)
