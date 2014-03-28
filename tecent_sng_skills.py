# coding: utf8

import re
import urllib2

skills = {
    '分布式' : 0,
    '云计算' : 0,
    '互联网' : 0,
    '大容量' : 0,
    'C'      : 0,
    'C++'    : 0
    }

html = urllib2.urlopen('http://hr.tencent.com/position_detail.php?id=15013&keywords=SNG%20%E5%90%8E%E5%8F%B0&tid=0&lid=2218').read()

print html

