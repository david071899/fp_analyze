# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Sum

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term
from api.models import Wordcloud

import math

from count_tf.main import start_segment
from learn_seg_rnn.main import start_learning

def mining_and_counting (request):
  start_segment()
  count_idf (request)
  tf_idf (request)

def count_idf (request):
  print '--------------------------------'
  print '       start counting idf       '
  print '--------------------------------'

  post_amount = Post.objects.all().count()

  for term in Term.objects.all():
    term.idf = math.log10(post_amount / term.frequency_of_all_post)
    term.save()
    print term.idf

def tf_idf (request):
  print '--------------------------------'
  print '       start counting tf_idf    '
  print '--------------------------------'

  for post in Post.objects.filter(mining_check = True):
    term_amount = post.termofpost_set.all().aggregate(Sum('quantity'))['quantity__sum']
    for term in post.termofpost_set.all():

      # only 大於一個字的名詞 count tf_idf
      if (term.term.flag == 'n' or term.term.flag == 'nz' or term.term.flag == 'nr' or term.term.flag == 'ns') and len(term.term.value) > 1:
        term.tf_idf = term.term.idf * (term.quantity / float(term_amount))
      else:
        term.tf_idf = 0

      term.save()

      print term.tf_idf

def term_rank_by_post (request):

  for year in xrange(2014,2017):
    for month in xrange(1,13):
      all_posts = Post.objects.filter(release_time__year = year, release_time__month = month)
      all_terms = list()
      for post in all_posts:
        for term in post.termofpost_set.order_by('-tf_idf')[:5]:
          all_terms.append(term.term.value)

      terms_set = set(all_terms)
      terms_freq = [[x,all_terms.count(x)] for x in terms_set]

      print terms_set

      Wordcloud.objects.update_or_create(
        year = year,
        month = month,
        defaults = {
          'word_data': terms_freq
        }
      )

def learn_seg_rnn (request):
  start_learning()
