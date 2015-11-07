#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
这个小程序是为了将一个电影网（高清网 http://gaoqing.la/）的1080P资源遍历下保存下来，
'''

import urllib2
import lxml.html as parser
from gevent import monkey; monkey.patch_socket()
from gevent.pool import Pool
pool = Pool(2)

#网站禁止爬虫，需加一个表头伪装浏览器头
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}


# GLOBAL VARIABLES
g_movie_urls      = []
g_movie_infos     = []



def get_movie_urls():
    global OUT_OF_RANGE_FLAG, g_movie_urls
    page_index = 1

    while True:
        url = "http://gaoqing.la/1080p/page/%d" %page_index
        req = urllib2.Request(url, headers = HEADERS)
        try:
            resp = urllib2.urlopen(req)
            htmlSource = resp.read()
        except:
            print "All movie resources have been found."
            print "There are %d pages and %d movies in total." %(page_index -1, len(g_movie_urls))
            print "Program are doing selection, please wait..."
            return 0

        try:
            html = parser.document_fromstring(htmlSource)
            urls = html.xpath("//div/div/h2/a/@href")
        except:
            print "Analysis html failed :("

        for url in urls:
            g_movie_urls.append(url)

        #parse next page
        page_index += 1

    return 0

def Analysis_single_movie(url):
    global VOTE_ThRESHOLD, g_movie_infos
    movie_info = []

    try:
        #Due to the bandwitdh, we need a timeout method to 
        req = urllib2.Request(url, headers = HEADERS)
        resp = urllib2.urlopen(req, timeout = 100000)
        htmlSource = resp.read()
    except:
        print "Analysis url[%s] failed." %url
        return -1

    try:
        html = parser.document_fromstring(htmlSource)

        #Pre check #2: skip the vote of movie which is lower than expected
        #some movies don't have a vote number
        vote_value    = html.xpath("//p[*]/span[10]/text()")
        if len(vote_value) == 0:
            vote_value    = ["none", ]
        movie_name    = html.xpath("//div[1]/h1/text()")
        #some movies don't have a douban link
        movie_link    = html.xpath("//p[*]/span[11]/text()")
        if len(movie_link) == 0:
            movie_link    = ["none", ]
        titles        = html.xpath("//*[@id='post_content']/p[*]//a//text()")
        magnets       = html.xpath("//*[@id='post_content']/p[*]//a/@href")
        movie_info.append("%s" %movie_name[0])
        movie_info.append("%s" %vote_value[0])
        index = 0
        magnet_info = []

        for magnet in magnets:
            #print index, titles[index], magnets[index]
            if True:#"BluRay" in title and "1080p" in title:
                tmp_info = []

                #sometimes titles are split into two parts)
                if len(titles) == len(magnets) * 2:
                    tmp_info.append("%s%s" %(titles[index * 2], titles[index * 2 + 1]))
                    tmp_info.append("%s" %magnets[index])
                else:
                    tmp_info.append("%s" %titles[index])
                    tmp_info.append("%s" %magnets[index])

                if len(tmp_info) > 0 and "BluRay" in tmp_info[0] and "1080p" in tmp_info[0]:
                    magnet_info.append(tmp_info)

            index += 1

        if len(magnet_info):
            movie_info.append(magnet_info)
        else:   #sometimes there are only 720P BluRay resources, skip this one
            return 1

        if len(movie_info):
            g_movie_infos.append(movie_info)
        
        return 0

    except:
        print "Get movie[%s] info failed, maybe unique html format OR resources are failed, please check it manually." %url
        return -1

def Analysis_movies():
    global g_movie_urls

    #g_movie_urls = ["http://gaoqing.la/inside-out.html", "http://gaoqing.la/knock-knock.html"]
    #g_movie_urls = ["http://gaoqing.la/jurassic-world.html"]
    #g_movie_urls = ["http://gaoqing.la/vendetta-2.html"]

    pool.map(Analysis_single_movie, g_movie_urls)

    return 0
 
def Save_to_html():
    global g_movie_infos
    print "There are %d movies" %len(g_movie_infos)

    html_head = "<!DOCTYPE html><html><head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"><style type=\"text/css\"> body {margin: 60px;} h1 {font-size: 20px;} b, p,div {font-size: 16px;} </style><title>gaoqingla网1080P索引</title></head><body><ol>"
    html_end = "</ol></body></html>"

    try:
        f = open("gaoqingla_info.html", "w")
        f.write(html_head)
        for movie in g_movie_infos:
            urls = movie[2]
            f.write("<li><h1>%s</h1><b>%s</b><ul>" %(movie[0].encode("utf-8"), movie[1].encode("utf-8")))
            for url in urls:
                f.write("<div align=left><a href=\"%s\">%s</a></div>" 
                    %(url[1].encode("utf-8"), url[0].encode("utf-8")))
            f.write("</ul></li>")
        f.write(html_end)

    finally:
        f.close()

def run():
    get_movie_urls()
    Analysis_movies()
    Save_to_html()

if __name__ == "__main__":
    from timeit import Timer
    t = Timer("run()", "from __main__ import run")
    print "runtine time of script is %.1f seconds" %t.timeit(1)