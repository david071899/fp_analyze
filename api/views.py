from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.core import serializers

import json

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term

def all_terms(requrest):

  data = Term.objects.filter(Q(flag = 'n') | Q(flag = 'nz') | Q(flag = 'nr') | Q(flag = 'ns') )

  data = data.extra(where=["CHAR_LENGTH(value) > 1"])

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
