from django.shortcuts import render

from django.http import JsonResponse

from data_parser.models import Post, User, Comment

from django.db.models import Sum

# Create your views here.

def posts(requests):
  data = dict()

  data['amount'] = Post.objects.all().count()
  data['likes_amount'] = Post.objects.aggregate(Sum('like_count'))['like_count__sum']
  data['comments_amount'] = Post.objects.aggregate(Sum('comment_count'))['comment_count__sum']

  return JsonResponse(data)
