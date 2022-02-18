import os
import re
import codecs
import scrapy

from quotes.items import QuotesItem


class QuotespiderSpider(scrapy.Spider):

    txt = ".txt"  # save the results as txt
    all = True  # scrape entire site, or just part of it?
    fn = "quotes.toscrape"  # file used to save result
    dn = fn + ".com"  # the site's domain name
    firstPage = ["https://" + dn + "/page/1/"]  # the url of the site's first page
    scope = [
        "https://" + dn + "/page/1/",
        "https://" + dn + "/page/2/",
        "https://" + dn + "/page/3/",
        "https://" + dn + "/page/4/",
    ]  # pages on the site that will be scraped when all=False

    name = "QuoteSpider"
    allowed_domains = [dn]
    start_urls = [dn]

    # each time spider is run, previous results are deleted
    def delFile(self):
        if os.path.exists(self.fn + self.txt):
            os.remove(self.fn + self.txt)

    # spider starts running
    def start_requests(self):
        self.delFile()
        pages = self.firstPage if self.all else self.scope

        for page in pages:
            yield scrapy.Request(page, self.parse)

    # extract data
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

    def parse(self, response):
        self.extractData(response)

        if self.all:
            next = response.css('li.next > a::attr(href)').extract_first()
            if next is not None:
                yield scrapy.Request(response.urljoin(next))

    def writeTxt(self, q):
        with codecs.open(self.fn + self.txt, "a+", "utf-8") as f:
            f.write(q["quote"] + "\r\n")
            f.write(q["author"] + "\r\n")
            f.write(q["tags"] + "\r\n\n")
