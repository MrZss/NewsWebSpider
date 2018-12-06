# -*- coding: utf-8 -*-
import scrapy  # 可以写这句注释下面两句，不过下面要更好
from scrapy.spiders import Spider
from scrapy.selector import Selector
import time
from scrapy import Request
from Lieyun_Spider.items import Post  # 此处如果报错是pyCharm的原因
from Lieyun_Spider.timestamp import timestamp




class LieyunSpider(Spider):
    name = "lyspider"
    allowed_domains = ["lieyunwang.com"]  # 允许爬取的域名，非此域名的网页不会爬取
    start_urls = [
        "http://www.lieyunwang.com/t/电商"

        # 起始url，此例只爬这个页面
    ]
    url_list = [
        "http://www.lieyunwang.com/t/社交",
        "http://www.lieyunwang.com/t/硬件",
        "http://www.lieyunwang.com/t/传媒",
        "http://www.lieyunwang.com/t/文化",
        "http://www.lieyunwang.com/t/娱乐",
        "http://www.lieyunwang.com/t/工具",
        "http://www.lieyunwang.com/t/生活",
        "http://www.lieyunwang.com/t/金融",
        "http://www.lieyunwang.com/t/医疗",
        "http://www.lieyunwang.com/t/企业服务",
        "http://www.lieyunwang.com/t/旅游",
        "http://www.lieyunwang.com/t/房产",
        "http://www.lieyunwang.com/t/家居",
        "http://www.lieyunwang.com/t/教育",
        "http://www.lieyunwang.com/t/汽车",
        "http://www.lieyunwang.com/t/交通",
        "http://www.lieyunwang.com/t/物流",
        "http://www.lieyunwang.com/t/人工智能",
        "http://www.lieyunwang.com/t/无人车",
        "http://www.lieyunwang.com/t/无人机",
        "http://www.lieyunwang.com/t/机器人",
        "http://www.lieyunwang.com/t/vr",
        "http://www.lieyunwang.com/t/AR",
        "http://www.lieyunwang.com/t/体育",
        "http://www.lieyunwang.com/t/共享",
        "http://www.lieyunwang.com/t/出海",
        "http://www.lieyunwang.com/t/消费"

    ]
    url_list_pass = []
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

        divs = selector.xpath(
            '//*[starts-with(@class, "article-container")]/div[@class="article-bar clearfix"]')  # 取出所有的楼层

        for each in divs:
            item = Post()  # 实例化一个Item对象
            href = each.xpath('div/a/@href')[0].extract()
            content_url = 'http://www.lieyunwang.com' + href
            item['title'] = each.xpath('div[@class="article-info pore"]/a/text()').extract()[0].encode('utf-8')
            item['author'] = each.xpath('div[@class="article-info pore"]/div[@class="article-info-tool clearfix"]/div/a/text()')[0].extract().encode('utf-8')

            time = each.xpath('//*[starts-with(@class, "time")]/text()').extract()[0].encode('utf-8')

            item['post_time'] = timestamp(time)
            # ## 猎云有的是一天前这种格式  后期在处理


            item['summary'] = each.xpath('div[@class="article-info pore"]/p/text()')[0].extract().encode('utf-8')

            item['img_url'] = each.xpath('a/img/@src')[0].extract().encode('utf-8')
            #
            item['post_from'] = '猎云网'

            yield scrapy.Request(content_url,meta={'item': item}, callback=self.content_parse)
        # for url in self.url_list:
        #     if url not in self.url_list_pass:
        #         yield Request(url, callback=self.parse)
        #         self.url_list_pass.append(url)

    def content_parse(self, response):
        item = response.meta['item']
        url= response.url
        url = url.split('/')
        item['_id']='L'+url[-1]
        tags = response.xpath('//ul[starts-with(@class, "article-tags mb20 clearfix")]/li/a/text()').extract()
        for tag in tags:
            item['tag'] = tag.encode('utf-8')
        p_list = response.xpath('//*[starts-with(@class, "main-text")]/p')
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









