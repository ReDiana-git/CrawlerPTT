#!/usr/bin/env python
# coding: utf-8

# In[1]:


# ! pip install requests requests_html
# ! pip install lxml


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


# In[3]:


# 因為拿到的網址不是完整的，所以把它轉成完整的網址

def fullUrl(url):
    domain = 'https://www.ptt.cc/bbs'
    fetch_url = urllib.parse.urljoin(domain, url)
    return fetch_url


# In[4]:


def fetch(url):
    response = requests.get(url)
    response = requests.get(url, cookies={'over18': '1'})  # 一直向 server 回答滿 18 歲了 !
    return response


# In[5]:


def parse_article_entries(doc):
    html = HTML(html=doc)
    post_entries = html.find('div.r-ent')
    return post_entries


# In[6]:


# 爬取說頁面上有哪些文章
def parse_article_meta(ent):
    ''' Step-3 (revised): parse the metadata in article entry '''
    # 基本要素都還在
    meta = {
        'title': ent.find('div.title', first=True).text,
        'push': ent.find('div.nrec', first=True).text,
        'date': ent.find('div.date', first=True).text,
    }

    try:
        # 正常狀況取得資料
        meta['author'] = ent.find('div.author', first=True).text
        meta['link'] = ent.find('div.title > a', first=True).attrs['href']
    except AttributeError:
        # 文章已被刪除的狀況
        deleteMeta = { 'title': '文章已被刪除' }
        return deleteMeta

    return meta


# In[7]:


# 讀取到的字串時間轉換成邊準時間

def month_formate(month):
    
    if month == "Jan":
        return 1
    elif month == "Feb":
        return 2
    elif month == "Mar":
        return 3
    elif month == "Apr":
        return 4
    elif month == "May":
        return 5
    elif month == "Jun":
        return 6
    elif month == "Jul":
        return 7
    elif month == "Aug":
        return 8
    elif month == "Sep":
        return 9
    elif month == "Oct":
        return 10
    elif month == "Nov":
        return 11
    elif month == "Dec":
        return 12


def article_time_formate(timeValue):
    
    timeValue = timeValue.replace(':',' ')
    timeValue = timeValue.split(' ')
    timeSet = {
        'year' : timeValue[6],
        'month' : month_formate(timeValue[1]),
        'date' : timeValue[2],
        'hour' : timeValue[3],
        'minute' : timeValue[4]
    }
    return timeSet


# In[8]:


# 讀取文章日期

def parse_article_time(doc):
    
    html = HTML(html=doc)
    metaline = html.find('div.article-metaline')
    targetMetaline = metaline[2]
    timeValue = targetMetaline.find('span.article-meta-value', first=True).text
    formatedTimeValue = article_time_formate(timeValue)
    
    return formatedTimeValue


# In[9]:


# 讀取文章內容

def parse_article_content(doc):
    
    html = HTML(html=doc)
    metaline = html.find('div[id="main-content"]', first=True)

    
    # 過濾作者、文章標題、時間等元素
    element = metaline.find('.article-metaline')
    for ele in element:
        ele.element.drop_tree()
    
    element = metaline.find('.article-metaline-right')
    for ele in element:
        ele.element.drop_tree()
        
    element = metaline.find('.push')
    for ele in element:
        ele.element.drop_tree()
        
    element = metaline.find('span')
    element[-1].element.drop_tree()
    element[-2].element.drop_tree()
    
    contentValue = ''.join(metaline.text)
    
    return contentValue


# In[10]:


# 讀取文章的推文

def parse_article_push(doc):
    
    html = HTML(html=doc)
    push = html.find('div[class="push"]')
    pushArr = []
    
    for pu in push:
        pushMeta ={
            'pushUser' : pu.find(".push-userid", first=True).text,
            'pushContent' : pu.find(".push-content", first=True).text[2:]
        }
        pushArr.append(pushMeta)
        
    return pushArr
#     pprint(pushArr)
    
# url = 'https://www.ptt.cc/bbs/movie/M.1681964687.A.CE2.html'
# resp = fetch(url)
# parse_article_push(resp.text)
    


# In[11]:


# 單獨爬取某的頁面

def parse_single_article(meta):
    print(meta['title'])
    if meta['title'] == '文章已被刪除':
        return meta
    resp = fetch(fullUrl(meta['link']))
    try:
        meta['time'] = parse_article_time(resp.text)
        meta['content'] = parse_article_content(resp.text)
        meta['push'] = parse_article_push(resp.text)
    except:
        deleteMeta = { 'title': '文章已被刪除' }
        return deleteMeta
    return meta
    


# In[12]:


def parse_page_article(url):
    # url = 'https://www.ptt.cc/bbs/movie/index.html'
    resp = fetch(url)  # step-1
    post_entries = parse_article_entries(resp.text)  # step-2
    pageContent = []

    for entry in post_entries:
        meta = parse_article_meta(entry)
        pageContent.append(parse_single_article(meta))
        
    return pageContent



# In[13]:


Domain = "https://www.ptt.cc/bbs/"
# club = "Gossiping"
# start = 39200
# end = 39250

def parsing(num,club):
    url = Domain + club +"/index" + str(num) + ".html"
    result = parse_page_article(url)
    
    return result




