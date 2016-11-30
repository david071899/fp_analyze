from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core import serializers

import json
import datetime

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term

def all_terms (requrest):

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

  all_posts = Post.objects.filter(release_time__year = year, release_time__month = month)

  terms_dict = dict()

  for post in all_posts:
    terms = post.termofpost_set.filter(tf_idf__gt = 0)
    terms = terms.order_by('-tf_idf')[:10]
    for term in terms:
      if term.term.value in terms_dict:
        terms_dict[term.term.value] += 10
      else:
        terms_dict[term.term.value] = 0

  json_data = [[key, value] for key, value in terms_dict.iteritems()]

  response = JsonResponse(json_data, safe = False)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "*"

  return response




  