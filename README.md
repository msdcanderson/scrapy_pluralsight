# scrapy_pluralsight
Pluralsight Scrapy course

## Creating spider

Example using scrapy.spider class

```
scrapy startproject quotes
cd quotes
scrapy genspider QuoteSpider quotes.toscrape.com
scrapy crawl QuoteSpider
```

Example using Crawlspider

```
scrapy genspider --template=crawl QuoteCrawler quotes.toscrape.com
```