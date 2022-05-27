import bs4
import urllib.request as req
from urllib.parse import quote

# input 使用 UrlDecode 編碼


class get_basic_info:
    def __init__(self, keyword):
        self.keyword_urldecode = quote(keyword)
        self.url_front = "https://libholding.ntut.edu.tw/booksearch.do?searchtype=simplesearch&search_field=FullText&search_input="
        self.url_back = "&searchsymbol=hyLibCore.webpac.search.common_symbol&execodehidden=true&execode=&ebook="
        self.url = self.url_front + self.keyword_urldecode + self.url_back

    def executive(self):

        # let program like a people
        # 建立一個 Request 物件，附加 Headers 的資訊
        requert = req.Request(self.url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        })

        with req.urlopen(requert) as response:
            data = response.read().decode("utf-8")
        # print(data)

        # ---解析原始碼---

        root = bs4.BeautifulSoup(data, "html.parser")
        # print(root.li.string)  # 作者：韓國瑜

        # 尋找 class = "bookDetail" 的 div 標籤
        authers = root.find_all("div", class_="bookDetail")
        authers = root.find_all("li")
        print(authers)
        # for auther in authers:
        #     if auther.a != None:  # 如果標題包含 li 標籤 (沒有被刪除)，印出來
        #         print(auther.a)


get_basic_info("跟著月亮").executive()
