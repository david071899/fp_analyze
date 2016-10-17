# -*- coding: utf-8 -*-
from django.shortcuts import render

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term

import os
import re
import jieba

def count_tf (request):
  
  jieba.load_userdict(os.path.join(os.path.dirname(__file__), 'jieba/cowbieDict.txt'))      # 讀取自定義辭典

  for post in Post.objects.all():
    
    print post.id

    # 刪除靠北清大 title & release time
    content = del_surplus_string(post.content)       

    # 斷行成一個 array
    sentence_list = content.split('\n')              

    # 對每一行做斷字
    for sentence in sentence_list:                   

      # 刪除標點符號
      sentence = remove_punctuation(sentence)        

      seg_list = jieba.lcut(sentence)
      
      result = dict()

      for word in seg_list:

        # 重複的詞跳過
        if word not in result.keys():                
          result[word] = seg_list.count(word) 

    for key,value in result.iteritems():

      # 取出或是創造一筆新的資料（詞）
      Term.objects.get_or_create(             
        value = key,
        defaults = {
          'frequency_of_all_post': 0
        }
      )

      # 出現在文章的次數加一
      term = Term.objects.get(value = key)
      term.frequency_of_all_post += 1                
      term.save()

      # 取出或是創造詞與文章的關係
      TermOfPost.objects.get_or_create(              
        post = post,
        term = term,
        defaults = {
          'quantity': value
        }
      )

    post.term_frequency = result
    post.save()

# def store_term (request):
  

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
