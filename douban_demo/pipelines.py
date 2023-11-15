# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

import openpyxl
import pymysql


class DbPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',
                                    user='root',
                                    password='root',
                                    database='heima')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.data = []

    # 我建议这里用sqlalchemy框架
    def process_item(self, item, spider):
        title = item.get('title', '')
        rank = item.get('rank', '')
        subject = item.get('subject', '')
        intro = item.get('intro', '')
        duration = item.get('duration', '')
        self.data.append((title, rank, subject, duration, intro))
        if 10 == len(self.data):
            self._write_to_db()
        return item

    def _write_to_db(self):
        # 准备一个容器比如10条，然后插入一次
        if not len(self.data):
            return
        self.cursor.executemany(
            'insert into movie (title,rating,subject,duration,intro) values (%s,%s,%s,%s,%s)',
            self.data
        )
        # 这里后后面
        self.conn.commit()
        self.data.clear()

    def close_spider(self, spider):
        self._write_to_db()
        self.conn.close()


class ExcelPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.append(('标题', '评分', '主题'))

    def close_spider(self, spider):
        self.wb.save("data/电影数据.xlsx")

    def process_item(self, item, spider):
        title = item.get('title', '')
        rank = item.get('rank', '')
        subject = item.get('subject', '')
        self.ws.append((title, rank, subject))
        return item
