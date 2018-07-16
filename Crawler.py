# -*- coding: UTF-8 -*-

import json
import requests
import time

from bs4 import BeautifulSoup
from bs4.element import NavigableString

def main():

    crawler = PttCrawler()
    crawler.crawl(board="Gossiping", start=10001, end=11000)

    #res = crawler.parse_article("https://www.ptt.cc/bbs/Gossiping/M.1119928928.A.78A.html")
    #crawler.output("test", res)


class PttCrawler:

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
        '''文章內容的生成器
        Args:
            page: 頁面網址
        Returns:
            文章內容的生成器
        '''

        res  = self.session.get(page, verify=False)
        soup = BeautifulSoup(res.text, "lxml")

        for article in soup.select(".r-ent"):
            try:
                yield self.main + article.select(".title")[0].select("a")[0].get("href")
            except:
                pass # (本文已被刪除)

    def pages(self, board=None, index_range=None):
        '''頁面網址的生成器
        Args:
            board: 看板名稱
            index_range: 文章頁數範圍
        Returns:
            網址的生成器
        '''
        
        target_page = self.root + board + "/index"

        if range is None:
            yield target_page + ".html"
        else:
            for index in index_range:
                yield target_page + str(index) + ".html"

    def parse_article(self, url, mode):
        '''解析爬取的文章，整理進dict
        Args:
            url: 欲爬取的PTT頁面網址
            mode: 欲爬取回文的模式。全部(all)、推文(up)、噓文(down)、純回文(normal)
        Returns:
            article: 爬取文章後資料的dict
            
        '''
        
        # 處理mode標誌
        if mode == 'all':
            mode = 'all'
        elif mode == 'up':
            mode = u'推'
        elif mode == 'down':
            mode = u'噓'
        elif mode == 'normal':
            mode = '→'
        else:
            raise ValueError("mode變數錯誤", mode)

        raw  = self.session.get(url, verify=False)
        soup = BeautifulSoup(raw.text, "lxml")

        try:
            article = {}

            # 取得文章作者與文章標題
            article["Author"] = soup.select(".article-meta-value")[0].contents[0].split(" ")[0]
            article["Title"]  = soup.select(".article-meta-value")[2].contents[0]

            # 取得內文
            content = ""
            for tag in soup.select("#main-content")[0]:
                if type(tag) is NavigableString and tag !='\n':
                    content += tag
                    break
            article["Content"] = content

            # 處理回文資訊
            upvote = 0
            downvote = 0
            novote = 0
            response_list = []

            for response_struct in soup.select(".push"):

                #跳脫「檔案過大！部分文章無法顯示」的 push class
                if "warning-box" not in response_struct['class']:

                    response_dic = {}
                    
                    # 根據不同的mode去採集response
                    if mode == 'all':
                        response_dic["Content"] = response_struct.select(".push-content")[0].contents[0][1:]
                        response_dic["Vote"]  = response_struct.select(".push-tag")[0].contents[0][0]
                        response_dic["User"]  = response_struct.select(".push-userid")[0].contents[0]
                        response_list.append(response_dic)
                        
                        if response_dic["Vote"] == u"推":
                            upvote += 1
                        elif response_dic["Vote"] == u"噓":
                            downvote += 1
                        else:
                            novote += 1
                    else:
                        response_dic["Content"] = response_struct.select(".push-content")[0].contents[0][1:]
                        response_dic["Vote"]  = response_struct.select(".push-tag")[0].contents[0][0]
                        response_dic["User"]  = response_struct.select(".push-userid")[0].contents[0]

                        if response_dic["Vote"] == mode:
                            response_list.append(response_dic)
                            
                            if mode == u"推":
                                upvote += 1
                            elif mode == u"噓":
                                downvote += 1
                            else:
                                novote += 1

            article["Responses"] = response_list
            article["UpVote"] = upvote
            article["DownVote"] = downvote
            article["NoVote"] = novote

        except Exception as e:
            print(e)
            print(u"在分析 %s 時出現錯誤" % url)

        return article

    def output(self, filename, data):
        '''爬取完的資料寫到json文件
        Args:
            filename: json檔的文件路徑
            data: 爬取完的資料
        '''
        
        try:
            with open(filename+".json", 'wb+') as op:
                op.write(json.dumps(data, indent=4, ensure_ascii=False).encode('utf-8'))
                print('爬取完成~', filename + '.json', '輸出成功！')
        except Exception as err:
            print(filename + '.json', '輸出失敗 :(')
            print('error message:', err)
        
    def crawl(self, board="Gossiping", mode='all', start=1, end=2, sleep_time=0.5):
        '''爬取資料主要接口
        Args:
            board: 欲爬取的看版名稱
            mode: 欲爬取回文的模式。全部(all)、推文(up)、噓文(down)、純回文(normal)
            start: 從哪一頁開始爬取
            end: 爬取到哪一頁停止
            sleep_time: sleep間隔時間
        '''

        crawl_range = range(start, end)

        for page in self.pages(board, crawl_range):
            res = []
            
            for article in self.articles(page):
                res.append(self.parse_article(article, mode))
                time.sleep(sleep_time)
            
            print(u"已經完成 %s 頁面第 %d 頁的爬取" %(board, start))
            self.output(board + str(start), res)
            
            start += 1


if __name__ == '__main__':
    main()
