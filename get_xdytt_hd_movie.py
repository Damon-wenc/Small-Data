#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
这个小程序是为了将一个电影网（小电影天堂）的资源遍历下保存下来，
大致凭借2个依据：1. 1080p，2. 豆瓣评分6.0以上，

'''

import requests
# http://www.xdytt.com/?item=movie
# http://www.xdytt.com/page/1?item=movie
# http://www.xdytt.com/page/2?item=movie
# http://www.xdytt.com/page/3?item=movie
# http://www.xdytt.com/page/165?item=movie

# GLOBAL VARIABLES
web_encoding      = ""
OUT_OF_RANGE_FLAG = "没找到您想要的资源，试试改变搜索条件吧！"
movie_urls        = []


def get_movie_urls():
    global web_encoding, OUT_OF_RANGE_FLAG
    page_index = 1

    while True:
        url = "http://www.xdytt.com/page/%d?item=movie" %page_index
        try:
            r = requests.get(url)

            if web_encoding == "":
                web_encoding = r.encoding

            if OUT_OF_RANGE_FLAG.decode(web_encoding) in r.text:
                print "All movie resources have been found. Operation done."
                break



            page_index += 1
        except:
            print "Failed to get to the web page."
            break


def run():
    get_movie_urls()

if __name__ == "__main__":
    run()