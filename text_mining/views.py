# -*- coding: utf-8 -*-
from django.shortcuts import render

# from data_parser.models import Post, User, Comment, TermOfPost
# from text_mining.models import Term

# import os
# import sys
# import re
# from threading import Thread
# import jieba

from count_tf.main import start_segment
from learn_seg_rnn.main import start_learning

def count_tf (request):
  start_segment()

def laern_seg_rnn (request):
  start_learning()

