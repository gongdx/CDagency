# -*- coding: utf-8 -*-
# 成都市经济和信息化局

import scrapy
from CDagency.items import *
import re


class CdJingjijuSpider(scrapy.Spider):
    name = 'CD08jingjiju'
    allowed_domains = ['cdjx.chengdu.gov.cn']
    start_urls = [
        'http://cdjx.chengdu.gov.cn/search/s?q=1&qt=不忘初心、牢记使命&pageSize=10&sort=D&database=all&siteCode=5101900200&docQt=&page=1']

    def parse(self, response):
        news = response.xpath("//div[contains(@class,'discuss') or contains(@class,'topic')]")
        # print(response.text)
        for new in news:
            item = CDagency()
            item["col_name"] = "CD08jingjiju"

            # item['url'] = new.xpath('.//a[@class="link"]/@href').extract()
            item['pub_time'] = new.xpath('.//span[@class="colo-666"]/text()').extract_first()
            item['title'] = new.xpath('.//a[contains(@class,"fl")]/@title').extract_first()

            bureau = new.xpath('.//a[@class="link"]/text()').extract_first()
            bureau = "".join(bureau).strip()
            item['bureau'] = bureau
            # yield item

            href = new.xpath('.//a[@class="link"]/@href').extract_first()
            # print(href)
            initial_url = 'http://cdjx.chengdu.gov.cn/search/' + str(href)
            # print(detail_url)

            yield scrapy.Request(url=initial_url, callback=self.get_detail_url, meta={'item': item, 'url': initial_url},
                                 dont_filter=True)

        # 获取下一页链接
        current_url = response.url  # 当前页面

        num = ''  # 当前页面数
        for x in current_url[::-1]:
            if x == '=':
                break
            num = x + num

        next_url = 'http://cdjx.chengdu.gov.cn/search/s?q=1&qt=不忘初心、牢记使命&pageSize=10&sort=D&database=all&siteCode=5101900200&docQt=&page=' + str(
            int(num) + 1)
        if int(num) < 15:
            yield scrapy.Request(next_url, callback=self.parse)

    def get_detail_url(self, response):
        item = response.meta['item']

        detail_url = re.search('location.href\ =\ "(.*?)";', response.text).group(1)
        # print(detail_url)
        item['detail_url'] = detail_url

        yield scrapy.Request(url=detail_url, callback=self.get_text, meta={'item': item, 'url': detail_url},
                             dont_filter=True)

    def get_text(self, response):
        item = response.meta['item']

        content_list = response.xpath('//div[@id="top" or @class="main-show-txt"]//text()').extract()
        # 对文本进行拼接
        remove = re.compile(r'\s')
        douhao = re.compile(',')
        content = ''
        for string in content_list:
            string = re.sub(remove, '', string)
            string = re.sub(douhao, '', string)
            content += string
        item['content'] = content

        # department = response.xpath('//span[@class="xxly"]/text()').extract_first()
        # item['department'] = department

        # 判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育", "专题讲座", "专题党课", "主题党日", "专题报告", "知识竞赛", "研讨交流会", "座谈会", "专题学习会", "集中学习周", "读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item
