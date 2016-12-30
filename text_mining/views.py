# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Sum

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term
from api.models import Wordcloud

import math
from itertools import groupby

from segment.main import start_segment
from learn_seg_rnn.main import start_learning

def mining_and_counting (request):
  start_segment()
  count_idf (request)
  tf_idf (request)
  term_rank_by_post2 (request)

def segment (request):
  start_segment()

def count_idf (request):
  print '--------------------------------'
  print '       start counting idf       '
  print '--------------------------------'

  post_amount = Post.objects.count()

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

  print '--------------------------------'
  print '    start counting terms rank   '
  print '--------------------------------'

  for year in xrange(2014,2017):
    for month in xrange(1,13):
      all_posts = Post.objects.filter(release_time__year = year, release_time__month = month)
      all_terms = list()
      for post in all_posts:
        for term in post.termofpost_set.order_by('-tf_idf')[:10]:
          all_terms.append(term.term.value) if term.tf_idf > 0 else 0

      terms_set = set(all_terms)

      terms_freq = map(lambda x: [x, all_terms.count(x)] if all_terms.count(x) > 2 else [], terms_set)
      terms_freq = filter(None, terms_freq)

      print terms_set

      Wordcloud.objects.update_or_create(
        year = year,
        month = month,
        defaults = {
          'word_data': terms_freq
        }
      )

def term_rank_by_post2 (request):
  # order post by school and time
  posts = Post.objects.order_by('school', 'release_time')
  # separate post by datetime
  posts = separate_posts_by_datetime(posts)
  # start count term rank
  count_term_rank(posts)

def count_trend_by_school (request):
  pass


def learn_seg_rnn (request):
  start_learning()

# ------------------ private function ---------------------

def separate_post_by_school (school):
  return Post.objects.filter(school = school)

def separate_posts_by_datetime (posts):
  return groupby(posts, lambda post: post.school + '/' + str(post.release_time.year) + '/' + str(post.release_time.month))

def count_term_rank (posts):
  for post_iter in posts:
    
    school = post_iter[0].split('/')[0]
    year = post_iter[0].split('/')[1]
    month = post_iter[0].split('/')[2]

    post_grouper = post_iter[1]

    all_terms = list()
    for post in post_grouper:
      for term in post.termofpost_set.order_by('-tf_idf')[:10]:
        all_terms.append(term.term.value) if term.tf_idf > 0 else 0

    terms_set = set(all_terms)
    terms_freq = map(lambda x: [x, all_terms.count(x)] if all_terms.count(x) > 3 else [], terms_set)
    terms_freq = filter(None, terms_freq)

    print school, year, '/', month, 'finished'

    Wordcloud.objects.update_or_create(
      year = year,
      month = month,
      school = school,
      defaults = {
        'terms': terms_set, 
        'word_data': terms_freq
      }
    )
