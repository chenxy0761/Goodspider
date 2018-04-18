# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from openpyxl import Workbook


class GoodspiderPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.append(['商品URL', '商品ID', '一级目录', '二级目录', '三级目录', '商品名称','商品价格','商品描述','加购URL','店铺ID'])  # 设置表头

    def process_item(self, item, spider):  # 工序具体内容
        line = [item['url'], item['productID'], item['one'], item['two'], item['three'], item['name'], item['price'], item['description'], item['initCartUrl'], item['shopID']]  # 把数据中每一项整理出来
        self.ws.append(line)  # 将数据以行的形式添加到xlsx中
        self.wb.save('test/good.xlsx')  # 保存xlsx文件
        # return item