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
        "https://www.imobiliare.ro/vanzare-apartamente/timisoara")

    with open('result_imobiliare.html', 'wb') as file:
        file.write(contents)

with open('result_imobiliare.html', 'r', encoding='utf-8') as file:
    contents = file.read()

soup = BeautifulSoup(contents, 'html.parser')
pretty_html = soup.prettify()
offerNodes = soup.body.find_all('div', attrs={'class': 'box-anunt'})

offers = []
for offerNode in offerNodes:
    if 'proiect' in offerNode.attrs['class']:
        continue
    offer = Offer()

    price = offerNode.find(
        'div', attrs={"itemprop": "price"}).text  # .strip().replace("€", "EUR")
    offer.price = price.strip()

    titleNode = offerNode.find('a', attrs={'itemprop': 'name'})
    title = titleNode.span.text.strip()
    offer.title = title

    url = titleNode['href']
    offer.url = url

    imgUrl = offerNode.find('img', 'landscape')
    if imgUrl and imgUrl['src']:
        # print(imgUrl)  # ['src']
        offer.imgUrl = imgUrl['src']

    details_spans = offerNode.find('ul', 'caracteristici').find_all('li')

    details = []

    for detail in details_spans:
        details.append(detail.text.strip())
    
    offer.details = details

    offers.append(offer)

json_arr = json.dumps(offers, default=obj_dict, indent=4, sort_keys=True)
with open("output_imobiliare.json", 'w', encoding='utf-8') as file:
    file.write(json_arr)
