# -*- coding: UTF-8 -*-

import json
import requests
import time

from bs4 import BeautifulSoup
from bs4.element import NavigableString

def main():

    crawler = PttCrawler()
    crawler.crawl(board="Gossiping", start=73, end=100)

    #res = crawler.parse_article("https://www.ptt.cc/bbs/Gossiping/M.1119928928.A.78A.html")
    #crawler.output("test", res)


class PttCrawler(object):

    root = "https://www.ptt.cc/bbs/"
    main = "https://www.ptt.cc"
    gossip_data = {
        "from":"bbs/Gossiping/index.html",
        "yes": "yes"
    }

    def __init__(self):
        self.session = requests.session()
        requests.packages.urllib3.disable_warnings()
        self.session.post("https://www.ptt.cc/ask/over18",
                           verify=False,
                           data=self.gossip_data)

    def articles(self, page):

        res  = self.session.get(page,verify=False)
        soup = BeautifulSoup(res.text, "lxml")

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

        try:
            article = {}
            article["title"]   = soup.select(".article-meta-value")[2].contents[0]

            content = ""
            for tag in soup.select("#main-content")[0]:
                if type(tag) is NavigableString and tag !='\n':
                    content += tag
                    break
            article["content"] = content

            response_list = []
            for response_struct in soup.select(".push"):

                #跳脫「檔案過大！部分文章無法顯示」的 push class
                if "warning-box" not in response_struct['class']:

                    response_dic = {}
                    response_dic["content"] = response_struct.select(".push-content")[0].contents[0][1:]
                    response_dic["vote"]  = response_struct.select(".push-tag")[0].contents[0][0]
                    response_dic["user"]  = response_struct.select(".push-userid")[0].contents[0]

                    response_list.append(response_dic)

            article["responses"] = response_list
        except Exception as e:
            print(e)
            print(u"在分析 %s 時出現錯誤" % url)

        return article

    def output(self, filename, data):

        with open(filename+".json", 'w') as op:
            op.write(json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8'))

    def crawl(self, board="Gossiping", start=1, end=2, sleep_time=0.5):

        crawl_range = range(start,end)


        for page in self.pages(board, crawl_range):
            res = []
            for article in self.articles(page):
                res.append(self.parse_article(article))
                time.sleep(sleep_time)
            self.output(board + str(start), res)

            print(u"已經完成 %s 頁面第 %d 頁的爬取" %(board,start))
            start += 1


if __name__ == '__main__':
    main()
