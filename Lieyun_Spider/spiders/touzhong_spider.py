# -*- coding: utf-8 -*-
import scrapy  # 可以写这句注释下面两句，不过下面要更好
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request

from Lieyun_Spider.timestamp02 import timestamp
from Lieyun_Spider.items import Post



class HeartsongSpider(Spider):
    name = "touzhong"
    allowed_domains = ["chinaventure.com.cn"]  # 允许爬取的域名，非此域名的网页不会爬取
    start_urls = [
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/180257.shtml"


        # 起始url，此例只爬这个页面
    ]
    # url_list = [
    #
    #
    # ]
    # url_list_pass = []
    cookies = {}

    # 发送给服务器的http头信息，有的网站需要伪装出浏览器头进行爬取，有的则不需要
    headers = {
        # 'Connection': 'keep - alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    }

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }

    def parse(self, response):
        selector = Selector(response)  # 创建选择器
        item = Post()  # 实例化一个Item对象
        li_list = selector.xpath('//*[starts-with(@class, "left_01 left_02 m_t_40")]/div[@class="news_list_01"]/ul/li')  # 取出所有的楼层
        for li in li_list:
            href = li.xpath('h3/a/@href')[0].extract()
            content_url = 'https://www.chinaventure.com.cn' + href
            item['summary']= li.xpath('p/text()')[0].extract()
            time = li.xpath('div[@class="t_01"]/div[@class="tt_01"]/@data-option')[0].extract().encode('utf-8')
            item['post_time'] = timestamp(time)


            yield scrapy.Request(content_url,meta={'item': item}, callback=self.content_parse)
        # for url in self.url_list:
        #     if url not in self.url_list_pass:
        #         yield Request(url, callback=self.parse)
        #         self.url_list_pass.append(url)

    def content_parse(self, response):
        item = response.meta['item']
        url = response.url
        url = url.split('/')
        _id = url[-1].split('.')
        item['_id'] = 'T' + _id[0]
        item['title'] = response.xpath('//*[starts-with(@class, "h1_01")]/text()').extract()[0]
        spans=response.xpath('//*[starts-with(@class, "details_01_l")]/span/text()').extract()
        if len(spans)==3:
            item['author']=spans[1]

        else:
            item['author']='佚名'


        item['tag'] = response.xpath('//div[starts-with(@class, "lab_01 m_t_40")]/a/text()').extract()
        item['img_url'] = "无"
        item['post_from'] = '投中网'
        p_list = response.xpath('//*[starts-with(@class, "content_01 m_t_30 detasbmo")]/p')
        p_content = []
        for p in p_list:
            if p.xpath('img/@src').extract():

                p_content.append({'type': 'img', 'body': p.xpath('img/@src').extract()})
            else:
                p_content.append({'type': 'text', 'body': p.xpath('text()').extract()})

        item['content'] = p_content
        item['comment'] =[]   # 评论 类型为一个列表
        item['coll_num'] = 1  # 收藏量
        item['share_num'] = 1  # 分享量
        yield item

    def sub_parse(self, response):
        selector = Selector(response)  # 创建选择器
        divs = selector.xpath(
            '//*[starts-with(@class, "search-tab-bar search-information")]/div[@class="article-bar clearfix"]')  # 取出所有的楼层

        for each in divs:
            href = each.xpath('div/a/@href')[0].extract()
            content_url = 'http://www.lieyunwang.com' + href

            yield scrapy.Request(content_url, callback=self.content_parse)


