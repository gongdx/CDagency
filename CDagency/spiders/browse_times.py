import requests
import json

def getBrowseTimes(url):
    #指定ajax-post请求的url（通过抓包进行获取）
    #url = 'http://cdfao.chengdu.gov.cn/cdwqb/c107685/2019-06/26/content_41f0218975e74bb6876478d067781521.shtml'

    el_list = url.split('/')

    browse_url = 'http://' + el_list[2] + '/cms-access-count/accessCount/addCount.do'
    resourceId = el_list[-1].split('.')[0][8:]
    resourceUrl = el_list[4] + '/'

    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
        'x-requested-with':'XMLHttpRequest'
    }

    # 处理post请求携带的参数(从抓包工具中获取)
    data = {
        'type': '2',
        'resourceId': resourceId,
        'url': resourceUrl 
    }

    # 2.发起基于ajax的post请求
    response = requests.post(url=browse_url,data=data,headers = Headers)

    #获取响应内容：响应内容为json串
    data = response.text
    data = json.loads(data)

    return data['count']