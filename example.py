# -*- coding: UTF-8 -*-

from sys import argv
from Crawler import PttCrawler

def main():

    crawler = PttCrawler()
    mode = 'up' # 只爬推文

    if len(argv) == 3:
        mode = argv[2]
        result = crawler.parse_article(argv[1], mode)
        crawler.output("result", result)

    elif len(argv) == 5:
        mode = argv[4]
        crawler.crawl(board=argv[1], start=int(argv[2]), end=int(argv[3]), mode=argv[4])

    else:
        print("使用方式有兩種：")
        print("1) python %s 欲爬取的url" % argv[0])
        print("2) python %s 欲爬取的版面 從哪一頁開始爬 爬到哪一頁為止" % argv[0])

if __name__=="__main__":
    main()
