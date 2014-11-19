# Small-Data
In honor of **big data** :D

I've just got some 'small data' here. There are several small programs about getting, parsing and analysing info on some websites. As most cases are Chinese sites, I'll describe my ideas in Chinese~ You may read my code for more information ~\(≧▽≦)/~

## 说明
验证版本: Python V2.7.6

以下的只是简单的几个Python程序, 用以收集一些网站上我突发奇想的不严谨的信息, 仅做参考~

### 1. movie_years.py
这个是我从[豆瓣电影TOP250](http://movie.douban.com/top250?start=0&filter=&type=)系列直接抓取下来的, 目的是想查看一下伟大电影的诞生与经济大小年是否有对应关系. 当然这个实现方法明显是不合理的, 一是我的样品库太小了, 二是好多好电影, 特别是近年的, 或许需要时间及机缘才会被社会所接纳对吧(例如大话西游), 所以这里只是仅供一个构思, 主要是练习一下Python对网页的抓取.

下面是一小段Python输出

> ......

> year 1994 has 12 great moives

> year 1995 has 7 great moives

> year 1996 has 4 great moives

> year 1997 has 5 great moives

> year 1998 has 11 great moives

> ......

结果也正是说明这不靠谱╮(╯▽╰)╭, 或许可以换个思路? or 再改善下?

详情请自行阅读及运行movie_years.py

### 2.tecent_sng_skills.py
这个.. 是想找出腾讯SNG部后台招聘所需要哪些技能, 期待针对性学习一下吧。程序通过遍历所有[SNG+深圳+后台](http://hr.tencent.com/position.php?keywords=SNG+%E5%90%8E%E5%8F%B0&lid=2218&tid=0)招聘网页, 对其中skills_array数组中的关键字（挺2的...就这法子最简单）进行热度记录, 最后按照热度从低到高的顺序排列出来,. 哈哈, 提高匹配度^_^o~！

下面是一小段Python输出

> ......

> skill: 大容量网络			 heat [9]

> skill: tcp/ip			 heat [10]

> skill: 数据结构			 heat [11]

> skill: 网络安全			 heat [11]

> skill: c/c++			 heat [21]

> ......

预知详情如何, 还请亲自运行程序及查看源码