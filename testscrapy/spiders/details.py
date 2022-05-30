import pymongo
import scrapy
from testscrapy import settings
from testscrapy.items import AppDetailsItem
from testscrapy.items import AppDetailsLinksItem

class DetailsSpider(scrapy.Spider):
    name = 'details'
    allowed_domains = ['google.com']
    start_urls = ['http://google.com/']

    def parse(self, response):
        mongodb_client = pymongo.MongoClient('mongodb://' + settings.MONGODB_HOST + ':' + settings.MONGODB_PORT)
        mydb = mongodb_client[settings.MONGODB_DBNAME]
        mycol = mydb[settings.MONGODB_DOCNAME_DOWNLOAD]

        for data in mycol.find():
            details_link = data['details']
            yield scrapy.Request(details_link, callback=self.parse_details)


    def parse_details(self, response):
        '''
        crawl the details of the apks
        '''

        more_links = response.xpath('//div[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc t4qqld LMoCf"]/a/@href').extract()
        for link in more_links:
            yield scrapy.Request(link, callback=self.parse_details)

        app_name = response.xpath('//h1[@itemprop="name"]/span/text()').extract()
        app_star = response.xpath('//div[@class="TT9eCd"]/text()').extract()
        comment_count = response.xpath('//div[@class="g1rdde"]/text()').extract()[0]
        introduction = response.xpath('//div[@class="bARER"]/text()').extract()[0]
        pic_src = response.xpath('//div[@class="qxNhq"]/img/@src').extract()
        update_date = response.xpath('//div[@class="xg1aie"]/text()').extract()
        keywords = response.xpath('//span[@class="VfPpkd-vQzf8d"]/text()').extract()[2:-2]

        item = AppDetailsItem()
        item['app_name'] = app_name
        item['app_star'] = app_star
        item['comment_count'] = comment_count
        item['introduction'] = introduction
        item['pic_src'] = pic_src
        item['update_date'] = update_date
        item['keywords'] = keywords

        print(item)
        yield item

    def parse_more_links(self, response):
        urls = response.xpath('//a[@class="Si6A0c ZD8Cqc"]/@href').extract()
        if not urls:
            urls = response.xpath('//a[@class="Si6A0c Gy4nib"]/@href').extract()
        base_url = 'https://play.google.com'

        for each in urls:
            apk_name = each[23:]
            details_url = base_url + each
            item = AppDetailsLinksItem()
            item['name'] = apk_name
            item['details_link'] = details_url
            print(item)
            yield item