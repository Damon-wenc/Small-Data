#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
这个小程序是为了将一个电影网（小电影天堂）的资源遍历下保存下来，
大致凭借2个依据：1. BluRay && 1080p，2. 豆瓣评分6.0以上，

'''

import urllib2
import lxml.html as parser
from gevent import monkey; monkey.patch_socket()
import gevent


# GLOBAL VARIABLES
OUT_OF_RANGE_FLAG = "没找到您想要的资源，试试改变搜索条件吧！"
VOTE_ThRESHOLD    = 6.0
g_movie_urls      = []
g_movie_infos     = []



def get_movie_urls():
    global OUT_OF_RANGE_FLAG, g_movie_urls
    page_index = 1

    while True:
        url = "http://www.xdytt.com/page/%d?item=movie" %page_index
        
        try:
            sock = urllib2.urlopen(url)
            htmlSource = sock.read()
            sock.close()
        except:
            print "Get web page failed."
            sock.close()
            break


        if OUT_OF_RANGE_FLAG in htmlSource:
            print "All movie resources have been found. Operation done."
            break

        try:
            html = parser.document_fromstring(htmlSource)
            urls = html.xpath("//div/div[2]/h1/a/@href")
        except:
            print "Analysis html failed :("

        for url in urls:
            g_movie_urls.append(url)
        
        if page_index >= 5:
            break

        #parse next page
        page_index += 1

    return 0

def Analysis_single_movie(url):
    global VOTE_ThRESHOLD, g_movie_infos
    movie_info = []

    try:
        sock = urllib2.urlopen(url)
        htmlSource = sock.read()
        sock.close()
    except:
        print "Get web page failed."
        sock.close()
        return -1

    try:
        html = parser.document_fromstring(htmlSource)

        #Pre check #1: skip the vote of movie which is lower than expected
        vote_value = html.xpath("//div[1]/div[2]/div[3]/span[2]/text()")
        vote = "%s" %vote_value[0]

        try:
            vote = float(vote)
        except:
            return 1

        if vote < VOTE_ThRESHOLD:
            return 1

        #Pre check #2: Check if HD("BluRay") resources exists
        if "BluRay" not in htmlSource:
            return 1

        movie_name    = html.xpath("//div/div/div[1]/h1/text()")
        movie_summary = html.xpath("//*[@id='summary']/p/text()")
        titles        = html.xpath("//li[*]/span[1]/a[1]/@title")
        magnets       = html.xpath("//li[*]/span[1]/a[2]/@href")
        sizes         = html.xpath("//li[*]/span[2]/span/text()")
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
        print "Get movie info failed."
        return -1

def Analysis_movies():
    global g_movie_urls, g_movie_infos
    #g_movie_urls = ["http://www.xdytt.com/subject/12101.html", "http://www.xdytt.com/subject/11751.html"]

    #for url in g_movie_urls:
        #Analysis_single_movie(url)

    jobs = [gevent.spawn(Analysis_single_movie, url) for url in g_movie_urls]
    gevent.joinall(jobs, timeout = 1000)

    return 0
 
def Save_to_html():
    global g_movie_infos
    print g_movie_infos.__sizeof__()

    html_head = "<!DOCTYPE html><html><head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"><title>xdytt.com小电影天堂FHD索引</title></head><body><ol>"
    html_end = "</ol></body></html>"

    try:
        f = open("movie_info.html", "w")
        f.write(html_head)
        for movie in g_movie_infos:
            urls = movie[3]
            f.write("<li><h4>%s</h4><b>%s</b><p><small>%s</small></p><ul>" %(movie[0].encode("utf-8"), movie[1].encode("utf-8"), movie[2].encode("utf-8")))
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
    #Analysis_single_movie("http://www.xdytt.com/subject/12101.html")
    Save_to_html()

if __name__ == "__main__":
    from timeit import Timer
    t = Timer("run()", "from __main__ import run")
    print "runtine time of script is %.1f seconds" %t.timeit(1)
    #run()