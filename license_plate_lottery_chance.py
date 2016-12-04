#!/usr/bin/python
# -*- coding: utf-8 -*-

def yaohao_rate():
    Got_It      = 0.0045

    print "\n\n" + "*" * 66
    print "  \t单身狗寂寞摇\t\t\t两个人摇啊摇"
    for i in range(1, 101):
        print "%3d个月内摇到号的概率是%.3f%%" %(i, (1 - (1 - Got_It) ** i) * 100),
        print "\t",
        print "%3d个月内摇到号的概率是%.3f%%" %(i, (1 - (1 - Got_It * 2) ** i) * 100)
        if i % 12 == 0:
            print "~" * 25,
            print "%2d年过去了" %(i/12),
            print "~" * 25

if __name__ == "__main__":
    yaohao_rate()