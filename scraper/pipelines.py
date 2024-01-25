# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from asgiref.sync import sync_to_async
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TheodoTeamPipeline(object):
    async def process_item(self, item, spider):
        await sync_to_async(item.save)()
        return item
