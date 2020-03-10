# -*- coding: utf-8 -*-

#####################成都市监管局###########################
################################################

import scrapy
from CDagency.items import *
import re


class JianguanjuSpider(scrapy.Spider):
    name = 'CD33jianguanju'
    allowed_domains = ['cdwglj.chengdu.gov.cn/']
    start_urls = ['http://cdwglj.chengdu.gov.cn/search/s?q=1&qt=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&pageSize=10&database=all&siteCode=5101000037&docQt=&page=1']

    def parse(self, response):
        news = response.xpath("//div[@class='classify project']//div")

        for new in news:
            item = CDagency()
            item["col_name"] = "CD33jianguanju"

            # item['url'] = new.xpath('.//a[@class="link"]/@href').extract()
            item['pub_time'] = new.xpath('.//span[@class="colo-666"]/text()').extract_first()
            # item['title'] = new.xpath('.//a[contains(@class, "fl")]/@title').extract_first()

            bureau = new.xpath('.//a[@class="link"]/text()').extract_first()
            # item["type"] = str(type(bureau))
            bureau = str(bureau)
            bureau = "".join(bureau).strip()
            item['bureau'] = bureau

            # yield item
            href = new.xpath('.//a[@class="link"]/@href').extract_first()
            # print(href)
            initial_url = 'http://cdwglj.chengdu.gov.cn/search/' + str(href)
            # item["initial_url"] = initial_url

            # print("*"*50)
            # print(initial_url)
            # print("*"*50)

            # yield item
            # detail_url = 'http://cdmzj.chengdu.gov.cn/' + re.search('location.href\ =\ "(.*?)";', response.text).group(1)

            yield scrapy.Request(url=initial_url, callback=self.get_detail_url, meta={'item': item, 'url': initial_url}, dont_filter=True)
    #
        for i in range(2):
            next_url = 'http://cdwglj.chengdu.gov.cn/search/s?q=1&qt=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%EF%BC%8C%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&pageSize=10&database=all&siteCode=5101000037&docQt=&page=' + str(i+2)
            # print("^"*50)
            # print(next_url)
            # print("^"*50)
            yield scrapy.Request(next_url, callback=self.parse)

    def get_detail_url(self, response):
        item = response.meta['item']

        # detail_url = re.search('location.href\ =\ "(.*?)";', response.text).group(1)
        detail_url = re.findall('location.href\ =\ "(.*?)";', response.text)[0]
        # print(detail_url)
        # print(response.text)
        # print(detail_url)
        # detail_url = 'http://cdwglj.chengdu.gov.cn'+detail_url
        item['detail_url'] = detail_url
    #     item['responsetext'] = response.text
    #     yield item
    #
        yield scrapy.Request(detail_url, callback=self.get_text, meta={'item':item,'url':detail_url}, dont_filter=True)

    def get_text(self, response):
        item = response.meta['item']

        # content_list = response.xpath('//div[@id="detail"]//p//text()').getall()
        # content = "".join(content_list).strip()
        # 对文本进行拼接   compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象
        # remove = re.compile(r'\s')
        # douhao = re.compile(',')
        # content = ''
        # for string in content_list:
        #     #将空格和逗号替换成空字符
        #     string = re.sub(remove, '', string)
        #     string = re.sub(douhao, '', string)
        #     content += string

        content_title = response.xpath("/html/head/title/text()").get()
        content_title = "".join(content_title).strip()
        item['title'] = content_title

        content = response.xpath("//div[@id='myTable']//p//text()").getall()
        content = "".join(content).strip()     #去空格
        content = "".join(content.split())     #去'\xa0\xa0\xa0 \xa0'
        item["content"] = content

        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item
