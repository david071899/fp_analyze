# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Sum

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term

# import os
# import sys
# import re
# from threading import Thread
# import jieba
import math

from count_tf.main import start_segment
from learn_seg_rnn.main import start_learning

def count_tf (request):
  start_segment()

def laern_seg_rnn (request):
  start_learning()

def count_idf (request):
  post_amount = Post.objects.all().count()

  for term in Term.objects.all():
    term.idf = math.log10(post_amount / term.frequency_of_all_post)
    term.save()
    print term.idf

def tf_idf (request):
  for post in Post.objects.filter(mining_check = True):
    term_amount = post.termofpost_set.all().aggregate(Sum('quantity'))['quantity__sum']
    for term in post.termofpost_set.all():

      # only 名詞 count tf_idf
      if term.flag == 'n' or term.flag == 'nz' or term.flag == 'nr' or term.flag == 'ns':
        term.tf_idf = term.term.idf * (term.quantity / float(term_amount))
      else:
        term.tf_idf = 0

      term.save()

      print term.tf_idf
