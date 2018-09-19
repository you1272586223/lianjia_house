# -*- coding: utf-8 -*-
import math

import scrapy

from lianjia_house.items import LianjiaHouseItem

# 爬取的区域
# areas = {'浦东': 'pudong', '闵行': 'minhang', '宝山': 'baoshan', '徐汇': 'xuhui', '普陀': 'putuo',
#                  '杨浦': 'yangpu', '长宁': 'changning', '松江': 'songjiang', '嘉定': 'jiading', '黄浦': 'huangpu',
#                  '静安': 'jingan', '闸北': 'zhabei', '虹口': 'hongkou', '青浦': 'qingpu',
#                  '奉贤': 'fengxian', '金山': 'jinshan', '崇明': 'chongming',
#                  '上海周边': 'shanghaizhoubian'
#                  }

# 奉贤   ---> 已爬
areas = {'金山': 'jinshan'}

class LianjiahouseSpider(scrapy.Spider):
    name = 'lianJiaHouse'
    allowed_domains = ['sh.lianjia.com']

    # 入口地址
    start_urls = ['https://sh.lianjia.com/zufang/']

    # 爬取上海所有区域
    def parse(self, response):
        # area_list = response.xpath('//div[@class="bd"]//dd[@data-index="0"]//div[@class="option-list"]//a')
        for key, val in areas.items():
            # url = 'https://sh.lianjia.com' + area.xpath('.//@href').extract_first()
            # name = area.xpath('.//text()').extract_first()
            # if name == '不限':
            #     continue
            url = 'https://sh.lianjia.com/zufang/' + val
            name = key
            print(url + "======>>" + name + "=======>" + areas.get(name))
            yield scrapy.Request(url, callback=self.parse_next, meta={'areaName': name})


    # 每个区域租房的下一页的内容
    def parse_next(self, response):
        areaName = response.meta['areaName']
        totalHouse = response.xpath('//div[@class="wrapper"]//div[@class="list-head clear"]//h2//span/text()').extract_first()
        print(areaName + '：下所有的租房信息,总共有' + totalHouse + '套房源')
        for url in self.nextUrl(areas.get(areaName), totalHouse):
            yield scrapy.Request(url, callback=self.parse_item, meta={'areaName': areaName})

    # 爬取具体的租房信息
    def parse_item(self, response):
        print('当前爬取的url:' + response.url)
        areaName = response.meta['areaName']
        house_list = response.xpath('//div[@class="con-box"]//div[@class="list-wrap"]//ul//li')

        if house_list.xpath('.//p') != []:
            print('没有找到相关内容,跳过')
            return
        for house in house_list:
            item = LianjiaHouseItem()
            item['district'] = areaName
            item['cover_img'] = house.xpath('.//div[@class="pic-panel"]//a//img//@src').extract_first()
            item['detail_url'] = house.xpath('.//div[@class="pic-panel"]//a//@href').extract_first()
            item['title'] = house.xpath('.//div[@class="info-panel"]//h2//a//text()').extract_first()
            item['address'] = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-1"]//div[@class="where"]//a//span//text()').extract_first().replace(
                u'\xa0', u'')
            item['hall'] = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-1"]//div[@class="where"]//span[@class="zone"]//text()').extract_first().replace(
                u'\xa0', u'')
            item['area'] = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-1"]//div[@class="where"]//span[2]//text()').extract_first().replace(
                u'\xa0', u'')
            item['orientation'] = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-1"]//div[@class="where"]//span[3]//text()').extract_first().replace(
                u'\xa0', u'')

            # 循环获取标签
            item['label'] = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-1"]//div[@class="chanquan"]//span//text()').extract()
            # 循环获取描述
            desc = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-1"]//div[@class="other"]//text()').extract()
            s = ''
            for row in desc:
                s += (row + " ")
            item['description'] = s

            # 价格和单位
            item['price'] = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-3"]//div[@class="price"]//span//text()').extract_first()
            item['price_unit'] = \
                house.xpath('.//div[@class="info-panel"]//div[@class="col-3"]//div[@class="price"]//text()').extract()[
                    1]

            item['update_time'] = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-3"]//div[@class="price-pre"]//text()').extract_first().replace(
                u'更新', '')
            item['browse_people'] = house.xpath(
                './/div[@class="info-panel"]//div[@class="col-2"]//div[@class="square"]//span[@class="num"]//text()').extract_first().replace(
                u'更新', '')
            item['house_type'] = "租房"
            yield item

    # 生成下一页链接
    def nextUrl(self, area, totalHouse):
        url = 'https://sh.lianjia.com/zufang/' + area + '/pg{}'
        pageSize = 30
        pageCount = math.ceil(int(totalHouse) / pageSize)
        print('pageSize=' + str(pageSize) + '  总页数pageCount=' + str(pageCount))
        if pageCount >= 100:
            pageCount = 100
        for i in range(pageCount):
            yield url.format(i + 1)
