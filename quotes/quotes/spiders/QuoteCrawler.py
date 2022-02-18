import os
import re
import codecs
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from quotes.items import QuotesItem


class QuotecrawlerSpider(CrawlSpider):
    txt = ".txt"
    fn = "quotes.toscrape"
    dn = fn + ".com"

    name = "QuoteCrawler"
    allowed_domains = [dn]
    start_urls = ["https://" + dn + "/page/1/"]

    rules = (
        Rule(LinkExtractor(restrict_css="li.next"), callback="parse_page", follow=True),
        # Rule(LinkExtractor(allow=r"page/"), callback="parse_page", follow=True),
        )

    def writeTxt(self, q):
        with codecs.open(self.fn + self.txt, "a+", "utf-8") as f:
            f.write(q["quote"] + "\r\n")
            f.write(q["author"] + "\r\n")
            f.write(q["tags"] + "\r\n\n")

    def extractData(self, res):
        q = QuotesItem()

        for quote in res.css("div.quote"):
            q["quote"] = (
                '"'
                + re.sub(
                    r"[^\x00-\x7f]", r"", quote.css("span.text::text").extract_first()
                )
                + '"'
            )
            q["author"] = quote.css("small.author::text").extract_first()
            q["tags"] = ", ".join(
                str(s) for s in quote.css("div.tags > a.tag::text").extract()
            )

            self.writeTxt(q)

    def parse_page(self, res):
        self.extractData(res)
