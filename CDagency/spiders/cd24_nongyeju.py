#成都市农业农村局

# -*- coding: utf-8 -*-
import scrapy
from CDagency.items import *
import re


class CdNongyejuSpider(scrapy.Spider):
    name = 'CD24nongyeju'
    allowed_domains = ['cdagri.chengdu.gov.cn']
    start_urls = ['http://cdagri.chengdu.gov.cn/search/s?q=1&qt=不忘初心、牢记使命&pageSize=10&sort=D&database=all&siteCode=5101000014&docQt=&page=1']

    def parse(self, response):
        """"默认的解析回调函数"""
        news = response.xpath("//div[contains(@class,'discuss') or contains(@class,'topic')]")

        for new in news:
            item = CDagency()
            item["col_name"] = "CD24nongyeju"

            # 标题
            title = new.xpath(".//a[contains(@class, 'fl')]/@title").getall()
            title = "".join(title).strip()
            # print(title)

            # 新闻链接
            href = new.xpath(".//a[@class='fl txt_color']/@href").get()
            initial_url = 'http://cdagri.chengdu.gov.cn/search/' + str(href)
            # detail_url = 'http://cdfao.chengdu.gov.cn/cdwqb/c107685/' + re.search('location.href\ =\ "(.*?)";', response.text).group(1)

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

            yield scrapy.Request(url=initial_url, callback=self.get_detail_url, meta={'item': item, 'url': initial_url}, dont_filter=True)

        # 获取下一页链接
        current_url = response.url #当前页面

        num = '' #当前页面数
        for x in current_url[::-1]:
            if x == '=':
                break
            num = x + num

        next_url = 'http://cdagri.chengdu.gov.cn/search/s?q=1&qt=不忘初心、牢记使命&pageSize=10&sort=D&database=all&siteCode=5101000014&docQt=&page=' + str(int(num)+1)
        if int(num) < 15:
            yield scrapy.Request(next_url, callback=self.parse)

    def get_detail_url(self, response):
        """获取详情页面链接"""
        item = response.meta['item']

        detail_url = re.search('location.href\ =\ "(.*?)";', response.text).group(1)
        # print(detail_url)
        item['detail_url'] = detail_url

        yield scrapy.Request(url=detail_url, callback=self.get_text, meta={'item': item, 'url': detail_url},
                             dont_filter=True)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']
        # 获取详细内容
        content_list = response.xpath('//div[@class="details-inner"]//text()').getall()

        # 对文本进行拼接
        remove = re.compile(r'\s')
        douhao = re.compile(',')
        content = ''
        for string in content_list:
            string = re.sub(remove, '', string)
            string = re.sub(douhao, '', string)
            content += string

        item['content'] = content

        # 获取部门信息，部门信息和发布时间浏览量在一起不知如何分离
        # department = response.xpath('//span[@class="details-time"]/text()').get()
        # department = "".join(department).strip()
        # item['department'] = department

        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)


        yield item

