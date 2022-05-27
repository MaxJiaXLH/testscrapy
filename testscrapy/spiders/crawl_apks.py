from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pymongo
import urllib.request
from testscrapy import settings

class DownloadApks:

    def get_links(self, link):
        #print("start")
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': settings.APK_DOWNLOADER_PATH,
                 "download.prompt_for_download": False,
                 'profile.default_content_settings.popups': 0,
                 }
        options.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome(chrome_options=options, executable_path=settings.DRIVER_PATH)
        driver.get(link)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "file-list")))
        except Exception:
            print(link + " not found")
            return

        element = driver.find_element_by_xpath('''//ul[@class='file-list']/li/a''')

        apk_name = element.text.split("\n")[0]
        apk_link = element.get_attribute('href')
        #print(apk_name + " : " + apk_link)

        item = {'name': apk_name, 'links': apk_link}
        driver.quit()
        return item

    def download(self):
        mongodb_client = pymongo.MongoClient('mongodb://' + settings.MONGODB_HOST + ':' + settings.MONGODB_PORT)
        mydb = mongodb_client[settings.MONGODB_DBNAME]
        mycol = mydb[settings.MONGODB_DOCNAME_DOWNLOAD]
        download_path = settings.APK_DOWNLOADER_PATH

        for data in mycol.find():
            filename = data['name'].replace(' ', '_') + '.apk'
            filepath = download_path + '/' + filename
            try:
                urllib.request.urlretrieve(data['links'], filename=filepath)
            except Exception as e:
                print(filename + " error")