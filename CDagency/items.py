# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import Join, Compose


class CDagency(Item):
    # 去空字符
    bureau = Field(output_processor=Join(separator=''))  # 机构名
    title = Field(output_processor=Join(separator=''))  # 新闻标题
    pub_time = Field(output_processor=Join(separator=''))  # 新闻发布时间
    content = Field(output_processor=Join(separator=''))  # 新闻内容
    detail_url = Field(output_processor=Join(separator=''))  # 新闻内容链接
    type = Field(output_processor=Join(separator=''))  # 新闻所属活动类型
    browse_times = Field(output_processor=Join(separator=''))  # 浏览次数
    col_name = Field(output_processor=Join(separator=''))  # 存入MongoDB的集合名称

    #responsetext = Field(output_processor=Join(separator=''))
    #initial_url = Field(output_processor=Join(separator=''))
    # title = Field(output_processor=Join(separator=''))
    #department = Field(output_processor=Join(separator=''))
