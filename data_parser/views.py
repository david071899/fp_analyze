# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import  render_to_response

from django.template import RequestContext

from data_parser.models import Post, User, Comment

import requests
import facebook

# Create your views here.
def parse_all_post (request):

  app_data = {'app_id': '253935675007631',
              'app_secret': '4248e9d611cb3ad467d73614a96c2a5e'}

  access_token_request_url = ("https://graph.facebook.com/oauth/access_token?"
    "client_id=253935675007631"
    "&client_secret=4248e9d611cb3ad467d73614a96c2a5e"
    "&grant_type=client_credentials")

  access_token = requests.get(access_token_request_url).text.split('=')[-1]
  
  # access_token = 'EAACEdEose0cBAFEzSEpGQAd05X2QflsHyY5dMH1lY6WMYeUZAq0ienIcQMEkZBj23hzMhEmILRRNmlvQzzGFBeniTy75Hjsnq9jIkb6WimMydNHmTDjAmlGwyE8iu9PHwZAMZCJap2u2eiXFgoytIUa0vVDaeMrvY1azC23ZCpwZDZD'

  graph = facebook.GraphAPI(access_token = access_token, version = '2.2')

  cowbeiNTHU_id = graph.get_object(id = 'cowbeiNTHU')['id']

  print cowbeiNTHU_id

  cowbeiNTHU_post = graph.get_connections(id = cowbeiNTHU_id, connection_name = 'posts?fields=likes.limit(100),comments.limit(100){like_count,from,message},created_time,message')

  while True:
    try:
      
      for p in cowbeiNTHU_post['data']:

        if 'message' in p.keys():
          create_post(p)

          if 'likes' in p.keys():
            create_user(p, 'like')

          if 'comments' in p.keys():
            create_user(p, 'comment')

      cowbeiNTHU_post = requests.get(cowbeiNTHU_post['paging']['next']).json()

    except  Exception as e:

      print e  
      break

  return render_to_response('index.html', RequestContext(request, locals()))

def create_post (data):

  like_count = len(data['likes']['data']) if 'likes' in data.keys() else 0
  comment_count = len(data['comments']['data']) if 'comments' in data.keys() else 0  

  Post.objects.update_or_create(
    post_id = data['id'],
    defaults = {
      'content': data['message'],
      'release_time': data['created_time'],
      'like_count': like_count,
      'comment_count': comment_count
    }
  )

  print data['message']

def create_user (data, data_resource):
  post = Post.objects.get(post_id = data['id'])

  if data_resource == 'like':   

    for like in data['likes']['data']:
      User.objects.update_or_create(
        user_id = like['id'],
        defaults = {
          'name': like['name'],
        }
      )

      User.objects.get(user_id = like['id']).like_post.add(post)

  elif data_resource == 'comment':
    
    for comment in data['comments']['data']:
      User.objects.update_or_create(
        user_id = comment['from']['id'],
        defaults = {
          'name': comment['from']['name'],
        }
      )

      user = User.objects.get(user_id = comment['from']['id'])
      create_comment(user, post, comment)

def create_comment (user, post, comment):
  comment_id = comment['id']
  like_count = comment['like_count']
  content = comment['message'].encode("utf-8")

  Comment.objects.update_or_create(
    comment_id = comment_id,
    defaults = {
      'user': user,
      'post': post,
      'like_count': like_count,
      'content': content
    } 
  )

  


