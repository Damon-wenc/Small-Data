# Small-Data
In honor of **big data** :D

I've got some 'small data' here. There are several small programs about getting, parsing and analysing info on some websites. As most cases are Chinese sites, I'll describe all my ideas in Chinese~ You may read my code for more information ~\(≧▽≦)/~

## 说明
验证版本: Python V2.7.6

以下的只是简单的几个Python程序, 用以收集一些网站上不严谨的信息, 仅做参考~

### 1. movie_years.py
这个是我从[豆瓣电影TOP250](http://movie.douban.com/top250?start=0&filter=&type=)系列直接抓取下来的, 目的是想查看一下伟大电影的诞生与经济大小年是否有对应关系. 当然这个实现方法明显是不合理的, 一是我的样品库太小了, 二是好多好电影, 特别是近年的, 或许需要时间及机缘才会被社会所接纳对吧(例如大话西游), 所以这里只是仅供一个构思, 主要是练习一下Python对网页的抓取。这第一个爬虫简单得略粗糙了，权当练习吧。

下面是一小段Python输出

> 电影名   年代   地区   评分

> 肖申克的救赎   1994   美国   9.6

> 这个杀手不太冷   1994   法国   9.4

> 阿甘正传   1994   美国   9.4

> ......

> year 1994 has 12 great moives

> year 1995 has 7 great moives

> year 1996 has 4 great moives

> year 1997 has 5 great moives

> year 1998 has 11 great moives

> ......




结果也正是说明这不靠谱╮(╯▽╰)╭

详情请自行阅读及运行movie_years.py

*===update===*

*像这种利用正则表达式来爬网页的，很可能一段时间过后网页规则就变了，爬不下来了。所以要么掌握方法，要么及时行乐。*

### 2.tecent_sng_skills.py
这个..实用性来说肯定是自娱自乐。目的是想找出腾讯SNG部后台招聘所需要哪些技能, 期待针对性学习一下。程序通过遍历所有[SNG+深圳+后台](http://hr.tencent.com/position.php?keywords=SNG+%E5%90%8E%E5%8F%B0&lid=2218&tid=0)招聘网页, 对其中skills_array数组中的关键字（最偷懒且不严谨的做法）进行热度记录, 最后按照热度从低到高的顺序排列出来。努力提高匹配度咯。

下面是一小段Python输出

> ......

> heat [24]	 skill: 优化

> heat [27]	 skill: 架构

> heat [31]	 skill: 沟通

> heat [32]	 skill: c/c++

> heat [34]	 skill: linux

> ......

预知详情如何, 还请亲自运行程序及查看源码


### 3.爬取一个电影网站（感谢[小电影天堂](http://www.xdytt.com))的高清资源
想看好电影，新的电影可以尽可能地在影院观看，贡献票房，老的经典大片就只有在网上，咳咳，搜一下资源了。发现一个很好的网站：[小电影天堂](http://www.xdytt.com)，真心希望它能持久并坚挺，不过它的同行倒是已经有数不清的先烈牺牲了。所以这里打算利用下Python的爬虫，保存一部分电影资源下来，以备后用。

采用的且基于技术主要有:

1. Python 2.7.10(MacOS X 默认)
2. lxml.html 及 xpath
3. gevent 及 pool

由于之前熟悉的是re正则表达式及多线程/进程方式，这次想用不同的技术尝试一下，决定从[知乎](http://www.zhihu.com/question/24590883)的讨论中挑选gevent作高效率的协程，lxml来爬取数据。事实证明确实不错，效率嘛.. 在熟悉了之后是挺高的，就是这学习曲线有点陡，没入门前环境配置、字体编码、文档、博客都是花了不少时间啃的，不过入门后还挺好，效率的确高。

需要注意的点有：

1. 因为是爬别人的网站，所以要注意好心人可能是建站按流量走的，所以尽量不要反复无意义的去爬网页，且爬的时候控制下速度，别丧心病狂地开多线程... 要做到良心限速。
2. 可能是网速限制，或者是网站限制连接数，发现在用gevent爬网页在同时“线程数”比较多的时候，会报gevent的诡异的错误。由于spawn没有连接数限制，所以切换到Pool，来限制下连接数。在家里测试6M网络最多开40路同时就能跑满。
3. 同时在打开网页调用urllib2时也要相应的增加超时时间，协程多了相对有点慢。

随脚本一起上传了结果文档：movie_info.html(*另存为后用浏览器打开格式就清晰了*)，发现速度还不错，从3000多个链接爬675个6.0分以上的1080P电影下来一共花费10分钟多一点，蹲个坑就搞定了... 而且是在限速了的情况下。攒着慢慢看 XD

### 4.爬取另一个高清网站
发现了另一个高清网站，挺好的[高清网](http://gaoqing.la)，打算故技重施保存下... 以为是个简单的修改下爬取规则就好了，结果发现了下面的问题：

1. [高清网](http://gaoqing.la)限制了爬虫的获取，所以Google了下，需要增加一个表头来模拟浏览器登录，解决了这个问题。
2. 呃...... 蛋疼的事儿来了，也不知道是故意还是无意的，这网站的网页结构真是千变万化，各种规则随手拈来，新旧网页结构也不太一样，所以过滤起来真是麻烦，最后还是有点问题，已经尽力了。留个教训吧，以后如果网站规则太难以捉摸，还是量力而行比较好。。。

技术没有什么变化，所以参照上一篇功能，就不写了哈。

结果也上传了：gaoqingla_info.html，同理，在GitHub打开怪怪的，下载后排版就正常了。

