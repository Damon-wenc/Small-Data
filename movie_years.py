# -*- coding: utf-8 -*-

import urllib2
import re
import collections

page = 10

url = 'http://movie.douban.com/top250?start=%d&filter=&format='

# this regulation was failed. douban changed it's web layout.
#info_re = re.compile(r'<img alt="(.+?)".+?bd.+?br.+?                            (.+?)&nbsp;/&nbsp;(.+?)&nbsp;/&nbsp;.+?rating.+?<em>(.+?)</em></span>', re.DOTALL)

# 4.20.2016 
info_re = re.compile(r'img alt="(.+?)" src.+?<div class="bd">.+?(\d+)&nbsp;/&nbsp;(.+?)&nbsp;/&nbsp;.+?<span class="rating_num" property="v:average">(.+?)</span>', re.DOTALL)

'''
parse 10 pages of movie brief introduction
'''
movies = []
for i in range(0, page):
    print "Please wait..."
    page_url = url %(i*25)
    html = urllib2.urlopen(page_url).read()
    for x in info_re.findall(html):
        tmp = []
        tmp.append(x[0])
        tmp.append(x[1])
        tmp.append(x[2])
        tmp.append(x[3])
        movies.append(tmp)

print "%-40s\t\t%-10s\t%-30s\t\t%-10s" %("电影名", "年代", "地区", "评分")
for item in movies:
    print '%-40s\t%-10s\t%-30s\t%-10s' %(item[0].decode('utf-8'), item[1].decode('utf-8'), item[2].decode('utf-8'), item[3].decode('utf-8'))

'''
accounting and print the result
'''
trend = {}
for item in movies:
    if item[1] in trend:
        trend[item[1]] += 1
    else:
        trend[item[1]] = 1

year = 1895
while year < 2014:
    if str(year) in trend:
        print 'year %d has %d great moives' %(year, trend[str(year)])
    year = year + 1
print 
    
