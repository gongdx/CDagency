# 社治委

import scrapy
import re
from CDagency.items import *

class CdShezhiweiSpider(scrapy.Spider):
    name = 'CD02shezhiwei'
    allowed_domains = ['cdswszw.gov.cn']

    cookies = {
        'ASP.NET_SessionId': 'zwfsjgjb3riq31d1gczfppif'
    }
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        'x-requested-with': 'XMLHttpRequest'
    }

    def start_requests(self):
        start_urls = 'http://www.cdswszw.gov.cn/Search/?key=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&chnlId=&count=10'
        return [scrapy.FormRequest(start_urls, callback=self.parse, headers=self.Headers, cookies=self.cookies)]

    def parse(self, response):
        """"默认的解析回调函数"""
        a = 1
        news = response.xpath("//ul[@class='nonicon_listd']/li")

        for new in news:
            item = CDagency()
            item["col_name"] = "CD02shezhiwei"

            # 新闻链接
            href = new.xpath('.//a[@class="search_title"]/@href').extract_first()
            detail_url = 'http://www.cdswszw.gov.cn/' + href
            # 存到item
            item['detail_url'] = detail_url

            yield scrapy.Request(detail_url, callback=self.get_text, meta={'item': item, 'url': detail_url},
                                 headers=self.Headers, cookies=self.cookies, dont_filter=True)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        # 标题
        title = response.xpath('//div[@class="article_title"]//text()').get()
        title = "".join(title).strip()

        detail = response.xpath('//div[@class="article_info"]//text()').get().strip()
        # 发布时间
        start = detail.find('发布日期')
        pub_time = detail[start + 5:start + 15]
        # 发布单位
        bureau = '中共成都市委城乡社区发展治理委员会'
        # 浏览次数
        start2 = detail.find('查看次数')
        
        browse_times = ''
        for i in detail[start2+5:]:
            if i in ['0','1','2','3','4','5','6','7','8','9']:
                browse_times = browse_times + i
            else:
                break
        browse_times = int(browse_times)

        # 获取详细内容
        content_list = response.xpath('//div[contains(@class,"pbox")]//text()').getall()
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

        # 判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育", "专题讲座", "专题党课", "主题党日", "专题报告", "知识竞赛", "研讨交流会", "座谈会", "专题学习会", "集中学习周", "读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item
