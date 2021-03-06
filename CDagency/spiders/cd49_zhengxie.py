# -*- coding: utf-8 -*-
#成都市政协

import scrapy
import re
from CDagency.items import *

class CdZhengxieSpider(scrapy.Spider):

    name = 'CD49zhengxie'
    allowed_domains = ['cdcppcc.gov.cn']

    cookies = {
            'Hm_lvt_bfcedbba82bbcea63714a8479f973c2b':'1582558603,1582981618',
            'Hm_lpvt_bfcedbba82bbcea63714a8479f973c2b' : '1582995081'
        }

    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        'x-requested-with':'XMLHttpRequest'
    }

    def start_requests(self):
        start_urls = 'http://www.cdcppcc.gov.cn/index.php?m=search&c=index&a=init&typeid=89&siteid=1&q=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&page=1'
        return [scrapy.FormRequest(start_urls,callback=self.parse, headers = self.Headers, cookies = self.cookies)]

    def parse(self, response):
        """"默认的解析回调函数"""
        news = response.xpath("//a[@class='l-tit']")
        
        for new in news:

            item = CDagency()
            item["col_name"] = "CD49zhengxie"

            # 新闻链接
            href = new.xpath('./@href').extract_first()

            # 存到item
            item['detail_url'] = href

            yield scrapy.Request(href, callback=self.get_text,meta={'item': item, 'url': href},dont_filter=True)

        # 获取下一页链接
        current_url = response.url #当前页面
        
        num = '' #当前页面数
        for x in current_url[::-1]:
            if x == '=':
                break
            num = x + num

        next_url = 'http://www.cdcppcc.gov.cn/index.php?m=search&c=index&a=init&typeid=89&siteid=1&q=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&page=' + str(int(num)+1)
        if int(num) < 30:
            yield scrapy.Request(next_url, callback=self.parse, headers = self.Headers, cookies = self.cookies)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        # 标题
        title = response.xpath('//div[contains(@class,"show-title")]//text()').get() 
        title = "".join(title).strip()

        # 发布时间
        pub_time = response.xpath('//span[@class="show-inputtime"]//text()').get()[5:15] 
        # 发布单位
        bureau = '成都市政协'  
        # 获取详细内容
        content_list = response.xpath('//div[contains(@class,"show-content")]//text()').getall()

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
        item['pub_time'] = pub_time

        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item