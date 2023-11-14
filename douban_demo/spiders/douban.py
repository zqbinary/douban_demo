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
            yield movie_item
            """
        # 方案1
        # 有bug page1 可以叫 https://movie.douban.com/top250
        # 也可以叫 https://movie.douban.com/top250?start=0&filter=
        # 导致多取
        for href in sel.css('div.paginator > a::attr(href)'):
            # 让url 完整
            url = response.urljoin(href.get())
            # 加入请求
            # 框架可以自动去重url
            yield Request(url=url)
"""
