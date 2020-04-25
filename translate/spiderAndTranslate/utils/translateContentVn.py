# -*- coding: utf-8 -*-
'''
# Created on Mar-17-20 09:22
# translateContent.py
# @author: Lucius
'''
import os, django, sys
sys.path.append(os.path.dirname(os.path.abspath('.')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'translate.settings'
django.setup()
import requests
import json

from spiderAndTranslate.models import UserProfile, OriginalBooks, OriginalBooksContent, TanslationBookContentVI, TranslationBooksVI
from baiduTranslateVn import BaiduTranslation

books_VI = TranslationBooksVI.objects.all()

for book_VI in book_VI:
  book_content = OriginalBooksContent.objects.filter(book = book_VI.book)
  if book_content:
    for content in book_content:
      book_content_VI = TanslationBookContentVI()
      book_content_VI.book = book_VI
      book_content_VI.chapter_name = BaiduTranslation(content.chapter_name, 'zh', 'vie').translate()
      print(BaiduTranslation(content.chapter_name, 'zh', 'vie').translate())
      book_content_VI.chapter_index = content.chapter_index
      book_content_VI.chapter_content = BaiduTranslation(content.chapter_content, 'zh', 'vie').translate()
      book_content_VI.words = content.words
      book_content_VI.save()