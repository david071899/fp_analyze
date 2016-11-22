from django.shortcuts import render

from django.http import JsonResponse
from django.core import serializers
import json

from data_parser.models import Post, User, Comment, TermOfPost
from text_mining.models import Term

def all_terms(requrest):

  json_data = [list(x) for x in Term.objects.values_list('value', 'frequency_of_all_post')]

  return JsonResponse(json_data, safe = False)
