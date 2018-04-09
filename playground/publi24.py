import urllib.request
import json
from bs4 import BeautifulSoup
import cssutils


class Offer:
    def __init__(self, title, price, url, imgUrl, imgData):
        self.title = title
        self.price = price
        self.url = url
        self.imgUrl = imgUrl

    def __repr__(self):
        return "Title: " + self.title + '\nPrice: ' + self.price + '\nURL: ' + self.url + '\nImage URL: ' + self.imgUrl


def do_request(url):
    req = urllib.request.Request(url, data=None,
                                 headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    contents = urllib.request.urlopen(req).read()
    return contents


def obj_dict(obj):
    return obj.__dict__


if False:
    contents = do_request(
        "https://www.publi24.ro/anunturi/imobiliare/de-vanzare/apartamente/timis/")

    with open('result_publi24.html', 'wb') as file:
        file.write(contents)

with open('result_publi24.html', 'r', encoding='utf-8') as file:
    contents = file.read()

soup = BeautifulSoup(contents, 'html.parser')
pretty_html = soup.prettify()
offerNodes = soup.body.find_all('li', attrs={'class': 'ad-result'})
i = 0
offers = []
for offerNode in offerNodes:
    price = offerNode.find(
        'div', attrs={"class": "ad-price"}).strong.text.replace("€", "EUR")

    titleNode = offerNode.find('a', attrs={'itemprop': 'name'})
    title = titleNode.text.strip()

    url = titleNode['href']

    imgNode = offerNode.find('a', attrs={'itemprop':'url'})
    imgNodeCss = cssutils.parseStyle(imgNode['style'])
    imgUrl = imgNodeCss['background-image'].replace('url(', '').replace(')', '')

    # print(imgUrl.extract())
    # imgRequest = urllib.request.Request(imgUrl)
    # imgData = None

    # # imgData = urllib.request.urlopen(imgRequest).read()

    # # file = open("image", 'wb')
    # # file.write(imgData)
    # # file.close()

    desc = offerNode.find('div', attrs={'itemprop': 'description'}).text.strip()

    offer = Offer(title, price, "https://www.publi24.ro" + url, imgUrl, "imgData")
    offer.desc = desc

    offers.append(offer)
    i += 1

json_arr = json.dumps(offers, default=obj_dict, indent=4, sort_keys=True)
with open("output_publi24.json", 'w', encoding='utf-8') as file:
    file.write(json_arr)
