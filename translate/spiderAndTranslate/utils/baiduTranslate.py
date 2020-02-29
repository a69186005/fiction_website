# -*- coding: utf-8 -*-
'''
# Created on Feb-21-20 20:36
# baiduTranslate.py
# @author: Lucius
'''
import requests
import hashlib
import urllib
import random
import json
import time
# from translate.settings import BAIDU_APPID, BAIDU_SECRET_KEY


# Build baidu translation event
MY_URL = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
BAIDU_APPID = '20200221000386872'
BAIDU_SECRET_KEY = '5sAg2tooWe7SIYMxI_YH'
MAX_PART_WORDS = 1900

class BaiduTranslation(object):

  def __init__(self, text, fromLang, toLang):
    self.text = text
    self.fromLang = fromLang
    self.toLang = toLang
  
  def __getSign(self,text):
    salt = random.randint(32768, 65536)
    self.salt = salt
    sign = BAIDU_APPID + text + str(salt) + BAIDU_SECRET_KEY
    sign = hashlib.md5(sign.encode()).hexdigest()

    return sign

  def __spliteText(self):
    text = self.text
    text_length = len(text)
    text_newGroup = []
    if text_length < 1900:
      text_newGroup.append(text)

    else:
      divide_part = (text_length // MAX_PART_WORDS) + 2 # based on the length of text to divide some parts, every part is under 1900 
      textGroup = text.split('\n')
      textGroup_length = len(textGroup)
      divide_words = len(textGroup) // divide_part
      start = 0
      end = len(textGroup)
      for i in range(divide_part):
        end = start + divide_words
        new_conetnt = ''
        last_content = ''
        if end > textGroup_length:
          part_content = textGroup[start:]
          for content in part_content:
            last_content = last_content + content + '~'
          text_newGroup.append(last_content)
        else:
          part_content = textGroup[start:end]
          for content in part_content:
            new_conetnt = new_conetnt + content + '~'
          text_newGroup.append(new_conetnt)
          start += divide_words
      
    # print(len(text_newGroup))
    return text_newGroup
  
  def translate(self):
    textGroup = self.__spliteText() # Get splite text
    fromLang = self.fromLang
    toLang = self.toLang
    header = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    results = ''
    for text in textGroup:
      if text != '':
        sign = self.__getSign(text) # Get sign
        salt = self.salt
        text = urllib.parse.quote(text) # urlencoded
        requestData = 'appid=' + str(BAIDU_APPID) + '&q=' + text + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
        try:
          response = requests.post(MY_URL, data=requestData, headers=header)
          result = response.json()['trans_result'][0]['dst']

          results += result
        except Exception as e:
          print (e)
      time.sleep(1)
    return results
  

'''
text = '星海之主'
fromLang = 'zh'
toLang = 'en'
translate = BaiduTranslation(text, fromLang, toLang)
print(translate.translate())
'''