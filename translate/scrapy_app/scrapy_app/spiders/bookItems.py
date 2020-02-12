# -*- coding: utf-8 -*-
'''
# Created on Feb-11-20 10:38
# bookItems.py
# @author: Lucius
'''
import scrapy

class BookItems(scrapy.Item):
  book_id = scrapy.Field()
  book_name = scrapy.Field()
  book_author = scrapy.Field()
  book_category = scrapy.Field()
  book_tags = scrapy.Field()
  book_abstract = scrapy.Field()
  total_words = scrapy.Field()
  book_url = scrapy.Field()
  

class ChapterItems(scrapy.Item):
  book_id = scrapy.Field()
  chapter_name = scrapy.Field()
  chapter_index = scrapy.Field()
  chapter_content = scrapy.Field()
  words = scrapy.Field()
  chapter_url = scrapy.Field()
