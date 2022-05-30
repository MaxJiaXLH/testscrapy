import scrapy
from testscrapy.items import AppDetailsItem
from testscrapy.spiders.crawl_apks import DownloadApks
from testscrapy.items import ApkDownloadLinksItem
from testscrapy.items import AppDetailsLinksItem

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
        base_url = 'https://play.google.com'


        for each in urls:
            apk_name = each[23:]
            details_url = base_url + each
            item = AppDetailsLinksItem()
            item['name'] = apk_name
            item['details_link'] = details_url
            print(item)
            yield item

        # #get download links of apks
        # download = DownloadApks()
        # for each in urls:
        #     apk_name = each[23:]
        #     download_link = download_link_base + apk_name
        #     res = download.get_links(download_link)
        #     if res:
        #         item = ApkDownloadLinksItem()
        #         item['name'] = res['name']
        #         item['links'] = res['links']
        #         print(item)
        #         yield item
        #
        # #download apk files
        # download.download()

