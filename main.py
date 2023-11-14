from scrapy import cmdline


def main():
    # cmdline.execute("scrapy crawl douban -o result2.csv".split())
    #pipeline
    cmdline.execute("scrapy crawl douban".split())
    # cmdline.execute("scrapy crawl douban result1.csv".split())


if __name__ == '__main__':
    main()
