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
        "https://homezz.ro/anunturi_apartamente_de-vanzare_in-timisoara-tm.html")

    with open('result_homezz.html', 'wb') as file:
        file.write(contents)

with open('result_homezz.html', 'r', encoding='utf-8') as file:
    contents = file.read()

soup = BeautifulSoup(contents, 'html.parser')
pretty_html = soup.prettify()
offerNodes = soup.body.find_all('a', attrs={'class': 'main_items'})
i = 0
offers = []
for offerNode in offerNodes:
    price = offerNode.find(
        'span', attrs={"class": "price"}).text.strip().replace("€", "EUR")

    titleNode = offerNode.find('span', attrs={'class': 'title'})
    title = titleNode.text.strip()

    url = offerNode['href']

    imgNode = offerNode.find('div', attrs={'class': 'overflow_image'})
    if imgNode.img:
        imgUrl = imgNode.img['src']

    info_details_spans = offerNode.find('div', 'info_details').find_all('span')
    area = info_details_spans[1].text
    category = info_details_spans[2].text
    zone = offerNode.find('span', 'area').text

    offer = Offer(title, price, url, imgUrl, "imgData")
    offer.area = area
    offer.category = category
    offer.zone = zone

    offers.append(offer)
    # i += 1

json_arr = json.dumps(offers, default=obj_dict, indent=4, sort_keys=True)
with open("output_homezz.json", 'w', encoding='utf-8') as file:
    file.write(json_arr)
