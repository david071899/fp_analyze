from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django.core import serializers
import json

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term

def all_terms(requrest):

  json_data = [list(x) for x in Term.objects.values_list('value', 'frequency_of_all_post')]

  response = JsonResponse(json_data, safe = False)
  response["Access-Control-Allow-Origin"] = "*"
  response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
  response["Access-Control-Max-Age"] = "1000"
  response["Access-Control-Allow-Headers"] = "*"

  return response
