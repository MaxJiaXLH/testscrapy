# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ApkDownloadLinksItem(scrapy.Item):
    name = scrapy.Field()
    links = scrapy.Field()


class AppDetailsLinksItem(scrapy.Item):
    name = scrapy.Field()
    details_link = scrapy.Field()


class AppDetailsItem(scrapy.Item):
    app_name = scrapy.Field()
    app_star = scrapy.Field()
    comment_count = scrapy.Field()
    introduction = scrapy.Field()
    pic_src = scrapy.Field()
    update_date = scrapy.Field()
    keywords = scrapy.Field()
