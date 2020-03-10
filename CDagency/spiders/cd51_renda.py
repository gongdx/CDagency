#成都人大

import scrapy
import re
from CDagency.items import *
from .browse_times import getBrowseTimes
import json
from lxml import etree

class CdRendaSpider(scrapy.Spider):

    name = 'CD51renda'
    allowed_domains = ['cdrd.gov.cn']

    start_urls = 'http://www.cdrd.gov.cn/website/npc/manage/search/querySearchList.jspx?'

    Headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
        }
    
    def start_requests(self):

        data = {
            'dto[\'keyword\']': '不忘初心、牢记使命',
            'dto[\'dateType\']': 'all',
            'dto[\'page\']': '0',
            'dto[\'size\']': '5'
        }
        for i in range(1,30):
            data['dto[\'page\']'] = str(i)
            yield scrapy.FormRequest(self.start_urls,formdata=data,callback=self.parse,headers = self.Headers)

    def parse(self, response):
        """"默认的解析回调函数"""

        #获取响应内容：响应内容为json串
        data = response.text
        data = json.loads(data)

        news = data['list']
        for new in news:
        #获取接口返回值
            item = CDagency()
            item["col_name"] = "CD51renda"

            # 标题
            title = new['title']
            title = "".join(title).strip()
            item['title'] = title

            # 新闻链接
            contentid = new['contentid']
            detail_url = 'http://www.cdrd.gov.cn/website/jdpl/'+ str(contentid) +'.jhtml'
            item['detail_url'] = detail_url

            # 发布时间
            pub_time = new['publishdate']
            # 发布单位

            bureau = '成都人大'

            # 获取详细内容
            text = etree.HTML(new['txt'])
            content_list = text.xpath('//p//text()')

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
            item['pub_time'] = pub_time.strip(' 日期：').strip()
            item['bureau'] = bureau

            #判断新闻内容所属类型
            item["type"] = []
            type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
            for type_list in type_lists:
                if type_list in content:
                    item["type"].append(type_list)

            yield item

        #获取下一页请求
        
        