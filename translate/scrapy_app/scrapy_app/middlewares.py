# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class ScrapyAppSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyAppDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# My custom Middlewares about user-angent and ip proxy

# Random User-Angent Middleware

from fake_useragent import UserAgent

class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua = UserAgent()
        request.headers.setdefault("User-Agent", ua.random)
    '''
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())
    '''

# Random ip proxy from ip pool 

from scrapy import signals
import requests
from scrapy_app.settings import PROXY_ADDRESS, PROXY_OTHER_ADDRESS
import json
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
        ConnectionRefusedError, ConnectionDone, ConnectError, \
        ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed

from scrapy.exceptions import NotConfigured
from scrapy.core.downloader.handlers.http11 import TunnelError

proxy_ip = ""

class RandomProxy(object):

    EXCEPTIONS_TO_RETRY = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError)

    def process_request(self, request, spider):
        # proxy = random.choice(PROXY_LIST)
        global proxy_ip
        if proxy_ip == "":
            proxy_ip = self.get_proxy_ip()
            request.meta['proxy'] = proxy_ip
        else:
            request.meta['proxy'] = proxy_ip
    
    def process_response(self, request, response, spider):  
        global proxy_ip
        if response.status != 200:
            proxy_ip = ""
            # print("this is response ip:"+proxy)  
            # 对当前reque加上代理  
            del request.meta['proxy']
            return request
        return response
    
    def process_exception(self, request, exception, spider):
        global proxy_ip
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY):
            print(exception)
            proxy_ip = self.get_proxy_ip() 
            request.meta['proxy'] = proxy_ip
            proxy_ip = ""
            del request.meta['proxy']
            return request
    
    def get_proxy_ip(self):   
        res = requests.get(PROXY_OTHER_ADDRESS)
        res_data = res.json()
        # print(res_data["code"])
        if res_data["code"] == 0:
            proxy = "http://" + str(res_data["data"][0]["ip"]) + ':' + str(res_data["data"][0]["port"])
        else:
            return False
        return proxy
    
