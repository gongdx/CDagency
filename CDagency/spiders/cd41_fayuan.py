#成都市法院

import scrapy
import re
from CDagency.items import *
import json
from lxml import etree


class CdFayuanSpider(scrapy.Spider):
    
    name = 'CD41fayuan'
    allowed_domains = ["cdfy.chinacourt.gov.cn"]

    cookies = {
        'PHPSESSID':'jlb0056oh5sbf4k3ar34mbs4f7'
    }
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        'Upgrade-Insecure-Requests': '1'
    }

    def start_requests(self):
        start_urls = 'http://cdfy.chinacourt.gov.cn/article/search/content_time_publish_begin/2002-01-01/content_time_publish_end/2030-03-03/article_category_id//content_author//keyword/%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD/button/%E6%8F%90%E4%BA%A4/page/1.shtml'
        yield scrapy.FormRequest(start_urls,callback=self.parse, headers = self.Headers, cookies = self.cookies)

    def parse(self, response):
        """"默认的解析回调函数"""
        #获取响应内容
        data = etree.HTML(response.text)
        news = data.xpath('//*[@id="container"]/div[3]/ul')

        for new in news:

            item = CDagency()
            item["col_name"] = "CD41fayuan"

            # 新闻链接
            href = new.xpath('./li[@class="title"]/a/@href')[0]
            detail_url = 'http://cdfy.chinacourt.gov.cn' + href
            # 存到item
            item['detail_url'] = detail_url

            yield scrapy.Request(detail_url, callback=self.get_text,meta={'item': item, 'url': detail_url},headers = self.Headers, cookies = self.cookies,dont_filter=True)
        
        # 获取下一页链接
        current_url = response.url #当前页面

        num = '' #当前页面数
        for x in current_url[::-1]:
            if x == '/':
                break
            num = x + num
        num = num.strip('.shtml')

        next_url = 'http://cdfy.chinacourt.gov.cn/article/search/content_time_publish_begin/2002-01-01/content_time_publish_end/2030-03-03/article_category_id//content_author//keyword/%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD/button/%E6%8F%90%E4%BA%A4/page/'+ str(int(num)+1) +'.shtml'
        if int(num) < 5:
            yield scrapy.FormRequest(next_url,callback=self.parse, headers = self.Headers, cookies = self.cookies)


    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        # 标题
        title = response.xpath('//div[@class="b_title"]//text()').get()

        detail = response.xpath('//div[@class="sth_a"]/span//text()').get()
        # 发布时间
        index1 = detail.find('发布时间')
        pub_time = detail[index1+5 : index1+15]
        # 来源
        '''
        index2 = detail.find('作者')
        department = detail[index2+3 : index1]
        department = "".join(department).strip()
        '''

        # 发布单位
        bureau = '成都法院'  

        # 获取详细内容
        #content_list = response.xpath('//div[@class="text general"]//text()').getall()
        content_list = response.xpath('//div[@class="detail"]/div[3]//text()').getall()
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
        #item['department'] = department
        item['pub_time'] = pub_time

        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item