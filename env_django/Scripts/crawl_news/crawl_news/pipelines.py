# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import MySQLdb

class RecruitPipeline(object):
    def open_spider(self, spider):
        conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='news',
        charset='utf8'
        )
        self.conn=conn
        self.cursor = conn.cursor()

    def process_item(self, item, spider):
        sql="insert into news_news(news_title,text,writer_id,style,date,author_id) value (%s,%s,0,%s,now(),0)"
        self.cursor.execute(sql,(item['title'],item['text'],item['type']))
        self.conn.commit()
        print("charuchenggong")
        return item

    def close_spider(self, spider):
        self.conn.close()
'''
import MySQLdb
import json
from urllib.parse import quote
class CrawlNewsPipeline(object):
    
    collection_name = 'crawl_news'
    
    
    def __init__(self,item,spider):
        conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='test',
        )
        
        self.cursor = conn.cursor()
        print("开始插入")
        sql="insert into test(title,text,author,type) value (%s,%s,%s,%s)"
        self.cursor.execute(sql,(item['title'],item['text'],item['author'],item['type']))
        self.conn.commit()
        return item
    
        
        conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='test',
        )
        
        self.cursor = conn.cursor()
        print("开始插入")
        sql="insert into test(title,text,author,type) value (%s,%s,%s,%s)"
        self.cursor.execute(sql,(item['title'],item['text'],item['author'],item['type']))
        self.conn.commit()
        return item
    '''
    

