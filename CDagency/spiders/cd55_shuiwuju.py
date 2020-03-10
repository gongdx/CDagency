#四川税务局


import scrapy
import re
from CDagency.items import *
import json
from lxml import etree

class CdShuiwujuSpider(scrapy.Spider):

    name = 'CD55shuiwuju'
    allowed_domains = ['sichuan.chinatax.gov.cn']
    start_urls = 'http://sichuan.chinatax.gov.cn/jsearchfront/interfaces/cateSearch.do'

    cookies = {
        'user_sid':'27c690603dae4214b3d4779db5caf5d9',
        '_q':'%E5%B8%82%E5%B1%80%20%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD%2C%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD',
        'JSESSIONID':'372D76DCF7D5F36025380B85899C58FD',
        'sid':'031acbe40fc38eaad03933bcab952b62',
        'searchsign':'2fbee418954f49a5946fae126b21b0d0',
        'yfx_c_g_u_id_10003707':'_ck20022423093012849417136519432',
        'yfx_mr_10003707':'%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search',
        'yfx_mr_f_10003707':'%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search',
        'yfx_key_10003707':'',
        'zh_choose_1':'s',
        'zh_choose_undefined':'s',
        'yfx_f_l_v_t_10003707':'f_t_1582556970243__r_t_1583229185258__v_t_1583229185258__r_c_4'
    }

    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }

    def start_requests(self):

        Datas = {
            'websiteid': '510000000000000',
            'q': '不忘初心、牢记使命',
            'p': '1',
            'pg': '12',
            'pos':'', 
            'cateid': '8',
            'tpl': '3'
        }

        for i in range(1,100):
            Datas['p'] = str(i)
            yield scrapy.FormRequest(self.start_urls,formdata=Datas,callback=self.parse, headers = self.Headers, cookies = self.cookies)

    def parse(self, response):
        """"默认的解析回调函数"""
        #规范化str，符合json格式
        data = response.text
        data_json = json.loads(data)
        
        for new in data_json['result']:

            item = CDagency()
            item["col_name"] = "CD55shuiwuju"

            new = etree.HTML(new)
            # 新闻链接
            href = new.xpath('//a[@target="_blank"]/@href')[0]
            url = 'http://sichuan.chinatax.gov.cn/jsearchfront/' + href
            # 存到item
            item['detail_url'] = url

            yield scrapy.Request(url, callback=self.get_text, meta={'item': item, 'url': href},dont_filter=True)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        # 标题
        title = response.xpath('//div[@id="title"]//text()').get()
        title = "".join(title).strip()
        # 发布时间
        time = response.xpath('//td[@class="fasj-td"]//text()').get()
        start1 = time.find('发布时间')
        pub_time = time[start1+6 : start1+16]
        pub_time = "".join(pub_time).strip()
        # 来源
        '''
        lai = response.xpath('//td[@class="ly-td"]//text()').get()
        start2 = lai.find('来源')
        department = lai[start2+3:]
        department = "".join(department).strip()
        '''

        # 发布单位
        bureau = '国家税务总局四川省税务局'  

        # 获取详细内容
        content_list = response.xpath('//div[@class="info-cont"]//text()').getall()
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
        # item['department'] = department
        item['pub_time'] = pub_time

        #判断新闻内容所属类型
        item["type"] = []
        type_lists = ["主题教育","专题讲座","专题党课","主题党日","专题报告","知识竞赛","研讨交流会","座谈会","专题学习会","集中学习周","读书班"]
        for type_list in type_lists:
            if type_list in content:
                item["type"].append(type_list)

        yield item