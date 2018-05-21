# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

def head_option(xs):
    if xs:
        return xs[0]

    return None


class BgbSpider(CrawlSpider):
    name = 'bgb'
    allowed_domains = ['www.gesetze-im-internet.de']
    start_urls = ['https://www.gesetze-im-internet.de/bgb/inhalts_bersicht.html']

    rules= [Rule(LinkExtractor(allow=(), restrict_xpaths=["//div[@id='blaettern_weiter']//a"]),
                 callback="parse_item",
                 follow=True)]


    def parse_item(self, response):
        print("Processing %s" % response.url)

        paragraph = response.css(".jnenbez::text").extract_first()
        title = response.css(".jnentitel::text").extract_first()

        paragraphs = response.css("div.jurAbsatz::text").extract()


        result = {
            'paragraph': paragraph,
            'titel': title,
            'absaetze': paragraphs
        }

        print(repr(result))

        yield result

