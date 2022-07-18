from pprint import pprint
from lxml import html
import requests
import re
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client['news']
mainNews = db.mainNews

headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
session=requests.session()

url='https://lenta.ru/'
response=session.get(url,headers=headers)
dom=html.fromstring(response.text)
news=dom.xpath("//a[contains(@class,'card')]")

for newsItem in news:
    source=url
    href=newsItem.get('href')
    title=newsItem.xpath(".//*[contains(@class,'title')]/text()")
    date="-".join(re.findall("\d+",href))
    pprint(f"{url}\n{href}\n{title}\n{date}")
    mainNews.insert_one({'url':url,'title':title,"href":href,"date":date})
