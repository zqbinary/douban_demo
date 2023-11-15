import scrapy


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    rank = scrapy.Field()
    subject = scrapy.Field()
    duration = scrapy.Field()
    intro = scrapy.Field()
