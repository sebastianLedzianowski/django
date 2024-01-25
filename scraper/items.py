# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy_djangoitem import DjangoItem
from quotesapp.models import Tag, Author, Quote


class TagItem(DjangoItem):
    django_model = Tag

class AuthorItem(DjangoItem):
    django_model = Author

class QuoteItem(DjangoItem):
    django_model = Quote
    tags = scrapy.Field()