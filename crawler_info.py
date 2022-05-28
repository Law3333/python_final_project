import bs4
import urllib.request as req
from urllib.parse import quote


class get_basic_info:
    def __init__(self, keyword):

        # input 使用 UrlDecode 編碼
        self.keyword_urldecode = quote(keyword)

        # Headers info
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        }

    def get_isbn(self):
        '''Get ISBN of book'''

        url = f"https://libholding.ntut.edu.tw/booksearch.do?searchtype=simplesearch&search_field=FullText&search_input={self.keyword_urldecode}&searchsymbol=hyLibCore.webpac.search.common_symbol&execodehidden=true&execode=&ebook="

        data = self.link_connect(url)

        # ---解析原始碼(html)---
        root = bs4.BeautifulSoup(data, "html.parser")
        # print(root.li.string)  # 作者：韓國瑜

        # 尋找 class = "bookDetail" 的 div 標籤
        book_info = root.find_all("div", class_="bookDetail")
        book_info = root.find_all("li")
        print(book_info)
        # for auther in book_info:
        #     if auther.a != None:  # 如果標題包含 li 標籤 (沒有被刪除)，印出來
        #         print(auther.a)

    def get_info(self):
        '''Get basic info of book'''

        url = f"https://libholding.ntut.edu.tw/maintain/rightFrame.jsp?searchtype=simplesearch&search_field=FullText&search_input={self.keyword_urldecode}&searchsymbol=hyLibCore.webpac.search.common_symbol&execodehidden=true&execode=&ebook=&resid=188829727&nowpage=1"

        data = self.link_connect(url)
        print(data)

        root = bs4.BeautifulSoup(data, "html.parser")

    def link_connect(self, url):

        # let program like a people
        # 建立一個 Request 物件，附加 Headers 的資訊
        self.requert = req.Request(url, headers=self.headers)

        with req.urlopen(self.requert) as response:
            data = response.read().decode("utf-8")

        return data


get_basic_info("跟著月亮").get_info()
