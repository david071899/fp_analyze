# -*- coding: utf-8 -*-
from django.shortcuts import render

from data_parser.models import Post, User, Comment

import os
import re
import jieba

def count_tf (request):
  
  jieba.load_userdict(os.path.join(os.path.dirname(__file__), 'jieba/cowbieDict.txt'))      # 讀取自定義辭典

  for post in Post.objects.all():
    
    print post.id

    
    content = del_surplus_string(post.content)       # 刪除靠北清大 title & release time
    
    sentence_list = content.split('\n')              # 斷行成一個 array

    for sentence in sentence_list:                   # 對每一行做斷字
      
      sentence = remove_punctuation(sentence)        # 刪除標點符號

      seg_list = jieba.lcut(sentence)
      
      result = dict()

      for word in seg_list:
        if word not in result.keys():                # 重複的詞跳過
          result[word] = seg_list.count(word) 

    post.term_frequency = result
    post.save()

def store_term (request):
  

def remove_punctuation (text):

  text = re.sub("[\s+\.\!\/_,$:><=?%^*(+\"\']+|[+——：！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), text)

  return text

def del_surplus_string (content) :
  sen_array = content.split('\n')
  try:
    del sen_array[0]
    del sen_array[-1]
  except:
    return content
  return ''.join(sen_array)
