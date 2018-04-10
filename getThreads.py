#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
##Created on Thu Jan 18 19:21:28 2018

##@author: Oskar & Cloobert
"""
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import requests
import re
import datetime
import pymongo


def get_html(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')

def getThread(html):
  threads_data = {}
  try:
      #threads_data['ThreadID'] = re.search('t(\d+)',html.find('a',class_="hover-toggle thread-goto-lastpost visible-xs-inline-block")['href'])[0]
      ThreadID = re.search('t(\d+)',html.find('a',class_="hover-toggle thread-goto-lastpost visible-xs-inline-block")['href'])[0]
      serc = 'thread_title_' + ThreadID
      threads_data['ThreadTitles'] = html.find('a', id=serc).text
      threads_data['CreatorID'] = re.search('u(\d+)', str(html))[0]
      threads_data['NumOfViews'] = re.search('(\d+) visningar', str(html))[0]
      threads_data['NumOfAnswers'] = re.search('(\d+) svar', str(html))[0]
  except TypeError:
      print('error')
  except AttributeError:
      print('AttributeError ',serc)
  return threads_data,ThreadID


#reads a html page and returns a list with all posts
def get_posts(page,url):
    return page.select("div.post")

#reads one post and extracts the data and returns a dic
def get_post_data(post,url):
    post_data={}
    try:
        #post_data['PostID'] = re.search('[0-9]+',post.select('div.post_message')[0]['id'])[0]
        PostID = re.search('[0-9]+',post.select('div.post_message')[0]['id'])[0]
        post_data['Message'] = post.select('div.post_message')[0].get_text().strip().replace('\n',' ').replace('  ',' ').replace('\t',' ')
        post_data['Time'] = re.search('[0-9]{2}:[0-9]{2}',post.select('div.post-heading')[0].get_text())[0]
        post_data['Date'] = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}',post.select('div.post-heading')[0].get_text())[0]
        #post_data['ThreadID'] = re.search('t[0-9]+',url)[0]
        post_data['AuthorID'] = re.search('u[0-9]+',post.find('a',class_="post-user-username dropdown-toggle")['href'])[0]

    except TypeError:
        print(f'TypeError on {url}')

    except AttributeError:
        print(f'AttributeError on {url}')

    return post_data,PostID

#Reads all posts in one page and returns a list containing a dictionariy for each post
def read_posts(posts,url):
    dic={}
    for post in posts:
        Data,PostID = get_post_data(post,url)
        dic[PostID] = Data
    return dic

#Gets the number of pages
def get_post_pages(url):
    if get_html(url).find('span', class_='input-page-jump'):
        return int(get_html(url).find('span', class_='input-page-jump')['data-total-pages'])
    else:
        return int(1)

def get_thread_posts(threadUrl):
    postPages = get_post_pages(threadUrl)
    posts = {}

    for i in range(1, postPages+1) :
        new_url = threadUrl + 'p' + str(i)
        posts = dict(**posts,read_posts(get_posts(get_html(new_url),new_url),new_url)
        if i%100 == 0:
            print(f'{i} of {postPages} in thread {threadUrl} pages read')

    apa
    return apa

def put_in_cage(dict, collectionName):

    client = pymongo.MongoClient('mongodb://< ip-adress >:< port >/')
    db = client.threads_database
    collection = db.create_collection(collectionName)
    result = collection.posts.insert_many(dict)

    check = result.count() % len(dict)



    return "det gick bra " eller "det gick jättedåligt"

def release_fart():



def Main():
    #Hämta trådar --> Skriv i dict
    url = 'https://www.flashback.org/'
    if url[len(url)-1] == '/':
            url = url[0:len(url)-1]
    # threads url
    url_threads = url + '/f13'


    #Hämta data för varje tråd --> Skriv i dict

    #Ange hur många sidor som skall crawlas
    #pageNum = np.arange(1,423)
    pageNum = np.arange(110,111)
    threadsLst = []
    # creating empty dict for threads
    threadsDic = {}
    for i in pageNum:
      UrlToRequest = str(url_threads + 'p' + str(i))
      print(UrlToRequest)
      RequestedPage = get_html(UrlToRequest)
      htmlFiltered = RequestedPage.select('#threadslist > tbody > tr')
      for j in range(1, len(htmlFiltered)):
        threadData,ThreadID = getThread(htmlFiltered[j])
        threadsDic[ThreadID] = threadData
        #print(threadsDic)

        #Explore the Posts in ThreadID
        init_url = url + '/' + ThreadID
        max_pages=get_post_pages(init_url)
        #print(f'Max Pages in {init_url} is {max_pages}')
        #if len(lst)-counter > 25:
            #print(f'{len(lst)} posts saved')
            #counter = len(lst)
    #for p in range(0, 2):
        postsDic = {}
        for i in range(1,max_pages+1):
            new_url=init_url + 'p' + str(i)
            postsDic[ThreadID]={**postsDic,**read_posts(get_posts(get_html(new_url),new_url),new_url)}
            #lst=lst+read_posts(get_posts(get_html(new_url),new_url),new_url)
            #if i%5 == 0:
                #print(f'{i} of {max_pages} in thread {p} pages read')
        threadsDic[ThreadID]["Posts"] = postsDic

        #print(threadsDic)

Main()

# print(np.arange(110,111))
#
# turl = 'https://www.flashback.org/f13'
# page =  get_html(turl)
# threads = getThread(page)
# threadID = re.search('t(\d+)',page.find('a',class_="hover-toggle thread-goto-lastpost visible-xs-inline-block")['href'])[0]
#
#
# print(threadID)
#
# posts=get_posts(page,turl)
# post_data = read_posts(posts,turl)
# read_posts(get_posts(get_html(new_url),new_url),new_url)
#
# print(post_data)
#
#
# #base url
# url = 'https://www.flashback.org/'
# if url[len(url)-1] == '/':
#         url = url[0:len(url)-1]
#
# # threads url
# url_threads = url + '/f13'
#
# # creating empty dict for threads
# threads = {}
# filename = f'{str(datetime.datetime.today().date())}_{p}.csv'
# pd.DataFrame(lst).to_csv(f'~\Documents\PythonPath\TextAnalysisOnFlashback\SavedData\{filename}')
# print(f'Saved file {filename}')
#
# #threadsLst.append(getThread(htmlFiltered[j]))
# if j%25 == 0:
# print(f'{j} of {len(threadsLst)} threads collected')
#
# url = 'https://www.flashback.org/t2266379'
#
# for p in threadIDs:
#     init_url = url + '/' + p
#     max_pages=get_post_pages(init_url)
#     print(f'Max Pages in {init_url} is {max_pages}')
#     if len(lst)-counter > 25:
#         print(f'{len(lst)} posts saved')
#         counter = len(lst)
#
#     save_posts(threadUrl)
#
#
# # num of pages declared by looking in the source code at: view-source:https://www.flashback.org/f13
# pageNum = np.arange(1,423)
# threadsLst = []
#
# for i in pageNum:
#   UrlToRequest = str(url_threads + 'p' + str(i))
#   print(UrlToRequest)
#   RequestedPage = get_html(UrlToRequest)
#   htmlFiltered = RequestedPage.select('#threadslist > tbody > tr')
#
#   for j in range(1, len(htmlFiltered)):
#     threadsLst.append(getThread(htmlFiltered[j]))
#     if j%25 == 0:
#       print(f'{j} of {len(threadsLst)} threads collected')
#
#
#
# threads = pd.DataFrame.from_dict(threadsLst)
#
# #threadIDs = list(threads['ThreadID'])
#
# threadIDs = list(threads['ThreadID'])
# # fetch all posts for all threads
# lst=[]
# print('Booting up...')
# counter = 0
# import datetime
# #print(str(datetime.datetime.today().date()))
# threadDict = {}
# for p in threadIDs:
#
#     init_url = url + '/' + p
#     max_pages=get_post_pages(init_url)
#     print(f'Max Pages in {init_url} is {max_pages}')
#     if len(lst)-counter > 25:
#         print(f'{len(lst)} posts saved')
#         counter = len(lst)
# #for p in range(0, 2):
#     postDict = {}
#     for i in range(1,max_pages+1):
#         new_url=init_url + 'p' + str(i)
#         postDict[p]={**postDict[p],**read_posts(get_posts(get_html(new_url),new_url),new_url)}
#         lst=lst+read_posts(get_posts(get_html(new_url),new_url),new_url)
#         #if i%5 == 0:
#             #print(f'{i} of {max_pages} in thread {p} pages read')
#
#     filename = f'{str(datetime.datetime.today().date())}_{p}.csv'
#     pd.DataFrame(lst).to_csv(f'~\Documents\PythonPath\TextAnalysisOnFlashback\SavedData\{filename}')
#     print(f'Saved file {filename}')
#
#
# #posts=pd.DataFrame(lst)
#
#
# #
# #
# # threads.to_csv('~\Documents\PythonPath\TextAnalysisOnFlashback\Treads.csv')
# # pwd()
# #
# # threads = pd.DataFrame(pd.read_csv('~\Documents\PythonPath\TextAnalysisOnFlashback\Treads2.csv',sep = ';',encoding='cp1252',escapechar='"',quoting=3))
# # type(threads)
# # threadIDs
#
# turl = 'https://www.flashback.org/t110543'
# page =  get_html(turl)
# posts=get_posts(page,turl)
# post_data = read_posts(posts,turl)
# read_posts(get_posts(get_html(new_url),new_url),new_url)
#
# print(post_data)
