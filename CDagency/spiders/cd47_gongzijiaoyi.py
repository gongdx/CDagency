# -*- coding: utf-8 -*-
#市公共资源交易中心

import scrapy
import re
from CDagency.items import *
from .browse_times import getBrowseTimes
import json
from lxml import etree

class CdGgzySpider(scrapy.Spider):

    name = 'CD47ggzy'
    allowed_domains = ['cdggzy.com']


    def start_requests(self):
        start_urls = 'https://www.cdggzy.com/site/Handler.ashx?form=Search&action=GetSearNewchList&searchstring=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD'
        data = {
            'pageindex' : '1',
            'pagesize': '15'
        }

        Headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
            'x-requested-with':'XMLHttpRequest'
        }

        return [scrapy.FormRequest(start_urls,formdata=data,callback=self.parse,headers = Headers)]

    def parse(self, response):
        """"默认的解析回调函数"""

        #获取响应内容：响应内容为json串
        data = response.text
        data = json.loads(data)

        text = data['showinfo']
        response = etree.HTML(text)

        news = response.xpath('//td[@class="td_left"]')
        for new in news:

            item = CDagency()
            item["col_name"] = "CD47ggzy"

            # 标题
            title = new.xpath(".//a[@target='_blank']/@title")
            title = "".join(title).strip()
            item['title'] = title

            # 新闻链接
            initial_url = new.xpath(".//a[@target='_blank']/@href")[0]
            item['detail_url'] = initial_url

            Headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
                'x-requested-with':'XMLHttpRequest'
            }

            yield scrapy.Request(url=initial_url, headers = Headers, callback=self.get_text, meta={'item': item, 'url': initial_url},dont_filter=True)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']
        
        # 获取详细内容
        content_list = response.xpath('//div[@class="content-div"]//text()').getall()

        # 对文本进行拼接
        remove = re.compile(r'\s')
        douhao = re.compile(',')
        content = ''
        for string in content_list:
            string = re.sub(remove, '', string)
            string = re.sub(douhao, '', string)
            content += string

        # 发布时间
        
        pub_time = response.xpath("//*[@id='form1']/div[2]/div[4]/div[2]/div/div/div/h3/span[2]/text()").get()
        # 发布单位
        bureau = response.xpath("//*[@id='form1']/div[2]/div[4]/div[2]/div/div/div/h3/span[1]/text()").get()
        #bureau = "".join(bureau).strip()

        # 存到item
        item['content'] = content
        item['pub_time'] = pub_time.strip(' 日期：').strip()
        item['bureau'] = bureau

        # 获取浏览量
        #url = response.meta['url']
        
        #item['browse_times'] = getBrowseTimes(url)
        
        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item