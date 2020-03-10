#成都直属机关工委


import scrapy
import re
from CDagency.items import *
import json
from lxml import etree


class CdJiguanSpider(scrapy.Spider):

    
    name = 'CD05Jiguan'
    allowed_domains = ["cdjgdj.gov.cn"]
    start_urls = 'http://cdjgdj.gov.cn/website/sitefiles/services/cms/search/output.aspx?publishmentSystemID=1'

    cookies = {
        'UM_distinctid':'170947a24f2210-0c85f6544da128-4313f6b-e1000-170947a24f4856',
        'CNZZDATA1277834536':'512877084-1583038999-http%253A%252F%252Fcdjgdj.gov.cn%252F%7C1583159015'
    }
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        'X-Requested-With': 'XMLHttpRequest'
    }


    def start_requests(self):

        Datas = {
            'ajaxDivID': 'ajaxElement_2_401',
            'pageNum': '0',
            'isHighlight': 'False',
            'isRedirectSingle': 'False',
            'isDefaultDisplay': 'False',
            'dateAttribute': 'AddDate',
            'successTemplateString': 'ZuEMimNtzLfCBErUvaN3ReqOyeloyf59KtMNmpJ0add0ldVUXTxvM5XUjEsho7O9p0add0KfoudNw0fDH4TaN2KduejiCVt7VrdkDGtPnj0add0m0add0AW1NtiRummoh6hRWIsBxtw0add016ARMZsi6M9DRdn0add0PUVmTnMg0yoXAyQPMOHUCxPMDjspJZ9FLeR7YhephjnupHxOlWhRof1FHHpAgnN6aa4a4MBng8h0NvT3PlTooLhbGZnKJ2xvtfwLJmvU0slash0fr5TdylL1e1VkQNBs8J7fQvVOJO5Tf7CXlt0slash0dnHdqpm0slash0g40slash0kkFzx0n1BQl8lrvCRx5OBqRcQZJ0add0b2gUYD0slash0IBm5qq42Zge310add0x0add0MLk7JUQKEocYM4oKbJ0slash0mpjd41tUgA5Br3JFXOtqHn9iwGNpgvU4G8cDwCO60NdArj9Yd4c1pxFSvBAay3hRDEz7SCTZztnROXExfFhpj17LbHGOgEAQ74G90add0KaJgSHK732MyAEPPPTTTpOA0516cWjkQ0slash0e0slash0iFdQO6MQG7hOk1zrr89OJI17UJGvPld0add0rW7OxYtePadNj8NmXAt7Sp70slash0aJK1BSUnR6f4p0hkR50add0PWmuwdKLQ4M3d8N0slash062PPMCDzQlWT5F1XSUTWgKbfMmF0add0lntLsl2Iw6FXaKVLSRTYysCCuq0add0eNB9ffToJhCQCURTYMbyqQh1hTurKSgOXoWo2YuDnNJpcY45her70add00TWcP8QbCz0add09ZMFBB6pUcv1Rqjq2CyeIyYeRDm460i1qJBNBQKVebXQza4ikvN90GFqahf3vD88ZKD0slash0h3Pkgn0add0DOhpdStDrAhQJpiM7ZO61S4vhUnbBPb0add00slash0Y0add05R0slash0SRn4lGVUoBXwMzZX8hOQWO0add0kVL3K8oPykyZwPtUlfiNsC8I90ApGnxZch0slash0onAw2ifgNVuUDnPLxA7J5FuXR9ySn0add0z83uCGUOwhBbYWDLloFmTt9rvqzAOefT7XLZhCOltm00hS3W6k5Q4oBFAlVXlx0slash0DNfA0tBVTCNIN5oyL0add0c6qUrtCGHseXF2pMByFZHLVlJx9KmS7Dp8ZA4WsfLKAzls0NWwvT0add0ce0slash0YJHX3bL0XfXxyOZyjySuXan0add0tC4vxkh10RbjrZ5sM367VYpTf7Kr0slash0nfbhCXHZs0slash06x6MlBBIiMiffh9huLQGjl4olB0add0Ywb9UVIuBfdNcX1jJSKP0add0gCx0F9FbiYxLcxcwa51uNmyUwt4qiNC9tdJcf7bOdtM57PSCF5y1ob0add0fX6uAs1hI0slash0r8ekonXsuxh0add0iwWBvJdAxaTmqgyPM1pyDpWRk93S50WOxtf0slash0pAqSyHLKsy0KfrMZJXnDXiEfrT5KhVW1HS0add00qJq0slash0K0add0p0DZCfvt0ZD0YX0t5JDU31IJuT6u8lzO8lNNnXjvVgrb521PFPq1Be0F9TvPpeapN2hkgl4XHG4KS9s0lO0slash0X2J3Xxa1vS3ME81r2EFWZMJDwdL9pUrx35ac79peXQEj0slash0HkNlH2fknTM5retCH4kuP8Cbdi6vc0r5PqWT0ZBGHLTEltLPyVajpACN0slash0NYs0OpH2DR0add0CskFOGRBgGiTtc5Kmoy0add00add0F0add03dt0slash0xSe9VidBYzhjPRa0slash0Nu0add0Abt0xReOmcla5gXT0slash0nCMwoi4qFlFxLHZGi8HDouOFuqVNnKlqneKkYenZB7x7zILkucRcm0slash0tiNofHvbs0add0mLpt7CvKAUSspfk1ubdbaoQfVjir1uE6SrPNEVqK3MctsH2xXCzzFoxTnw1vbsoFpIx89QlEH7Kd0Kvsicp6y27BnGiI0slash0AimIg0VKu5aVhcxJpTDLk0XZC2YWDB3lK5Ug0add0ZM4Acq0slash0c0add0Fq1UNOUPdjMd2oO1P7GvQn6P9gopuIhCRBnwqDiavV81aP0DfOUS413dPWFo2bIx0slash00add0Fnw70comhgthQYnU146ddfAbhLHic130jeAdXfPq76BixLPaqF0add0uMujnxii6mwAqGQUZVlYgT00add00slash0kkeMpDUPqbP8arILnpyghVg1pyVPS54X119lVeDpQ8YpAFnMj3gHV7KChyhHTD77LNwQW4O0kD0slash0esFzUxbLXNpSFveDa2t4qxueqh1Jp3gKshiTCwA2kVwlowdPDANx0add08BJ8hetcinQ9jcxJHRyevWWS0add0paFFa63EERM0vPwNfDzT3Lt0slash0T63BWOrxfGJFv1muXJpy5HPyizz79c0slash0pwza1uF4fHkr0slash0sssUAujJkJvspAmAe14rjii7gBAEQHbOMmMisUyllDtBar0yy8n8TAgmxuRnpxuwCQDM181QGbQo0add0p7IpyYDrd8HApxgttpT8KaRQX6MA1XDj7ub35B3Pq0slZXHtBtN7JvWVOnZMC4O8rx7mtjgYmCFQEurtfpaX0bA0add06XeGamX1usxA0slash0fRe7HDinLmiN9i1r4xjCVkCsWOGegQReI7dX7L2aTXdZ5b2BRRjACSy0add0aLPaqyNQI3C9gBcz75E10CI7KMQfVBK0slash0FGB8rWXggljhiWFWKzA9mxiXE9MzBLc18ey3RPS66bNCfTQoxT7YMiQY0add0mEQp43TwzN6qbH0Ad4Io0fGEspuGxEYniHRpWbNNvEg1hgCd8KlZMYZVOyHqAKUBtG1SYEY3u8i0slash0772UHJVlZpwQJA0add0zMDEA1sifKBBrLm46lOKdv6lmYeHNy9BhqYjlJXgvVyCSdAHihVo4ZFxJDi8PRkRfGq2xQGjFarp8NyJSxulsIky4jwC2HsKPKKt540add0PLRXF2Ehq0add0wc0slash0asVflS70o5uXJh4ITRhGaW6KqCEIMbw30add0Ez1AgVTs85492ZQH1UzOTo5bJWrKcyJLYQGZulNWEixfq0JqW9sCnzNN0add0X0slash01hkZZyIY9ef7xZQfbDs7F0slash0hWlxOto0add0lvjxmrEpyHAy4affV0add00YvEUpjaP5KXnwBSBp3u56x0HxGXlb69ob9C0add0C8H1ImpnnXVpu68c1bVLpW6hNSBcVKDGqBLXQUUkS7WBhL0add0r0jHtvrX0slash0EZj7sFoG1uX77XK8vUWoWvRairy2tmpdbMsL0add0nXC5xxZ9TGrvrG7b8PXEdUTO03Thi1dyVk14SF0slash0XNGHVez0add01Z5o4RxtmlYtKUl2GYoX0add0cyYJb69TpcWdmNPN6u0add0jAoPk9Rkc6FKcXpRqhXHNn1GmgIIDKFoTdoMHIIXXze7uAfvFr0add0jO3RpeRl02T0QGOlgzygMCaDCTMzD4DeJLJnVYqF091uGQ0slash0bkoROTEnGC20UQaBstt60slash0UcvxwWDs9RoIL04L8L9JTstxsdZbgDlJAzqa9DwAqbRUBom0add0RoNE9p1bJoFNHGkbrG8VO7jdYrJUbwCG90qYu9A0OgHFzSf67Ux1eGniDolqlxympPd01yeXNmRwpT4DUXmjtwrp0add0qhQLe5WTXrIXBNe6j60re87Djw4R0add0fJAKjXbHxyEhoiwYuma7irG0UOm98dsaYDaRvRjI2XBaEWIQkoOSL6IEgrF2n0add0UX6iUZQjRwxQMlrbM0slash0nIblsdx0slash0D0UdmeWq1QIWVHW0add0GbbN9X2bKDBf600add0EoAQeB6NbPF04wIytxNvBFvsKwxCKyjjHQX0kxA8JxcTh0add0jpHeV7m9cePeMUApO85Dv6JtvGYEZOKWW10slash0OHILETQ4TRB86kJPzbD0add0MNvPY3NAU9ayn6oRYxZmbVozUe507sEPMUaW8vRbvqJqt3QPAgWj0slash0mGjPECxCMWhBULCPxao4QUZ3QMlkUcBHeW3sP0slash0uMzjn1zlPMEJX0add0XppaUkUpTMV482d8nGjY7DdJUpOaDBoLFoEQfmK4mA2exVWlhe2mV1IpaoZ3JYx4tAIvap9GjmbVtjhINScwooe0add0Lk5ohTUYt6lUyEdtj7HVtCQoTqv0OycteqUI0add0Nw3UaL9McN0slash0N0add0tgFn8S7BJv6kLX0xxA0ze8TkK1n0slash0kVKlCPM4Jkp3NceodIeS2OG4xiQNpyf78VNqAx5M00slash0Azg1BuqV6QsZMk7gx0add0nsS18KzS1Uwj0add0WPQ21MoPnmSTYe4QbKdgmxuWkHg7Gin8v6LwoRPhu0jSHhEJBrMBuZkwPGl4yIpgcd9Whko8CYeKZfxDdIjLNGP0add0Kyyxi0add01ZYpA9FY126cIFE3JPDhWTlQELxQus2L8tXVoVtbMFZymQij6tDfPRnjFZzAur6v95fSJvB0slash06azZ4nmjyM5mY7q6vQH2sAhWl86WNDRlN00add0So0slash0Mq7d0uIc9O0i0slash01KqTvCEoj1WLNiS4BBlTz0add0RgwQP9flZnBdrKDNvTg0add0b40add0c4k0slash0kFU9NMThD4sJN7UPbuUlwNLEaDYuCoFdkXYRlYldCcVfzG57d0slash07gYRUBtqpTQOG13j82jK8jpZQgURYndsYcue0slash09EUcqTVhplZb0slash0pDxXYI0slash06FVNruJqRaUvjq0slash0jSdRRxO2OGhjwnD6GIBISsEhLBlvzOp08CXi9f5x0pOxBvG7BwnEUyuwioA0dKuVYcPiu7KTIQ1HEP2T7Ku1Q2RwdwV1I3TUBXoaxdGo0slash0Z4H3QyhOoSOtyN46hEU0KUrk831W8ZPVWvAxOpjVvCBTypaiyswEroceH2RmgCuF8cmjZ80slash0MFE0WIUbNBnGq0slash0FbvZUOgBPIvCLwiQBOaJKrR4lTRstZsP3ynaeKnjvb2Da0add0aGkAN8ZpHNVpQO849k2TvDboif0add07wNMXwnuPEUQxrEdD5wSZXterRk13PoGAZ5pA8iQZw26aBL4KziipZc1Li2jzknvUI41IHJPTg0slash0dw9jFpzIqo3QLcFiaCWQYYjSannb2Og0equals00equals0',
            'failureTemplateString': 'ZuEMimNtzLfCBErUvaN3ReqOyeloyf59jYcLZSHtj4d6AYqp90add0DHKgxv0add0XoW0slash08Y9tuoMIrGxKdlu1Jd7SdmDHT7qD0slash0q8N3loMw10do10T7r3HSaOabiI03q7mKOzKpbh9D4P80lm8GVlyxYSLlof9e8RuJK0add0C6IyK2wZejCbod6X8i1RDpNYSevFYYCQ3VT0cZT0slash0e8RH5iAav7edC4sQpNAEIdUe770Nz58Ins9vWvNl1JpZkDX68U1aL1oIP4A72U1ruN00add0oHVAFCe0slash08jbWAyyyvyhwTQpNu73BY6RNr4kcvPpK9fUTXONBMRQFZZwYRp40add0XejkDtlTq0slash0YCH0add0Lto33QIEvRS0slash0XvzBy0slash0FQvovijJF3nfcDrDdIwmZ1Li5vIFm55FR28CH3c8lImR1u5Kj71h0add09GXvlZJKI1z3j0slash0md7BkLFjzAdB1wg0equals00equals0',
            'pageIndex': '0',
            'word': '不忘初心牢记使命',
            'channelID': '1'
        }

        for i in range(4):
            Datas['pageIndex'] = str(i)
            yield scrapy.FormRequest(self.start_urls,formdata=Datas,callback=self.parse, headers = self.Headers, cookies = self.cookies)

    def parse(self, response):
        """"默认的解析回调函数"""
        #获取响应内容
        data = etree.HTML(response.text)
        news = data.xpath('//li')

        for new in news:

            item = CDagency()
            item["col_name"] = "CD05Jiguan"

            # 新闻链接
            href = new.xpath('./a/@href')[0]
            detail_url = 'http://cdjgdj.gov.cn' + href
            # 存到item
            item['detail_url'] = detail_url

            yield scrapy.Request(detail_url, callback=self.get_text,meta={'item': item, 'url': detail_url},headers = self.Headers, cookies = self.cookies,dont_filter=True)

    def get_text(self, response):
        """获取详细的文本信息"""
        item = response.meta['item']

        # 标题
        title = response.xpath('//div[@class="newsdetail"]/h2//text()').get()
        # 发布时间
        pub_time = response.xpath('//p[@class="date"]/span[2]//text()').get()[3:]
        # 发布单位
        bureau = '中共成都市直属机关工委'  

        # 获取详细内容
        content_list = response.xpath('//div[@class="detailcontent"]//text()').getall()
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