import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?search_field=name&search_field=description&text=react+laravel&items_on_page=20'
    ]
    page = 0

    def parse(self, response: HtmlResponse):
        if response.xpath("//div[@class='serp-item']"):
            self.page = self.page + 1
            yield response.follow(
                f'/search/vacancy?search_field=name&search_field=description&text=react+laravel&items_on_page=20&page={self.page}',
                self.parse
            )
        print(f'page - {self.page}')
        jobs = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").getall()
        for job in jobs:
            yield response.follow(job, self.jobItemParse)

    def jobItemParse(self, response: HtmlResponse):
        title = response.xpath("//h1[@data-qa='vacancy-title']//text()").getall()
        salary = response.xpath("//div[@data-qa='vacancy-salary']//text()").getall()
        company = response.xpath("//a[@data-qa='vacancy-company-name']/@href").get()
        url = response.url
        yield JobparserItem(title=title, salary=salary, company=company, url=url)
