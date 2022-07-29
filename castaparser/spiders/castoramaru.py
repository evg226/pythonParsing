import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse

from castaparser.items import CastaparserItem


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('search')}"]

    def parse(self, response: HtmlResponse):
        nextPage = response.xpath("//a[contains(@class,'next')]/@href").get()
        if nextPage:
            yield response.follow(nextPage, callback=self.parse)
        itemLinks = response.xpath("//a[@class='product-card__img-link']/@href")
        for itemLink in itemLinks:
            yield response.follow(itemLink, callback=self.parseItem)

    def parseItem(self, response: HtmlResponse):
        loader = ItemLoader(item=CastaparserItem(), response=response)
        loader.add_xpath('title', "//h1[contains(@class,'product-essential__name')]/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('price', "//span[@class='price']/span/span/text()")
        loader.add_xpath('images', "//img[contains(@class,'top-slide__img')]/@data-src")
        loader.add_xpath('_id', "//button[contains(@class,'to-cart-button')]/@data-product-id")
        loader.add_xpath('specLabel',"//div[contains(@class,'product-specifications')]//span[contains(@class,'specs-table__attribute-name')]/text()")
        loader.add_xpath('specValue',"//div[contains(@class,'product-specifications')]//dd[contains(@class,'specs-table__attribute-value')]/text()")

        yield loader.load_item()
