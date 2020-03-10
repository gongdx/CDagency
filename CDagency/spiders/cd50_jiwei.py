#市纪委监察委

import scrapy
import re
from CDagency.items import *

class CdJiweiSpider(scrapy.Spider):

    
    name = 'CD50jiwei'
    allowed_domains = ['ljcd.gov.cn']
    
    cookies = {
            'zh_choose':'n',
            'Hm_lvt_05cfbb07a3a82bc9823a49b70346b4c5':'1583042532',
            'isNewOpen':'false',
            'gwdshare_firstime':'1583042547336',
            'sYQDUGqqzHsearch_history':'%u4E0D%u5FD8%u521D%u5FC3%u3001%u7262%u8BB0%u4F7F%u547D%7Cundefined',
            'Hm_lpvt_05cfbb07a3a82bc9823a49b70346b4c5':'1583043062'
        }

    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        'x-requested-with':'XMLHttpRequest'
    }

    def start_requests(self):
        start_urls = 'http://www.ljcd.gov.cn/index.php?m=search&c=index&a=init&typeid=&siteid=1&q=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&page=1'
        return [scrapy.FormRequest(start_urls,callback=self.parse, headers = self.Headers, cookies = self.cookies)]

    def parse(self, response):
        """"默认的解析回调函数"""
        news = response.xpath("//p[@class='p_tit']")
        
        for new in news:

            item = CDagency()
            item["col_name"] = "CD50jiwei"

            # 新闻链接
            detail_url = new.xpath('.//a[@target="_blank"]/@href').extract_first()
            # 存到item
            item['detail_url'] = detail_url

            yield scrapy.Request(detail_url, callback=self.get_text,meta={'item': item, 'url': detail_url},headers = self.Headers, cookies = self.cookies,dont_filter=True)

        # 获取下一页链接
        current_url = response.url #当前页面
        
        num = '' #当前页面数
        for x in current_url[::-1]:
            if x == '=':
                break
            num = x + num

        next_url = 'http://www.ljcd.gov.cn/index.php?m=search&c=index&a=init&typeid=&siteid=1&q=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&page=' + str(int(num)+1)
        if int(num) < 15:
            yield scrapy.Request(next_url, callback=self.parse, headers = self.Headers, cookies = self.cookies)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        # 标题
        title = response.xpath('//div[@class="xq_tite"]/h2//text()').get().strip()
        s = ""
        for x in title:
            if x == '' or x == '\n' or x == '\t':
                continue
            s = s + x
        title = s

        detail = response.xpath('//div[@class="xq_tite"]/span//text()').get().strip()
        # 发布时间
        start = detail.find('发布时间')
        pub_time = detail[start+5:start+15]
        # 发布单位
        bureau = '中共成都市纪律检查委员会 成都市监察委员会'  

        # 获取详细内容
        content_list = response.xpath('//div[@class="content1"]//text()').getall()
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