# -*- coding: utf-8 -*-
#成都市信访局

import scrapy
import re
from CDagency.items import *

class CdXinfangjuSpider(scrapy.Spider):

    name = 'CD39xinfangju'
    allowed_domains = ['xinfang.chengdu.gov.cn']
    start_urls = ['http://xinfang.chengdu.gov.cn/search.html?keys=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD']

    def parse(self, response):
        """"默认的解析回调函数"""
        news = response.xpath("//div[@class='text']")
        
        for new in news:

            item = CDagency()
            item["col_name"] = "CD39xinfangju"

            # 新闻链接
            href = new.xpath('./h2/a/@href').get()
            detail_url = 'http://xinfang.chengdu.gov.cn' + href
            # 存到item
            item['detail_url'] = detail_url

            yield scrapy.Request(detail_url, callback=self.get_text,meta={'item': item, 'url': detail_url},dont_filter=True)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        # 标题
        title = response.xpath('//div[@class="text-title"]/h2//text()').get()
        title = "".join(title).strip()

        detail = response.xpath('//div[@class="text-title"]/h3//text()').get()
        # 发布时间
        index1 = detail.find('发布时间')
        pub = detail[index1+5 : index1+16]
        pub_time = ''
        for j in pub:
            if j in ['0','1','2','3','4','5','6','7','8','9']:
                pub_time = pub_time + j
            elif j in ['年','月']:
                pub_time = pub_time + '-'

        # 发布单位
        bureau = '成都市信访局'  
        #浏览次数
        start2 = detail.find('浏览次数')
        browse_times = ''
        for i in detail[start2+5:]:
            if i in ['0','1','2','3','4','5','6','7','8','9']:
                browse_times = browse_times + i
            else:
                break
        browse_times = int(browse_times)

        # 获取详细内容
        content_list = response.xpath('//div[@class="text-body"]//text()').getall()
        # 对文本进行拼接
        remove = re.compile(r'\s')
        douhao = re.compile(',')
        content = ''
        for string in content_list:
            string = re.sub(remove, '', string)
            string = re.sub(douhao, '', string)
            content += string

        # 存到item
        item['content'] = content
        item['title'] = title
        item['bureau'] = bureau
        item['browse_times'] = browse_times
        item['pub_time'] = pub_time

        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item