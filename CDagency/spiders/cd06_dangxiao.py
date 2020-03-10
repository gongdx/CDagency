#市委党校

import scrapy
import re
from CDagency.items import *

class CdDangxiaoSpider(scrapy.Spider):

    
    name = 'CD06dangxiao'
    allowed_domains = ['cddx.gov.cn']
    start_urls = ['https://www.cddx.gov.cn/page/search?keyword=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&page=1']

    def parse(self, response):
        """"默认的解析回调函数"""
        news = response.xpath("//a[@target='_blank']")
        
        for new in news:

            item = CDagency()
            item["col_name"] = "CD06dangxiao"

            # 新闻链接
            href = new.xpath('./@href').extract_first()
            detail_url = 'https://www.cddx.gov.cn' + href
            # 存到item
            item['detail_url'] = detail_url

            yield scrapy.Request(detail_url, callback=self.get_text,meta={'item': item, 'url': detail_url},dont_filter=True)

        # 获取下一页链接
        current_url = response.url #当前页面
        
        num = '' #当前页面数
        for x in current_url[::-1]:
            if x == '=':
                break
            num = x + num

        next_url = 'https://www.cddx.gov.cn/page/search?keyword=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&page=' + str(int(num)+1)
        if int(num) < 10:
            yield scrapy.Request(next_url, callback=self.parse)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        # 标题
        title = response.xpath('//div[@class="news-title"]//text()').get() 
        title = "".join(title).strip()

        # 发布时间
        pub_time = response.xpath('//div[@class="news-info"]/span//text()').get()[5:]
        # 发布单位
        bureau = '中共成都市委党校'  
        #浏览次数
        browse_times = response.xpath('//div[@class="news-info"]/span[3]//text()').get().strip()

        # 获取详细内容
        content_list = response.xpath('//div[contains(@class,"news-cont")]//text()').getall()
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