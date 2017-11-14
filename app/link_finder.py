import re
from app.general import *
from app.parser import Parser
import sys, traceback

ignore_regex_1 = '(/wiki/)(?!Main_Page)(([0-9a-z%,!_\-/()]*)('
ignore_regex_2 = ')([0-9a-z%,!_\-/()]*))(?!:|.jpg|.png)'

without_keyword_regex = re.compile('(/wiki/)(?!Main_Page)([0-9a-z%_–\-/()!\'\"*+;.:,$]*)', re.IGNORECASE)
ignore_list = [".jpg", ":", ".png"]
normal_regex = re.compile('([0-9a-zA-Z_\-/().:,$%]*)', re.MULTILINE)


class LinkFinder:

    def __init__(self, base_url, page_url, domain_name, count):
        self.base_url = base_url
        self.page_url = page_url
        self.page_title = get_url_title(self.page_url)
        self.domain_name = domain_name
        self.links = []
        self.count = count
        self.titles = []
        self.ignore_regex = None

    def scrape_links(self, html, keyword):

        parser = Parser(self.count, self.page_title, self.page_url, html)

        # options for text transformation
        # parser.case_folding = False
        # parser.handle_punctuation = False

        body_content = parser.get_body_content()
        urls = body_content.find_all("a")

        parser.convert_to_plain_text()
        parser.store_document()

        try:
            self.ignore_regex = re.compile(ignore_regex_1 + keyword.strip() + ignore_regex_2, re.IGNORECASE)
        except:
            # error in ignore regex
            traceback.print_exc(file=sys.stdout)
            pass

        for link in urls:
            if link.has_attr("href"):
                # change keyword to lower case
                # focused crawling
                if keyword.strip() != "":
                    m = self.ignore_regex.match(link.get("href"))
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

                # getting all the links and titles
                if m is not None:
                    new_link = self.domain_name + m.group()

                    if new_link not in self.links:
                        self.links.append(new_link)
                        self.titles.append(get_url_title(new_link))

    def page_links(self):
        return self.links

    def page_titles(self):
        return self.titles

    def get_current_page_title(self):
        return self.page_title

    def error(self, message):
        pass

