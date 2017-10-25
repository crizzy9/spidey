from bs4 import BeautifulSoup as soup
from general import store_document
import re

ignore_regex_1 = '(/wiki/)(?!Main_Page)(([0-9a-z_\-/()]*)('
ignore_regex_2 = ')([0-9a-z_\-/()]*))(?!:|.jpg|.png)'

# add all special characters

# allowed_characters = ['', '-', '_', '.', '+', '!', '*', ',', '$', ':', '/', '\'', '\"']

# check for other special characters also like @ % & etc but check if they are not params or references like dont take # values

without_keyword_regex = re.compile('(/wiki/)(?!Main_Page)([0-9a-z%_–\-/()!\'\"*+;.:,$]*)', re.IGNORECASE)
ignore_list = [".jpg", ":", ".png"]
normal_regex = re.compile('([0-9a-zA-Z_\-/().:,$%]*)', re.MULTILINE)


class LinkFinder:

    def __init__(self, base_url, page_url, domain_name, count):
        super().__init__()
        self.base_url = base_url
        self.page_url = page_url
        self.domain_name = domain_name
        self.links = []
        self.count = count

    def scrape_links(self, html, keyword, only_store_documents):
        page_soup = soup(html, "html.parser")
        header = page_soup.h1
        body_content = page_soup.find("div", {"id": "bodyContent"})
        urls = body_content.find_all("a")
        # urls = page_soup.find_all("a")

        header_text = header.text

        store_document(self.count, header.text, self.page_url, page_soup)

        if not only_store_documents:
            ignore_regex = re.compile(ignore_regex_1 + keyword + ignore_regex_2, re.IGNORECASE)

            for link in urls:
                if link.has_attr("href"):
                    # try to do keyword check outside loop
                    # focused crawling
                    if keyword.strip() != "":
                        m = ignore_regex.match(link.get("href"))
                        if m is not None:
                            string = str(m.group())
                            index = string.lower().find(keyword)
                            if string[index - 1].isalpha():
                                continue

                    # normal crawling
                    else:
                        m = without_keyword_regex.match(link.get("href"))
                        if m is not None and any(ext in m.group() for ext in ignore_list):
                            continue

                    if m is not None:
                        new_link = self.domain_name + m.group()

                        if new_link not in self.links:
                            self.links.append(new_link)


    def page_links(self):
        return self.links

    def error(self, message):
        pass

