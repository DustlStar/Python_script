# -*- coding: utf-8 -*-

"""
@anthor: lbwen
@time: 2019/3/27 - 20:26
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
    :param html:目录页源代码
    :return:每章链接
    """
    # head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
    # html = requests.get(start_url, headers=head).content.decode('GB2312')
    html = requests.get(start_url).content.decode('GBK')
    toc_url_list = []
    toc_url = re.findall('href="(\d*.html)"', html, re.S)
    for url in toc_url:
        toc_url_list.append(start_url + url)
    return toc_url_list

def Crawler_save(url):
    # head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'}
    # html = requests.get(url, headers=head).content.decode('GBK')
    try:
        html = requests.get( url , timeout = 60)
        html = html.content.decode('GBK')
    except Exception as e:
        print(e)
    selector = scrapy.Selector(text=html)
    book_name = selector.xpath("//a[@href='index.html']/text()").extract_first()
    chapter_name = selector.xpath("//font[@color='#dc143c']/text()").extract_first()
    text_block = selector.xpath("//p").extract_first()
    text_block = text_block.replace('<br>' , ' ')
    os.makedirs( book_name , exist_ok = True )
    # print(' 正在保存 ' + book_name + chapter_name )
    with open( book_name + '/' + chapter_name + '.txt', 'w') as f:
        f.write(text_block)
        print( book_name + chapter_name + '已保存成功' )


start = time.time()
url = "https://www.kanunu8.com/book3/6879/"
url_list = []
url_list = get_Urllist( url )
# print(url_list[0])
pool = Pool(5)
pool.map( Crawler_save , url_list )
end = time.time()
print( f'耗时：{ end - start }' )
