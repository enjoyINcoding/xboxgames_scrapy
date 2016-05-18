# -*- coding: utf-8 -*-
import scrapy
from xboxgames.items import XboxgamesItem


class PirceSpider(scrapy.Spider):
    name = "price_spider"
    allowed_domains = ["xbox.com"]
    start_urls = [
        "https://store.xbox.com/zh-HK/Xbox-One?Page=2"
    ]

    def parse(self, response):
        for href in response.xpath("//div[@class='gameTitle']"):
            url = href.xpath("a/@href").extract()
            url = 'https://store.xbox.com' + url[0]
            yield scrapy.Request(url, callback=self.parse_detail)
        current_page = response.xpath("//div[@class='currentPage']/text()").re('\d+')
        #print current_page
        next_page = int(current_page[0])+1
        if (next_page <= 1):#int(current_page[1])):
            url1 = self.start_urls[0][0:-1] + str(next_page)
            yield scrapy.Request(url1,callback=self.parse)

    def parse_detail(self, response):
        # filename = response.url.split("/")[-2] + '.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        for info in response.xpath("//div[@id='rightContentArea']"):
            item = XboxgamesItem()
            item['name'] = info.xpath("div[@class='title']/text()").extract()[0].strip()
            price = info.xpath("div[@id='purchaseInfo']/div/h1/text()").extract()
            if len(price):
                item['price'] =  price[0].strip()
            item['product_id'] = response.url[-36:]
            yield item
