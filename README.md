# PTT Crawler

一個用於練習 BeautifulSoap 的小實驗，

## Example

```python
    crawler = PttCrawler()
    crawler.crawl(board="欲爬取的看版名稱", start=100, end=102)
```
`start` 表示想從哪一頁開始爬取，`end` 則是爬到哪一頁時會停止，比方說想爬取八卦版的 90 ~ 100 頁，可以設定為：

```python
	crawler.crawl(board="Gossiping", start=90, end=101)
```

## Data format

每爬完一整頁的所有文章就會進行一次輸出，檔案格式為 json :

```json

    {
        "content": "文章內容",
        "responses": [
            {
                "content": "推文內容", 
                "vote": "推文立場(箭頭、推、噓)", 
                "user": "推文 ID"
            }
        ], 
        "title": "文章標題"
    }
```