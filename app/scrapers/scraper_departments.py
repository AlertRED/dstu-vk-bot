from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy


class Item(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()


class BlogSpider(CrawlSpider):
    name = 'departments'
    start_urls = ['https://donstu.ru/structure/science-education/']
    allowed_domains = ['donstu.ru']

    def parse(self, response):
        a = response.css('div.menu>ul>li>a::text').extract()
        b = response.css('div.menu>ul>li>a::attr(href)').extract()
        print(a[0], b[0])
        # print(response.css('div.menu>ul>li>a::text').extract())
