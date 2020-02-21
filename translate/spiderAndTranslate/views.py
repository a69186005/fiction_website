from uuid import uuid4
from urllib.parse import urlparse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password
from scrapyd_api import ScrapydAPI

from .utils import baiduTranslate # use baidu to translate fictions from chinese to english or other langs

from spiderAndTranslate.models import UserProfile, OriginalBooks, OriginalBooksContent
## import some functions
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
      

def is_valid_url(url):
  validate = URLValidator()
  try:
    validate(url)
  except ValidationError:
    return False
  return True