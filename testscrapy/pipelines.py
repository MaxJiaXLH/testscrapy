# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.dialects.postgresql import psycopg2

from testscrapy import settings
import pymongo


class MongoDBPipeline(object):

    def __init__(self):
        host = settings.MONGODB_HOST
        port = settings.MONGODB_PORT
        db_name = settings.MONGODB_DBNAME

        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post1 = db[settings.MONGODB_DOCNAME_DOWNLOAD]
        self.post2 = db[settings.MONGODB_DOCNAME_DETAILS]

    def process_item(self, item, spider):
        dic = dict(item)
        if "app_name" in dic:
            self.post2.insert(dic)
            return item
        elif "name" in dic:
            self.post1.insert(dic)
            return item


class PostgreSQLPipeline(object):

    def __init__(self):
        hostname = '192.168.12.130'
        username = 'postgres'
        password = 'postgres'
        database = 'weibo'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def process_item(self, item, spider):
        apk_download_links = dict(item)
        if "app_name" in apk_download_links:
            self.post2.insert(apk_download_links)
            return item
        elif "name" in apk_download_links:
            self.post1.insert(apk_download_links)
            return item
