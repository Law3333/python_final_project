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

            '''
            2022/06/13 
            原本為第一種方案，但是會因為圖書館系統'電子書'與'館藏書'排序問題，造成可能取到電子書，
            造成後面執行錯誤(因為電子書的格式不同)，所以之後的方案會先篩選是否為'館藏書'。

            # 尋找 Book ID
            # <input id="s511117" name="sid" type="checkbox" value="511117"/>
            book_info = str(root.find_all("input")[1])
            # print(book_info)
            # value="511117"/>
            book_info = book_info.split()[-1]
            #['5', '1', '1', '1', '1', '7']
            book_info = re.findall('\d', book_info)
            # get 511117
            book_id = str()
            for id in book_info:
                book_id += id

            return int(book_id)
            '''

            # 尋找 Book ID
            # //讀取account和館藏
            # loadAccount(555453);loadHoldIframe({"sid":"555453","execcode2":"m","execcode1":"m","cln":"http"}); (此為電子書)
            # loadAccount(509546);loadHoldIframe({"sid":"509546","execcode2":"m","execcode1":"a","cln":"CB"}); (此為館藏書，為目標)
            book_info = root.find_all(
                "script", type="text/javascript")[7].string

            book_info = book_info.replace(" ", "").replace(
                "\n", "").replace("\r", "").replace("\t", "")

            # loadAccount(555453);
            # loadHoldIframe({"sid":"555453","execcode2":"m","execcode1":"m","cln":"http"});
            # loadAccount(509546);
            # loadHoldIframe({"sid":"509546","execcode2":"m","execcode1":"a","cln":"CB"});
            book_info = re.search(
                "讀取account和館藏(.*?).*?input", book_info).group(0).replace('$("input', '').replace("讀取account和館藏", "").strip()

            book_info_list = book_info.split(';')
            book_info_list.pop(-1)  # 移除掉最後的 ; 的空白

            # 判斷 element 裡面是否有 http, 首先抓出 loadHoldIframe, 接著用 json 解析, 將 cln 不是 http 的 book id 回傳
            for value in book_info_list:
                if "loadHoldIframe" in value:
                    value = value.replace(
                        "loadHoldIframe(", "").replace(")", "")
                    value = json.loads(value)
                    if value['cln'] != "http":
                        # print(int(value['sid']))
                        return int(value['sid'])

        except:

            # parent.location.href = 'bookDetail.do?id=503958';
            book_info = root.script.string
            book_info = re.findall('\d', book_info)
            book_id = str()
            for id in book_info:
                book_id += id

            return int(book_id)

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
        # print(location_info)

        return location_info

    def get_basic_info(self):
        '''
        取得書的基本資料：
        包含
        - 條碼號
        - 作者
        - 索書號

        basic_info_list = ['', 'aLB', 'bA05', 'c1350240', 'd783.3886', 'e8555:2', 'pCB', 'k購買', 's244', 'tCCL', 'y2018', 'j平裝', 'oT2']

        條碼號(book_barcode) : c 
        索書號(book_request) : d + e + y

        '''

        book_id = self.get_book_id()
        # print(book_id)

        url = f"https://libholding.ntut.edu.tw/bookDetail.do?id={book_id}&Lflag=1"

        request_data = self.link_connect(url)
        root = bs4.BeautifulSoup(request_data, "html.parser")
        book_info = root.find("div", id="detailViewMARC").text

        '''--- target : basic_info = |aLB|bA05|c1350240|d783.3886|e8555:2|pCB|k購買|s244|tCCL|y2018|j平裝|oT2 ---'''

        book_info = book_info.replace(" ", "").replace(
            "\n", "").replace("\r", "").replace("\t", "")

        try:
            basic_info = re.search(
                "095(.*?).*?100", book_info).group(0).replace("095", "").replace("100", "").strip()

        except:
            basic_info = re.search(
                "095(.*?).*?110", book_info).group(0).replace("095", "").replace("110", "").strip()

        basic_info_list = basic_info.split('|')
        # ['', 'aLB', 'bA05', 'c1350240', 'd783.3886', 'e8555:2', 'pCB', 'k購買', 's244', 'tCCL', 'y2018', 'j平裝', 'oT2']

        c, d, e, y = str(), str(), str(), str()
        basic_info_list.pop(0)  # 移除掉空白

        for value in basic_info_list:
            if value[0] == "c":
                c = value[1:]
            elif value[0] == "d":
                d = value[1:]
            elif value[0] == "e":
                e = value[1:]
            elif value[0] == "y":
                y = value[1:]

        book_barcode = c
        book_request = d + " " + e + " " + y

        '''--- target : author ---'''
        # print(book_info)

        try:
            author_info = re.search(
                "1001(.*?).*?245", book_info).group(0).replace("1001", "").replace("245", "").replace("|a", "").strip()
        # print(author_info)
        except:
            author_info = re.search(
                "1102(.*?).*?245", book_info).group(0).replace("1102", "").replace("245", "").replace("|a", "").strip()
        # 有些書不乾淨還要在處理一下
        try:
            author_info = author_info.split('|')[0]
        except:
            pass

        location = self.get_location()

        print(author_info, "||", book_barcode,
              "||", book_request, "||", location)


if __name__ == '__main__':
    book_name = input("please input book name : ")
    get_basic_info(book_name).get_basic_info()


# get_basic_info("臺灣傳統古窯").get_basic_info()
# get_basic_info("青花瓷的故事").get_basic_info()
# get_basic_info("色繪古都 : 京都陶瓷漫步").get_basic_info()
# get_basic_info("跟著月亮").get_basic_info()
# get_basic_info("京阪奈地鐵遊").get_basic_info()
# get_basic_info("宋元明清瓷器鑑賞").get_basic_info()
# get_basic_info("能源，迫在眉睫的抉擇：為人類文明史續命，抑或摧毀人類文明的一場賭注").get_basic_info()


'''

鄧淑慧 || 1312840 || 464.0933 8563 2015 || 三樓書庫
芬雷 || 1293934 || 464.16092 874 2011 || 一樓暢銷文庫
陳彥璋 || 1334204 || 731.752185 8755 2017 || 一樓暢銷文庫
韓國瑜 || 1350240 || 783.3886 8555:2 2018 || 三樓書庫
mediaporta || 1339500 || 731.7509 8635 2018 ||  一樓經典文庫
劉如水 || 1307404 || 796.6 8768 2004 || 一樓暢銷文庫

'''


'''
2022/06/13
AttributeError: 'NoneType' object has no attribute 'group'
能源，迫在眉睫的抉擇：為人類文明史續命，抑或摧毀人類文明的一場賭注
509546(館藏)
555453(電子)
'''
