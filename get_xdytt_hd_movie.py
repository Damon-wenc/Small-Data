#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
这个小程序是为了将一个电影网（小电影天堂）的资源遍历下保存下来，
大致凭借2个依据：1. 1080p，2. 豆瓣评分6.0以上，

'''

import urllib2
import lxml.html as parser


# GLOBAL VARIABLES
OUT_OF_RANGE_FLAG = "没找到您想要的资源，试试改变搜索条件吧！"
movie_urls        = []
VOTE_ThRESHOLD    = 6.0


def get_movie_urls():
    global OUT_OF_RANGE_FLAG, movie_urls
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
            movie_urls.append(url)
        break

        #parse next page
        page_index += 1

def Analysis_single_movie(url):
    global VOTE_ThRESHOLD

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
        vote = float(vote)
        if vote < VOTE_ThRESHOLD:
            return 1

        #Pre check #2: Check if HD("BluRay") resources exists
        if "BluRay" not in htmlSource:
            return 1

        titles = html.xpath("//li[*]/span[1]/a[1]/@title")
        magnets= html.xpath("//li[*]/span[1]/a[2]/@href")
        sizes  = html.xpath("//li[*]/span[2]/span/text()")
        index = 0
        for title in titles:
            if "BluRay" in title and "1080P" in title:
                print titles[index]
                print sizes[index]
                print magnets[index]
            index += 1



    except:
        print "Get vote of movie failed."
        return -1




def run():
    #get_movie_urls()
    #Analysis_single_movie("http://www.xdytt.com/subject/12101.html")
    Analysis_single_movie("http://www.xdytt.com/subject/11751.html")

if __name__ == "__main__":
    run()