from urllib.parse import urljoin
import scrapy
from quotesapp.models import Tag, Author
from scraper.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes_spyder"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]

    def parse(self, response: scrapy.http.Response) -> None:
        for quote in response.xpath("//div[@class='quote']"):
            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author = quote.xpath("span/small/text()").extract_first()
            content = quote.xpath("span[@class='text']/text()").get()

            author_objs = Author.objects.filter(fullname=author)
            if author_objs.exists():
                author_instance = author_objs.first()

            quote_item = QuoteItem()
            quote_item["author"] = author_instance
            quote_item["content"] = content
            quote_item["tags"] = set()

            for tag in tags:
                quote_tags_obj, created = Tag.objects.get_or_create(name=tag)
                quote_item["tags"].add(quote_tags_obj)

            yield quote_item

        next_link = self.next_link(response)
        if next_link:
            full_next_url = urljoin(self.start_urls[0], next_link)
            yield scrapy.Request(url=full_next_url, callback=self.parse)

    def next_link(self, response: scrapy.http.Response) -> str:
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        return next_link
