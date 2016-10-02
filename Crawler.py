# -*- coding: UTF-8 -*-

import json
import requests
from bs4 import BeautifulSoup

def main():
    crawler = PttCrawler()
    crawler.crawl()

class PttCrawler(object):

    root = "https://www.ptt.cc/bbs/"
    main = "https://www.ptt.cc"
    gossip_data = {
        "from":"bbs/Gossiping/index.html",
        "yes": "yes"
    }

    def __init__(self):
        self.session = requests.session()
        self.session.post("https://www.ptt.cc/ask/over18",
                           verify=False,
                           data=self.gossip_data)

    def _test(self, text):

        with open("test.txt",'w') as input:
            input.write(text.encode("utf-8"))

    def articles(self, page):

        res  = self.session.get(page,verify=False)
        soup = BeautifulSoup(res.text, "lxml")
        #self._test(soup.prettify())

        for article in soup.select(".r-ent"):
            yield self.main + article.select(".title")[0].select("a")[0].get("href")

    def pages(self, board=None, index_range=None, output_dir="result/"):

        target_page = self.root + board + "/index"

        if range is None:
            yield target_page + ".html"
        else:
            for index in index_range:
                yield target_page + str(index) + ".html"

    def parse_article(self, url):

        raw  = self.session.get(url, verify=False)
        soup = BeautifulSoup(raw.text, "lxml")

        article = {}
        article["title"]   = soup.select(".article-meta-value")[2].contents[0]
        article["content"] = soup.select("#main-content")[0].contents[4]

        response_list = []

        for response_struct in soup.select(".push"):

            response_dic = {}
            response_dic["vote"] = response_struct.select(".push-tag")[0].contents[0]
            response_dic["user"] = response_struct.select(".push-userid")[0].contents[0]
            #response_dic["time"] = response_struct.select(".push-ipdatetime")[0].contents[0]
            response_dic["content"] = response_struct.select(".push-content")[0].contents[0]
            response_list.append(response_dic)

        article["responses"] = response_list
        return article

    def output(self, filename, data):

        with open(filename+".json", 'w') as op:
            op.write(json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8'))

    def crawl(self, board="Gossiping", start=1, end=2):

        crawl_range = range(start,end)

        for page in self.pages(board, crawl_range):
            res = []
            for article in self.articles(page):
                res.append(self.parse_article(article))
            self.output(board + str(start), res)
            start += 1

if __name__ == '__main__':
    main()
