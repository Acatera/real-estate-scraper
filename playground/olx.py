import urllib.request
import threading
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


class Offer:
    def __init__(self):
        """init"""


def do_request(url):
    req = urllib.request.Request(url, data=None,
                                 headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    contents = urllib.request.urlopen(req).read()
    return contents


def obj_dict(obj):
    return obj.__dict__


def process_page(soup, offers):
    offerNodes = soup.body.find_all('td', 'offer')
    for offerNode in offerNodes:
        if offerNode.table is None:
            continue

        offer = Offer()

        price = offerNode.find('p', 'price').strong.text.replace("€", "EUR")
        offer.price = price

        titleNode = offerNode.find('a', 'link')
        title = titleNode.strong.text
        offer.title = title

        url = titleNode['href']
        offer.url = url

        imgUrl = offerNode.find('img', 'fleft')
        if imgUrl is not None:
            offer.imgUrl = imgUrl['src']

        category = offerNode.find('small', 'breadcrumb').text.strip()
        offer.category = category

        detail_nodes = offerNode.find_all('tr')[1].find_all('p')

        location = detail_nodes[0].text.strip()
        offer.location = location

        timestamp = detail_nodes[1].text.strip().replace('Azi', datetime.now().date().isoformat())
        timestamp = timestamp.replace('Ieri', (datetime.now().date() - timedelta(days = 1)).isoformat())
        offer.timestamp = timestamp

        offers.append(offer)

def fetch_pager_pages(soup):
    page_urls = []
    page_spans = soup.find('div', 'pager').find_all('span', 'item', 'fleft')
    for span in page_spans:
        if span.a is not None:
            page_urls.append(span.a['href'])
    return page_urls


if False:
    contents = do_request(
        "https://www.olx.ro/imobiliare/apartamente-garsoniere-de-vanzare/timisoara/")

    with open('result_olx.html', 'wb') as file:
        file.write(contents)

with open('result_olx.html', 'r', encoding='utf-8') as file:
    contents = file.read()

soup = BeautifulSoup(contents, 'html.parser')
page_urls = fetch_pager_pages(soup)

offers = []
soups = []
soups.append(soup)

for url in page_urls:
    contents = do_request(url)
    soup = BeautifulSoup(contents, 'html.parser')
    soups.append(soup)

threads = [threading.Thread(
    target=process_page, args=(soup, offers)) for soup in soups]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

json_arr = json.dumps(offers, default=obj_dict, indent=4, sort_keys=True)
with open("output_olx.json", 'w', encoding='utf-8') as file:
    file.write(json_arr)
