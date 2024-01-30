from quotesapp.models import Quote, Author, Tag
from scraper.items import QuoteItem, AuthorItem


class TheodoTeamPipeline:

    def process_item(self, item, spider):
        if isinstance(item, QuoteItem):
            author = Author.objects.filter(fullname=item['author'])

            quote = Quote(content=item['content'], author=author.first())
            quote.save()

            tags = [Tag.objects.get_or_create(name=tag)[0] for tag in item['tags']]
            quote.tags.set(tags)
            quote.save()
        elif isinstance(item, AuthorItem):
            Author.objects.get_or_create(fullname=item['fullname'], born_date=item["born_date"],
                                         born_location=item["born_location"], content=item["content"])
        return item
