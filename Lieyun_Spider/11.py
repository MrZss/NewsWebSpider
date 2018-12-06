# -*- coding: UTF-8 -*-
import scrapy  # 可以写这句注释下面两句，不过下面要更好
from scrapy.spiders import Spider
from scrapy.selector import Selector
import urlparse
from scrapy import Request

from pymongo import MongoClient
from Lieyun_Spider.timestamp02 import timestamp
from Lieyun_Spider.items import Post, Tags, Tagmap, PostDetail
from xpinyin import Pinyin
import chardet

client = MongoClient('0.0.0.0', 27017)
db = client.lxqcxcy


class HeartsongSpider(Spider):
    name = "touzhong"
    allowed_domains = ["chinaventure.com.cn"]  # 允许爬取的域名，非此域名的网页不会爬取
    start_urls = [
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/180257.shtml"
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/177078.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/183464.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/79.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/79.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/79.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/182139.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/11.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/180184.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/184288.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/8.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/178457.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/176677.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/21.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/180466.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/176156.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/177152.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/23.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/98.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/industrylist/98.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/175591.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/176702.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/178757.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/175598.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/176016.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/175910.shtm",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/176146.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/176201.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/184089.shtml",
        "https://www.chinaventure.com.cn/cmsmodel/news/keywordlist/183493.shtml"

        # 起始url，此例只爬这个页面
    ]

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
        li_list = selector.xpath(
            '//*[starts-with(@class, "left_01 left_02 m_t_40")]/div[@class="news_list_01"]/ul/li')  # 取出所有的楼层
        for li in li_list:
            href = li.xpath('h3/a/@href')[0].extract()
            content_url = 'https://www.chinaventure.com.cn' + href
            href_id_1 = href.split('/')
            href_id_2 = href_id_1[4].split('.')

            item['_id'] = 'T' + href_id_2[0]
            item['title'] = li.xpath('h3/a/text()')[0].extract()
            item['summary'] = li.xpath('p/text()')[0].extract()
            time = li.xpath('div[@class="t_01"]/div[@class="tt_01"]/@data-option')[0].extract().encode('utf-8')
            item['post_time'] = timestamp(time)

            item['post_from'] = '投中网'

            item['coll_num'] = 1  # 收藏量
            item['share_num'] = 1  # 分享量
            item['coll'] = 'Post'
            item['img_url'] = "无"
            yield item
            yield scrapy.Request(content_url, callback=self.content_parse)
        for url in self.url_list:
            if url not in self.url_list_pass:
                yield Request(url, callback=self.parse)
                self.url_list_pass.append(url)

    def content_parse(self, response):
        item = PostDetail()
        url = response.url
        url = url.split('/')
        _id = url[-1].split('.')
        id = 'T' + _id[0]
        item['_id'] = 'T' + _id[0]
        #        item['title'] = response.xpath('//*[starts-with(@class, "h1_01")]/text()').extract()[0]
        spans = response.xpath('//*[starts-with(@class, "details_01_l")]/span/text()').extract()
        if len(spans) == 3:
            item['author'] = spans[1]

        else:
            item['author'] = '佚名'

        tags = response.xpath('//div[starts-with(@class, "lab_01 m_t_40")]/a/text()').extract()
        item['tag'] = tags
        for tag in tags:
            tag = tag.encode('utf-8')
            p = Pinyin()
            tags_id = p.get_pinyin(unicode(tag, "utf8"), '')
            tags_db = db.Tags
            tagmap_db = db.Tagmap
            if not tags_db.find_one({"_id": tags_id}):
                tag_data = {
                    '_id': tags_id,
                    'tagname': tag

                }
                tags_db.insert(tag_data)
            if not tagmap_db.find_one({"_id": tags_id}):
                id_arr = []
                id_arr.append(id)
                tagmap_data = {
                    '_id': tags_id,
                    'post_id': id_arr

                }
                tagmap_db.insert(tagmap_data)
            else:
                tagmap_db.update({"_id": tags_id}, {"$addToSet": {"post_id": id}})

        p_list = response.xpath('//*[starts-with(@class, "content_01 m_t_30 detasbmo")]/p')
        p_content = []
        for p in p_list:
            if p.xpath('img/@src').extract():

                p_content.append({'type': 'img', 'body': p.xpath('img/@src').extract()})
            else:
                p_content.append({'type': 'text', 'body': p.xpath('text()').extract()})

        item['content'] = p_content
        item['comment'] = []  # 评论 类型为一个列表
        item['coll'] = 'PostDetail'

        yield item

    def sub_parse(self, response):
        selector = Selector(response)  # 创建选择器
        divs = selector.xpath(
            '//*[starts-with(@class, "search-tab-bar search-information")]/div[@class="article-bar clearfix"]')  # 取出所有的楼层

        for each in divs:
            href = each.xpath('div/a/@href')[0].extract()
            content_url = 'http://www.lieyunwang.com' + href

            yield scrapy.Request(content_url, callback=self.content_parse)


