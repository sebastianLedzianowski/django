from urllib.parse import urljoin
import scrapy
from scraper.items import AuthorItem


class AuthorsSpyder(scrapy.Spider):
    name = "authors_spyder"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com"]

    def parse(self, response: scrapy.http.Response) -> None:
        author_links = self.author_links(response)
        for author_link in author_links:
            if author_link:
                full_url = f"{self.start_urls[0]}{author_link}/"
                yield scrapy.Request(url=full_url, callback=self.parse_author)

        next_link = self.next_link(response)
        if next_link:
            full_next_url = urljoin(self.start_urls[0], next_link)
            yield scrapy.Request(url=full_next_url, callback=self.parse)

    def author_links(self, response: scrapy.http.Response) -> list[str]:
        author_links = response.xpath(
            "//span[@class='text']/following-sibling::span/small[@class='author']/following-sibling::a[@href]/@href").getall()
        return author_links

    def next_link(self, response: scrapy.http.Response) -> str:
        next_link = response.xpath("//li[@class='next']/a/@href").get()
        return next_link

    def parse_author(self, response: scrapy.http.Response) -> None:
        author_item = AuthorItem()

        fullname = response.xpath("//h3[@class='author-title']/text()").extract_first()
        born_date = response.xpath("//span[@class='author-born-date']/text()").extract_first()
        born_location = response.xpath("//span[@class='author-born-location']/text()").extract_first()
        content = response.xpath("//div[@class='author-description']/text()").get()

        author_item["fullname"] = fullname
        author_item["born_date"] = born_date
        author_item["born_location"] = born_location[3:] if born_location else None
        author_item["content"] = content.strip() if content else None

        yield author_item
