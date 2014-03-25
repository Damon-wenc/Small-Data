# -*- coding: utf-8 -*-

import urllib2
import re
import collections

page = 10

url = 'http://movie.douban.com/top250?start=%d&filter=&format='

#title_re = re.compile(r'>\n                            <span class="title">(.+?)</span>')
#country_re = re.compile(r'&nbsp;/&nbsp;(.+?)&nbsp;/&nbsp;')
#year_re = re.compile(r'                            (.+?)&nbsp;/&nbsp;.+?&nbsp;/&nbsp;')
#rank_re = re.compile(r'rating.+?em>(.+?)</em></span>')
#info_re = re.compile(r'title">(.+?)</span>.+?title.+?bd.+?br.+?                            (.+?)&nbsp;/&nbsp;(.+?)&nbsp;/&nbsp;.+?rating.+?<em>(.+?)</em></span>', re.DOTALL)
info_re = re.compile(r'<img alt="(.+?)".+?bd.+?br.+?                            (.+?)&nbsp;/&nbsp;(.+?)&nbsp;/&nbsp;.+?rating.+?<em>(.+?)</em></span>', re.DOTALL)
movies = []
for i in range(0, page):
    page_url = url %(i*25)
    html = urllib2.urlopen(page_url).read()
    #movie = []
    for x in info_re.findall(html):
        tmp = []
        tmp.append(x[0])
        tmp.append(x[1])
        tmp.append(x[2])
        tmp.append(x[3])
        movies.append(tmp)
        #break
    #for x in title_re.findall(html):
        #print x
    #for y in country_re.findall(html):
        #print y
  #  for z in year_re.findall(html):
      #  index += 1
       # movie1.append(z)
        #print z
    #for w in rank_re.findall(html):
        #print w
for item in movies:
    print '%s\t\t\t%s\t\t\t%s\t\t\t%s' %(item[0], item[1], item[2], item[3])

trend = {}
for item in movies:
    if item[1] in trend:
        trend[item[1]] += 1
    else:
        trend[item[1]] = 1

#collections.OrderedDict(sorted(trend.items(), key=lambda t:t[1]))

#for name, address in trend.items():
    #print 'year %s has %d great moives' %(name, address)
year = 1895
while year < 2014:
    if str(year) in trend:
        print 'year %d has %d great moives' %(year, trend[str(year)])
    year = year + 1
    
