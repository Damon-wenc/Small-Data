#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
这个小程序是为了将一个电影网（小电影天堂）的资源遍历下保存下来，
大致凭借2个依据：1. BluRay && 1080p，2. 豆瓣评分6.0以上，

'''

import urllib2
import lxml.html as parser
from gevent import monkey; monkey.patch_socket()
from gevent.pool import Pool
pool = Pool(10)


# GLOBAL VARIABLES
OUT_OF_RANGE_FLAG = "没找到您想要的资源，试试改变搜索条件吧！"
VOTE_ThRESHOLD    = 6.0
g_movie_urls      = []
g_movie_infos     = []


''' get and save all specific movie urls in g_movie_urls[] for further analysis '''
def get_movie_urls():
    global OUT_OF_RANGE_FLAG, g_movie_urls
    page_index = 1

    while True:
        url = "http://www.xdytt.com/page/%d?item=movie" %page_index
        
        try:
            resp = urllib2.urlopen(url)
            htmlSource = resp.read()
        except:
            print "Get web page failed."
            break


        if OUT_OF_RANGE_FLAG in htmlSource:
            print "All movie resources have been found."
            print "There are %d pages and %d movies in total." %(page_index -1, len(g_movie_urls))
            print "Program are doing selection, please wait..."
            break

        try:
            html = parser.document_fromstring(htmlSource)
            urls = html.xpath("//div/div[2]/h1/a/@href")
        except:
            print "Analysis html failed :("

        for url in urls:
            g_movie_urls.append(url)

        #parse next page
        page_index += 1

    return 0

''' save info of target movies to g_movie_infos[] '''
def Analysis_single_movie(url):
    global VOTE_ThRESHOLD, g_movie_infos
    movie_info = []

    try:
        #Due to the bandwitdh, we need a timeout method to 
        resp = urllib2.urlopen(url, timeout = 10000)
        htmlSource = resp.read()
    except:
        print "Analysis url[%s] failed." %url
        return -1

    #Pre check #1: Check if HD("BluRay") resources exists
    if "BluRay" not in htmlSource:
        return 1

    try:
        html = parser.document_fromstring(htmlSource)

        #Pre check #2: skip the vote of movie which is lower than expected
        vote_value = html.xpath("//div[1]/div[2]/div[3]/span[2]/text()")
        if len(vote_value) != 0:
            vote = "%s" %vote_value[0]
        else:
            return 1

        try:
            vote = float(vote)
        except:
            return 1

        if vote < VOTE_ThRESHOLD:
            return 1

        movie_name    = html.xpath("//div/div/div[1]/h1/text()")
        movie_summary = html.xpath("//*[@id='summary']/p/text()")
        titles        = html.xpath("//li[*]/span[1]/a[1]/@title")
        magnets       = html.xpath("//li[*]/span[1]/a[2]/@href")
        sizes         = html.xpath("//li[*]/span[2]/span/text()")

        if len(titles) == 0:
            #In this situation, no magnet resources exsits, skip this movie
            return 1
        if len(movie_summary) == 0:
            movie_summary = []
            movie_summary.append("暂无介绍".decode("utf-8"))

        movie_info.append("%s" %movie_name[0])
        movie_info.append("%.1f" %vote)
        movie_info.append("%s" %movie_summary[0])

        index = 0
        magnet_info = []
        found_title = []

        for title in titles:  
            if "BluRay" in title and "1080P" in title:
                tmp_info = []
                #sometimes magnets are duplicated
                if "%s" %titles[index][5:] not in found_title:
                    found_title.append("%s" %titles[index][5:])
                    tmp_info.append("%s" %titles[index][5:])
                    tmp_info.append("%s" %sizes[index])
                    tmp_info.append("%s" %magnets[index])

                if len(tmp_info):
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
        print "Get movie[%s] info failed, maybe unique html format, please check it manually." %url
        return -1

def Analysis_movies():
    global g_movie_urls

    # Method 1, traditional ways
    # for url in g_movie_urls:
    #     Analysis_single_movie(url)

    # Method 2, 'free-style' spawn, not suitable in this situation
    # jobs = [gevent.spawn(Analysis_single_movie, url) for url in g_movie_urls]
    # gevent.joinall(jobs)

    # Method 3, 'limited-multithread' ways, I'll take this
    pool.map(Analysis_single_movie, g_movie_urls)

    return 0
 
''' save result to HTML file '''
def Save_to_html():
    global g_movie_infos
    print "There are %d movies" %len(g_movie_infos)

    html_head = "<!DOCTYPE html><html><head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"><style type=\"text/css\"> body {margin: 60px;} h1 {font-size: 20px;} b, p,div {font-size: 16px;} </style><title>xdytt.com小电影天堂FHD索引</title></head><body><ol>"
    html_end = "</ol></body></html>"

    try:
        f = open("movie_info.html", "w")
        f.write(html_head)
        for movie in g_movie_infos:
            urls = movie[3]
            f.write("<li><h1>%s</h1><b>%s</b><p>%s</p><ul>" %(movie[0].encode("utf-8"), movie[1].encode("utf-8"), movie[2].encode("utf-8")))
            for url in urls:
                f.write("<div align=left><a href=\"%s\">%s</a></div><div align=right><i>%s</i></div>" 
                    %(url[2].encode("utf-8"), url[0].encode("utf-8"), url[1].encode("utf-8")))
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