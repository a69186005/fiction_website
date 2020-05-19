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
from spiderAndTranslate.utils.baiduTranslateVn import BaiduTranslation


books_vi = TranslationBooksVI.objects.all()

for book_vi in books_vi:
  book_content = OriginalBooksContent.objects.filter(book = book_vi.book)
  existed_book = TanslationBookContentVI.objects.filter(book = book_vi)
  if existed_book:
    print ("It is an existed book")
  else:
    if book_content:
      try:
        for content in book_content:
          book_content_vi = TanslationBookContentVI()
          book_content_vi.book = book_vi
          book_content_vi.chapter_name = BaiduTranslation(content.chapter_name, 'zh', 'vie').translate()
          print(BaiduTranslation(content.chapter_name, 'zh', 'vie').translate())
          book_content_vi.chapter_index = content.chapter_index
          book_content_vi.chapter_content = BaiduTranslation(content.chapter_content, 'zh', 'vie').translate()
          book_content_vi.words = content.words
          book_content_vi.save()
      except:
        print("book_id:" + book_vi.book_name + ";" + "book_index:" + book_content_vi.chapter_index)
        print("save error")