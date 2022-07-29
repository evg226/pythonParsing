import hashlib
from pprint import pprint

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo import errors
from scrapy.utils.python import to_bytes


class CastaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongoBase = client.products

    def process_item(self, item, spider):
        collection = self.mongoBase[spider.name]
        try:
            collection.update_one({'_id': item['_id']}, {'$set': item})
        except errors as e:
            print(e)
        return item


class CastaimgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['images']:
            for image in item['images']:
                try:
                    yield scrapy.Request(image)
                except Exception as e:
                    print(item['title'])
                    print(e)

    def item_completed(self, results, item, info):
        item['images'] = []
        for imgInfo in results:
            if imgInfo[0]:
                item['images'].append(imgInfo[1])
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{item["_id"]}/{image_guid}.jpg'
