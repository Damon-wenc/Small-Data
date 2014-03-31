# coding: utf8

import re
import urllib2
from collections import OrderedDict

skill_heat = OrderedDict()
skills_array = ['c', 'c++', 'mysql', 'tcp/ip', 'cdn', 'linux', 'javascript', 'html',
                'nosql', 'hadoop', 'spark', 'storm', 'lbs', '经验', '架构', '容灾', '优化',
                '重构', '稳定', '沟通', '压力', '主动', '好学', '分布式', '云计算', '互联网',
                '数据库', '富媒体', '高性能', '高可靠', '高并发', '大数据', '海量数据', '网络处理',
                '存储架构', '数据处理', '精通c++', '安全逻辑', '通信系统', '面向对象', '操作系统',
                '软件工程', '设计模式', '数据结构', '网络安全', '安全漏洞', '网络攻击', '网络并发',
                '数据分析', '逻辑思维', '实时计算', '实时推荐', '分布式计算', '大容量网络',
                '大容量通信', '进程间通讯', '后台业务开发', '计算机基础结构', '互联网应用协议']


for item in skills_array:
    skill_heat[item] = 0


html = urllib2.urlopen('http://hr.tencent.com/position_detail.php?id=15013&keywords=SNG%20%E5%90%8E%E5%8F%B0&tid=0&lid=2218').read()


for name, address in skill_heat.items():
    if name == 'c':
        if html.lower().find('c、') != -1:
            skill_heat[name] += 1
            continue
        if html.lower().find('c/') != -1:
            skill_heat[name] += 1
            continue
    if html.lower().find(name) != -1:
        skill_heat[name] += 1


for name, address in OrderedDict(sorted(skill_heat.items(), key=lambda t: t[1])).items():
    print 'skill: %-20s heat: [%d]' %(name.decode('utf-8'), address)

#un-sorted result
#for name, address in skill_heat.items():
    #print 'skill: %-20s heat: [%d]' %(name.decode('utf-8'), address)

