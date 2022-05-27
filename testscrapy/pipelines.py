# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

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
        # update_one 可以更新重复数据
        if "app_name" in dic:
            self.post2.update_one(dic, {'$set': dic}, upsert=True)
            return item
        elif "name" in dic:
            self.post1.update_one(dic, {'$set': dic}, upsert=True)
            return item

    def close_spider(self, spider):
        pass


class PostgreSQLPipeline(object):
    hostname = settings.PGSQL_HOST
    username = settings.PGSQL_USERNAME
    password = settings.PGSQL_PASSWORD
    database = settings.PGSQL_DBNAME

    def __init__(self):
        pass

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
        print("PostgreSQL connection is closed")

    def process_item(self, item, spider):
        #TODO： 每次写入都要重新建立连接？如果连接写入init，与事物冲突？
        self.connection = psycopg2.connect(host=self.hostname, user=self.username, password=self.password, dbname=self.database)
        self.cur = self.connection.cursor()
        try:
            self.cur.execute(
                "INSERT INTO appdetails(app_name,app_star,comment_count,introduction,pic_src,update_date,keywords) VALUES (%s,%s,%s,%s,%s,%s,%s);",
                (item['app_name'], item['app_star'], item['comment_count'], item['introduction'], item['pic_src'],
                 item['update_date'], item['keywords']))
            self.connection.commit()
        except (Exception, psycopg2.Error) as error:
            print("Error while fetching data from PostgreSQL", error)
        finally:
            self.cur.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
        return item
