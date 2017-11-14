import re
from bs4 import BeautifulSoup as soup
from app.general import *


class Parser:

    # give options
    case_folding = True
    handle_punctuation = True
    parsed_content = ""

    # regex to remove punctuation
    punc_regex = re.compile(r'([!"#&\'()*+/:;<=>?@\\^_`{|}~])|([.,$])(?![0-9])|(?<![0-9])(%)|(\[[0-9a-zA-Z/]*])|([^\x00-\x7F\u2013]+)')

    def __init__(self, crawled):
        self.crawled = crawled

    def parse_documents(self):
        for doc in self.crawled:
            file_name = os.path.join('documents', doc)
            with open(file_name, 'r+') as f:
                content = f.read()
                body_content = soup(content, "html.parser")
                self.convert_to_plain_text(body_content)
                print("\nDOC: " + doc + "\n\n" + self.parsed_content)
                f.seek(0)
                f.truncate()
                title = doc.lower().translate(str.maketrans({'_': ' ', '(': '', ')': ''}))
                f.write(title + "\n " + str(self.parsed_content))

    # def __init__(self, count, page_title, page_url, html):
    #     self.doc_count = count
    #     self.title = page_title
    #     self.url = page_url
    #     # soup object
    #     self.page_soup = soup(html, "html.parser")
    #     self.body_content = self.page_soup.find("div", {"id": "bodyContent"})

    def convert_to_plain_text(self, content):
        all_p_tags = content.find_all("p")
        print("this is p tags", all_p_tags)
        self.parsed_content = ""
        for p in all_p_tags:
            # remove all span tags inside p tag
            [span.extract() for span in p('span')]
            # p.translate(str.maketrans('', '', '!"#$&\'()*+/:;<=>?@[\\]^_`{|}~'))
            # could use translate string.punctuations also but wont work with numbers in between
            if self.handle_punctuation:
                self.parsed_content += re.sub(self.punc_regex, '', self.get_tag_text(p))
            else:
                self.parsed_content += self.get_tag_text(p)

    # def store_document(self):
    #     store_document(self.title, self.url, self.parsed_content)

    # def get_body_content(self):
    #     return self.body_content

    def get_tag_text(self, tag):
        if self.case_folding:
            return tag.getText().lower()
        else:
            return tag.getText()




