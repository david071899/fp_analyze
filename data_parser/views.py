# -*- coding: utf-8 -*-
from django.conf import settings

from django.shortcuts import render
from django.shortcuts import  render_to_response

from django.template import RequestContext

from data_parser.models import Post, User, Comment

import requests
import facebook
import dotenv
import os

#load env variable
dotenv_path = os.path.join(settings.BASE_DIR, '.env')
dotenv.load_dotenv(dotenv_path)

def parse_all_post_content (request):

  app_data = {'app_id': os.environ.get("FB_APP_ID"),
              'app_secret': os.environ.get("FB_APP_SECRET")}

  access_token_request_url = ("https://graph.facebook.com/oauth/access_token?"
    "client_id={app_id}"
    "&client_secret={app_secret}"
    "&grant_type=client_credentials").format(**app_data)

  access_token = requests.get(access_token_request_url).text.split('=')[-1]

  print access_token

  graph = facebook.GraphAPI(access_token = access_token, version = '2.2')

  school = request.GET.get('school', 'nthu')

  if school == 'nthu':
    school_id = graph.get_object(id = 'cowbeiNTHU')['id']
  elif school == 'nctu':
    access_token = 'EAACEdEose0cBAKG9raBLxh4zPLIOmerEeNTFYt9pnd1UW2a1IAMVr4leUkKjWZCDAZBVB7P8ExESvZBZAbonHrDidlu411W09V0Viu1me6UvTesLz5S8vzNf61lLf1VzivP95xXgexZBVPvklLGtVC0vnXeJEGHunfhN2SZCUZBogZDZD'
    graph = facebook.GraphAPI(access_token = access_token, version = '2.2')
    school_id = graph.get_object(id = 'NCTUHATE')['id']
  elif school == 'ntu':
    school_id = graph.get_object(id = 'hateNTU')['id']
  elif school == 'nccu':
    school_id = graph.get_object(id = 'NCCUHate')['id']

  posts = graph.get_connections(id = school_id, connection_name = 'posts?fields=message,created_time')

  while True:
    try:
      for p in posts['data']:
        if 'message' in p.keys():
          print p['message']

          create_post(p, school)

      if 'paging' in posts:
        posts = requests.get(posts['paging']['next']).json()
      else:
        break

    except Exception as e:
      print e
      continue


  return render_to_response('index.html', RequestContext(request, locals()))


def create_post (data, school):
  Post.objects.update_or_create(
    post_id = data['id'],
    defaults = {
      'content': data['message'],
      'release_time': data['created_time'],
      'school': school,
    }
  )

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

  


