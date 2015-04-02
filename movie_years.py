# -*- coding: utf-8 -*-

import urllib2
import re
import collections

page = 10

url = 'http://movie.douban.com/top250?start=%d&filter=&format='

info_re = re.compile(r'<img alt="(.+?)".+?bd.+?br.+?                            (.+?)&nbsp;/&nbsp;(.+?)&nbsp;/&nbsp;.+?rating.+?<em>(.+?)</em></span>', re.DOTALL)
movies = []
for i in range(0, page):
    page_url = url %(i*25)
    html = urllib2.urlopen(page_url).read()
    for x in info_re.findall(html):
        tmp = []
        tmp.append(x[0])
        tmp.append(x[1])
        tmp.append(x[2])
        tmp.append(x[3])
        movies.append(tmp)
        
for item in movies:
    print '%s\t\t\t%s\t\t\t%s\t\t\t%s' %(item[0].decode('utf-8'), item[1].decode('utf-8'), item[2].decode('utf-8'), item[3].decode('utf-8'))

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
    
