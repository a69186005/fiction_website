# -*- coding: utf-8 -*-
import scrapy
import re
from uuid import uuid4
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from .bookItems import BookItems, ChapterItems

BASE_URL = "https://www.quanben.net"
bookitem = BookItems()
chapteritem = ChapterItems()

class BookcrawlSpider(CrawlSpider):
    name = 'bookCrawl'
    domains = ['https://www.quanben.net']
    start_urls = ['https://www.quanben.net/quanben/1.html']
    
    def parse(self, response):
        urls = response.xpath("//span[@class='s2']/a//@href").extract()
        for url in urls:
            new_url = BASE_URL + url
            yield scrapy.Request(new_url, meta={'url': new_url}, callback=self.parse_details_book)
        
        next_Page = response.xpath("//a[@class='next']//@href").extract()[0]
        if next_Page is not None:
            nextpage_url = BASE_URL + next_Page
            yield scrapy.Request(nextpage_url, callback=self.parse)
        else:
            return None


    def parse_details_book(self, response):
        bookitem['book_url'] = response.meta['url']
        book_id = str(uuid4())
        bookitem['book_id'] = book_id
        bookitem['book_name'] = response.css("h1::text").extract()[0]
        bookitem['book_author'] = response.css("em a::text").extract()[0]
        bookitem['book_category'] = response.css("div.fl a::text").extract()[1]
        bookitem['book_tags'] = ''
        bookitem['book_abstract'] = response.xpath("//p[@class='intro']//text()").extract()[2]

        yield bookitem

        chapter_urls = response.xpath("//dt[contains(text(), '全文阅读')]/following-sibling::dd//a//@href").extract()
        chapter_index = 0
        for chapter_url in chapter_urls:
            chapter_url_all = BASE_URL + chapter_url
            chapter_index += 1
            yield scrapy.Request(chapter_url_all, meta={'chapter_url': chapter_url_all, 'book_id': book_id, 'chapter_index': chapter_index}, callback= self.parse_chapter_content)

    
    def parse_chapter_content(self, response):   
        chapteritem['chapter_url'] = response.meta['chapter_url']
        chapteritem['book_id'] = response.meta['book_id']
        chapteritem['chapter_index'] = response.meta['chapter_index']
        chapteritem['chapter_name'] = response.css("h1::text").extract()[0]
        contents = response.css("div#BookText::text").extract()
        chapter_content = ''
        for content in contents:
            content_new = content.replace('\\xa0', '') + '\n'
            chapter_content = chapter_content + content_new
        chapteritem['chapter_content'] = chapter_content
        chapteritem['words'] = len(chapter_content)

        return chapteritem