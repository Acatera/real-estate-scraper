import urllib.request
import json
from bs4 import BeautifulSoup
import cssutils


class Offer:
    def __init__(self):
        """asdasd"""

def do_request(url):
    req = urllib.request.Request(url, data=None,
                                 headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    contents = urllib.request.urlopen(req).read()
    return contents


def obj_dict(obj):
    return obj.__dict__


if False:
    contents = do_request(
        "https://lajumate.ro/anunturi_apartamente-de-vanzare_in-timisoara-tm.html")

    with open('result_lajumate.html', 'wb') as file:
        file.write(contents)

with open('result_lajumate.html', 'r', encoding='utf-8') as file:
    contents = file.read()

soup = BeautifulSoup(contents, 'html.parser')
pretty_html = soup.prettify()
offerNodes = soup.body.find_all('a', attrs={'class': 'main_items'})

offers = []
for offerNode in offerNodes:
    offer = Offer()
    
    price = offerNode.find(
        'span', attrs={"class": "price"}).text.strip().replace("€", "EUR")
    offer.price = price[4:]

    titleNode = offerNode.find('span', attrs={'class': 'title'})
    title = titleNode.text.strip()
    offer.title = title

    url = offerNode['href']
    offer.url = url

    imgNode = offerNode.find('div', attrs={'class': 'overflow_image'})
    if imgNode.img:
        imgUrl = imgNode.img['src']
    offer.imgUrl = imgUrl

    offers.append(offer)

json_arr = json.dumps(offers, default=obj_dict, indent=4, sort_keys=True)
with open("output_lajumate.json", 'w', encoding='utf-8') as file:
    file.write(json_arr)
