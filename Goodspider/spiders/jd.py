# -*- coding: utf-8 -*-
import json
from urllib import urlencode

import scrapy
import time
from scrapy import Selector, Request
from Goodspider.items import GoodspiderItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['www.jd.com']
    start_urls = ['http://www.jd.com/']

    def start_requests(self):
        i = 1
        while i < 100:
            url = 'https://search.jd.com/Search?'
            # 拼接的时候field-keywords后面是不加等号的
            url += urlencode(
                {"keyword": "智能钢琴", "enc": "utf-8", "qrst": "1", "rt": "1", "stop": "1", "vt": "2",
                 "page": i, "s": "60", "click": "0"})
            i = i + 2
            time.sleep(1)
            yield scrapy.Request(url, callback=self.parse, )

    def parse(self, response):
        sel = Selector(response)
        ids = sel.xpath("//li/@data-sku").extract()
        for id in ids:
            time.sleep(1)
            try:
                price = sel.xpath('//div[@class="p-price"]/strong[@class="J_' + id + '"]/i/text()').extract()[0]
            except Exception as e:
                price = ""
            req_url = "https://item.jd.com/" + id + ".html"
            # req_url = "https://item.jd.com/1879150.html"
            yield Request(url=req_url, callback=self.parse_detail, meta={"data": price}, dont_filter=True)
        # req_url = "https://item.jd.com/1879150.html"
        # yield Request(url=req_url, callback=self.parse_detail, meta={"data": "1999"}, dont_filter=True)

    def parse_detail(self, response):
        sel = Selector(response)
        itemizes = sel.xpath('//div[@id="crumb-wrap"]//text()').extract()
        # # 把需要的数据保存到Item中，用来会后续储存做准备
        item = GoodspiderItem()
        item["url"] = response.url
        print(item["url"])
        item["productID"] = str(response.url).split("/")[-1].strip(".html")
        data = response.meta["data"]
        item["price"] = data
        list = []
        for itemize in itemizes:
            if itemize.strip() != "":
                list.append(itemize.strip())
        item["one"] = sel.xpath('//div[@id="crumb-wrap"]//div[@class="item first"]//text()').extract()[0]
        item["two"] = sel.xpath('//div[@id="crumb-wrap"]//div[@class="item"]//text()').extract()[0]
        item["three"] = sel.xpath('//div[@id="crumb-wrap"]//div[@class="item"]//text()').extract()[1]
        item["name"] = sel.xpath('//div[@id="crumb-wrap"]//div[@title]//text()').extract()[0]
        description = sel.xpath('//div[@class="sku-name"]/text()').extract()[0]
        item["description"] = description.strip()
        try:
            InitCartUrl = sel.xpath('//a[@id="InitCartUrl"]/@href').extract()[0]
        except Exception as e:
            InitCartUrl = "https:////cart.jd.com/gate.action?pid=" + item["productID"] + "&pcount=1&ptype=1"
        item["initCartUrl"] = "https:" + InitCartUrl
        shopID = sel.xpath('//div[@class="btns"]/a/@data-vid').extract()[0]
        item["shopID"] = shopID
        return item

        # 最后返回item，如果返回的数据类型是item，engine会检测到并把返回值发给pipelines处理
        # return item
