# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core import serializers

import json
import datetime
import operator

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
    start_month = 5 if year == 2014 else 1;
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

def department (request):
  department_list = ['理學院','數學系','物理系','化學系','理學院學士班','理雙','工學院','化學工程學系 ','化工',
  '動力機械工程學系','動機','材料科學工程學系','材料','工業工程與工程管理學系','工工','工學院學士班','工院',
  '電機資訊學院','資訊工程學系','資工','電機工程學系','電機','電機資訊學院學士班','電資院學士班','人文社會學院',
  '中國文學系','中文','外國語文學系','外文','外文系','人文社會學院學士班','人社','生命科學院','生命科學系','生科',
  '醫學科學系','醫科','生命科學院學士班','生科院學士班','原子科學院','工程與系統科學系','工科','生醫工程與環境科學系',
  '醫環','原子科學院學士班','原科','科技管理學院','計量財務金融學系','計財','經濟學系','經濟','科技管理學院學士班','科管',
  '清華學院學士班']

  json_data = dict()
  # query the data
  result = map(term_filter, department_list)
  # filter None data
  result = filter(lambda term: term != None, result)
  # Sorted data by frequency_of_all_post
  result = sorted(result, key = operator.attrgetter('frequency_of_all_post'), reverse = True)
  # detect club name & frequency
  json_data['dep_name'] = map(lambda term: term.value, result)

  json_data['dep_freq'] = map(lambda term: term.frequency_of_all_post, result)

  response = JsonResponse(json_data, safe = False)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "*"



def club (request):
  club_list = ['TEDxNTHU','清華模擬聯合國','模聯','經濟商管學生會','AIESEC','aiesec','青年領袖研習社',
  '清華國際社群','TICO','tico','禪學社','學員團契','信望愛團契','博客來學生團契','清交部落格','口琴社','弦樂社',
  '清華鼓坊','鋼琴社','合唱社','人聲樂創社','街音社','數位媒體創作社','戲劇社','書藝社','光畫社','光舞藝術社','當代舞蹈社',
  '國標社','世界民族舞蹈社','清華旗隊','圍棋社','西洋棋社','魔術社','中醫社','烹飪社','飲品社','調酒社','光舞社','國術社',
  '柔道社','劍道社','飛鏢社','自行車社','網球社','馬術社','啦啦隊','田徑隊','快樂兒童社','快兒','清華之愛社','清愛'
  ,'藍天','羅浮童子軍社','親善大使團','學生會','科服','原文','文服']

  json_data = dict()
  # query the data
  result = map(term_filter, club_list)
  # filter None data
  result = filter(lambda term: term != None, result)
  # Sorted data by frequency_of_all_post
  result = sorted(result, key = operator.attrgetter('frequency_of_all_post'), reverse = True)
  # detect club name & frequency
  json_data['club_name'] = map(lambda term: term.value, result)

  json_data['club_freq'] = map(lambda term: term.frequency_of_all_post, result)

  response = JsonResponse(json_data, safe = False)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "*"

  return response

def term_filter (name):
  return Term.objects.filter(value = name)[0] if Term.objects.filter(value = club_name) else None

