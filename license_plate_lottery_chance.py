#!/usr/bin/python
# -*- coding: utf-8 -*-

def yaohao_rate():
    Got_It      = 0.005
    Fail_Again  = 1 - Got_It

    for i in range(1, 101):
        print "%3d个月内摇到号的概率是%.3f%%" %(i, (1 - Fail_Again ** i) * 100)
        if i % 12 == 0:
            print "~~~~~~~~~%2d年过去了~~~~~~~~~" %(i/12)

if __name__ == "__main__":
    yaohao_rate()