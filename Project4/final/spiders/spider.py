import shutil
import scrapy
import os
import threading
from scrapy.exceptions import CloseSpider


class ConcordiaSpider(scrapy.Spider):
    """
    go to the top directory path and use  "scrapy crawl concordia -a file_num=100"
    """
    name = "concordia"
    file_num = 100
    lock = threading.Lock()

    def __init__(self, file_num=None, *args, **kwargs):
        shutil.rmtree("files")
        self.file_num = int(file_num)
        print("The number of crawled files is " + file_num)
        super(ConcordiaSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = [
            'https://www.concordia.ca/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page_urls = response.css('a::attr(href)').getall()
        if self.file_num <= 0:
            raise CloseSpider()
        path_list = response.request.url.split('/')
        if not path_list[len(path_list) - 1].endswith(".html") and not path_list[len(path_list) - 1] == '':
            return
        print("URL: " + response.request.url)
        file_path = "files/"
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        for i in range(3, len(path_list) - 1):
            file_path += path_list[i] + "/"
            if not os.path.exists(file_path):
                os.mkdir(file_path)
        if path_list[len(path_list) - 1] == '':
            file_path += "main.html"
        else:
            file_path += path_list[len(path_list) - 1]
        print("file path:   " + file_path)

        f = open(file_path, "w", encoding='utf-8')
        f.write(response.text)
        f.close()
        self.lock.acquire()
        self.file_num -= 1
        self.lock.release()

        for page_url in page_urls:
            if str(page_url).startswith("/"):
                next_page = response.urljoin(page_url)
                yield scrapy.Request(next_page, callback=self.parse)