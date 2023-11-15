from typing import Iterable

import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from douban_demo.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["https://movie.douban.com/top250"]

    # 方案2，重写 start_requests
    def start_requests(self) -> Iterable[Request]:
        # todo
        for page in range(10):
            yield Request(
                url=f'https://movie.douban.com/top250?start={25 * page}&filter=',
            )

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            movie_item = MovieItem()
            movie_item['title'] = list_item.css('span.title::text').get()
            movie_item['rank'] = list_item.css('span.rating_num::text').get()
            movie_item['subject'] = list_item.css('span.inq::text').get()
            detail_url = list_item.css('div > div.info > div.hd > a::attr(href)').get()
            yield Request(url=detail_url, callback=self.parse_detail, cb_kwargs={'item': movie_item})

    def parse_detail(self, response: HtmlResponse, **kwargs):
        movie_item = kwargs['item']
        sel = Selector(response)
        movie_item['duration'] = sel.css('span[property="v:runtime"]::text').get()
        movie_item['intro'] = sel.css('span[property="v:summary"]::text').get()
        yield movie_item
