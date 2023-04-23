#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pprint import pprint
from requests_html import HTML
import requests
import re
import urllib
from lxml import etree
from multiprocessing import Process, Pool
import time
import json
import CrawlerPTT as PTT
from functools import partial
import getopt
import sys


# In[3]:


start = 0
end = 0
Domain = "https://www.ptt.cc/bbs/"
club = ""
thread_num = 1

def multi_parsing(start,end):
    bigMap = []
    with Pool(thread_num) as pool:

        startTime = time.time()

        result = pool.map(partial(PTT.parsing,club = club), range(start,end))

        endTime = time.time()
        print('執行一共花了 %f 秒' % (endTime - startTime))

    for articles in result:
        for content in articles:
            bigMap.append(content)

    with open(club + " "+ str(start) + "-"+ str(end) +".json","w") as f:
        json.dump(bigMap,f,indent=4)

    f.close


# In[ ]:


if __name__ == '__main__':
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:],
            '',
            ['start=','end=','club=','thread='])
    except getopt.GetoptError as err:
        print('ERROR:', err)
        sys.exit(1)
    
    for opt, arg in options:
        if opt == '--start':
            start = int(arg)
        elif opt == '--end':
            end = int(arg)
        elif opt == '--club':
            club = arg
        elif opt == '--thread':
            thread_num = int(arg)
            
    print('開始使爬蟲 ' + club + ' 版')
    print('從 ' + str(start) + ' 到 ' + str(end) + ' 頁')
    print('一共開啟 '+ str(thread_num) +' 線程')
    print('========================')
            
    for i in range(start, end, 100):
        flag = True
        while flag:
            try:
                multi_parsing(i,i+100)
                flag = False
            except:
                print("連接錯誤 30 秒 CD 中")
                time.sleep(30)


# In[ ]:




