from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core import serializers

import json
import datetime

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term
from api.models import Wordcloud

def all_terms (request):

  data = Term.objects.filter(Q(flag = 'n') | Q(flag = 'nz') | Q(flag = 'nr') | Q(flag = 'ns') )

  data = data.extra(where = ["CHAR_LENGTH(value) > 1"])

  data = data.order_by('-frequency_of_all_post')[:50]

  shift_num = data[0].frequency_of_all_post / 200

  for i in data:
    i.frequency_of_all_post = i.frequency_of_all_post / shift_num

  json_data = [[x.value, x.frequency_of_all_post] for x in data]

  response = JsonResponse(json_data, safe = False)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "*"

  return response

def filter_post (request):
  year = request.GET.get('year', 2014)
  month = request.GET.get('month', 1)

  # all_posts = Post.objects.filter(release_time__year = year, release_time__month = month)


  # all_posts = all_posts.prefetch_related('termofpost_set').prefetch_related('terms')

  # terms_dict = dict()

  # for post in all_posts:
  #   terms = post.termofpost_set.filter(tf_idf__gt = 0)
  #   terms = terms.order_by('-tf_idf')[:10]
  #   for term in terms:
  #     if term.term.value in terms_dict:
  #       terms_dict[term.term.value] += 10
  #     else:
  #       terms_dict[term.term.value] = 10

  # json_data = [[key, value] for key, value in terms_dict.iteritems()]

  json_data = Wordcloud.objects.get(year = year, month = month).word_data

  response = JsonResponse(json_data, safe = False)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "*"

  return response


def trend (request):
  keyword = request.GET.get('keyword','')

  start_year = Post.objects.earliest('release_time').release_time.year
  start_month = Post.objects.earliest('release_time').release_time.month

  end_year = Post.objects.latest('release_time').release_time.year
  end_month = Post.objects.latest('release_time').release_time.month

  json_data = dict()

  json_data['start'] = { 'year': start_year, 'month': start_month }
  json_data['end'] = { 'year': end_year, 'month': end_month }
  json_data['period'] = []
  json_data['trend'] = []

  for year in xrange(start_year, end_year+1):
    for month in xrange(start_month, end_month+1):
      query = TermOfPost.objects.filter(post__release_time__year = year, post__release_time__month = month)
      amount = query.filter(term__value = keyword).count()
      date = str(year) + '/' + str(month)
      json_data['period'].append(date)
      json_data['trend'].append(amount)

  response = JsonResponse(json_data, safe = False)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "*"

  return response






  