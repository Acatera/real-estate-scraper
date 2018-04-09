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
        "https://www.romimo.ro/Apartamente/vanzare/Timis/Timisoara/?resultsperpage=100")

    with open('result_romimo.html', 'wb') as file:
        file.write(contents)

with open('result_romimo.html', 'r', encoding='utf-8') as file:
    contents = file.read()

soup = BeautifulSoup(contents, 'html.parser')
pretty_html = soup.prettify()
offerNodes = soup.body.find_all('div', attrs={'class': 'property_upselling'})

offers = []
for offerNode in offerNodes:
    offer = Offer()
    
    price = offerNode.find(
        'strong', attrs={"class": "price"}).text.strip().replace("€", "EUR")
    offer.price = price

    titleNode = offerNode.find('a', attrs={'name': 'title'})
    title = titleNode.text.strip()
    offer.title = title

    url = titleNode['href']
    offer.url = url

    imgUrl = offerNode.find('img', attrs={'class': 'property_img'})['src']
    offer.imgUrl = imgUrl

    details_spans = offerNode.find('ul').find_all('li')
    area = details_spans[0].text
    offer.area = area

    category = details_spans[1].text
    offer.category = category

    zone = offerNode.find('strong', 'location').text
    offer.zone = zone

    offers.append(offer)

json_arr = json.dumps(offers, default=obj_dict, indent=4, sort_keys=True)
with open("output_romimo.json", 'w', encoding='utf-8') as file:
    file.write(json_arr)
