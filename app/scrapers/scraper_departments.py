from time import sleep

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor


class Item(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()


class BlogSpider(CrawlSpider):
    name = 'departments'
    start_urls = ['https://donstu.ru/structure/science-education/']
    allowed_domains = ['donstu.ru']
    total = 0

    rules = (
        Rule(LinkExtractor(allow=('donstu.ru/structure/science-education/*/*')), callback='parse_item'),
    )

    def parse_item(self, response):
        name = response.css('div.container>div.title::text').extract()
        if len(name)>0:
            name = name[0]
        fio = response.css('a.photo>div.grad>div.title-inner>div.name::text').extract()
        first_name = last_name = patonomyc = ' '
        if len(fio)>0:
            first_name, last_name, patonomyc = fio[0].split(' ', 3)
        print('(%s) %s %s %s' % (name, first_name, last_name, patonomyc))

        sleep(5)

        # a = response.css('div.menu>ul>li>a::text').extract()
        # b = response.css('div.menu>ul>li>a::attr(href)').extract()
        # print(a[0], 'https://%s%s' % (self.allowed_domains[0], b[0]))
        # print(response.css('div.menu>ul>li>a::text').extract())


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(BlogSpider)
    process.start()
    print(BlogSpider.total)
