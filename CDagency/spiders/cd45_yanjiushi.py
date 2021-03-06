# -*- coding: utf-8 -*-
#成都市政府研究室

import scrapy
import re
from CDagency.items import *
from .browse_times import getBrowseTimes

class CdWaishijuSpider(scrapy.Spider):

    name = 'CD45yanjiushi'
    allowed_domains = ['cdyjs.chengdu.gov.cn']
    start_urls = ['http://cdyjs.chengdu.gov.cn/search/s?q=1&qt=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&pageSize=10&database=all&siteCode=5101000043&docQt=&page=1']

    def parse(self, response):
        """"默认的解析回调函数"""
        news = response.xpath("//div[contains(@class,'discuss') or contains(@class,'topic')]")
        for new in news:

            item = CDagency()
            item["col_name"] = "CD45yanjiushi"

            # 标题
            title = new.xpath(".//a[contains(@class, 'fl')]/@title").getall()
            title = "".join(title).strip()
            # print(title)

            # 新闻链接
            href = new.xpath('.//a[@class="link"]/@href').extract_first()
            # print(href)
            initial_url = 'http://cdyjs.chengdu.gov.cn/search/' + str(href)

            # 发布时间
            pub_time = new.xpath(".//span[@class='colo-666']/text()").get()
            # 发布单位
            bureau = new.xpath(".//a[@class='link']/text()").get()
            bureau = "".join(bureau).strip()

            # 存到item
            item['title'] = title
            # item['detail_url'] = detail_url
            item['pub_time'] = pub_time
            item['bureau'] = bureau

            # yield item

            yield scrapy.Request(url=initial_url, callback=self.get_detail_url, meta={'item': item, 'url': initial_url},dont_filter=True)

        # 获取下一页链接
        current_url = response.url #当前页面

        num = '' #当前页面数
        for x in current_url[::-1]:
            if x == '=':
                break
            num = x + num

        next_url = 'http://cdyjs.chengdu.gov.cn/search/s?q=1&qt=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&pageSize=10&database=all&siteCode=5101000043&docQt=&page=' + str(int(num)+1)
        if int(num) < 15:
            yield scrapy.Request(next_url, callback=self.parse)

    def get_detail_url(self, response):
        item = response.meta['item']

        detail_url = re.search('location.href\ =\ "(.*?)";', response.text).group(1)
        # print(detail_url)
        item['detail_url'] = detail_url

        yield scrapy.Request(url=detail_url, callback=self.get_text, meta={'item': item, 'url': detail_url},dont_filter=True)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']
        
        # 获取详细内容
        content_list = response.xpath('//p[contains(@style,"justify")]//text()').getall()

        # 对文本进行拼接
        remove = re.compile(r'\s')
        douhao = re.compile(',')
        content = ''
        for string in content_list:
            string = re.sub(remove, '', string)
            string = re.sub(douhao, '', string)
            content += string

        item['content'] = content

        # 获取部门信息,有其他内容
        # department = response.xpath('//div[@class="xwny-box"]/p/text()').get()
        # item['department'] = department

        # 获取浏览量
        url = response.meta['url']
        
        item['browse_times'] = getBrowseTimes(url)

        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item