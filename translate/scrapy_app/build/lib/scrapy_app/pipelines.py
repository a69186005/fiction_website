# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy.exceptions import DropItem
from scrapy_app.spiders.bookItems import BookItems, ChapterItems 
from spiderAndTranslate.models import OriginalBooks, OriginalBooksContent

class Bookspiple(object):
    def process_item(self, item, spider):
        books = OriginalBooks()
        contents = OriginalBooksContent() 
        if isinstance(item, BookItems):
            books.book_name = item['book_name']
            books.book_url = item['book_url']
            books.book_author = item['book_author']
            books.unique_id = item['book_id']
            books.book_abstract = item['book_abstract']
            books.book_category = item['book_category']
            books.book_tags = ''
            books.total_words = 0
            books.save()
        
        if isinstance(item, ChapterItems):
            book_id = item['book_id']
            book_info = OriginalBooks.objects.filter(unique_id=book_id)[0]
            contents.book = book_info
            contents.chapter_content = item['chapter_content']
            contents.chapter_index = item['chapter_index']
            contents.chapter_name = item['chapter_name']
            contents.chapter_url = item['chapter_url']
            contents.words = item['words']
            contents.save()

        return item
