# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaHouseItem(scrapy.Item):

    # 区域（浦东，黄埔...）
    district = scrapy.Field()

    # 封面图
    cover_img = scrapy.Field()

    # 详情地址
    detail_url = scrapy.Field()

    # 标题
    title = scrapy.Field()

    # 地址
    address = scrapy.Field()

    # 厅室
    hall = scrapy.Field()

    # 面积
    area = scrapy.Field()

    # 朝向
    orientation = scrapy.Field()

    # 描述
    description = scrapy.Field()

    # 标签
    label = scrapy.Field()

    # 价格
    price = scrapy.Field()

    # 价格单位
    price_unit = scrapy.Field()

    # 更新时间
    update_time = scrapy.Field()

    # 看房人数
    browse_people = scrapy.Field()

    # 房子类型 （新房，二手房，租房）
    house_type = scrapy.Field()



