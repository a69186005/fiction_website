"""translate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve

# import views
from spiderAndTranslate.views import Login, ChineseBook, EnglishBook, Crawl

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/', csrf_exempt(Login.as_view()), name="login"),
    url(r'^chinesebook/', csrf_exempt(ChineseBook.as_view()), name="chinesebook"),
    url(r'^englishbook/', csrf_exempt(EnglishBook.as_view()), name="englishbook"),
    url(r'^spider/', csrf_exempt(Crawl.as_view()), name="spider"),
]
