from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core import serializers
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from scrapyd_api import ScrapydAPI

from .utils.baiduTranslate import BaiduTranslation  # use baidu to translate fictions from chinese to english or other langs

from spiderAndTranslate.models import UserProfile, OriginalBooks, OriginalBooksContent, TanslationBookContentEN, TranslationBooksEN

# import some functions
import os
import json

scrapyd = ScrapydAPI('http://127.0.0.1:6800')
# Create your views here.

class Login(View):
  def get(self, request, *arg, **kwargs):
    return render(request, 'login.html')
  
  def post(self, request, *arg, **kwargs):
    data = eval(request.body)
    username = data['username']
    password = data['password']
    password_s = make_password(password, None, 'pbkdf2_sha256')
    existed_users = UserProfile.objects.filter(username=username)
    if existed_users:
      user = existed_users[0]
      result = check_password(password, user.password)
      if result:
        login(request, user)
        return JsonResponse({
          'status': 'success'
        })
      else:
        return JsonResponse({
          'status': 'fail',
          'message': 'Sorry, your password is wrong',
          'password': password_s
        })
    else:
      return JsonResponse({
        'status': 'fail',
        'message': 'Sorry, you are not a administrator'
      })

class Crawl(View):

  def get(self, request, *arg, **kwargs):
    return render(request, 'spider.html')

  def post(self, request, *arg, **kwargs):
    data = eval(request.body)
    url = data['url']
    if not url:
      return JsonResponse({
        'status': 'fail',
        'message': 'The paremeter is wrong'
      })
    if not is_valid_url(url):
      return JsonResponse({
        'status': 'fail',
        'message': 'The url is invalid'
      })
    domain = urlparse(url).netloc
    unique_id = str(uuid4())
    settings = {
      'unique_id':unique_id,
      'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    }

    task = scrapyd.schedule('default', 'icrawler', 
            settings=settings, url=url, domain=domain)

    return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started' })

class ChineseBook(View):
  def get(self, request, *arg, **kwargs):
    return render(request, 'chinesebook.html')
  
  def post(self, request, *arg, **kwargs):
    pass

class EnglishBook(View):
  def get(self, request, *arg, **kwargs):
    return render(request, 'englishbook.html')

  def post(self, request, *arg, **kwargs):
    pass

class CheckSpider(View):
  def get(self, request, *arg, **kwargs):
    task_id = request.GET.get('task_id', None)
    unique_id = request.GET.get('unique_id', None)

    if not task_id or not unique_id:
      return JsonResponse({'error': 'Missing args'})
    
    status = scrapyd.job_status('default', task_id)
    if status == 'finished':
      item = OriginalBooks.objects.get(unique_id=unique_id)
      try:        
        return JsonResponse({'data': item.to_dict['data']})
      except Exception as e:
        return JsonResponse({'error': str(e)})
    else:
      return JsonResponse({'status': status})

class Translate(View):
  def get(self, request, *arg, **kwargs):
    books = OriginalBooks.objects.all()

    for book in books:
      books_en = TranslationBooksEN()
      books_en.book = book
      books_en.book_name = BaiduTranslation(book.book_name, 'zh', 'en').translate()
      print(BaiduTranslation(book.book_name, 'zh', 'en').translate())
      books_en.book_author = BaiduTranslation(book.book_author, 'zh', 'en').translate()
      books_en.book_category = BaiduTranslation(book.book_category, 'zh', 'en').translate()
      books_en.book_abstract = BaiduTranslation(book.book_abstract, 'zh', 'en').translate()
      books_en.total_words_tran = 0
      books_en.save()

    return JsonResponse({'data': books})

class TranslateContent(View):
  def get(self, request, *arg, **kwargs):
    books_en = TranslationBooksEN.objects.all()

    for book_en in books_en:
      book_content = OriginalBooksContent.objects.filter(book = book_en.book)
      if book_content:
        for content in book_content:
          book_content_en = TanslationBookContentEN()
          book_content_en.book = book_en
          book_content_en.chapter_name = BaiduTranslation(content.chapter_name, 'zh', 'en').translate()
          print(BaiduTranslation(content.chapter_name, 'zh', 'en').translate())
          book_content_en.chapter_index = content.chapter_index
          book_content_en.chapter_content = BaiduTranslation(content.chapter_content, 'zh', 'en').translate()
          book_content_en.words = content.words
          book_content_en.save()
  
    return JsonResponse({'data': books_en})

class GetTranslateBookEN(View):
  def get(self, request, *arg, **kwargs):
    books_en = TranslationBooksEN.objects.all()

    return JsonResponse({
      'status': 'success',
      'data': json.loads(serializers.serialize('json', books_en, ensure_ascii=False))
    })

class GetTranslateContentEN(View):
  def get(self, request, *arg, **kwargs):
    book_id = request.GET['book']
    content_en = TanslationBookContentEN.objects.filter(book_id=book_id)
    print(content_en)

    return JsonResponse({
      'status': 'success',
      'data': json.loads(serializers.serialize('json', content_en, ensure_ascii=False))
    })



def is_valid_url(url):
  validate = URLValidator()
  try:
    validate(url)
  except ValidationError:
    return False
  return True