# -*- coding: utf-8 -*-
import scrapy
from xboxgames.items import XboxgamesItem
from scrapy.http.request import Request 


class TestSpider(scrapy.Spider):
    name = "test_spider"
    allowed_domains = ["xbox.com"]
    start_urls = [
        "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=12&ct=1463566090&rver=6.5.6509.0&wp=MBI_SSL&wreply=https:%2F%2Faccount.xbox.com:443%2Fpassport%2FsetCookies.ashx%3Frru%3Dhttps%253a%252f%252faccount.xbox.com%252fzh-HK%252fAccount%252fSignin%253freturnUrl%253dhttps%25253a%25252f%25252fstore.xbox.com%25253a443%25252fzh-HK%25252fXbox-One%25252fGames%25252fUnravel%25252f223a2738-eed8-437e-b961-9e6e4e7e67c6%2526pcexp%253dtrue%2526uictx%253dme&lc=3076&id=292543&cbcxt=0"
        #"https://store.xbox.com/zh-HK/Xbox-One/Games/Unravel/223a2738-eed8-437e-b961-9e6e4e7e67c6"
    ]

    def start_requests(self):  
        for url in self.start_urls:          
            yield Request(url, cookies={'xbox_info': 'Gold'},callback=self.parse)  

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

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
