"""fp_analyze URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from data_parser.views import parse_all_post, parse_all_post_content

from text_mining.views import mining_and_counting, learn_seg_rnn, term_rank_by_post

from api.views import all_terms, filter_post, trend

from front.views import index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^parse_all_post_content/', parse_all_post_content),
    url(r'^parse_all_post/', parse_all_post),
    url(r'^text_mining/mining_and_counting', mining_and_counting),
    url(r'^text_mining/term_rank_by_post', term_rank_by_post),
    url(r'^text_mining/laern_seg_rnn', learn_seg_rnn),
    url(r'^api/all_terms', all_terms),
    url(r'^api/filter_post', filter_post),
    url(r'^api/trend', trend),
    url(r'^index', index),
]
