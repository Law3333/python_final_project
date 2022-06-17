import bs4
from bs4 import BeautifulSoup
import urllib.request as req
import json
import re
from urllib.parse import quote
import requests

class get_photo:
    def __init__(self,keyword):

        self.keyword_urldecode = quote(keyword)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
        }

    def link_connect(self, url):

        self.requert = req.Request(url, headers=self.headers)

        with req.urlopen(self.requert) as response:
            data = response.read().decode("utf-8")

        return data

    def get_photo(self):

        url = f"https://search.books.com.tw/search/query/key/{self.keyword_urldecode}/cat/all"
        request_data = self.link_connect(url)
        root = bs4.BeautifulSoup(request_data, "html.parser")
        # response = requests.get(url)
        # root = BeautifulSoup(response.text, "html.parser")

        book_info = root.find_all("div", {"class":"box"})[0]
        book_info = book_info.find('img')
        
        book_img = str(book_info["data-src"])
        book_img = re.search("^(.*?).*?&",book_img).group(0).replace("&","")
        book_name = str(book_info["alt"]).replace("/","")
        print(book_name,book_img)

        try:
            req.urlretrieve(book_img, "../Download_image/"+book_name+".jpg")
        except:
            pass




# get_photo("臺灣傳統古窯").get_photo()
# get_photo("青花瓷的故事").get_photo()
# get_photo("色繪古都 : 京都陶瓷漫步").get_photo()
# get_photo("跟著月亮").get_photo()
# get_photo("京阪奈地鐵遊").get_photo()
# get_photo("宋元明清瓷器鑑賞").get_photo()






        