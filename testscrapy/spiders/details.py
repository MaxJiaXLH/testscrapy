import pymongo
import scrapy
from testscrapy import settings
from testscrapy.items import AppDetailsItem
from testscrapy.items import AppDetailsLinksItem

class DetailsSpider(scrapy.Spider):
    name = 'details'
    allowed_domains = ['google.com']
    start_urls = ['https://play.google.com/store']

    def parse(self, response):
        mongodb_client = pymongo.MongoClient('mongodb://' + settings.MONGODB_HOST + ':' + str(settings.MONGODB_PORT))
        mydb = mongodb_client[settings.MONGODB_DBNAME]
        mycol = mydb[settings.MONGODB_DOCNAME_DOWNLOAD]
        ori = len(list(mycol.find()))
        i = 0
        for data in mycol.find():
            print('count------------:' + str(ori-i))
            details_link = data['details_link']
            i+=1
            yield scrapy.Request(details_link, callback=self.parse_details)


    def parse_details(self, response):
        '''
        crawl the details of the apks
        '''

        more_links1 = response.xpath('//div[@class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-INsAgc VfPpkd-LgbsSe-OWXEXe-dgl2Hf Rj2Mlf OLiIxf PDpWxe P62QJc t4qqld LMoCf"]/a/@href').extract()
        more_links2 = response.xpath(
            '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[2]/c-wiz[2]/section/header/div/div[2]/a/@href').extract()
        more_links3 = response.xpath('//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[2]/c-wiz[3]/section/header/div/div[2]/a/@href').extract()
        more_links = more_links1 + more_links2 + more_links3
        for link in more_links:
            base_url = 'https://play.google.com'
            yield scrapy.Request(base_url + link, callback=self.parse_more_links)


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

        yield item

    def parse_more_links(self, response):
        urls1 = response.xpath('//a[@class="Si6A0c ZD8Cqc"]/@href').extract()
        urls2 = response.xpath('//a[@class="Si6A0c Gy4nib"]/@href').extract()
        urls3 = response.xpath('//a[@class="Si6A0c nT2RTe"]/@href').extract()
        urls = urls1+urls2+urls3
        base_url = 'https://play.google.com'
        for each in urls:
            apk_name = each[23:]
            details_url = base_url + each
            item = AppDetailsLinksItem()
            item['name'] = apk_name
            item['details_link'] = details_url
            yield item
