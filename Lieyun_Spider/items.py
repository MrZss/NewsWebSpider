# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Post(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()     #帖子的标题
    author = scrapy.Field()    #帖子的作者
    post_time = scrapy.Field() #发表时间 时间戳格式
    summary = scrapy.Field()   #概述
    tag = scrapy.Field()       #标签
    img_url = scrapy.Field()   #主图片
    post_from =  scrapy.Field()#源网站
    content = scrapy.Field()   #帖子的内容
    comment = scrapy.Field()   #评论 类型为一个列表
    coll_num = scrapy.Field()  #收藏量
    share_num = scrapy.Field() #分享量

