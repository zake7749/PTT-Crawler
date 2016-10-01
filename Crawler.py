import requests
from bs4 import BeautifulSoup


def main():
    crawler = PttCrawler()
    crawler.crawl(left_bound=10, right_bound=60)

class PttCrawler(object):

    root = "https://www.ptt.cc/bbs/"
    gossip_data = {
        "from":"bbs/Gossiping/index.html",
        "yes": "yes"
    }

    def __init__(self):
        self.session = requests.session()
        #self.session.post("https://www.ptt.cc/ask/over18",
        #                   verify=False,
        #                   data=self.gossip_data)

    def _test(self):
        res = self.session.get("https://www.ptt.cc/bbs/Gossiping/index.html",verify=False)
        with open('test.txt','w') as input:
            input.write(res.text.encode('utf-8'))

    def links(self, page=None):

        pass

    def pages(self, board=None, index_range=None, output_dir="result/"):

        target_page = self.root + board + "/index"

        if range is None:
            yield target_page + ".html"
        else:
            for index in index_range:
                yield target_page + str(index) + ".html"

    def crawl(self, board=None, left_bound=1, right_bound=1):

        l = int(left_bound)
        r = int(right_bound)
        crawl_range = range(l,r)

        for page in self.pages("Gossiping", crawl_range):
            for link in self.links(page):
                pass

if __name__ == '__main__':
    main()
