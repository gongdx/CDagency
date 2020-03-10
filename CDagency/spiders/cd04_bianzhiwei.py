# -*- coding: utf-8 -*-
#成都市委机构编制委员会办公室

import scrapy
from CDagency.items import *
import re


class CdBianzhiweiSpider(scrapy.Spider):

    name = 'CD04bianzhiwei'
    allowed_domains = ['cdswbb.gov.cn']

    def start_requests(self):

        start_urls = 'http://www.cdswbb.gov.cn/Search/?key=%B2%BB%CD%FC%B3%F5%D0%C4%A1%A2%C0%CE%BC%C7%CA%B9%C3%FC'

        Headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
            'x-requested-with':'XMLHttpRequest'
        }

        return [scrapy.FormRequest(start_urls,callback=self.parse,headers = Headers)]

    def parse(self, response):
        news = response.xpath("//ul[@class='news_list']/li")

        for new in news:
            item = CDagency()
            item["col_name"] = "CD04bianzhiwei"

            # 解析响应中的各项信息
            title = new.xpath(".//a[@target='_blank']/text()").getall()
            title = "".join(title).strip()
            # print(title)

            # detail_url = new.xpath(".//a[@class='fl txt_color']/@href").get()
            # detail_url = 'http://cdfao.chengdu.gov.cn/search/' + detail_url
            detail_url = 'http://www.cdswbb.gov.cn' + new.xpath('.//a[@target="_blank"]/@href').get()
            pub_time = new.xpath(".//span[@class='news_date']/text()").get()
            # source = new.xpath(".//a[@class='link']/text()").get()
            # source = "".join(source).strip()

            item['bureau'] = '成都市委机构编制委员会办公室'
            item['title'] = title
            item['detail_url'] = detail_url
            item['pub_time'] = pub_time
            # item['source'] = source

            # yield item

            Headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
                'x-requested-with':'XMLHttpRequest'
            }

            yield scrapy.Request(url=detail_url, headers=Headers, callback=self._get_text, meta={'item': item, 'url': detail_url})

    def _get_text(self, response):
        item = response.meta['item']

        content_list = response.xpath('//div[@class="news_body"]//text()').extract()
        # 对文本进行拼接
        remove = re.compile(r'\s')
        douhao = re.compile(',')
        content = ''
        for string in content_list:
            string = re.sub(remove, '', string)
            string = re.sub(douhao, '', string)
            content += string
        item['content'] = content

        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item
