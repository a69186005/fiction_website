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

from spiderAndTranslate.models import UserProfile, OriginalBooks, OriginalBooksContent, TanslationBookContentEN, TranslationBooksEN
from spiderAndTranslate.utils.baiduTranslate import BaiduTranslation


books_en = TranslationBooksEN.objects.all()

for book_en in books_en:
  book_content = OriginalBooksContent.objects.filter(book = book_en.book)
  existed_book = TanslationBookContentEN.objects.filter(book = book_en.book)
  if existed_book:
    print ("It is an existed book")
  else:
    if book_content:
      try:
        for content in book_content:
          book_content_en = TanslationBookContentEN()
          book_content_en.book = book_en
          book_content_en.chapter_name = BaiduTranslation(content.chapter_name, 'zh', 'en').translate()
          print(BaiduTranslation(content.chapter_name, 'zh', 'en').translate())
          book_content_en.chapter_index = content.chapter_index
          book_content_en.chapter_content = BaiduTranslation(content.chapter_content, 'zh', 'en').translate()
          book_content_en.words = content.words
          book_content_en.save()
      except:
        print("book_id:" + book_en.book_name + ";" + "book_index:" + book_content_en.chapter_index)
        print("save error")