import requests
from bs4 import BeautifulSoup
import time
import json

class Cinemas(object):
    def __init__(self):
        self.url = "https://maoyan.com/cinemas"
        self.host = "https://maoyan.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
        }
        # 请求参数
        self.parameters = {"offset": 0}
        self.city_id = "0" # 城市ID
        self.cinemas = []
        self.cinema_info = []

    def get_list(self, debug=False):
        while True:
            try:
                response = requests.get(self.url, params=self.parameters, headers=self.headers, cookies={'ci': self.city_id})
            except ConnectionError:
                time.sleep(9.9)
                continue

            print("INFO -> List URL: <%s> %s" % (response.url, response.status_code))
            if response.status_code == 200:
                r_html = response.text.encode(response.encoding).decode("utf-8")
                soup = BeautifulSoup(r_html, "html5lib")

                # 触发阈值程序结束
                if soup.find("div", class_="no-cinemas"):
                    print("INFO -> List END")
                    break

                list = soup.find_all("div", class_="cinema-cell")
                for item in list:
                    itemDom = item.find("a", "cinema-name")

                    val = itemDom.get("data-val").replace("}", "").split()[-1]
                    chinema = {
                        "url": itemDom.get("href"),
                        "bid": itemDom.get("data-bid"),
                        "cinema_id":val,
                        "name": itemDom.get_text()
                    }
                    self.cinemas.append(chinema)
            else:
                print("ERROR -> Network Error")
                time.sleep(9.9)

            if debug:
                break

            self.parameters["offset"] += 12

    def get_info(self):
        for item in self.cinemas:
            response = requests.get(self.host + item.get("url"), headers=self.headers)

            print("INFO -> Cinemas URL: <%s> %s" % (self.host + item.get("url"), response.status_code))
            if response.status_code != 200:
                print("ERROR -> Network Error")
                time.sleep(9.9)
                continue
            else:
                r_html = response.text.encode(response.encoding).decode("utf-8")
                soup = BeautifulSoup(r_html, "html5lib")

                addressDom = soup.find("div", "address text-ellipsis")
                telphoneDom = soup.find("div", "telphone")
                mapDom = soup.find("div", "cinema-map")
                avatarDom = soup.find("img", "avatar")

                chinema_info = {
                    "cinema_id": item.get("cinema_id"),
                    "name": item.get("name"),
                    "address": addressDom.get_text(),
                    "telphone": telphoneDom.get_text().split("：")[-1],
                    "location": {
                        "lat": mapDom.get("data-lat"),
                        "lng": mapDom.get("data-lng")
                    },
                    "avatar": avatarDom.get("src")
                }
                self.cinema_info.append(chinema_info)

if __name__ == "__main__" :

    cinemas = Cinemas()
    cinemas.get_list()
    cinemas.get_info()
    print("Cinemas Count: " + str(len(cinemas.cinema_info)))
    with open("static/cinemas.json", "wt", encoding="utf-8") as f:
        json.dump(cinemas.cinema_info, f, ensure_ascii=False)

    print("save file: static/cinemas.json")
