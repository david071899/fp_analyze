# -*- coding: utf-8 -*-

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term

import os
import sys
import re
from threading import Thread
import jieba

def start_segment ():
  jieba.enable_parallel(4)
  # 讀取自定義辭典
  for jeiba_dict in os.listdir(os.path.join(os.path.dirname(__file__), '../jieba')): 
    jieba.load_userdict(os.path.join(os.path.dirname(__file__), '../jieba/' + jeiba_dict))

  # 初始化 generator
  generator = post_generator()

  thread_list = []

  # 使用 4 個 thread
  for i in xrange(4):
    thread = Thread(target = seg_article, args = (generator, ))
    thread_list.append(thread)
    thread.start()

  for thread in thread_list:
    thread.join()
  

def remove_punctuation (text):

  text = re.sub("[s+.!/_,$:><=?%^*(+\"\']+|[+——：！，。“「」＝＋？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), text)

  return text

def del_surplus_string (content) :
  sen_array = content.split('\n')
  try:
    del sen_array[0]
    del sen_array[-1]
  except:
    return content
  return ''.join(sen_array)

def post_generator():
  post = Post.objects.filter(mining_check = False)
  print '.................................................'
  print ' now have', post.count(), 'posts wait for mining '
  print '.................................................'
  array = list(post)
  i = 0
  while (i < len(array)):
    yield array[i]
    i += 1

def seg_article(post_generator):

  post_amount = len(Post.objects.all())

  i = 0

  while (i < post_amount):

    try:
      post = post_generator.next()
    except:
      break;

    print post.id
    # 刪除靠北清大 title & release time
    content = del_surplus_string(post.content)
    # 刪除標點符號
    content = remove_punctuation(content)

    seg_list = jieba.lcut(content)

    # 清除 \n & 空白
    seg_list = filter(lambda a: a != '\n' and a != ' ', seg_list)
    # seg_list = filter(lambda a: a != ' ', seg_list)

    result = dict()

    for word in seg_list:

      # 重複的詞跳過
      if word not in result.keys():                
        result[word] = seg_list.count(word)

    for key,value in result.iteritems():
      try:
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
      except:
        print "!"*120
        print "Unexpected error:", sys.exc_info()[0]
        print "!"*120
        continue

    post.term_frequency = result
    post.mining_check = True
    post.save()
