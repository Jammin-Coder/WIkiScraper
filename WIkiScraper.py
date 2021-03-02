#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests


class MyParsers:
    def __init__(self, parser=None):
        if not parser:
            self.parser = "lxml"
        else:
            self.parser = parser

    def soupify(self, html):
        return BeautifulSoup(html, self.parser)

    def remove_newlines(self, string):
        parsed_string = ""
        string_segments = string.split("\n")
        if string_segments:
            for i in range(len(string_segments)):
                parsed_string += str(string_segments[i]) + " "
            return parsed_string
        else:
            return string

    def remove_br(self, string):
        split_data = str(string).split("<br/>")
        td = ""
        for item in split_data:
            td += str(item) + " "
        td = self.soupify(td)
        return td

    def parse_table_rows(self, rows):
        # Original code in case something breaks
        # for tr in table_rows:
        #     th = tr.find("th")
        #     td = tr.find("td")
        #
        #     if th and td:
        #         td = self.remove_br(td)
        #         th_text = th.text
        #         td_text = self.remove_newlines(td.text)
        #         info = self.parse_colon_values(th_text, td_text)
        #         print(info)
        #     elif td:
        #         # Filter out useless td's and print good ones.
        #         pass
        info = ""
        for tr in rows:
            th = tr.find("th")
            td = tr.find("td")

            if th and td:
                td = self.remove_br(td)
                th_text = th.text
                td_text = self.remove_newlines(td.text)
                info += self.parse_colon_values(th_text, td_text) + "\n"
            elif td:
                # Filter out useless td's and print good ones.
                pass
        return info

    def parse_colon_values(self, string1, string2):
        if not ":" == string1[-1]:
            new_string = string1 + ": " + string2
        else:
            new_string = string1 + " " + string2
        return new_string


class WikiScraper:
    def __init__(self,  search_term, parser):
        self.html_parser = parser
        self.my_parser = MyParsers(self.html_parser)

        self.search_term = search_term
        self.base_url = "https://en.wikipedia.org/w/index.php?search="
        self.full_url = self.base_url + search_term
        source = requests.get(self.full_url).text
        self.soup = self.my_parser.soupify(source)

    def get_infobox(self):
        infobox = self.soup.find("table", class_="infobox")
        return infobox

    # Get infobox, parse data and display neatly
    def show_info(self):
        infobox = self.my_parser.soupify(str(self.get_infobox()))
        table_rows = infobox.table.find_all("tr")
        info = self.my_parser.parse_table_rows(table_rows)
        print(info)

    # TODO
    """
        def get_styles(self):
            Get styles to
            display images and stats neatly on html page.
    """


search_term = input("Enter something >> ")
print(f"Results for {search_term}:\n")
wiki_scrape = WikiScraper(search_term, "lxml")
wiki_scrape.show_info()
