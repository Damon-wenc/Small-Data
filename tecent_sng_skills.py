# coding: utf8

import re
import urllib2
from collections import OrderedDict


######## construct skill keywords Dict ########
skill_heat = OrderedDict()
skills_array = ['c/c++', 'python', 'mysql', 'tcp/ip', 'cdn', 'linux', 'nosql', 
                'hadoop', 'spark', 'storm', 'lbs', '经验', '架构', '容灾', '优化', '脚本', 
                '重构', '稳定', '沟通', '压力', '主动', '好学', '分布式', '云计算', '自动化', '虚拟化'
                '数据库', '富媒体', '高性能', '高可靠', '高并发', '大数据', '海量数据', '网络处理', 
                '存储架构', '数据处理', '精通c++', '安全逻辑', '通信系统', '面向对象', '操作系统', '索引系统', 
                '软件工程', '设计模式', '数据结构', '网络安全', '安全漏洞', '网络攻击', '网络并发',
                '数据分析', '逻辑思维', '实时计算', '实时推荐', '广告变现', '广告后台', '分布式计算', '大容量网络',
                '大容量通信', '进程间通讯', '后台业务开发', '互联网业务', '无线互联网', 
                '计算机基础结构', '互联网应用协议']
for item in skills_array:
    skill_heat[item] = 0


######## parse web(url) and update keywords heat in Dict ########
def web_parse(url):
    html = urllib2.urlopen(url).read()

    for name, address in skill_heat.items():
        if name == 'c/c++':
            if html.lower().find('c、c++') != -1:
                skill_heat[name] += 1
                continue
            if html.lower().find('c/c++') != -1:
                skill_heat[name] += 1
                continue
        if html.lower().find(name) != -1:
            skill_heat[name] += 1


######## main function ########
def get_info():
    start_url = 'http://hr.tencent.com/position.php?keywords=SNG+%E5%90%8E%E5%8F%B0&lid=2218&tid=0'

    position_num_re = re.compile(r'class="lightblue total">(\d+?)</span>个职位')
    position_url_re = re.compile(r'<a target="_blank" href="(.+?)">SNG')
    position_num = 0
    position_url = ''
    html = urllib2.urlopen(start_url).read()
    for x in position_num_re.findall(html):
        position_num = int(x)   #find how many positions are avaliable
        print '%d SNG positions have been found. Please wait a little while...\n\n' %position_num

    base_url = 'http://hr.tencent.com/position.php?keywords=SNG%s后台&lid=2218&tid=0&start=%d#a'
    index = 0
    while index <= (position_num / 10): #each page got 10 positions at most
        target_url = base_url %('%20', index * 10) #get position index page
        html = urllib2.urlopen(target_url).read()
        for y in position_url_re.findall(html):
            web_parse('http://hr.tencent.com/' + y)
        index += 1
    
    display_result()


######## show keywords heat ########
def display_result():
    print 'skills heat are as below:\n'
    #sorted result
    for name, address in OrderedDict(sorted(skill_heat.items(), key=lambda t: t[1])).items():
        print 'skill: %s\t\t\t heat [%d]' %(name.decode('utf-8'), address)

    #un-sorted result
    #for name, address in skill_heat.items():
    #    print 'skill: %-20s heat: [%d]' %(name.decode('utf-8'), address)

    print '为了高匹配^_^o~ 努力！'


if __name__ == '__main__':
    get_info()
