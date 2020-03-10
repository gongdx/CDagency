# -*- coding: utf-8 -*-
#成都市住房公积金管理中心


import scrapy
import re
from CDagency.items import *
import json
from lxml import etree

class CdGongjijinSpider(scrapy.Spider):

    name = 'CD38gongjijin'
    allowed_domains = ['api.chengdu.gov.cn','cdzfgjj.gov.cn','cdzfgjj.chengdu.gov.cn/']

    cookies = {
            'yfx_c_g_u_id_10000063':'_ck20022113090310338032502363169', 
            'UM_distinctid':'1707573b02232e-03d1512927b302-6313f69-e1000-1707573b0235b3',
            'yfx_mr_f_10000063':'%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search',
            'yfx_mr_10000063':'%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search',
            'yfx_key_10000063':'',
            'yfx_c_g_u_id_10008022':'_ck20022500235316831607112375875',
            'yfx_f_l_v_t_10008022':'f_t_1582561433676__r_t_1582790585274__v_t_1582790585274__r_c_1',
            'yfx_c_g_u_id_10008071':'_ck20022920272912701324292521200',
            'yfx_f_l_v_t_10008071':'f_t_1582979249247__r_t_1582979249247__v_t_1582979249247__r_c_0',
            'yfx_f_l_v_t_10000063':'f_t_1582261743032__r_t_1583130219635__v_t_1583130219635__r_c_8'
        }

    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0"
    }

    def start_requests(self):
        start_urls = 'http://api.chengdu.gov.cn/gjjAdmin/getItemsApi.php?x-msc-token=z1o5s0zmrNXBPq3s0eI7yxJUV9PtZoKL&callback=jQuery112404108622152531227_1583131608166&search=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&newPage=1&length=10&_=1583131608179'
        return [scrapy.FormRequest(start_urls,callback=self.parse, headers = self.Headers, cookies = self.cookies)]

    def parse(self, response):
        """"默认的解析回调函数"""
        #规范化str，符合json格式
        head = ''
        for x in response.text:
            if x != '{':
                head = head + x
            else:
                break
        end = ''
        for x in response.text[::-1]:
            if x != '}':
                end = x + end
            else:
                break
        data = response.text.strip(head).strip(end)
        data_json = json.loads(data)
        
        for new in data_json['data']:

            item = CDagency()
            item["col_name"] = "CD38gongjijin"

            # 新闻链接
            info_id = new['INFO_ID']
            
            href = 'http://api.chengdu.gov.cn/gjjAdmin/getItemsApi.php?x-msc-token=z1o5s0zmrNXBPq3s0eI7yxJUV9PtZoKL&callback=jQuery112402593983158861346_1583138180938&listInfo='+ info_id +'&_=1583138180939'

            url = 'http://cdzfgjj.chengdu.gov.cn/cdzfgjj/jknry/jk_det.shtml?detailid=' + info_id
            # 存到item
            item['detail_url'] = url

            yield scrapy.Request(href, callback=self.get_text, headers = self.Headers, cookies = self.cookies, meta={'item': item, 'url': href},dont_filter=True)

        # 获取下一页链接
        current_url = response.url #当前页面
        
        #取当前页面数
        start_index = current_url.find('newPage')
        end_index = current_url.find('&length')
        num = current_url[start_index+8 : end_index]

        next_url = 'http://api.chengdu.gov.cn/gjjAdmin/getItemsApi.php?x-msc-token=z1o5s0zmrNXBPq3s0eI7yxJUV9PtZoKL&callback=jQuery112404108622152531227_1583131608166&search=%E4%B8%8D%E5%BF%98%E5%88%9D%E5%BF%83%E3%80%81%E7%89%A2%E8%AE%B0%E4%BD%BF%E5%91%BD&newPage='+ str(int(num)+1) +'&length=10&_=1583131608179'
        if int(num) < 10:
            yield scrapy.Request(next_url, callback=self.parse, headers = self.Headers, cookies = self.cookies)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        #规范化str，符合json格式
        head = ''
        for x in response.text:
            if x != '{':
                head = head + x
            else:
                break
        end = ''
        for x in response.text[::-1]:
            if x != '}':
                end = x + end
            else:
                break
        data = response.text.strip(head).strip(end)
        data_json = json.loads(data)

        # 标题
        title = data_json['data']['TITLE']

        # 发布时间
        pub_time = data_json['data']['RELEASED_DTIME'][:10]
        # 发布单位
        bureau = data_json['data']['SOURCE']
        # 获取详细内容
        content_str = data_json['data']['INFO_CONTENT']
        content_list = etree.HTML(content_str).xpath('//p[contains(@style,"text-")]//text()')

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