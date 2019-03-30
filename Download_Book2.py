# -*- coding: utf-8 -*-

"""
@anthor: lbwen
@time: 2019/3/29 - 16:18
"""
import re
import os
import requests
import time
import scrapy
from multiprocessing.dummy import Pool


def get_Urllist(start_url):
    """
    获取每一章链接，存储到一个列表并返回
    :return:每章链接
    """
    html = requests.get(start_url).content.decode('gbk')
    toc_url_list = []
    toc_url = re.findall('href="(\d*.html)"', html, re.S)
    for url in toc_url:
        toc_url_list.append(start_url + url)
    return toc_url_list


def Crawler_save(url):
    try:
        html = requests.get(url, timeout=100)
        html = html.content.decode('gbk')
        selector = scrapy.Selector(text=html)
        chapter_name = selector.xpath("//font[@color='#dc143c']/text()").extract_first()
        text_block = selector.xpath("//p").extract_first()
        text_block = text_block.replace('<br>', ' ')
        book_name = selector.xpath("//td[@width='44%']/strong/a/text()").extract_first()
        os.makedirs(book_name, exist_ok=True)
        # print(' 正在保存 ' + book_name + chapter_name )
        with open(book_name + '/' + chapter_name + '.txt', 'w', encoding="utf-8") as f:
            f.write(text_block.replace(u'\xa0', u' '))
            print(book_name + chapter_name + '已保存成功')
    except Exception as e:
        print(e)


start = time.time()
# url = "https://www.kanunu8.com/book3/6879/"
# url = "https://www.kanunu8.com/book2/10936/"
url = "https://www.kanunu8.com/book2/10923/"
url_list = []
url_list = get_Urllist(url)
pool = Pool(5)
pool.map(Crawler_save, url_list)
end = time.time()
print(f'耗时：{ end - start }')
