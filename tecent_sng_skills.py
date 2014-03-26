# coding: utf8

import re
import urllib2

html = urllib2.urlopen('http://hr.tencent.com/position_detail.php?id=15013&keywords=SNG%20%E5%90%8E%E5%8F%B0&tid=0&lid=2218').read()
r = re.compile(r'熟练掌握(.+?)编程语言')

for x in r.findall(html):
    print x
