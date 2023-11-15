# douban movie top 250

通过豆瓣电影top250，学习 scrapy demo

# install

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

mkdir data # data 是数据目录

# 功能

爬豆瓣250电影名单，分页下载。item的数据部分列表就有，部分要到详情页。
下载目标，有通过命令行的方案，-o 到 json,csv,txt。或通过 pipeline, 下载到数据库，excel。

