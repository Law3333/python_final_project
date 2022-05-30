import bs4
import urllib.request as req
import json
import re
from urllib.parse import quote


class get_basic_info:
    def __init__(self, keyword):

        # input 使用 UrlDecode 編碼
        self.keyword_urldecode = quote(keyword)

        # Headers info
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        }

    def link_connect(self, url):

        # let program like a people
        # 建立一個 Request 物件，附加 Headers 的資訊
        self.requert = req.Request(url, headers=self.headers)

        with req.urlopen(self.requert) as response:
            data = response.read().decode("utf-8")

        return data

    def get_book_id(self):
        '''
        這邊連到搜尋畫面的 API
        '''

        url = f"https://libholding.ntut.edu.tw/booksearch.do?searchtype=simplesearch&search_field=FullText&search_input={self.keyword_urldecode}&searchsymbol=hyLibCore.webpac.search.common_symbol&execodehidden=true&execode=&ebook="

        request_data = self.link_connect(url)

        '''
        ---解析原始碼(html)---

        這裡有兩種情況：
        1.如果輸入書名很完整，系統會跳過搜尋畫面，直接進入該本書的資訊，接著會收到一串包含ID的資料
        例如：<script>parent.location.href = 'bookDetail.do?id=503958';</script>
        接著再利用 ID 進行下一步

        2.如果輸入書名非完整，系統會進入搜尋畫面，得到搜尋資料頁面的API(一大堆HTML)
        首先，要先解析這一堆 HTML ，找到 ID 再進行下一步 

        '''

        root = bs4.BeautifulSoup(request_data, "html.parser")

        try:
            '''在這邊先嘗試第二種情況，如果錯誤則進行第一種情況'''

            # 尋找 Book ID
            # <input id="s511117" name="sid" type="checkbox" value="511117"/>
            book_info = str(root.find_all("input")[1])
            # value="511117"/>
            book_info = book_info.split()[-1]
            #['5', '1', '1', '1', '1', '7']
            book_info = re.findall('\d', book_info)
            # get 511117
            book_id = str()
            for id in book_info:
                book_id += id

            return book_id

        except:
            # parent.location.href = 'bookDetail.do?id=503958';
            book_info = root.script.string
            book_info = re.findall('\d', book_info)
            book_id = str()
            for id in book_info:
                book_id += id

            return book_id

    def get_location(self):
        '''
        這邊連到的是搜尋畫面裡面的 rightFrame.jsp API

        取得館藏地點

        '''

        url = f"https://libholding.ntut.edu.tw/maintain/rightFrame.jsp?searchtype=simplesearch&search_field=FullText&search_input={self.keyword_urldecode}&searchsymbol=hyLibCore.webpac.search.common_symbol&execodehidden=true&execode=&ebook=&resid=188829727&nowpage=1"

        request_data = self.link_connect(url)

        root = bs4.BeautifulSoup(request_data, "html.parser")

        # search book basic info
        book_info = root.find_all("script")[-1].string
        book_info = book_info.replace("\n", "").replace("\r", "")  # 移除換行
        # 抓取存有館藏地點的dict
        location_dict = re.search(
            "var LOC2_json = (.*).*?var SE_json", book_info).group(1)
        location_dict = json.loads(location_dict)
        location_info = location_dict['dataset'][0]['input']
        print(location_info)

        return location_info

    def get_basic_info(self):
        '''
        取得書的基本資料：
        包含
        - 條碼號
        - 作者
        - 索書號
        '''

        book_id = self.get_book_id()

        url = f"https://libholding.ntut.edu.tw/bookDetail.do?id={book_id}&Lflag=1"

        request_data = self.link_connect(url)

        root = bs4.BeautifulSoup(request_data, "html.parser")

        # book_info = |aLB|bA05|c1350240|d783.3886|e8555:2|pCB|k購買|s244|tCCL|y2018|j平裝|oT2
        book_info = root.find_all(
            "td", style="word-break: break-all; width: 500px")
        # book_info = book_info.split('|')
        '''
        book_info = 
        ['\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t', 'aLB', 'bA05', 'c1350240', 'd783.3886', 'e8555:2', 'pCB', 'k購買', 's244', 'tCCL', 'y2018', 'j平裝', 'oT2\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t']
        
        條碼號 : c
        索書號 : d + e + 3        
        
        
        '''

        print(book_info)


# get_basic_info("跟著月亮").get_location()
get_basic_info("臺灣傳統古窯").get_basic_info()
# get_basic_info("跟著月亮").get_basic_info()
