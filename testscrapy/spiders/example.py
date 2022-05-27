import scrapy
from testscrapy.items import AppDetailsItem
from testscrapy.spiders.crawl_apks import DownloadApks
from testscrapy.items import ApkDownloadLinksItem

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['google.com', "apkcombo.com"]
    start_urls = ['https://play.google.com/store/games']

    def parse(self, response):
        '''
        crawl https://play.google.com/store/games
        get all the apks urls for details
        '''
        urls = response.xpath('//a[@class="Si6A0c Gy4nib"]/@href').extract()
        download_link_base = 'https://apkcombo.com/de/apk-downloader/#package='

        #get download links of apks
        download = DownloadApks()
        for each in urls:
            apk_name = each[23:]
            download_link = download_link_base + apk_name
            res = download.get_links(download_link)
            if res:
                item = ApkDownloadLinksItem()
                item['name'] = res['name']
                item['links'] = res['links']
                print(item)
                yield item

        #Get APK's details and save to MongoDB
        base_url = 'https://play.google.com'
        for each in urls:
            url = base_url + each
            yield scrapy.Request(url, callback=self.parse_details)

        #download apk files
        download.download()

    def parse_details(self, response):
        '''
        crawl the details of the apks
        '''
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

